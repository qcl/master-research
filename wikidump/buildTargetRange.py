# -*- coding: utf-8 -*-
# qcl

import sys
import os

f = open("../dbpedia/dbpedia.instance.sorted.id.txt","r")
i = 1
r = open("./range/enwiki.01.range","r")
o = open("./range/target.01.id","w")
s = int(r.readline())
e = int(r.readline())

for line in f:
    t = int(line)
    if t <= e:
        o.write(str(t)+"\n")
    else:
        i += 1
        print "enwiki-%02d" % (i)
        o.close()
        r.close()
        o = open("./range/target.%02d.id" % (i),"w")
        r = open("./range/enwiki.%02d.range" % (i),"r")
        s = int(r.readline())
        e = int(r.readline())
        o.write(str(t)+"\n")
