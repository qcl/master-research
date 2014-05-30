# -*- coding: utf-8 -*-
# qcl
#

import sys
import projizz

if len(sys.argv) <= 1:
    print "$ python ./simpleSortedPtnViewer.py [ps json]"
else:
    filename = sys.argv[1]
    ps = projizz.jsonRead(filename)
    sortedt = projizz.getSortedPatternStatistic(ps) 
    model,table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    for ptnId in sortedt:
        print "%s\t%s\t%s" % (ptnId, table[ptnId]["pattern"],sortedt[ptnId])
