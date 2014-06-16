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



    for ans in itr:
        count += 1
        key = "%s.txt" % (ans["revid"])     # get revid
        #targetName = ans["_id"].replace("(","").replace(")","").split("_")  # get entity name's part
        types = ans["type"]

        # Now only consider properties, no references.
        relation = ans["observed"]
        ptnEx = contentPtnJson[key]
        #article = projizz.articleSimpleSentenceFileter(contentJson[key])

        for keyname in expResult:

            args = keyname.split("-")
            degree = int(args[0])
            ambig  = args[1]
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
                    
                    # not in table
                    if not ptnId in table:
                        continue
                    
                    # not in `training set'
                    if not ptnId in st:
                        continue

                    # if it's non-used pattern, ignore it.
                    if not table[ptnId]["used"]:
                        continue
                    if "eval" in table[ptnId] and not table[ptnId]["eval"]:
                        continue

                    # check confidence
                    if table[ptnId]["confidence"] < confidence:
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
                                # TODO
                        else:
                            # TODO
                            th = 0.75
                            if ambigu == "50":
                                th = 0.5
                            pass
            
            # Evaluation
            # TODO

        # XXX
                # if only one relation
                if len(rfp) < 2:

                    if st[ptnId][0][1]["support"] > 0 and not rfp[0] in relaEx:
                        relaEx.append(rfp[0])

                # more than one relation
                else:
                    # using the first as the answer
                    if st[ptnId][0][1]["support"] > 0 and not rfp[0] in relaEx:
                        relaEx.append(rfp[0])

        # Remove impossible relations
        toBeRemove = []
        for attribute in relaEx:
            # speical case, produced
            if domainRange[attribute] == "":
                continue

            if not domainRange[attribute]["domain"] in types:
                if not attribute in toBeRemove:
                    toBeRemove.append(attribute)

        for attribute in toBeRemove:
            relaEx.remove(attribute)

        # Evaluation
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
    return partAns
        
        # XXX
    
        if count % 100 == 0:
            print "worker #%d done %d." % (jobid,count)

    return expResult

#
#   Main Program
#
#
def main(inputPtnPath,outputPath,pspath,inputPath,confidence):
    
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

    # XXX
    # FIXME
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
    if len(sys.argv) > 5:
        inputPtnPath = sys.argv[1]
        inputPath = sys.argv[2]
        pspath = sys.argv[3]
        outputPath = sys.argv[4]
        confidence = float(sys.argv[5])
        main(inputPtnPath,outputPath,pspath,inputPath,confidence)
    else:
        print "$ python ./eval.py [input-ptn-dir] [input-article-dir] [pattern statistic json path] [output-filename.out] [confidence]"

