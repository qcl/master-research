# -*- coding: utf-8 -*-
import sys
import os

prev = 0
for line in sys.stdin:
    if "    <id>" in line and line[4:8] == "<id>":
        ID = line[8:line.index("</id>")]
        if prev == 0:
            print int(ID)
        if int(ID) < prev:
            print "Yo!",ID
        prev = int(ID)

print prev
        
