# -*- coding: utf-8 -*-
# qcl
# Generate 1-gram (that is, word feq) from dir

threadLimit = 30

import nltk
import os
import sys
import time
import Queue
import threading
import simplejson as json

def oneGramByFile(inputFileName):
    print "File:%s" % (inputFileName)
    f = open(inputFileName,"r")
    words = {}
    for line in f:
        tokens = nltk.word_tokenize(line)
        for token in tokens:
            if not token in words:
                words[token] = 0
            words[token] += 1
    f.close()
    return words

def main(source,target):
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
                    #msg(filename)
                    files.task_done()
                except:
                    #msg("error! "+str(ident))
                    break

                # do something here
                gram = oneGramByFile(os.path.join(source,filename))
                tmp_g = open(os.path.join(target,filename),"w")

                json.dump(gram,tmp_g)
                
                tmp_g.close()
                # end of thread/run


    # starting threading
    
    for x in xrange(threadLimit):
        th = worker()
        th.start()
        #th = threading.Thread(target=thread,)
        #th.daemon = True
        #th.start()

    # reading list
    totalCount = 0
    for fj in os.listdir(source):
        if not ".txt" in fj:
            continue
        totalCount+=1
        files.put(fj)

    print "Number of files =",totalCount

    files.join()
  
    print totalCount

    pass


if __name__ == "__main__":
    # gen 1-gram from source/*.txt then save it to target dir
    if len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]
        if len(sys.argv) > 3:
            isStem = True

        main(source,target)

    else:
        print "$ python ./oneGramGeneratorPool.py [source dir] [target dir] (stemming)"
