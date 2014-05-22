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

def tryToFindRela(jobid, filename, dataInputPath, resultOutPath, ptnOutputPath, model, tree):
    content = projizz.combinedFileReader(os.path.join(dataInputPath,filename))
    print "Worker %d : Read %s into filter" % (jobid,filename)
    count = 0
    dealL = 0
    results = {}
    patternEx = {}
    for articleName in content:
        result = {}
        pattern = []
        article = projizz.articleSimpleSentenceFileter(content[articleName])
        for line in article:
            tokens = projizz._posTagger.tag(line)
            patternExtracted = projizz.naiveExtractPatterns(tokens,model)

            for ptnId,start,to in patternExtracted:
                dealL += 1
                rels = tree[ptnId]["relations"]

                if len(rels) < 4:
                    for r in rels:
                        if not r in result:
                            result[r] = 0
                        result[r] += 1

                if not ptnId in pattern:
                    pattern.append(ptnId)
                
                if dealL % 10000 == 0:
                    print "Worker %d deal with %d lines." % (jobid,dealL)
                    
        
        results[articleName] = result
        patternEx[articleName] = pattern
        count += 1
        if count % 100 == 0:
            print "Worker %d deal with %d files" % (jobid,count)
            gc.collect()

    projizz.combinedFileWriter(results,os.path.join(resultOutPath,filename))
    projizz.combinedFileWriter(patternEx,os.path.join(ptnOutputPath,filename))
    print "Worker %d : Write results out to %s." % (jobid,filename)


def main(dataInputPath,resultOutPath,ptnOutputPath):

    model, table = projizz.readPrefixTreeModel("../prefix_tree_model/patternTree.json")

    if not os.path.isdir(resultOutPath):
        os.mkdir(resultOutPath)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print "Number of core: %d" % (multiprocessing.cpu_count())
    start_time = datetime.now()
    
    jobN = 0
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            pool.apply_async(tryToFindRela, (jobN, filename, dataInputPath, resultOutPath,ptnOutputPath, model, table))
            jobN+=1

    pool.close()
    pool.join()

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

    projizz.combinedFileWriter(model,os.path.join(ptnOutputPath,"model"))
    projizz.combinedFileWriter(table,os.path.join(ptnOutputPath,"table"))


if __name__ == "__main__":
    if len(sys.argv) > 3:
        dataInputPath = sys.argv[1]
        resultOutPath = sys.argv[2]
        ptnOutputPath = sys.argv[3]
        main(dataInputPath,resultOutPath,ptnOutputPath)
    else:
        print "$ python ./testRun.py [data input dir] [data output dir] [ptn output dir]"
