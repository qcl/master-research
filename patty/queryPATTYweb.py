# -*- coding: utf-8 -*-
# qcl

import os
import sys
import urllib
import urllib2

url = "https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/pattyweb/index"
headers = {
        "Content-Type":"text/x-gwt-rpc; charset=UTF-8",
        "X-GWT-Module-Base":"https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/pattyweb/",
        "X-GWT-Permutation":"279729ADFF9BCD38F34BF9867E3C3A57",
        "User-Agent":"ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.99 Safari/537.36",
        }

def getData(rela):
    return "7|0|8|https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/pattyweb/|D752A98D9EFAE77BA5E912E43E7AB231|mpi.pattyweb.client.PatternService|getyagoRelationsSearchResults|java.lang.String/2004016611|dbpedia|"+rela+"|wkpDeepPaths_setsofngrams_pos_limitedyago|1|2|3|4|3|5|5|5|6|7|8|"

def getYAGOData(rela):
    return "7|0|8|https://d5gate.ag5.mpi-sb.mpg.de/pattyweb/pattyweb/|D752A98D9EFAE77BA5E912E43E7AB231|mpi.pattyweb.client.PatternService|getyagoRelationsSearchResults|java.lang.String/2004016611|yago|"+rela+"|wkpDeepPaths_setsofngrams_pos_limitedyago|1|2|3|4|3|5|5|5|6|7|8|"

urlopener = urllib2.build_opener( urllib2.HTTPSHandler() )
#request = urllib2.Request(url,data,headers)

#response = urlopener.open(request)
#result = response.read()

#print result

f = open("./patty.dbpedia.Relations.json")
for line in f:
    if "," in line:
        relaName = line[2:-3]
        print relaName
        request = urllib2.Request(url,getData(relaName),headers)
        g = open("./relationships/%s.txt" % (relaName), "w")
        response = urlopener.open(request)
        result = response.read()
        g.write(result)
        g.close()
f.close()

