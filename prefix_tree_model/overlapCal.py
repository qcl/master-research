# -*- coding: utf-8 -*-
# qcl
# Calculate the overlap of each relationship (property)
# Relationship Files location: ../naive_model/PbR
# Pattern Prefix Tree location: ./patternTree.json

import os
from projizzTreeModel import readModel

def overlapDetect():
    print "Start to detect overlap between relationships"
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
            patterns[t["_ptn_"]].append(relation)

        print relation,len(overlap[relation]),overlap[relation]

        f.close()

    print "unique patten #:",len(patterns)

    #for relation in overlap:
    #    over = 

if __name__ == "__main__":
    overlapDetect()
