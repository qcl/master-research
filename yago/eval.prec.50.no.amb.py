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

# true - postive            Real Ans: True    False
# true - negative    Model told:
# false - postive                 Yes  tp      fp     
# false - negative                 No  fn      tn

def filterFunction(jobid,filename,inputPtnPath,model,table,partAns,validate):
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

                if not ptnId in validate:
                    continue

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
            
def main(inputPtnPath,outputPath,pspath):
    
    model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    properties = projizz.buildYagoProperties({"tp":[],"tn":[],"fp":[],"fn":[]})
    sp = projizz.getSortedStatistic(projizz.jsonRead(pspath))
    validate = []
   
    # Get Top P75 Relation
    for relation in sp:
        for ptnId,ptnS in sp[relation]:
            ptnData = table[ptnId]
            if float(ptnS["support"])/float(ptnS["total"]) >= 0.75:
                validate.append(ptnId)

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table,partAns,validate )))
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
    if len(sys.argv) > 3:
        inputPtnPath = sys.argv[1]
        pspath = sys.argv[2]
        outputPath = sys.argv[3]
        main(inputPtnPath,outputPath,pspath)
    else:
        print "$ python ./yago.pattern.statistics.py [input-ptn-dir] [pattern statistic json path] [output-filename.out]"

