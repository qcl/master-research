# -*- coding: utf-8 -*-
# qcl
# do some statistics on pattern and relation
# and check the error type

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

# error type
# (1)   
# (2)
# (3)

def filterFunction(jobid,filename,inputPtnPath,model,table,partAns,st,domainRange,inputPath,confidence):
    # read patterns in articles
    contentPtnJson = json.load(open(os.path.join(inputPtnPath,filename),"r"))
    
    print "Worker %d : Read %s into filter" % (jobid,filename)

    # connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    count = 0

    # prepare keys for multiple-exp
    # degree: 1 ~ 5
    # ambigu: select 1, select n (threshold:.5, .75), select all
    # type or not: no type info, type info
    
    expResult = {}

    for deg in range(1,6):
        for typ in ["n","t"]:
            if not deg == 1:
                for amb in ["one","50","75","all"]:
                    keyname = "%d-%s-%s" % (deg,amb,typ)
                    expResult[keyname] = copy.deepcopy(partAns)
            else:
                keyname = "%d-1-%s" % (deg,typ)
                expResult[keyname] = copy.deepcopy(partAns)
    
    print "worker %d build expResult" % (jobid)

    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])     # get revid
        #targetName = ans["_id"].replace("(","").replace(")","").split("_")  # get entity name's part
        types = ans["type"]

        # Now only consider properties, no references.
        relation = ans["observed"]

        # origin properties, 理論上應該會比 observed 還要多
        originRela = ans["properties"]
        
        ptnEx = contentPtnJson[key]
        #article = projizz.articleSimpleSentenceFileter(contentJson[key])

        for keyname in expResult:

            args = keyname.split("-")
            degree = int(args[0])
            ambigu = args[1]
            typ    = args[2]

            # Relation extraction
            relaEx = []
            for line in ptnEx:
                # line[0]: line number
                # line[1]: array of patterns

                for ptn in line[1]:
                    # ptn[0]: pattern ID
                    # ptn[1]: start position in line
                    # ptn[2]: end position in line

                    ptnId = "%d" % (ptn[0])

                    if not projizz.isPatternValidate(ptnId, table, confidence=confidence, st=st):
                        continue

                    rfp = table[ptnId]["relations"]

                    # check degree
                    if len(rfp) > degree:
                        continue

                    if len(rfp) == 1:   # or degree == 1
                        if st[ptnId][0][1]["support"] > 0 and not rfp[0] in relaEx:
                            if typ == "t":
                                if domainRange[rfp[0]]["domain"] in types:
                                    relaEx.append(rfp[0])
                            else:
                                relaEx.append(rfp[0])

                    else:
                        if ambigu == "one":
                            if typ == "t":
                                for ptnst in st[ptnId]:
                                    # ptnst[0] = relation
                                    # ptnst[1] = {"support": , "total": }
                                    if ptnst[1]["support"] > 0 and domainRange[ptnst[0]]["domain"] in types:
                                        if not ptnst[0] in relaEx:
                                            relaEx.append(ptnst[0])
                                            break

                            
                            else:
                                if st[ptnId][0][1]["support"] > 0 and not rfp[0] in relaEx:
                                    relaEx.append(rfp[0])
                                
                        elif ambigu == "all":
                            for ptnst in st[ptnId]:
                                if typ == "t":
                                    if domainRange[ptnst[0]]["domain"] in types:
                                        if not ptnst[0] in relaEx:
                                            relaEx.append(ptnst[0])
                                else:
                                    if not ptnst[0] in relaEx:
                                        relaEx.append(ptnst[0])
                        else:
                            th = 0.75
                            if ambigu == "50":
                                th = 0.5
                            
                            b = st[ptnId][0][1]["support"]
                            if b > 0:
                                for ptnst in st[ptnId]:
                                    if float(ptnst[1]["support"])/float(b) >= th:
                                        if typ == "t":
                                            if domainRange[ptnst[0]]["domain"] in types and not ptnst[0] in relaEx:
                                                relaEx.append(ptnst[0])
                                        else:
                                            if not ptnst[0] in relaEx:
                                                relaEx.append(ptnst[0])

            
            # Evaluation
            for attribute in expResult[keyname]:

                # special case, ignore.
                if attribute == "produced":
                    continue

                postive = False
                true = False

                if attribute in relaEx:
                    postive = True
                if attribute in relation:
                    true = True
            
                if true:
                    if postive:
                        expResult[keyname][attribute]["tp"].append(ans["revid"])
                    else:
                        expResult[keyname][attribute]["fn"].append(ans["revid"])
                else:
                    if postive:
                        expResult[keyname][attribute]["fp"].append(ans["revid"])
                    else:
                        # ignore true-negative
                        pass
    
        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return expResult

#
#   Main Program
#
#
def main(inputPtnPath,outputPath,pspath,inputPath,confidence,outputFilename):
    
    #model, table = projizz.readPrefixTreeModelWithTable("./yagoPatternTree.model","./yagoPatternTree.table")
    model, table = projizz.readPrefixTreeModelWithTable("../yago//yagoPatternTree.model","../patty/yagoPatternTreeWithConfidence.table")
    properties = projizz.buildYagoProperties({"tp":[],"fp":[],"fn":[]})
    st = projizz.getSortedPatternStatistic(projizz.jsonRead(pspath))
    domainRange = projizz.getYagoRelationDomainRange()

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(filterFunction, (t,filename,inputPtnPath,model,table,partAns,st,domainRange,inputPath,confidence )))
            t += 1
    pool.close()
    pool.join()

    expResult = {}
    for res in result:
        r = res.get()
        for keyname in r:

            if not keyname in expResult:
                expResult[keyname] = copy.deepcopy(properties)

            for m in r[keyname]:
                if m == "produced":
                    continue
                expResult[keyname][m]["tp"] += r[keyname][m]["tp"]
                expResult[keyname][m]["fp"] += r[keyname][m]["fp"]
                expResult[keyname][m]["fn"] += r[keyname][m]["fn"]


    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)

    for keyname in expResult:
        p = expResult[keyname]
        if not os.path.isdir(os.path.join(outputPath,keyname)):
            os.mkdir(os.path.join(outputPath,keyname))
        projizz.jsonWrite(p,os.path.join(outputPath,keyname,outputFilename))
        print "start write out to %s" % (os.path.join(outputPath,keyname))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 6:
        inputPtnPath = sys.argv[1]
        inputPath = sys.argv[2]
        pspath = sys.argv[3]
        outputPath = sys.argv[4]
        outputFilename = sys.argv[5]
        confidence = float(sys.argv[6])
        main(inputPtnPath,outputPath,pspath,inputPath,confidence,outputFilename)
    else:
        print "$ python ./eval.py [input-ptn-dir] [input-article-dir] [pattern statistic json path] [outpu-path] [output-filename.out] [confidence]"

