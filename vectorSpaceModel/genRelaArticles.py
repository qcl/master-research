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
def mapper(jobid,filename,inputPath,inputPtnPath,model,table,confidence):

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

    linesByRelations = {}

    for ans in itr:
        count += 1

        key = "%s.txt" % (ans["revid"])
        relation = ans["observed"]

        ptnEx = contentPtnJson[key]
        article = projizz.articleSimpleSentenceFileter(contentJson[key])
       
        supportInstanceByFile[key] = {}
        linesByRela = {}

        for line in ptnEx:
            # line[0]: line number
            # line[1]: array of patterns
            lineText = article[line[0]]

            for ptn in line[1]:
                # ptn[0]: pattern ID
                # ptn[1]: start position in line
                # ptn[2]: end position in line
                ptnId = "%d" % (ptn[0])

                if not projizz.isPatternValidate(ptnId, table, confidence=confidence):
                    continue

                # give up degree > 5 's pattern
                if len(table[ptnId]["relations"]) > 5:
                    continue

                for rela in table[ptnId]["relations"]:
                    # it's a support instance
                    if rela in relation:
        
                        if not rela in linesByRela:
                            linesByRela[rela] = []
                        if not line[0] in linesByRela[rela]:
                            linesByRela[rela].append(line[0])

        for rela in linesByRela:
            if not rela in linesByRelations:
                linesByRelations[rela] = []
            for lineN in linesByRela[rela]:
                linesByRelations[rela].append(article[lineN])

        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return linesByRelations
#
#
#
def preprocess(inputPath,inputPtnPath,outputPath,confidence):

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
            result.append( pool.apply_async( mapper, (t,filename,inputPath,inputPtnPath, model, table, confidence))  )
            t += 1
    pool.close()
    pool.join()

    modelArticles = {}

    # Reducer
    for r in result:
        sibr = r.get()

        for rela in sibr:
            if not rela in modelArticles:
                modelArticles[rela] = []
            modelArticles[rela] += sibr[rela]

    #
    #   relation.json: [line, line, line, ....]
    #

    for rela in modelArticles:
        print rela
        projizz.jsonWrite(modelArticles[rela],os.path.join(outputPath,"%s.json" % (rela))) 

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

#
#
#
if __name__ == "__main__":
    if len(sys.argv) > 4:
        # args
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        confidence = float(sys.argv[4])
        preprocess(inputPath,inputPtnPath,outputPath,confidence)
    else:
        print "$ python ./genRelaArticles.py [input-train-article-dir] [input-train-ptn-dir] [output-article-dir] [confidence]"
