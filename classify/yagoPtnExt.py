# -*- coding: utf-8 -*-
# qcl
# test run, only possible property number < 4 will be propose.
#
import os
import gc
import sys
import projizz
import multiprocessing

from datetime import datetime

def tryToFindRela(jobid, filename, dataInputPath, ptnOutputPath, model, table):
    content = projizz.combinedFileReader(os.path.join(dataInputPath,filename))
    print "Worker %d : Read %s into filter" % (jobid,filename)
    count = 0
    dealL = 0
    patternEx = {}
    for articleName in content:
        pattern = []
        article = projizz.articleSimpleSentenceFileter(content[articleName])
        lineCount = 0
        for line in article:
            dealL += 1
            tokens = projizz._posTagger.tag(line)
            patternExtracted = projizz.naiveExtractPatterns(tokens,model)
            if len(patternExtracted) > 0:
                pattern.append((lineCount,patternExtracted))
            if dealL % 10000 == 0:
                print "Worker %d deal with %d lines." % (jobid,dealL)
            lineCount += 1
        
        patternEx[articleName] = pattern
        count += 1
        if count % 100 == 0:
            print "Worker %d deal with %d files" % (jobid,count)
            gc.collect()

    projizz.combinedFileWriter(patternEx,os.path.join(ptnOutputPath,filename))
    print "Worker %d : Write results out to %s." % (jobid,filename)

def main(dataInputPath,ptnOutputPath):

    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model","../yago/yagoPatternTree.table")

    if not os.path.isdir(ptnOutputPath):
        os.mkdir(ptnOutputPath)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print "Number of core: %d" % (multiprocessing.cpu_count())
    start_time = datetime.now()
    
    jobN = 0
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            pool.apply_async(tryToFindRela, (jobN, filename, dataInputPath, ptnOutputPath, model, table))
            jobN+=1

    pool.close()
    pool.join()

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        dataInputPath = sys.argv[1]
        ptnOutputPath = sys.argv[2]
        main(dataInputPath,ptnOutputPath)
    else:
        print "$ python ./testRun.py [data input dir] [ptn output dir]"
