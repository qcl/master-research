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
from projizzWorker import Manager
from projizzReadNGramModel import toStringForm

def main(inputFiles,outputPath,n):
    rule = ".json"
    files = Queue.Queue(0)

    # if target dir not exist, create it.
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    def workerFunction(jobObj,tid,args):
        content = json.load(open(os.path.join(inputFiles,jobObj),"r"))
        print "worker #%02d read file %s" % (tid,jobObj)
        dealL = 0
        rawGram = {}
        for subFilename in content:
            ngl = []
            for line in content[subFilename]:
                dealL += 1
                if n == 2:
                    # FIXME
                    ngs = line.lower().replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(")"," ").replace("("," ").split()
                    if len(ngs) > 2:
                        for i in xrange(1,len(ngs)):
                            ngl.append("%s\t%s" % (ngs[i-1],ngs[i]))

                    else:
                        pass

                else:
                    # do the n-gram using nltk
                    ngs = ngrams(word_tokenize(line.lower()),n)
                    if len(ngs) > 1:
                        continue
                    for ng in ngs:
                        ngl.append(toStringForm(ng))
            
                if dealL%10000 == 0:
                    print "worker #%02d deal with %d lines" % (tid,dealL)

            rawGram[subFilename] = ngl

        json.dump(rawGram,open(os.path.join(outputPath,jobObj),"w"))

    fileNameList = []
    for filename in os.listdir(inputFiles):
        if rule in filename:
            fileNameList.append(filename)
            #files.put(filename)
            
    fileNameList.sort()
    for filename in fileNameList:
        files.put(filename)

    manager = Manager(workerNumber=15)
    manager.setJobQueue(files)
    manager.setWorkerFunction(workerFunction)
    manager.startWorking()

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        n      = int(sys.argv[1])
        inputFiles = sys.argv[2]
        outputPath = sys.argv[3]

        main(inputFiles,outputPath,n)

    else:
        print "$ python ./ngramGenerator.py [n] [input-files-dir] [output-files-dir]"

