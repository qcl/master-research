# -*- coding: utf-8 -*-
# qcl
# Generate n-gram from wiki files (in .json)
#

threadLimit = 5

import os
import sys
import time
import Queue
import threading
import pickle
import gc
import simplejson as json
from nltk.util import ngrams
from nltk import word_tokenize

def main(inputFiles,outputPath,n):
    rule = ".json"
    files = Queue.Queue(0)

    # if target dir not exist, create it.
    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    # define each thread
    class worker(threading.Thread):
        def __init__(self,tid):
            threading.Thread.__init__(self)
            self.daemon = True
            self.tid = tid
        def run(self):
            ident = threading.currentThread().ident
            print "worker#%02d start working!" % (self.tid)
            while True:
                try:
                    filename = files.get()
                    print "worker#%02d get data" % (self.tid)
                except:
                    break

                # do something here
                print "worker#%02d reading %s" % (self.tid, filename)
                
                # reading file
                f = open(os.path.join(inputFiles,filename),"r")
                fileContent = json.load(f)
                f.close()

                # deal with
                bigGrames = {}
                for subFileName in fileContent:
                    fc = fileContent[subFileName]
                    grams = {}
                    for line in fc:
                        ngs = ngrams(word_tokenize(line.lower()),n)
                        if len(ngs) < 1:
                            continue
                        
                        for ng in ngs:
                            if not ng in grams:
                                grams[ng] = 0
                            grams[ng] += 1
                    bigGrames[subFileName] = grams

                # write out to .pkl
                f = open(os.path.join(outputPath,filename.replace(".json",".pkl")),"w")
                pickle.dump(bigGrames,f)
                print "worker#%02d write to %s" % (self.tid, filename.replace(".json",".pkl"))
                f.close()

                # end of thread/run
                gc.collect()
                files.task_done()
                
            print "worker#%02d end." % (self.tid)



    # starting threading
    for x in xrange(threadLimit):
        th = worker(x)
        th.start()

    # reading list
    totalCount = 0
    for fj in os.listdir(inputFiles):
        if not rule in fj:
            continue
        totalCount+=1
        
        files.put(fj)

    print "Number of files =",totalCount

    files.join()
  
    print totalCount
    time.sleep(1)
    print "Done"

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        n      = int(sys.argv[1])
        inputFiles = sys.argv[2]
        outputPath = sys.argv[3]

        main(inputFiles,outputPath,n)

    else:
        print "$ python ./ngramGenerator.py [n] [input-files-dir] [output-files-dir]"

