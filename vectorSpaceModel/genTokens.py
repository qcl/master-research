# -*- coding: utf-8 -*-
# qcl
# build tokens

import os
import sys
import copy
import projizz
import pymongo
import multiprocessing
from datetime import datetime
from nltk.stem import *

#
#
#
def mapper(jobid,filename,inputPath,outputPath,model,table):

    # Read article
    article = projizz.jsonRead( os.path.join(inputPath,filename) )

    stemmer = PorterStemmer()
    tks = {}

    print "Worker %d : Read %s into filter" % (jobid,filename)

    count = 0
    for line in article:
        count += 1
        tokens = projizz.getTokens(line)

        for token in tokens:
            t = stemmer.stem(token) 

            if t not in tks:
                tks[t] = 0

            tks[t] += 1

        if count % 500 == 0:
            print "worker %d done %d lines" % (jobid,count)


    # Remove stopwords
    for sw in projizz._stopwords:
        _sw = stemmer.stem(sw)
        if _sw in tks:
            tks.pop(_sw)

    projizz.jsonWrite(tks,os.path.join(outputPath,filename.replace(".json",".tf")))
    print "worker %d write out." % (jobid)

    return (filename,tks)
#
#
#
def preprocess(inputPath,outputPath):

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
            result.append( pool.apply_async( mapper, (t,filename,inputPath,outputPath model, table))  )
            t += 1
    pool.close()
    pool.join()

    words = {}
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

    



    # Calculate td-idf weight


    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 2:
        # args
        inputPath = sys.argv[1]
        outputPath = sys.argv[2]
        preprocess(inputPath,outputPath)
    else:
        print "$ python ./genTokens.py [model article .json dir] [output-dir]"
