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

def buildProperties(path):
    properties = {}
    for filename in os.listdir(path):
        if ".txt" in filename:
            properties[filename[:-4]] = {
                "tp":[], # true - postive            Real Ans: True    False
                "tn":[], # true - negative    Model told:
                "fp":[], # false - postive                 Yes  tp      fp     
                "fn":[]  # false - negative                 No  fn      tn
                }
    return properties

def filterFunction(jobid,filename,inputPtnPath,model,table,partAns):
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    print "Worker %d : Read %s into filter" % (jobid,filename)

    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    count = 0

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])

        # Now only consider properties, no references.
        relation = ans["properties"]
        ptnEx = contentPtnJson[key]
        relaEx = []
        for line in ptnEx:
            for ptn in line[1]:
                ptnId = "%d" % (ptn[0])
                if not ptnId in ptns:
                    ptns.append(ptnId)
                rfp = table[ptnId]["relations"]
                if len(rfp) < 2:
                    if not rfp[0] in relaEx:
                        relaEx.append(rfp[0])

        for attribute in partAns:
            postive = False
            true = False

            if attribute in relaEx:
                postive = True
            if attribute in relation:
                true = True

            if true:
                if postive:
                    partAns[attribute]["tp"].append(ans["revid"])
                else:
                    partAns[attribute]["fn"].append(ans["revid"])
            else:
                if postive:
                    partAns[attribute]["fp"].append(ans["revid"])
                else:
                    partAns[attribute]["tn"].append(ans["revid"])
        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)
    return partAns
            
def main(inputPtnPath,outputPath):
    
    model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    properties = buildProperties("./yagoRelation/")

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table,partAns )))
            t += 1
    pool.close()
    pool.join()

    for res in result:
        r = res.get()
        for m in r:
            properties[m]["tp"] += r[m]["tp"]
            properties[m]["tn"] += r[m]["tn"]
            properties[m]["fp"] += r[m]["fp"]
            properties[m]["fn"] += r[m]["fn"]

    print "start write out to %s" % (outputPath)
    json.dump(properties,open(outputPath,"w"))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        inputPtnPath = sys.argv[1]
        outputPath = sys.argv[2]
        main(inputPtnPath,outputPath)
    else:
        print "$ python ./yago.pattern.statistics.py [input-ptn-dir] [output-filename.out]"

