# -*- coding: utf-8 -*-
# qcl
#

import sys
import projizz

if len(sys.argv) <= 1:
    print "$ python ./simpleSortedViewer.py [ps json]"
else:
    filename = sys.argv[1]
    ps = projizz.jsonRead(filename)
    sortedp = projizz.getSortedStatistic(ps)
    model,table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    for relation in sortedp:
        print relation
        for ptnId,ptnS in sortedp[relation]:
            print "%s\t%s %s %s" % (relation,table[ptnId]["pattern"],ptnId,ptnS)
