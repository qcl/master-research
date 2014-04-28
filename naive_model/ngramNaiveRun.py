# -*- coding: utf-8 -*-
# qcl
# Generate raw n-gram from wiki reource.
#

import simplejson as json
import os
import sys
import Queue
from nltk.util import ngrams
from nltk import word_tokenize
from datetime import datetime
from projizzWorker import Manager
from projizzReadNGramModel import toStringForm,readModel

def main(modelPath,inputFiles,outputPath):
    ngram,models = readModel(modelPath)
    rule = ".json"
    files = Queue.Queue(0)

    start_time = datetime.now() 

    # if target dir not exist, create it.
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    def workerFunction(jobObj,tid,args):
        content = json.load(open(os.path.join(inputFiles,jobObj),"r"))
        print "worker #%02d read file %s" % (tid,jobObj)
        dealL = 0
        count = 0
        results = {}
        for subFilename in content:
            count += 1
            ngl = []
            for line in content[subFilename]:
                dealL += 1
                # FIXME - only implement bigram
                ngs = line.lower().replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(")"," ").replace("("," ").split()
                for i in xrange(1,len(ngs)):
                    ngl.append("%s\t%s" % (ngs[i-1],ngs[i]))
                
                # try to find hit.
                result = {}
                if len(ngl) < 1:
                    continue
                for model in models:
                    mn = models[model]
                    for ng in ngs:
                        if ng in mn:
                            if not model in result:
                                result[model] = 0
                            result[model] += 1

                if dealL%10000 == 0:
                    print "worker #%02d deal with %d lines" % (tid,dealL)
            
            if count % 100 == 0:
                print "worker #%02d scan %d files" % (tid,count)
            results[subFilename] = result

        json.dump(results,open(os.path.join(outputPath,jobObj),"w"))

    fileNameList = []
    for filename in os.listdir(inputFiles):
        if rule in filename:
            #fileNameList.append(filename)
            files.put(filename)
            
    #fileNameList.sort()
    #for filename in fileNameList:
    #    files.put(filename)

    manager = Manager(workerNumber=25)
    manager.setJobQueue(files)
    manager.setWorkerFunction(workerFunction)
    manager.startWorking()

    diff = datetime.now() - start_time
    print "All job done, use %d.%d secs" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        modelPath  = sys.argv[1]
        inputFiles = sys.argv[2]
        outputPath = sys.argv[3]

        main(modelPath,inputFiles,outputPath)

    else:
        print "$ python ./ngramNaiveRun.py [ModelFilePath] [input-files-dir] [output-files-dir]"

