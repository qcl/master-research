# -*- coding: utf-8 -*-
# qcl
# test run, only possible property number < 4 will be propose.
#
import os
import sys
import projizz
import multiprocessing

def tryToFindRela(jobid, filename, dataInputPath, resultOutPath, model, tree):
    content = projizz.combinedFileReader(os.path.join(dataInputPath,filename))
    count = 0
    for articleName in content:
        article = projizz.articleSimpleSentenceFileter(content[articleName])
        for line in article:
            tokens = projizz._posTagger.tag(line)
            patternExtracted = projizz.naiveExtractPatterns(tokens,model)

        # TODO

def main(dataInputPath,resultOutPath):

    model, table = projizz.readPrefixTreeModel("../prefix_tree_model/patternTree.json")

    if not os.path.isdir(resultOutPath):
        os.mkdir(resultOutPath)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print "Number of core: %d" % (multiprocessing.cpu_count())
    start_time = datetime.now()
    
    jobN = 0
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            pool.apply_async(tryToFindRela, (jobN, filename, dataInputPath, resultOutPath, model, table))
            jobN+=1

    pool.close()
    pool.join()

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        dataInputPath = sys.argv[1]
        resultOutPath = sys.argv[2]
        main(dataInputPath,resultOutPath)
    else:
        print "$ python ./testRun.py [data input dir] [data output dir]"
