# -*- coding: utf-8 -*-
# qcl
# prefix tree model naive runner.
# create: 2014.04.28
# modify: 2014.04.29

import os
import re
import gc
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


def filterFiles(jobid,filename,dataInputPath,resultOutPath,treeModel,debug):

    # get the pos tag name
    def getPosTagName(pos):
        tagName = "_na_"
        if pos[-2:] == "DT":    # [[det]]
            tagName = "[[det]]"
        elif pos[:2] == "JJ":   # [[adj]]
            tagName = "[[adj]]"
        elif pos[:3] == "PRP":  # [[pro]]
            tagName = "[[pro]]"
        elif pos == "CD":       # [[num]]
            tagName = "[[num]]"
        elif pos == "CC":       # [[con]]
            tagName = "[[pos]]"
        elif pos == "MD":       # [[mod]]
            tagName = "[[mod]]"
        elif pos == "IN":       # [[prp]]
            tagName = "[[prp]]"
        return tagName

    content = json.load(open(os.path.join(dataInputPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)
    postagger = PerceptronTagger()
    tokenizer = SelfDoingTokenizer()
    removeRefwords = re.compile(r"\[\d+\]")
    count = 0
    dealL = 0
    exception = False
    results = {}
    for subFilename in content:

        result = {}

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
            travarsingTrees = {}

            treeCount = 0
            for word,pos in posSet:
                #print word,pos,"  ",
                
                tagName = getPosTagName(pos)
                
                treeByWord = -1
                treeByPOS  = -1

                # If this node is a root 
                if word in treeModel:
                    treeByWord = treeCount
                    travarsingTrees[treeCount] = treeModel
                    treeCount+=1
                    
                if tagName in treeModel:
                    treeByPOS = treeCount
                    travarsingTrees[treeCount] = treeModel
                    treeCount+=1

                needRemove = []
                needAppend = []
                for treeId in travarsingTrees:
                    tree = travarsingTrees[treeId] 
               
                    # 先收割
                    if "_rls_" in tree:
                        for relation in tree["_rls_"]:
                            if not relation in result:
                                result[relation] = 0
                            result[relation] += 1

                    if treeId == treeByWord:
                        travarsingTrees[treeId] = tree[word]
                    elif treeId == treeByPOS:
                        travarsingTrees[treeId] = tree[tagName]
                    else:
                        inWord = False
                        inTag  = False
                        if word in tree:
                            inWord = True
                            travarsingTrees[treeId] = tree[word]

                        if tagName in tree:
                            inTag = True
                            if inWord:
                                needAppend.append((treeCount,tree[tagName]))
                                treeCount += 1
                            else:
                                travarsingTrees[treeId] = tree[tagName]
                        
                        if not inWord and not inTag:
                            needRemove.append(treeId)
   
                #print len(travarsingTrees),len(needRemove),len(needAppend)

                for treeId in needRemove:
                    travarsingTrees.pop(treeId)
                for treeId,tree in needAppend:
                    travarsingTrees[treeId] = tree

            # end of core algorithm

            dealL += 1
            #print line
            
            if dealL % 10000 == 0:
                print "Worker %d deal with %d lines." % (jobid,dealL)
        
        # end of article
        results[subFilename] = result
        # print subFilename,result

        count += 1
        if count % 100 == 0:
            print "Worker %d deal with %d files" % (jobid,count)
            gc.collect()
            if debug:
                break

        if exception:
            print "Worker %d exception @ %d / %d " % (jobid,dealL,count)
            break

    # write the result out.
    json.dump(results,open(os.path.join(resultOutPath,filename),"w"))
    print "Worker %d : Write results out to %s." % (jobid,filename)


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
            if debug:
                # debug model just test 1 file in 1 process
                # filterFiles(jobN,filename,treeModel,debug)
                pool.apply_async(filterFiles, (jobN,filename,dataInputPath,resultOutPath,treeModel,debug))
                break
            else:
                pool.apply_async(filterFiles, (jobN,filename,dataInputPath,resultOutPath,treeModel,debug))
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

