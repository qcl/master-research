# -*- coding: utf-8 -*-
# qcl
# Using thread pool, to run naive model.
#
# Naive Model ( 1-gram )
# * Histogram
#   * L1 dist
#   * L2 dist
# * Bag of words
#   * (偽) VSM
#   * match words

threadLimit = 30

import os
import sys
import time
import Queue
import threading
import simplejson as json

msgQ = Queue.Queue(0)

def msg(message):
    msgQ.put(message)

# read .json model
def readModels(models):
    model = {}
    for m in os.listdir(models):
        if not ".json" in m:
            continue
        print "Reading model %s from %s" % (m[:-5],m)
        f = open(os.path.join(models,m),"r")
        model[m[:-5]] = json.load(f)
        f.close()
    return model

def main(models,curpus,result):
    model = readModels(models)
    files = Queue.Queue(0)

    

    # define each thread
    class worker(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.daemon = True
        def run(self):
            ident = threading.currentThread().ident
            #msg("Start! "+str(ident))
            while True:
                #if files.empty():
                #    #msg("empty! "+str(ident))
                #     break
                try:
                    filename = files.get()
                    msg(filename)
                    files.task_done()
                except:
                    #msg("error! "+str(ident))
                    break

                # do something here

                #msg(filename)
            #msg("End! "+str(ident))

    # starting threading
    
    cond = threading.Condition()
    for x in xrange(threadLimit):
        th = worker()
        th.start()
        #th = threading.Thread(target=thread,)
        #th.daemon = True
        #th.start()

    # reading list
    totalCount = 0
    for fj in os.listdir(curpus):
        if not ".json" in fj:
            continue
        totalCount+=1
        files.put(fj)

    print "Number of files =",totalCount

   

    #while threading.activeCount() > 1:
    #    if not msgQ.empty():
    #        ms = msgQ.get()
    #        print ms,files.qsize(),msgQ.qsize(),threading.activeCount()
    #    else:
    #        pass 

    files.join()
  
    print totalCount, msgQ.qsize()

    pass

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        models = sys.argv[1]
        corpus = sys.argv[2]
        result = sys.argv[3]

        main(models,corpus,result)

    else:
        print "$ python ./naiveModelRunPool.py [models-dir] [corpus-dir] [result-dir]"

