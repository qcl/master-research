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

def mapper(jobid, filename, inputPath, inputPtnPath, table, st, partAns, domainRange, confidence, nbcPath):

    # read articles and patterns
    contentJson = projizz.jsonRead(os.path.join(inputPath,filename))
    contentPtnJson = projizz.jsonRead(os.path.join(inputPtnPath,filename))

    classifiers = projizz.getNBClassifiers(nbcPath)
    print "Worker %d : Read %s" % (jobid,filename)

    # connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    queries = map(lambda x: x[:-4], contentPtnJson)
    itr = collection.find({"revid":{"$in":queries}})
    print "worker %d query=%d, result=%d" % (jobid,len(queries),itr.count())

    count = 0
    expResult = partAns
    relaEx = []
    
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

            lineText = article[line[0]]
            if lineText[0] == "^":  # It's a wikipeida reference comments, ignore it!
                continue

            for ptn in line[1]:
                # ptn[0]: pattern ID
                # ptn[1]: start position in line
                # ptn[2]: end position in line

                ptnId = "%d" % (ptn[0])

                ptntks = table[ptnId]["pattern"]

                if not projizz.isPatternValidate(ptnId, table, confidence=confidence, st=st):
                    continue
        
                rfp = table[ptnId]["relations"]

                # check degree
                if len(rfp) > 5:
                    continue

                # if no support, ignore this pattern
                if st[ptnId][0][1]["support"] <= 0:
                    continue

                for ptnst in st[ptnId]:
                    # ptnst[0] = relation
                    # ptnst[1] = {"support":,"total": }
                    if domainRange[ptnst[0]] not in types:
                        continue

                    if classifiers[ptnst[0]] == None:
                        continue

                    if classifiers[ptnst[0]].classify(lineText) == "pos":
                        if not ptnst[0] in relaEx:
                            relaEx.append(ptnst[0])


        #### Evaluation
        for attribute in expResult:

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
                    expResult[attribute]["tp"].append(ans["revid"])
                else:
                    expResult[attribute]["fn"].append(ans["revid"])
            else:
                if postive:
                    expResult[attribute]["fp"].append(ans["revid"])
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
def main(inputPath, inputPtnPath, nbcPath, confidence, psfile, outputPath, outputFilename): 
    
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model","../patty/yagoPatternTreeWithConfidence.table")
    properties = projizz.buildYagoProperties({"tp":[],"fp":[],"fn":[]})
    domainRange = projizz.getYagoRelationDomainRange()
    st = projizz.getSortedPatternStatistic( projizz.jsonRead(psfile) )

    projizz.checkPath(outputPath)

    start_time = datetime.now()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()) 
    t = 0
    result = []
    for filename in os.listdir(inputPtnPath):
        if ".json" in filename:
            partAns = copy.deepcopy(properties)
            result.append(pool.apply_async(mapper, ( t, filename, inputPath, inputPtnPath, table, st, partAns, domainRange, confidence, nbcPath  )))
            #result.append( mapper( t, filename, inputPath, inputPtnPath, table, partAns, domainRange, confidence, vsmData  ))
            t += 1
    pool.close()
    pool.join()

    expResult = copy.deepcopy(properties)
    for res in result:
        r = res.get()
        for m in r:
            if m == "produced":
                continue
            expResult[m]["tp"] += r[m]["tp"]
            expResult[m]["fp"] += r[m]["fp"]
            expResult[m]["fn"] += r[m]["fn"]

    projizz.jsonWrite(expResult,os.path.join(outputPath,outputFilename))
    print "start write out to %s" % (os.path.join(outputPath,outputFilename))

    diff = datetime.now() - start_time
    print "Spend %d.%d seconds" % (diff.seconds, diff.microseconds)

if __name__ == "__main__":
    if len(sys.argv) > 7:
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]

        nbcPath = sys.argv[3]
        confidence = float(sys.argv[4])
        psfile = sys.argv[5]

        outputPath = sys.argv[6]
        outputFilename = sys.argv[7]

        main(inputPath, inputPtnPath, nbcPath, confidence, psfile, outputPath, outputFilename)
    else:
        print "$ python ./eval.py [input-dir] [input-ptn-dir] [nbc-dir] [confidence] [psfile] [output-dir] [output-filename.out]"

