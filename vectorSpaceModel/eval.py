# -*- coding: utf-8 -*-
# qcl
# vector space eval

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

def mapper(jobid, filename, inputPath, inputPtnPath, table, partAns, domainRange, confidence):

    # read articles and patterns
    contentJson = projizz.jsonRead(os.path.join(inputPath,filename))
    contentPtnJson = projizz.jsonRead(os.path.join(inputPtnPath,filename))

    print "Worker %d : Read %s" % (jobid,filename)

    # connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    count = 0
    expResult = {}

    # threshold: 0.3 0.4 0.5 0.6 0.7 0.8

    for th in range(3,9):
        expResult[th] = copy.deepcopy(partAns)
    
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
        article = projizz.articleSimpleSentenceFileter(contentJson[key])

        # TODO

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
        
        for keyname in expResult:

            threshold = float(keyname)/10




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
def main(inputPath, inputPtnPath, vsmPath, confidence, outputPath, outputFilename): 
    
    model, table = projizz.readPrefixTreeModelWithTable("../yago//yagoPatternTree.model","../patty/yagoPatternTreeWithConfidence.table")
    properties = projizz.buildYagoProperties({"tp":[],"fp":[],"fn":[]})
    domainRange = projizz.getYagoRelationDomainRange()

    projizz.checkPath(outputPath)

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(mapper, ( t, filename, inputPath, inputPtnPath, table, partAns, domainRange, confidence  )))
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
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]

        vsmPath = sys.argv[3]
        confidence = float(sys.argv[4])

        outputPath = sys.argv[5]
        outputFilename = sys.argv[6]

        main(inputPath, inputPtnPath, vsmPath, confidence, outputPath, outputFilename)
    else:
        print "$ python ./eval.py [input-dir] [input-ptn-dir] [vsm-dir] [confidence] [output-dir] [output-filename.out]"

