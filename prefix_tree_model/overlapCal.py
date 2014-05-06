# -*- coding: utf-8 -*-
# qcl
# Calculate the overlap of each relationship (property)
# Relationship Files location: ../naive_model/PbR
# Pattern Prefix Tree location: ./patternTree.json

import os
import sys
from projizzTreeModel import readModel

def overlapDetect():
    #print "Start to detect overlap between relationships"
    treeModel = readModel("./patternTree.json")

    overlap = {}
    patterns = {}
    for filename in os.listdir("../naive_model/PbR"):
        relation = filename[:-4]
        f = open(os.path.join("../naive_model/PbR",filename),"r")
        overlap[relation] = {}
        for line in f:
            words = line[:-2].lower().split()
            #print filename,words
            t = treeModel
            for word in words:
                t = t[word]

            for rls in t["_rls_"]:
                if not rls in overlap[relation]:
                    overlap[relation][rls] = 0
                overlap[relation][rls] += 1
            
            if not t["_ptn_"] in patterns:
                patterns[t["_ptn_"]] = []
            if relation not in patterns[t["_ptn_"]]:
                patterns[t["_ptn_"]].append(relation)

        #print relation,len(overlap[relation]),overlap[relation]

        f.close()

    #print "unique patten #:",len(patterns)

    if len(sys.argv) > 1:
        for relation in overlap:
            over = overlap[relation]
            over = sorted(over.items(), key=lambda x:x[1],reverse=True)
            print relation
            rela, total = over[0]
            for rela,count in over:
                p = 100*float(count)/float(total)
                if p > 50.0:
                    print "\t",rela,count,"(%.2f%%)" % (p)
                else:
                    break
    else:
        sortedPattern = sorted(patterns.items(), key=lambda x:len(x[1]), reverse=True)
        for ptn,rls in sortedPattern:
            print ptn,len(rls)
    


if __name__ == "__main__":
    overlapDetect()
