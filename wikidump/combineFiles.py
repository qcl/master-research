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
        def __init__(self,threadID):
            threading.Thread.__init__(self)
            self.daemon = True
            self.tid = threadID
        def run(self):
            ident = threading.currentThread().ident
            print "worker#%02d start to work!" % (self.tid)
            while True:
                try:
                    fileCollection = files.get()
                    print "worker#%02d get file collection part %d" % (self.tid,fileCollection["part"])
                    files.task_done()
                except:
                    print "worker#%02d err!" % (self.tid)
                    break

                # do something here
                col = fileCollection["files"]
                ofn = os.path.join(outputPath,"%06d.json" % (fileCollection["part"]))
                f = {}
                for fn in col:
                    fc = []
                    fp = open(os.path.join(inputFiles,fn),"r")
                    for line in fp:
                        if len(line) > 0:
                            if line[-1] == "\n":
                                line = line[:-1]
                            if len(line) > 0:
                                fc.append(line)
                    fp.close()
                    f[fn] = fc
                fp = open(ofn,"w")
                json.dump(f,fp)
                fp.close()
                print "worker#%02d write to %s." % (self.tid,ofn)
                # end of thread/run
            print "worker#%02d end!" % (self.tid)



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
    
    print files.qsize()

    # starting threading
    for x in xrange(threadLimit):
        th = worker(x)
        th.start()


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

