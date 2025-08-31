#!/usr/bin/env python3

import requests
import xml.etree.ElementTree
import re
import sqlite3
from dateutil import parser
from datetime import datetime,timedelta,timezone
import sys

dbfile="wr.db"
werelateurl = "https://www.werelate.org"
rssurl = werelateurl+"/wiki/Special:Recentchanges?feed=rss"

#------------------------------------------------------------------------
def getrss(url):
     
    response = requests.get(url)
    response.raise_for_status()

    root = xml.etree.ElementTree.fromstring(response.content)

    pages = []
    # The standard structure of an RSS feed: <rss><channel><item><link>
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        pubDate = item.find('pubDate').text
        creator = item.find('dc:creator').text if item.find('dc:creator') else ""
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
    txt = response.text
    print(txt)
    # reconstruct into valid xml
    txt = re.sub("\s*<show_sources_images_notes/>\s*", "", txt)
    g = re.search(r"(<person>.*)(</person>)(.*)", txt, flags=re.DOTALL)
    txt = g.group(1) + g.group(2)
    body = xml.etree.ElementTree.Element("body", {})
    body.text = g.group(3)
    root = xml.etree.ElementTree.fromstring(txt)
    root.append(body)
    return root

def getscore(root):
    score = 0
    # go through each source_citation
    #<source_citation id="S2" title="Source:Find A Grave" record_name="{{fgravemem|28164527|Henry Sylvester Davis}}"/>
    sources = {}
    for s in root.findall('source_citation'):
        sources[s.get('id')] = s
        if (s.get('title').startswith('Source:')):
            score = score + 3
        elif (s.get('title').startswith('MySource:')):
            score = score + 2
        else:
            score = score + 1
             
    # go through each event_fact
    #<event_fact type="Death" date="15 Jul 1939" place="Noble, Ohio, United States" sources="S2"/>
    for e in root.findall('event_fact'):
        if (e.find("sources")):
            sources = re.split("[,\s]+", e.find("sources").text)

    score = score + len(root.find("body").text)/256

    return score
        
#------------------------------------------------------------------------
def opendb():
    return sqlite3.connect(dbfile)
    
def addhist(db, name, verid, ts, user):
    cursor = db.cursor()
    # normalize the timestamp to something sqlite can cope  with
    ts = parser.parse(ts).replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ')
    
    cursor.execute('INSERT OR IGNORE INTO vers (name, id, ts, user, score, scorever) VALUES (?,?,?,?,?,?)',
                   (name, verid, ts, user, 0, 0))
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
                raw = getscore(getraw(p['title'], verid))
                addhist(db, p['title'], verid, h['pubDate'], h['creator'])

def main():
    action = sys.argv[1]
    if (action == "crawlrss"):
        crawlrss()
    elif (action == "score"):
        score = getscore(getraw(sys.argv[2]))
        print(score)
    else:
        print("Error: unknown action")
        
#------------------------------------------------------------------------
if __name__ == "__main__":
    main()
