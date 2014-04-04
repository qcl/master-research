# -*- coding: utf-8 -*-
# qcl
# read target.*.revid and query wiki api

import sys
import os
import urllib2
import json
import gc
import Queue
import threading
import time
from HTMLParser import HTMLParser

class QCLWikiParser(HTMLParser):
    resultString = u""

    def getResult(self):
        return self.resultString

    def handle_starttag(self,tag,sttrs):
        pass
    def handle_endtag(self,tag):
        pass
    def handle_data(self,data):
        self.resultString += data



def main(inputFile):
    print "Input range file:",inputFile
    revIds = Queue.Queue(0)

    done = []

    def thread():
        ident = threading.currentThread().ident
        while True:
            if revIds.empty():
                break
            try:
                revid = revIds.get()
            except:
                break
            if revid == None:
                continue
        
            rps = urllib2.urlopen("http://en.wikipedia.org/w/api.php?format=json&action=parse&prop=text&oldid=%s" % (revid))
            result = json.load(rps)
            if "error" in result:
                pass
                print "Query",revid,"error:",result["error"]["info"]
            else:
                title = result["parse"]["title"]
                html = result["parse"]["text"]["*"]
    
                #FIXME - parser
                parser = QCLWikiParser()
                parser.feed(html)
                o = open("%s.txt" % revid,"w")
                o.write(parser.getResult().encode("utf-8").replace("[edit]",""))
                o.close()
                o = open("%s.html" % revid,"w")
                o.write(html.encode("utf-8"))
                o.close()
                print "[DONE] %s,%s" % (title,revid)
    
            #print revIds.empty()
            #print revid,ident
            revIds.task_done()
            done.append(revid)
        # done
        pass

    f = open(inputFile,"r")

    l = 0
    for line in f:
        line = line.split("\t")
        wikiId = line[0]
        revId = line[1][:-1]
        revIds.put(revId)
        l+=1
    f.close()

    #targetLen = len(revIds)
   
    for x in xrange(45):
        t = threading.Thread(target=thread)
        t.start()

    #revIds.join()
    #time.sleep(1)
    #print "revIds join"

    while threading.activeCount() > 1:
        time.sleep(1)
        print "sleep",threading.activeCount(),revIds.qsize()

        if revIds.empty():
            break

    print l,len(done)

    sys.exit(0)

    #count = 0
    #while count < targetLen:
    #    gc.collect()
    #    print revIds[count]
    #
    #    count+=1
    #    if count == 1:
    #        break

        


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Usage: python queryWikiApi.py targets.revid"
