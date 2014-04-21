# -*- coding: utf-8 -*-
# qcl
# Projizz I/O Worker Model

import gc
import time
import Queue
import threading

class Manager:
    def __init__(self,workerNumber=30):
        self.workerNumber = workerNumber

    def setJobQueue(self,queue):
        self.jobQueue = queue

    def setWorkerFunction(self,fnc):
        self.workerFnc = fnc
    
    def startWorking(self):

        theQueue = self.jobQueue
        theWorkingFunction = self.workerFnc

        class worker(threading.Thread):
            def __init__(self,tid):
                threading.Thread.__init__(self)
                self.daemon = True
                self.tid = tid
            def run(self):
                print "Worker #%02d start working!" % (self.tid)
                while True:
                    try:
                        jobObj = theQueue.get()
                        print "Worker #%02d get job" % (self.tid)
                    except:
                        break
                   
                    theWorkingFunction(jobObj,self.tid)
                    theQueue.task_done()
                    gc.collect()
                print "Worker #%02d done jobs" % (self.tid)

        totalJobNumber = theQueue.qsize()

        for i in xrange(self.workerNumber):
            th = worker(i)
            th.start()

        theQueue.join()
        print "Total job # %d" % (totalJobNumber)
        time.sleep(1)
        print "Done"


        

if __name__ == "__main__":
    print "Projizz Worker Model Demo"

    def test(jobObj,tid):
        print "%02d - %d" % (tid,jobObj)

    q = Queue.Queue(0)
    for i in xrange(1000000):
        q.put(i)

    m = Manager(50)
    m.setJobQueue(q)
    m.setWorkerFunction(test)
    m.startWorking()

