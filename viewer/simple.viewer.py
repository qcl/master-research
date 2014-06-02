# -*- coding: utf-8 -*-
# qcl

import projizz
import pymongo
import os
import sys

def main(part,revid):

    # Paths (on NLG workstation)
    inputPath = "/tmp2/ccli/yago-part-%s/" % (part)
    inputPtnPath = "/tmp2/ccli/yago-ptn-part-%s/" % (part)
    spPath = "../yago/yagoPSv1/ps.%s.json" % (part)

    # connect to database
    connect = pymongo.Connection()
    db = connect.projizz
    collection = db.result.yago.answer
    itr = collection.find({"revid":revid})

    # find filename
    a = os.popen("grep -nr \"%s\" %s" % (revid,inputPath)).readline()
    targetFilename = a.split(":")[0].split("/")[-1]
    key = "%s.txt" % (revid)

    

    pattern = projizz.jsonRead(inputPtnPath+targetFilename)[key]
    article = projizz.articleSimpleSentenceFileter(projizz.jsonRead(inputPath+targetFilename)[key])
    st = projizz.getSortedPatternStatistic(projizz.jsonRead(spPath))
    domainRange = projizz.getYagoRelationDomainRange();
    model, table = projizz.readPrefixTreeModelWithTable("../yago/yagoPatternTree.model","../yago/yagoPatternTree.table")

    print "Part %s, RevID=%s, in %s" % (part,revid,targetFilename)

    for ans in itr:

        targetName = ans["_id"].replace("(","").replace(")","").split("_")  # get entity name's part
        types = ans["type"]
        answers = ans["properties"]

        print "Target=%s\nTarget token=%s" % (ans["_id"],targetName)
       
        for line in pattern:
            lineText = article[line[0]]
            named = False
            for namedToken in targetName:
                if namedToken in lineText:
                    named = True
                    break

            if not named:   # No target name in line text
                continue    # go to next line.

            for ptn in line[1]:
                ptnId = "%d" % (ptn[0])
                #rfp = table[ptnId]["relations"]
                if not ptnId in st:
                    continue

                for ps in st[ptnId]:
                    if float(ps[1]["support"])/float(ps[1]["total"]) > 0:
                        if domainRange[ps[0]]["domain"] in types:
                            print "#%d %s" % (line[0],lineText)
                            isIn = "(X)"
                            if ps[0] in answers:
                                isIn = "(O)"
                            print "%s %s/%s/{%d,%d}/ %s" % (isIn,ptnId,table[ptnId]["pattern"],ps[1]["support"],ps[1]["total"],ps[0])

                        pass

                    # select top 1
                    break


        # prevent second ans
        break

if __name__ == "__main__":
    if len(sys.argv) > 2:
        part = sys.argv[1]
        revid = sys.argv[2]
        main(part,revid)
    else:
        print "$ python simple.viewer.py [part#] [revid]"
