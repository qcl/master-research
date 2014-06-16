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

def filterFunction(jobid,filename,inputPtnPath,model,table,properties,confidence):
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    patterns = {}

    count = 0

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])

        # Now only consider properties, no references.
        relation = ans["observed"]
        
        ptnEx = contentPtnJson[key]

        uniPtnIds = []
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

                # Check the confidence value
                if table[ptnId]["confidence"] < confidence:
                    continue
                
                # here, is validated pattern.
                if not ptnId in uniPtnIds:
                    uniPtnIds.append(ptnId)

        for ptnId in uniPtnIds:
            
            ptnR = table[ptnId]["relations"]
                
            for rela in ptnR:

                if not ptnId in properties[rela]:
                    properties[rela][ptnId] = {"total":0,"support":0}

                properties[rela][ptnId]["total"] += 1
                
                if rela in relation:
                    properties[rela][ptnId]["support"] += 1

    return properties


#
#   Main Program
#
def main(inputPtnPath,outputPath,confidence):
    
    start_time = datetime.now()

    #model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    # using new table (2014.06.16)
    model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","../patty/yagoPatternTreeWithConfidence.table")

    properties = projizz.buildYagoProperties({})

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table,copy.deepcopy(properties),confidence )))
            t += 1
    pool.close()
    pool.join()

    for res in result:
        r = res.get()

        for rela in r:
            for ptnId in r[rela]:
                if not ptnId in properties[rela]:
                    properties[rela][ptnId] = {"total":0,"support":0}
                properties[rela][ptnId]["total"] += r[rela][ptnId]["total"]
                properties[rela][ptnId]["support"] += r[rela][ptnId]["support"]
   
    json.dump(properties,open(outputPath,"w"))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        inputPtnPath = sys.argv[1]
        outputPath = sys.argv[2]
        confidence = float(sys.argv[3])
        main(inputPtnPath,outputPath,confidence)
    else:
        print "$ python ./yago.pattern.statistics.py [input-ptn-dir] [output-filename.json] [confidence value]"

