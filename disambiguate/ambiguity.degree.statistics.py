# -*- coding: utf-8 -*-
# qcl
# do some statistics on pattern and relation

import os
import sys
import copy
import projizz
import multiprocessing
import simplejson as json
import pymongo
from datetime import datetime

def filterFunction(jobid,filename,inputPtnPath,model,table,properties):
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    patterns = {}

    statistics = {}

    count = 0

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])
        articleId = ans["revid"]
        # Now only consider properties, no references.
        relation = ans["observed"]
        
        ptnEx = contentPtnJson[key]

        uniPtnIds = {}
        for line in ptnEx:
            for ptn in line[1]: # line[0] is line number, line[1] is the content of line.
                ptnId = "%d" % (ptn[0]) # [patternId, start, to]

                # ptn id not in table, ignroe
                if not ptnId in table:
                    continue

                # for table using confidence
                if not table[ptnId]["used"]:    # ignore non-used pattern
                    continue
                if "eval" in table[ptnId] and not table[ptnId]["eval"]:
                    continue                    # ignore eval=false 's pattern

                # here, is validated pattern.
                if not ptnId in uniPtnIds:
                    uniPtnIds[ptnId] = 0
                uniPtnIds[ptnId] += 1           # count sentence level freq.


        degrees = []

        for ptnId in uniPtnIds:
            
            ptnR = table[ptnId]["relations"]    # the pattern may used in those relations
            degree = len(ptnR)                  # the degree of ambiguity

            # for articles statistics
            if not degree in degrees:
                degrees.append(degree)

            if not degree in properties:
                properties[degree] = {}

            if not ptnId in properties[degree]:
                properties[degree][ptnId] = {"occ":[],"sup":{}}

            if not articleId in properties[degree][ptnId]["occ"]:
                properties[degree][ptnId]["occ"].append(articleId)

            for rela in ptnR:
                if rela in relation:    # hit!
                    if not rela in properties[degree][ptnId]["sup"]:
                        properties[degree][ptnId]["sup"][rela] = []
                    if not articleId in properties[degree][ptnId]["sup"][rela]:
                        properties[degree][ptnId]["sup"][rela].append(articleId) 

        statistics[articleId] = degrees

        if count % 100 == 0:
            print "worker %d , deal with %d cases" % (jobid,count)
            
    return properties,statistics

def main(inputPtnPath,outputPath):
    
    start_time = datetime.now()

    #model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model","../patty/yagoPatternTreeWithConfidence.table")

    properties = projizz.buildYagoProperties({})

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table,copy.deepcopy(properties) )))
            t += 1
    pool.close()
    pool.join()

    statistics = {}

    for res in result:
        r,s = res.get()

        for degree in r:
            if not degree in properties:
                properties[degree] = {}

            for ptnId in r[degree]:
                if not ptnId in properties[degree]:
                    properties[degree][ptnId] = {"occ":[],"sup":{}}

                for occId in r[degree][ptnId]["occ"]:
                    if not occId in properties[degree][ptnId]["occ"]:
                        properties[degree][ptnId]["occ"].append(occId)

                for rela in r[degree][ptnId]["sup"]:
                    if not rela in properties[degree][ptnId]["sup"]:
                        properties[degree][ptnId]["sup"][rela] = []
                    for supId in r[degree][ptnId]["sup"][rela]:
                        if not supId in properties[degree][ptnId]["sup"][rela]:
                            properties[degree][ptnId]["sup"][rela].append(supId)

        for aid in s:
            statistics[aid] = s[aid]

    json.dump(properties,open(outputPath,"w"))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)
   
    # FIXME 儲存為JSON之後下面這段好像會跑非常非常久 

    ptnNum = 0
    occDocs = []
    for degree in range(1,18):
        if not degree in properties:
            print "%d\t%d\t%d\t%d" % (degree,0,0,0)
        else:
            occ = 0
            occs = 0
            for a in statistics:
                ds = statistics[a]
                if degree in ds:
                    occ += 1
                for i in ds:
                    if i <= degree:
                        occs += 1
                        break

            print "%d\t%d\t%d\t%d" % (degree,len(properties[degree]),occ,occs)

    # Calculate the number of articles which has no pattern.
    noPtnCount = 0
    for a in statistics:
        ds = statistics[a]
        if len(ds) == 0:
            noPtnCount += 1

    print noPtnCount,len(statistics)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPtnPath = sys.argv[1]
        outputPath = sys.argv[2]
        # TODO 需要注意路徑不存在的問題？
        main(inputPtnPath,outputPath)
    else:
        print "$ python ./ambiguity.degree.statistics.py [input-ptn-dir] [output-filename.json]"
