# -*- coding: utf-8 -*-
# count how many person in dbpedia.

import sys
import os
import rdflib

c = 0
name = ""
#g = rdflib.Graph()
for line in sys.stdin:
    if line[0] == "#":
        continue
    tmpN = line.split()[0][29:-1]
    if tmpN != name:
        print name
        name = tmpN
        c = c + 1
c = c - 1
print "total:",str(c)

