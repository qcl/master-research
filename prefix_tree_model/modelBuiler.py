# -*- coding: utf-8 -*-
# qcl
# Build prefix-tree model.
# merge all patterns into a prefix tree, then write to patternTree.json
import operator
import sys
import os
import simplejson as json
import pickle
from nltk import word_tokenize
from nltk.util import ngrams

pos = []
f = open("../naive_model/patternsByRelations.log","r")
max_len = 0
max_ptn = []
max_rls = ""

tree = {}

count = 0
dup = 0
for line in f:
    relationship = line.split("\t")[0]
    g = open("../naive_model/PbR/%s.txt" % (relationship),"r")

    print relationship

    for l in g:
        ws = l[:-1].lower().replace(";","").split()
        count += 1
        #print ws
        for w in ws:
            if "[[" in w or "*" in w:
                if not w in pos:
                    pos.append(w)
        t = tree
        for w in ws:
            if not w in t:
                t[w] = {}
            t = t[w]

        if "_rls_" in t:
            dup += 1
            if not relationship in t["_rls_"]:
                t["_rls_"].append(relationship)
            if len(t["_rls_"]) > max_len:
                max_len = len(t["_rls_"])
                max_rls = t["_rls_"]
                max_ptn = ws
        else:
            t["_rls_"] = [relationship]

    g.close()
f.close()

h = open("./patternTree.json","w")
json.dump(tree,h)
h.close()

# some testing code here.
print pos
print count,dup
print tree["has"]["released"]["on"]["_rls_"]
print max_len,max_ptn,max_rls
print tree.keys()
print len(tree.keys())
