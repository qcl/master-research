# -*- coding: utf-8 -*-
# qcl
# Count the overlap, and try to cluster the ontology
# Relationship Files location: ../naive_model/PbR
# Pattern Prefix Tree location: ./patternTree.json
# 
# 

import os
import sys
from projizzTreeModel import readModel

def buildOverlapMatrix():
    treeModel = readModel("./patternTree.json")
    keys = []

    # overlapMatrix [ relaA ] [ relaB ]
    # means that relaA in relaB count (%?)

    overlapMatrix = {}
    for filename in os.listdir("../naive_model/PbR/"):
        keys.append(filename[:-4])
    for relation in keys:
        overlapMatrix[relation] = {}
        for rela in keys:
            overlapMatrix[relation][rela] = 0

    # read tree
    for ontology in overlapMatrix:
        f = open("../naive_model/PbR/%s.txt" % (ontology), "r")
        for pattern in f:
            words = pattern[:-2].lower().split()
            t = treeModel
            for word in words:
                t = t[word]

            for relaA in t["_rls_"]:
                overlapMatrix[ontology][relaA] += 1

        f.close()

    for ontology in overlapMatrix:
        thisCount = overlapMatrix[ontology][ontology]
        for otherOntology in overlapMatrix[ontology]:
            if otherOntology == ontology:
                continue
            otherCount = overlapMatrix[ontology][otherOntology]
            if thisCount == otherCount:
                print ontology,otherOntology

if __name__ == "__main__":
    buildOverlapMatrix()
