# -*- coding: utf-8 -*-
# qcl
# prefix tree model naive runner.
# 2014.04.28

import os
import sys
# for import the worker model
sys.path.append("../naive_model/")
import nltk
import Queue
import simplejson as json
from datetime import datetime
from projizzWorker import Manager
from projizzTreeModel import readModel 

def main(treeModelPath,dataInputPath,resultOutPath):

    # read model
    treeModel = readModel(treeModelPath)

    # create output dir
    if not os.path.isdir(resultOutPath):
        os.mkdir(resultOutPath)

    def workerFunction(jobObj,tid,args):
        pass

    start_time = datetime.now()
    
    TheDATA = []
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            TheDATA.append(json.load(open(os.path.join(dataInputPath,filename),"r")))
            print "Read %s into memory..." % (filename)
   
    print len(TheDATA)

    diff = datetime.now()
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

