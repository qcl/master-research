# -*- coding: utf-8 -*-
# qcl
# calculate amibiguity degree

import projizz

def ambiguityDegree():
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../patty/yagoPatternTreeWithConfidence.table")

    maxDegree = 0
    degree = {}
  
    for pid in table:
        if table[pid]["used"]:
            if "eval" in table[pid] and not table[pid]["eval"]:
                continue

            d = len(table[pid]["relations"])
            if not d in degree:
                degree[d] = []
                if d > maxDegree:
                    maxDegree = d
            
            degree[d].append(pid)


    for d in range(1,maxDegree+1):
        if not d in degree:
            print d,"0"
            continue
        #print d,len(degree[d])

        for pid in degree[d]:
            print "%d\t%s\t%s\t%s\t%.5f\t%d" % (d,pid,table[pid]["pattern"],table[pid]["relations"],table[pid]["confidence"],table[pid]["support"])

if __name__ == "__main__":
    ambiguityDegree()
