# -*- coding: utf-8 -*-
# qcl

import sys
import os

#f = open("../dbpedia/dbpedia.instance.sorted.id.txt","r")
f = open("../dbpedia/dbpedia.instance.sorted.revid.txt","r")
i = 1
r = open("./range/enwiki.01.range","r")
o = open("./range/target.01.revid","w")
s = int(r.readline())
e = int(r.readline())

for line in f:
    t = int(line.split("\t")[0])
    if t <= e:
        o.write(line)
    else:
        i += 1
        print "enwiki-%02d" % (i)
        o.close()
        r.close()
        o = open("./range/target.%02d.revid" % (i),"w")
        r = open("./range/enwiki.%02d.range" % (i),"r")
        s = int(r.readline())
        e = int(r.readline())
        o.write(line+"\n")
