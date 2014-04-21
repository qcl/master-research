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
        def run(self):
            ident = threading.currentThread().ident
            while True:
                try:
                    fileCollection = files.get()
                except:
                    break

                # do something here
                # end of thread/run
                files.task_done()


    # starting threading
    for x in xrange(threadLimit):
        th = worker()
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

    #files.join()
  
    print totalCount
    time.sleep(1)
    print "Done"

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        inputFiles = sys.argv[1]
        outputPath = sys.argv[2]

        main(inputFiles,outputPath)

    else:
        print "$ python ./ngramGenerator.py [input-files-dir] [output-files-dir]"

