# -*- coding: utf-8 -*-
# qcl
# build tokens

import os
import sys
import copy
import math
import projizz
import pymongo
import multiprocessing
from datetime import datetime
from nltk.stem import *

#
#
#
def mapper(jobid,filename,inputPath,topN,outputPath,model,table):

    # Read article
    article = projizz.jsonRead( os.path.join(inputPath,filename) )

    stemmer = PorterStemmer()
    tks = {}

    print "Worker %d : Read %s into filter" % (jobid,filename)

    count = 0
    total = 0
    for line in article:
        count += 1
        tokens = projizz.getTokens(line)

        for token in tokens:
            t = stemmer.stem(token) 

            if t not in tks:
                tks[t] = 0

            tks[t] += 1
            total += 1

        if count % 1000 == 0:
            print "worker %d done %d lines" % (jobid,count)


    # Remove stopwords
    for sw in projizz._stopwords:
        _sw = stemmer.stem(sw)
        if _sw in tks:
            total -= tks[_sw]
            tks.pop(_sw)
        
    needRemove = []
    maxTF = 1
    for t in tks:
        # ignore only one time word
        if tks[t] <= 1:
            needRemove.append(t)
            total -= tks[t]
            continue

        # ignore the case contain number
        if "0" in t or "1" in t or "2" in t or "3" in t or "4" in t or "5" in t or "6" in t or "7" in t or "8" in t or "9" in t:
            needRemove.append(t)
            total -= tks[t]
            continue

        #if tks[t] > maxTF:
        #    maxTF = tks[t]

    for rm in needRemove:
        tks.pop(rm)

    projizz.jsonWrite(tks,os.path.join(outputPath,filename.replace(".json",".tfc")))
    
    ### select top N words
    # sort by tfc
    sortedTks = sorted(tks.items(), key=lambda x:x[1], reverse=True) 
    tks = {}
    maxTF = sortedTks[0][1]
    # Calculate tf
    top = 0
    for t,c in sortedTks:
        top += 1
        tks[t] = float(c)/float(maxTF) 
        if top == topN:
            break

    projizz.jsonWrite(tks,os.path.join(outputPath,filename.replace(".json",".tf")))
    print "worker %d write out." % (jobid)

    return (filename,tks)
#
#
#
def preprocess(inputPath,topN,outputPath):

    # Checking output path
    projizz.checkPath(outputPath)

    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../patty/yagoPatternTreeWithConfidence.table")

    start_time = datetime.now()

    # Processes pool
    proceessorNumber = multiprocessing.cpu_count()
    if proceessorNumber > 20:
        proceessorNumber = 20
    pool = multiprocessing.Pool(processes=proceessorNumber)
    t = 0
    result = []
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            result.append( pool.apply_async( mapper, (t,filename,inputPath, topN, outputPath, model, table))  )
            t += 1
    pool.close()
    pool.join()

    words = {}
    idf = {}
    tfs = {}

    # Reducer - DF
    types = 0
    for r in result:
        fn,tks = r.get()
        tfs[fn] = tks
        types += 1

        for t in tks:
            if t not in words:
                words[t] = 0
            words[t] += 1

    print "Doc#",types,"words#",len(words)

    projizz.jsonWrite(words,os.path.join(outputPath,"documentFreq.df"))

    # Calculate idf
    for w in words:
        if words[w] == 0:
            continue

        idf[w] = math.log(float(types)/float(words[w]),10)
    
    projizz.jsonWrite(idf,os.path.join(outputPath,"idf.idf"))
    print "Write out idf file"

    # Calculate td-idf weight
    for fn in tfs:
        tks = tfs[fn]
        weight = {}
        for t in tks:
            tf = tks[t]
            if t not in idf:
                continue
            
            weight[t] = tf * idf[t]

        projizz.jsonWrite(weight,os.path.join(outputPath,fn))
        print "build",fn,"tf-idf weight"


    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 3:
        # args
        inputPath = sys.argv[1]
        topN = int(sys.argv[2])
        outputPath = sys.argv[3]
        preprocess(inputPath,topN,outputPath)
    else:
        print "$ python ./genTopNTokens.py [model article .json dir] [topN] [output-dir]"
