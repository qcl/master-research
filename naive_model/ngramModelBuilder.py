# -*- coding: utf-8 -*-
# qcl
# Build ngram model.
import operator
import sys
import os
import simplejson as json
import pickle
from nltk import word_tokenize
from nltk.util import ngrams

if len(sys.argv) < 2:
    print "Usage: $ python ./ngramModelBuilder.py [N]"
    sys.exit(0)

n = int(sys.argv[1])
modelPath = "./%d-gramModel" % (n)

# create output model path
if not os.path.isdir(modelPath):
    os.mkdir(modelPath)

#pos = []
f = open("./patternsByRelations.log","r")
for line in f:
    pattern = line.split("\t")[0]
    g = open("./PbR/%s.txt" % (pattern),"r")

    print pattern

    count = 0
    grams = {}
    for l in g:
        ws = l[:-1].lower().replace(";","").split()
        ws = ngrams(ws,n)
        if len(ws) < 1:
            continue

        for word in ws:
            if not word in grams:
                grams[word] = 0
            grams[word] += 1
            count+=1

    for word in grams:
        grams[word] /= float(count)
   
    h = open(os.path.join(modelPath,"%s.pkl" % (pattern)),"w")
    pickle.dump(grams,h)
    #print json.dumps(grams)
    #sorted_words = sorted(grams.iteritems(), key=operator.itemgetter(1))
    #sorted_words.reverse()
    #
    #h.write("{\n")
    #
    #l = len(sorted_words)
    #k = 0
    #for w in sorted_words:
    #    k += 1
    #    if k == l:
    #        h.write("\"%s\":%s\n" % (json.dumps(w[0]),json.dumps(w[1])))
    #    else:
    #        h.write("\"%s\":%s,\n" % (json.dumps(w[0]),json.dumps(w[1])))
    # 
    #h.write("}")
    h.close()
    

    g.close()
f.close()
#print pos
