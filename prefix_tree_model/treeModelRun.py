# -*- coding: utf-8 -*-
# qcl
# prefix tree model naive runner.
# create: 2014.04.28
# modify: 2014.04.29

import os
import re
import sys
import nltk
import time
import Queue
import multiprocessing
import simplejson as json
from datetime import datetime
from projizzTreeModel import readModel 
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

def selfDoingTokenize(line):
    # remove []!?,()"'
    return line.lower().replace("["," ").replace("]"," ").replace("!"," ").replace("?"," ").replace(","," ").replace(")"," ").replace("("," ").replace("\""," ").replace("'"," ").split()

class SelfDoingTokenizer(nltk.tokenize.api.TokenizerI):
    """
    Self-doing tokenizer by Qing-Cheng Li for his master degree.
    Just hope to speed up, go! go! go!
    """
    def tokenize(self,s):
        """
        Just return the splited string.
        Consider that [\d+] removed by sent into this function
        """
        return s.split()
    
    def span_tokenize(self,s):
        for span in s.split():
            yield span


def filterFiles(jobid,filename,treeModel,debug):
    content = json.load(open(os.path.join(dataInputPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)
    postagger = PerceptronTagger()
    tokenizer = SelfDoingTokenizer()
    removeRefwords = re.compile(r"\[\d+\]")
    count = 0
    dealL = 0
    exception = False
    for subFilename in content:

        # start to read a article.
        pt = treeModel

        for line in content[subFilename]:
            lineObj = TextBlob(removeRefwords.sub("",line),pos_tagger=postagger,tokenizer=tokenizer)
            
            # give up too short string
            if len(lineObj.tokens) < 5:
                continue
            try:
                posSet = lineObj.tags
            except:
                exception = True
                break
    
            # Here start the core algorithm

            inPattern = False

            for word,pos in posSet:
                print word,pos,"  ",
                
                inTree = False
                tagName = ""
                # test word
                if word in pt:
                    inTree = True
                # test pos
                else:
                    if pos[-2:] == "DT":
                        # [[det]]
                        tagName = "[[det]]"
                    elif pos[:2] == "JJ":
                        # [[adj]]
                        tagName = "[[adj]]"
                    elif pos[:3] == "PRP":
                        # [[pro]]
                        tagName = "[[pro]]"
                    elif pos == "CD":
                        # [[num]]
                        tagName = "[[num]]"
                    elif pos == "CC":
                        # [[con]]
                        tagName = "[[pos]]"
                    elif pos == "MD":
                        # [[mod]]
                        tagName = "[[mod]]"
                    elif pos == "IN":
                        # [[prp]]
                        tagName = "[[prp]]"
                    if len(tagName) > 0:
                        if tagName in pt:
                            inTree = True


                if inTree:
                    if inPattern:
                        pass
                    else:
                        pass
                else:
                    if inPattern:
                        pass
                    else:
                        pass
                    # not in target set.

            # end of core algorithm

            dealL += 1
            
            if dealL % 10000 == 0:
                print "Worker %d deal with %d lines." % (jobid,dealL)
        count += 1
        if count % 100 == 0:
            print "Worker %d deal with %d files" % (jobid,count)
            if debug:
                break

        if exception:
            print "Worker %d exception @ %d / %d " % (jobid,dealL,count)
            break


def main(treeModelPath,dataInputPath,resultOutPath,debug):

    # read model
    treeModel = readModel(treeModelPath)

    # create output dir
    if not os.path.isdir(resultOutPath):
        os.mkdir(resultOutPath)
    
    if debug:
        pool = multiprocessing.Pool(processes=1)
    else:
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    print "Number of core: %d" % (multiprocessing.cpu_count())

    start_time = datetime.now()

    jobN = 0 
    for filename in os.listdir(dataInputPath):
        if ".json" in filename:
            pool.apply_async(filterFiles, (jobN,filename, treeModel,debug))
            # debug model just test 1 file in 1 process
            if debug:
                break
            jobN+=1

    pool.close()
    pool.join()

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds,diff.microseconds)

if __name__ == "__main__":
    # args
    if len(sys.argv) > 3:
        treeModelPath = sys.argv[1]
        dataInputPath = sys.argv[2]
        resultOutPath = sys.argv[3]

        if len(sys.argv) > 4:
            debug = True
        else:
            debug = False

        main(treeModelPath,dataInputPath,resultOutPath,debug)

    else:
        print "$ python ./treeModelRun.py [treeModelPath] [dataInputPath] [resultOutPath] (debug)"

