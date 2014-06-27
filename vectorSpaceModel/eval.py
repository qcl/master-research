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

def mapper(jobid, filename, inputPath, inputPtnPath, table, partAns, domainRange, confidence, vsmData):

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
    relaEx = {}

    # threshold: 0.3 0.4 0.5 0.6 0.7 0.8

    for th in range(3,9):
        expResult[th] = copy.deepcopy(partAns)
        relaEx[th] = []
    
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

        # Relation extraction
        for line in ptnEx:
            # line[0]: line number
            # line[1]: array of patterns

            for ptn in line[1]:
                # ptn[0]: pattern ID
                # ptn[1]: start position in line
                # ptn[2]: end position in line

                ptnId = "%d" % (ptn[0])

                if not projizz.isPatternValidate(ptnId, table, confidence=confidence):
                    continue
        
                rfp = table[ptnId]["relations"]
                
                # TODO - Modlify string, remove pattern text in string?
                cosRlt = projizz.vsmSimilarity( article[line[0]], vsmData, rfp )

                # NOTE - if cosine value > threshold then there is a relation (?)
                for keyname in expResult:
                    threshold = float(keyname)/10.0

                    for pr in cosRlt:
                        # Check type
                        if domainRange[pr]["domain"] in types:
                            if cosRlt[pr] > threshold:
                                if pr not in relaEx[keyname]:
                                    relaEx[keyname].append(pr)

            #### Evaluation
            for attribute in expResult[keyname]:

                # special case, ignore.
                if attribute == "produced":
                    continue

                postive = False
                true = False

                if attribute in relaEx[keyname]:
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
    idf,docs,lens = projizz.getVSMmodels(vsmPath)
    vsmData = (idf, docs, lens)

    projizz.checkPath(outputPath)

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(mapper, ( t, filename, inputPath, inputPtnPath, table, partAns, domainRange, confidence, vsmData  )))
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


    for keyname in expResult:
        p = expResult[keyname]
        keydirName = "vsm-%2.0f-%d" % (confidence,keyname)
        projizz.checkPath( os.path.join(outputPath,keydirName))
        projizz.jsonWrite(p,os.path.join(outputPath,keydirName,outputFilename))
        print "start write out to %s" % (os.path.join(outputPath,keydirName))

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

