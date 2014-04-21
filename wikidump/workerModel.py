# -*- coding: utf-8 -*-
# qcl
# Read file in, and combine them, then output to a .json file.
#

threadLimit = 30

import os
import sys
import time
import Queue
import threading
import simplejson as json

def main(inputFiles,outputPath,combineN):
    rule = ".txt"
    files = Queue.Queue(0)

    # define each thread
    class worker(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
            self.tid = tid
        def run(self):
            ident = threading.currentThread().ident
            print "worker#%02d start working!" % (self.tid)
            while True:
                try:
                    fileCollection = files.get()
                    print "worker#%02d get data" % (self.tid)
                    
                except:
                    break

                # do something here
                # end of thread/run
                files.task_done()
            print "worker#%02d end." % (self.tid)


    # starting threading
    for x in xrange(threadLimit):
        th = worker(x)
        #th.start()

    # reading list
    totalCount = 0
    part = 0
    collection = []
    for fj in os.listdir(inputFiles):
        if not rule in fj:
            continue
        totalCount+=1
        
        collection.append(fj)

        if len(collection) == combineN:
            files.put({"files":collection,"part":part})
            part += 1
            collection = []
            print "#job:%d" % (part)

    if len(collection) > 0:
        files.put({"files":collection,"part":part})
        part += 1
        print "#job:%d" % (part)

    print "Number of files =",totalCount

    files.join()
  
    print totalCount
    time.sleep(1)
    print "Done"

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        inputFiles = sys.argv[1]
        outputPath = sys.argv[2]
        combineN = int(sys.argv[3])

        main(inputFiles,outputPath,combineN)

    else:
        print "$ python ./combineFiles.py [input-files-dir] [output-files-dir] [combineNumber]"

