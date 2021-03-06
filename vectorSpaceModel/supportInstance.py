# -*- coding: utf-8 -*-
# qcl
# Proprecess for building VSM models to decide relation, at the same time, calculate the pattern's precision =p

import os
import sys
import copy
import projizz
import pymongo
import multiprocessing
from datetime import datetime

#
#
#
def mapper(jobid,filename,inputPath,inputPtnPath,model,table):

    # Read article
    contentJson = projizz.jsonRead( os.path.join(inputPath,filename) )
    # Read ptn
    contentPtnJson = projizz.jsonRead( os.path.join(inputPtnPath,filename) )

    print "Worker %d : Read %s into filter" % (jobid,filename)
    
    ### Connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    count = 0

    supportInstanceByFile = {}

    for ans in itr:
        count += 1

        key = "%s.txt" % (ans["revid"])
        relation = ans["observed"]

        ptnEx = contentPtnJson[key]
        article = projizz.articleSimpleSentenceFileter(contentJson[key])
       
        supportInstanceByFile[key] = {}

        for line in ptnEx:
            # line[0]: line number
            # line[1]: array of patterns
            lineText = article[line[0]]

            for ptn in line[1]:
                # ptn[0]: pattern ID
                # ptn[1]: start position in line
                # ptn[2]: end position in line
                ptnId = "%d" % (ptn[0])

                if not projizz.isPatternValidate(ptnId, table):
                    continue

                for rela in table[ptnId]["relations"]:
                    # it's a support instance
                    if rela in relation:
                        
                        if not ptnId in supportInstanceByFile[key]:
                            supportInstanceByFile[key][ptnId] = {}
                        if not rela in supportInstanceByFile[key][ptnId]:
                            supportInstanceByFile[key][ptnId][rela] = []

                        if not line[0] in supportInstanceByFile[key][ptnId][rela]:
                            supportInstanceByFile[key][ptnId][rela].append(line[0])

        for ptnId in supportInstanceByFile[key]:
            for rela in supportInstanceByFile[key][ptnId]:
                lines = supportInstanceByFile[key][ptnId][rela]
                supportInstanceByFile[key][ptnId][rela] = []
                for lineN in lines:
                    supportInstanceByFile[key][ptnId][rela].append(article[lineN])

        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return supportInstanceByFile
#
#
#
def preprocess(inputPath,inputPtnPath,outputPath):

    # Checking output path
    projizz.checkPath(outputPath)

    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model", "../patty/yagoPatternTreeWithConfidence.table")

    start_time = datetime.now()

    # Processes pool
    proceessorNumber = multiprocessing.cpu_count()
    if proceessorNumber > 20:
        proceessorNumber = 20
    pool = multiprocessing.Pool(processes=proceessorNumber)
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            result.append( pool.apply_async( mapper, (t,filename,inputPath,inputPtnPath, model, table))  )
            t += 1
    pool.close()
    pool.join()

    patternInstances = {}

    # Reducer
    for r in result:
        sibf = r.get()
        for key in sibf:
            for ptnId in sibf[key]:
                if not ptnId in patternInstances:
                    patternInstances[ptnId] = {}
                for rela in sibf[key][ptnId]:
                    for inst in sibf[key][ptnId][rela]:
                        if not rela in patternInstances[ptnId]:
                            patternInstances[ptnId][rela] = {}
                        if not key in patternInstances[ptnId][rela]:
                            patternInstances[ptnId][rela][key] = []
                        patternInstances[ptnId][rela][key].append(inst)

    
    # Write to files
    # NOTE
    # Output Format:
    # ptnId.json (json)
    # rela: keys
    #   key: line text
    for ptnId in patternInstances:
        projizz.jsonWrite(patternInstances[ptnId],os.path.join(outputPath,"%s.json" % (ptnId))) 

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 3:
        # args
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        preprocess(inputPath,inputPtnPath,outputPath)
    else:
        print "$ python ./supportInstance.py [all-input-train-article-dir] [all-input-train-ptn-dir] [output-instance-dir]"
