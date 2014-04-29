# -*- coding: utf-8 -*-
# qcl
# prefix tree model naive runner.
# create: 2014.04.28
# modify: 2014.04.29

import os
import sys
import nltk
import time
import Queue
import multiprocessing
import simplejson as json
from datetime import datetime
from projizzTreeModel import readModel 

def selfDoingTokenize(line):
    # remove []!?,()"'
    return line.lower().replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(")"," ").replace("("," ").replace("\""," ").replace("'"," ").split()

def filterFiles(jobid,filename):
    content = json.load(open(os.path.join(dataInputPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)
    count = 0
    dealL = 0
    for subFilename in content:
        for line in content[subFilename]:
            line = selfDoingTokenize(line)
            if len(line) > 3:
                pos = nltk.pos_tag(line)
                #print len(pos)
            dealL += 1
            
            if dealL % 1000 == 0:
                print "Worker %d deal with %d lines." % (jobid,dealL)
        count += 1
        if count % 100 == 0:
            print "Worker %d deal with %d files" % (jobid,count)

def main(treeModelPath,dataInputPath,resultOutPath):

    # read model
    treeModel = readModel(treeModelPath)

    # create output dir
    if not os.path.isdir(resultOutPath):
        os.mkdir(resultOutPath)

    pool = multiprocessing.Pool(processes=4)

    start_time = datetime.now()

    jobN = 0 
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            pool.apply_async(filterFiles, (jobN,filename, ))
            jobN+=1

    pool.close()
    pool.join()

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    # args
    if len(sys.argv) > 3:
        treeModelPath = sys.argv[1]
        dataInputPath = sys.argv[2]
        resultOutPath = sys.argv[3]

        main(treeModelPath,dataInputPath,resultOutPath)

    else:
        print "$ python ./treeModelRun.py [treeModelPath] [dataInputPath] [resultOutPath]"

