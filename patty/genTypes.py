# -*- coding: utf-8 -*-

f = open("./patty.wiki.pattern.domain.range.types.txt","r")

types = {}
types["person"] = 0
types["organization"] = 0

for line in f:
    a = line.split("\t")
    if a[0] == "1":
        print "%s\tperson" % (a[1].split()[0])
        types["person"] += 1
    else:
        b = a[1].split()
        if b[-1] == "org":
            print "%s\t%s" % (b[0],"organization")
            types["organization"] += 1
        else:
            print "%s\t%s" % (b[0],b[-1])
            if not b[-1] in types:
                types[b[-1]] = 0
            types[b[-1]] += 1

## print types dist
#for key in types:
#    print key,types[key]

