#!/usr/bin/env python3

import requests
import xml.etree.ElementTree
import re
import sqlite3
from dateutil import parser
from datetime import datetime,timedelta,timezone
import sys
import math

dbfile="wr.db"
werelateurl = "https://www.werelate.org"
rssurl = werelateurl+"/wiki/Special:Recentchanges?feed=rss"
#rssurl = werelateurl+"/wiki/Special:Recentchanges?feed=rss&limit=500&days=3"
count = {'fetchrss':0, 'fetchraw':0}
#------------------------------------------------------------------------
def getrss(url):
     
    response = requests.get(url)
    response.raise_for_status()
    count['fetchrss'] += 1;
    
    root = xml.etree.ElementTree.fromstring(response.content)
    # TBD this should actually come from the xml file...
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}

    pages = []
    # The standard structure of an RSS feed: <rss><channel><item><link>
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        creator = item.find('dc:creator', ns)
        if (type(creator) == "None"):
            creator = "unknown"
        else:
            creator = creator.text
        #print(f"rss item {title} {link} {pubDate} {creator}")

        pages.append({"title": title, "link": link, "pubDate": pubDate, "creator": creator})
    return pages

# get the raw xml from the page
def getraw(page, verid=None):
    url = None
    if (page.startswith("https://")):
        url = page+"?action=raw"
    else:
        url = f"{werelateurl}/w/index.php?title={page}&oldid={verid}&action=raw"

    response = requests.get(url)
    response.raise_for_status()
    count['fetchraw'] += 1;
    txt = response.text
    print(txt)

    # reconstruct into valid xml
    txt = re.sub("\s*<show_sources_images_notes/>\s*", "", txt)
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
    root = xml.etree.ElementTree.fromstring(txt)
    root.append(body)
    return root

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
    return sqlite3.connect(dbfile)
    
def addhist(db, name, verid, ts, user, score, scorever):
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
            cursor.execute("UPDATE vers SET score = ?, scorever = ? WHERE  name = ? AND id = ?",
                           (score, scorever, name, verid))
            db.commit()
    else:
        cursor.execute('INSERT OR IGNORE INTO vers (name, id, ts, user, score, scorever) VALUES (?,?,?,?,?,?)',
                       (name, verid, ts, user, score, scorever))
        db.commit()
    
#------------------------------------------------------------------------
def crawlrss():
    db = opendb()
    pgs = getrss(rssurl)
    for p in pgs:
        print(p)
        if (re.search('^(Person|Family):', p['title'])):
            hist = getrss(f"{werelateurl}/w/index.php?title={p['title']}&action=history&feed=rss")
            for h in hist:
                print("    ", end="")
                print(h)
                verid = None
                try:
                    verid = re.search("diff=(\d+)", h['link']).group(1)
                except AttributeError:
                    print(f"Error: cannot find version id in {h['link']}")
                print(f"        verid = {verid}")
                # TBD optimization: get a list of revs in db, and only update missing ones
                score = getscore(getraw(p['title'], verid))
                if (score[1] > 0):
                    addhist(db, p['title'], verid, h['pubDate'], h['creator'], score[0], score[1])

def updatescore():
    db = opendb()
    cursor = db.cursor()
    score = getscore(None)
    cursor.execute("SELECT * FROM vers WHERE scorever != ?", [score[1]])
    for row in cursor:
        score = getscore(getraw(row[0], row[1]))
        print(f"need to update score for {row[0]} ver {row[2]} was {row[4]} now {score[0]}")
        newrow = (row[0], row[1], row[2], row[3], score[0], score[1])
        addhist(db, row[0], row[1], row[2], row[3], score[0], score[1])
    
def main():
    action = sys.argv[1]
    if (action == "crawlrss"):
        crawlrss()
    elif (action == "score"):
        score = getscore(getraw(sys.argv[2]))
        print(f"quality store: {score[0]} {score[1]}")
    elif (action == "updatescore"):
        updatescore()
    else:
        print("Error: unknown action")
        
#------------------------------------------------------------------------
if __name__ == "__main__":
    main()
