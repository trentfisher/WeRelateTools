#!/usr/bin/env python3

import requests
import xml.etree.ElementTree
import re
import sqlite3
from dateutil import parser
from datetime import datetime,timedelta,timezone
import sys
import math
import time
import random
from bs4 import BeautifulSoup
import urllib

dbfile="wr.db"
werelateurl = "https://www.werelate.org"
rssurl = werelateurl+"/wiki/Special:Recentchanges?feed=rss&limit=5000&days=7"
allpersonurl = werelateurl+"/w/index.php?title=Special%3AAllpages&namespace=108&from="
allfamilyurl = werelateurl+"/w/index.php?title=Special%3AAllpages&namespace=110&from="
count = {'fetchrss':0, 'fetchraw':0, 'fetchhist':0}

# set up a persistent connection
wrsession = requests.Session()
wrsession.headers.update({'Connection': 'keep-alive'})

#------------------------------------------------------------------------
def getrss(url):
     
    response = wrsession.get(url)
    response.raise_for_status()
    count['fetchrss'] += 1;
    
    root = xml.etree.ElementTree.fromstring(response.content)
    # TBD this should actually come from the xml file...
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    pages = []
    # The standard structure of an RSS feed: <rss><channel><item><link>
    for item in root.findall('./channel/item'):
        itemrec = {}
        itemrec['title'] = item.find('title').text
        itemrec['link'] = item.find('link').text
        itemrec['pubDate'] = item.find('pubDate').text

        if (item.find('dc:creator', ns) == "None"):
            itemrec['creator'] = "unknown"
        else:
            itemrec['creator'] = item.find('dc:creator', ns).text
            
        if (itemrec['title'] == 'Special:Log/delete'):
            m = re.search('title="(Person|Family):(.+)">', item.find('description').text)
            if (m):
                itemrec['title'] = itemrec['delete'] = m.group(1)+":"+m.group(2)
        elif (itemrec['title'] == 'Special:Log/move'):
            m = re.search(' title="(Person|Family):(.+)">.+> renamed to <.+ title="(Person|Family):(.+)">',
                         item.find('description').text)
            if (m):
                itemrec['title'] = m.group(1)+":"+m.group(2)
                itemrec['move'] = m.group(3)+":"+m.group(4)
                print(f"RENAME {itemrec['title']} to {itemrec['move']}")
        pages.append(itemrec)
    return pages

# get the history for a given page
def gethist(name):
    url = f"https://www.werelate.org/w/index.php?title={urllib.parse.quote(name)}&action=history&limit=50"
    hist = []
    while True:
        print(f"fetching history page {url}")
        response = wrsession.get(url)
        response.raise_for_status()
        count['fetchhist'] += 1;

        soup = BeautifulSoup(response.content, 'html.parser')

        pagehistorylist = soup.find("ul", id="pagehistory")
        # deleted pages have no history
        if (not pagehistorylist):
            return []
        
        for histitem in pagehistorylist.find_all("li", recursive=False):
            creator = histitem.find("span", class_="history-user").find('a').get('title')
            # remove the User: prefix
            if (creator.startswith("User:")):
                creator = creator[5:]
            histlink = histitem.find("a", string=re.compile("^\d\d:\d\d, \d"))
            pubDate = histlink.string
            title = histlink.get("title")
            link = werelateurl+histlink.get("href")
            print(f" history {title} {creator} {link} {pubDate}")
            hist.append({"title": title, "link": link, "pubDate": pubDate, "creator": creator})

        # look for link to next page
        next_page_link = soup.find('a', string=re.compile('^next \d+'))
        if (next_page_link):
            url = 'https://www.werelate.org' + next_page_link.get('href')
        else:
            break
    return hist

    
# get the raw xml from the page
def getraw(page, verid=None):
    url = None
    if (page.startswith("https://")):
        url = page+"?action=raw"
    else:
        url = f"{werelateurl}/w/index.php?title={urllib.parse.quote(page)}&oldid={verid}&action=raw"

    response = wrsession.get(url)
    response.raise_for_status()
#    time.sleep(random.random())
    count['fetchraw'] += 1;
    txt = response.text
    #print(txt)

    # reconstruct into valid xml
    txt = re.sub("\s*<show_sources_images_notes/>\s*", "", txt)
    txt = re.sub("^\s+", "", txt)
    # some old versions have this
    txt,c = re.subn("child of family", "child_of_family", txt)
    if (c > 0):
        print("INVALID XML")
        
    g = None
    if (txt.startswith('<person>')):
        g = re.search(r"(<person>.*)(</person>)(.*)", txt, flags=re.DOTALL)
    elif (txt.startswith('<family>')):
        g = re.search(r"(<family>.*)(</family>)(.*)", txt, flags=re.DOTALL)
    # probably a redirect
    if (not g):
        print(f"Error: no content found in {page}")
        return None
    txt = g.group(1) + g.group(2)
    body = xml.etree.ElementTree.Element("body", {})
    body.text = g.group(3)
    try:
        root = xml.etree.ElementTree.fromstring(txt)
    except xml.etree.ElementTree.ParseError:
        print(f"Error: invalid xml for {page} ver {verid}")
        return None
    root.append(body)
    return root

# given the parsed xml returned by getraw(), pick out the relations, and massage
# them into lists with proper prefixes
def xml2relations(rec):
    relations = {
        "child_of_family": [],
        "spouse_of_family": [],
        "husband": [],
        "wife": [],
        "child": [],
        }
    if (not rec):
        return relations
    
    relations["child_of_family"]  = ["Family:"+f.get('title') for f in rec.findall("child_of_family")]
    relations["spouse_of_family"] = ["Family:"+f.get('title') for f in rec.findall("spouse_of_family")]
    relations["husband"]          = ["Person:"+f.get('title') for f in rec.findall("husband")]
    relations["wife"]             = ["Person:"+f.get('title') for f in rec.findall("wife")]
    relations["child"]            = ["Person:"+f.get('title') for f in rec.findall("child")]
    return relations

def getscore(root):
    score = 0
    scorever = 1  # increment this if the code below changes

    # if we got something non-xml, return 0 for everything which
    # should signal to the caller that it shouldn't be stored
    if (not isinstance(root,  xml.etree.ElementTree.Element)):
        return [0,0]
    
    # go through each source_citation
    #<source_citation id="S2" title="Source:Find A Grave" record_name="{{fgravemem|28164527|Henry Sylvester Davis}}"/>
    sources = {}
    for s in root.findall('source_citation'):
        if (not s.get('title')):
            sources[s.get('id')] = 1
        elif (s.get('title').startswith('Source:')):
            sources[s.get('id')] = 3
        elif (s.get('title').startswith('MySource:')):
            sources[s.get('id')] = 2
        else:
            sources[s.get('id')] = 1
        score = score + sources[s.get('id')]
        # if there is text in the source citation, add points
        if (s.text and len(s.text) > 8):
            score = score + 1
            
    # grab all the notes too... we store them as a source
    for n in root.findall("note"):
        if (n and len(n.text) > 8):
            sources[n.get("id")] = 1
        
    # notes get a score too
    for n in root.findall('note'):
        score = score + 1

    # go through each event_fact
    #<event_fact type="Death" date="15 Jul 1939" place="Noble, Ohio, United States" sources="S2"/>
    for e in root.findall('event_fact'):
        # each event scores a point
        score = score + 1
        # and points for each source according to it's type/value
        if (e.get("sources")):
            refs = re.split("[,\s]+", e.get("sources"))
            for s in refs:
                if (s in sources):
                    score = score + sources[s]
        if (e.get("notes")):
            refs = re.split("[,\s]+", e.get("notes"))
            for s in refs:
                score = score + 1

    # text in the page gets you points as well
    score = score + math.ceil(len(root.find("body").text)/256)
    # TBD count source refs <ref name="S1"/>

    return [score, scorever]
        
#------------------------------------------------------------------------
def opendb():
    db = sqlite3.connect(dbfile)
    db.execute('PRAGMA busy_timeout = 30000')
    return db

# add a page history entry to the database or update it if needed
def adddbhist(db, name, verid, ts, user, score, scoredif, scorever, newver):
    cursor = db.cursor()
    # normalize the timestamp to something sqlite can cope  with
    ts = parser.parse(ts).replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ')

    cursor.execute('SELECT * FROM vers WHERE name = ? AND id = ?',
                   [name, verid]);
    row = cursor.fetchone()
    if (row):
        print(f"already have {name} {verid}")
        # only update if the score has changed
        if (int(row[5]) < scorever):
            print(f"  update score from ver {row[5]} to {scorever}")
            cursor.execute("UPDATE vers SET score = ?, scoredif=?, scorever = ? WHERE  name = ? AND id = ?",
                           (score, scoredif, scorever, name, verid))
            db.commit()
    else:
        cursor.execute('INSERT OR IGNORE INTO vers (name, id, ts, user, score, scoredif, scorever, newver) VALUES (?,?,?,?,?,?,?,?)',
                       (name, verid, ts, user, score, scoredif, scorever, newver))
        db.commit()

def getdbhistids(db, name):
    cursor = db.cursor()
    cursor.execute('SELECT id FROM vers WHERE name = ? ORDER BY ts', [name])
    verlist = []
    for row in cursor:
        verlist.append(row[0])
    return verlist

def getdbhist(db, name):
    cursor = db.cursor()
    cursor.execute('SELECT ts,score,scoredif,newver,id FROM vers WHERE name = ? ORDER BY ts', [name])
    verlist = []
    for row in cursor:
        verlist.append(row)
    return verlist

def addrelations(db, name, rels):
    cursor = db.cursor()
    cursor.execute('INSERT OR IGNORE INTO relations (name, child_of_family, spouse_of_family, husband, wife, child) VALUES (?,?,?,?,?,?)',
                   [name,
                    "|".join(rels["child_of_family"]),
                    "|".join(rels["spouse_of_family"]),
                    "|".join(rels["husband"]),
                    "|".join(rels["wife"]),
                    "|".join(rels["child"])])
    db.commit()
    
def getrelations(db, name):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM relations WHERE name = ?', [name])
    row = cursor.fetchone()
    if (not row):
        return None
    rels = {
        "child_of_family":  row[1].split('|') if row[1] else [],
        "spouse_of_family": row[2].split('|') if row[2] else [],
        "husband":          row[3].split('|') if row[3] else [],
        "wife":             row[4].split('|') if row[4] else [],
        "child":            row[5].split('|') if row[5] else [],
        }
    return rels
    
def renamepage(db, oldname, newname):
    cursor = db.cursor()

    # check if the rename already happened
    cursor.execute('SELECT * FROM relations WHERE name = ?', [newname])
    row = cursor.fetchone()
    if (row):
        return

    # TBD check if origin exists
    
    cursor.execute("UPDATE vers SET name = ? WHERE  name = ?",
                   (newname, oldname))
    cursor.execute("UPDATE relations SET name = ? WHERE  name = ?",
                   (newname, oldname))
    db.commit()

def deletepage(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM vers WHERE name = ?', [name])
    cursor.execute('DELETE FROM relations WHERE name = ?', [name])
    db.commit()
    
    
#------------------------------------------------------------------------
def crawlrss():
    db = opendb()
    pgs = getrss(rssurl)
    for p in pgs:
        print(p)
        if ('delete' in p):
            print(f"DELETE {p['delete']}")
            deletepage(db, p['delete'])
        elif ('move' in p):
            print(f"RENAME {p['title']} to {p['move']}")
            renamepage(db, p['title'], p['move'])
        elif (re.search('^(Person|Family):', p['title'])):
            addpagehist(db, p['title'])
    print(f"RSS summary: {len(pgs)} entries from {pgs[-1]['pubDate']} to {pgs[0]['pubDate']}")

# fetch the history for a given page and add it to the DB
def addpagehist(db, name):
    hist = gethist(name)
    hist.reverse()   # oldest to newest
    lastscore = 0
    raw = None
    # optimization: get a list of revs in db, and only update missing ones
    verlist = getdbhist(db, name)
    #verdict = {t[-1]: t for t in verlist}
    verdict = {t[-1]: i for i,t in enumerate(verlist)}
    
    for h in hist:
        print("    ", end="")
        print(h)

        # check for renames
        m = re.search("(Person|Family):(.+) renamed to (Person|Family):(.+):", h['title'])
        if (m):
            print(f"Rename {m.group(1)}:{m.group(2)} to {m.group(3)}:{m.group(4)}")
            renamepage(db, m.group(1)+":"+m.group(2), m.group(3)+":"+m.group(4))
            # the original page is now a redirect page... but we don't care about that
            # but the version number we extract, below, is for that page
            # but that version is unimportant, skip it
            #name = m.group(3)+":"+m.group(4)
            continue
        
        # pick out the version number from the link url
        verid = None
        try:
            verid = re.search("oldid=(\d+)", h['link']).group(1)
        except AttributeError:
            print(f"Error: cannot find version id in {h['link']}")
            raise
        print(f"        verid = {verid} {h['pubDate']} new {h == hist[0]}")

        # skip if we already have it in the db
        if (verid in verdict):
            print(f"skipping version {verid} as it is already in db")
            lastscore = verlist[verdict[verid]][1]
            continue

        # get the raw xml content for calculating the score
        raw = getraw(name, verid)
        score = getscore(raw)

        # if it is the last record it is the latest, gather relations
        if (h==hist[-1]):
            relations = xml2relations(raw)
            addrelations(db, name, relations)

        if (score[1] >= 0):
            print(f"     score diff {score[0] - lastscore}")
            adddbhist(db, name, verid, h['pubDate'], h['creator'],
                    score[0], (score[0] - lastscore), score[1], int(h==hist[0]))
            lastscore = score[0]
        else:
            print("     no score on that one")

    # update the relations page as well, but only if we got something new
    if (raw):
        relations = xml2relations(raw)
        addrelations(db, name, relations)


def crawltree(name):
    db = opendb()
    connections = [name]
    visited = {}
    while connections:
        name = connections.pop(0)
        if (name in visited):
            continue
        visited[name] = True
        print(f"traversing {name}")

        # get the relations either from DB or xml
        relations = getrelations(db, name)
        if (not relations):
            relations = xml2relations(getraw(name))

            # now add it to the database
            addrelations(db, name, relations)
            addpagehist(db, name)

        # append all the relations on for the next iteration
        for r in ("child_of_family", "spouse_of_family", "husband", "wife", "child"):
            if (relations[r]):
                for i in (relations[r]):
                    if (not i in visited):
                        connections.append(i)
        print(f"connections visited {len(visited)} pending {len(connections)}")

def crawlall(startpage=""):
    db = opendb()

    if (startpage):
        m =re.search("^(Person|Family):(.+)", startpage)
        if (m.group(1) == "Person"):
            starturls = [allpersonurl+m.group(2), allfamilyurl]
        elif (m.group(1) == "Family"):
            starturls = [allfamilyurl+m.group(2), allpersonurl]
        else:
            print(f"do not know what to do with {startpage}")
            return
    else:
        if (random.random() > 0.5):
            starturls = [allpersonurl, allfamilyurl]
        else:
            starturls = [allfamilyurl, allpersonurl]
        
    for url in starturls:
        while True:
            print(f"Loading {url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            names = []
            contentbox = soup.find("td", id="contentbox")
            if not contentbox:
                print(f"Error: no contentbox in {url}")
                continue
            
            for link in contentbox.find_all("a", href=re.compile("/wiki/(Person|Family):")):
                # skip redirects
                if (link.find_parent(class_='allpagesredirect')):
                    continue
                name = link.get('title')
                #print(f"found link {name}")
                names.append(name)
            
            # got all the links, on to the next page
            next_page_link = soup.find('a', string=re.compile('^Next page '))
            if not next_page_link:
                print(f"no next page link, stopping")
                break
            url = 'https://www.werelate.org' + next_page_link.get('href')

            if (len(names)):
                print(f"all pages got {len(names)} pages, from {names[0]} to {names[-1]}")
            else:
                print(f"all pages got {len(names)} pages")
                continue
            
            # process the batch we just got, but if we have the last in the list
            # skip the whole batch
            #relations = getrelations(db, names[-1])
            #if (relations):
            #    continue

            for name in names:
                # try getting relations from db
                relations = getrelations(db, name)
                if (relations):
                    continue

                try:
                    # new page, fetch info and add to the db
                    relations = xml2relations(getraw(name))
                    addrelations(db, name, relations)
                    addpagehist(db, name)
                except Exception as e:
                    print(f"Failed to load info for {name}, skipping")
            
def pageinfo(db, name):
    relations = getrelations(db, name)
    verlist = getdbhist(db, name)

    print(relations)
    for h in verlist:
        print("    ", end="")
        print(h)


def jsontreeup(db, name):
    relations = getrelations(db, name)
    print(relations)
    
# this is used when the scoring algorithm changes, need to go back and update the scores
def updatescore():
    db = opendb()
    cursor = db.cursor()
    # this trick will get us the current version number of the scoring algorithm
    score = getscore(None)
    
    cursor.execute("SELECT * FROM vers WHERE scorever != ?", [score[1]])
    for row in cursor:
        score = getscore(getraw(row[0], row[1]))
        print(f"need to update score for {row[0]} ver {row[2]} was {row[4]} now {score[0]}")
        newrow = (row[0], row[1], row[2], row[3], score[0], score[1])
        adddbhist(db, row[0], row[1], row[2], row[3], score[0], score[1], 0)
    
def main():
    action = sys.argv[1]
    if (action == "crawlrss"):
        crawlrss()
    elif (action == "crawltree"):
        for p in sys.argv[2:]:
            crawltree(p)
    elif (action == "crawlall"):
        if len(sys.argv) <= 2:
            crawlall()
        else:
            for p in sys.argv[2:]:
                crawlall(p)
    elif (action == "getraw"):
        for p in sys.argv[2:]:
            print(getraw(p))
    elif (action == "score"):
        score = getscore(getraw(sys.argv[2]))
        print(f"quality store: {score[0]} {score[1]}")
    elif (action == "delete"):
        db = opendb()
        for p in sys.argv[2:]:
            deletepage(db, p)
    elif (action == "add"):
        db = opendb()
        for p in sys.argv[2:]:
            addpagehist(db, p)
    elif (action == "reload"):
        db = opendb()
        for p in sys.argv[2:]:
            deletepage(db, p)            
            addpagehist(db, p)
    elif (action == "info"):
        db = opendb()
        for p in sys.argv[2:]:
            pageinfo(db, p)
    elif (action == "jsontreeup"):
        db = opendb()
        jsontreeup(db, sys.argv[2])
        
    # only needed when the score schema changes
    elif (action == "updatescore"):
        updatescore()
    else:
        print("Error: unknown action")

    print(f"Counts:  {count}")
    
#------------------------------------------------------------------------
if __name__ == "__main__":
    main()
