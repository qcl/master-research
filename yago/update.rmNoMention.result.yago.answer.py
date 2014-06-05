# -*- coding: utf-8 -*-
# qcl
# 2014.06.05
# Remove non mentioned properties form answer set.

import os
import sys
import projizz
import multiprocessing
import simplejson as json
from datetime import datetime
from pymongo import Connection
from splitInto5part import splitTo5part

def updateAnswer(jobid,inputPath,filename):
    contenJson = projizz.jsonRead(os.path.join(inputPath,filename))
    print "#%d - %s" % (jobid,filename)
    connect = Connection()
    answerCollection = connect.projizz.result.yago.answer
    factCollection = connect.projizz.yago.facts

    queries = map(lambda x: x[:-4], contenJson)

    itr = answerCollection.find({"revid":{"$in":queries}})
    print "#%d - query=%d,result=%d" % (jobid,len(queries),itr.count())
    
    count = 0
    ty1g = 0
    ty2g = 0
    updateC = 0
    articles = []
    for ans in itr:
        count += 1
        articleID = "%s.txt" % (ans["revid"])
        articleName = ans["_id"]
        properties = ans["properties"]
        #not consider references.
        #references = ans["references"]

        if len(properties) == 0:
            # give up those no properties' article
            # print "#%d - give up %s (1)" % (jobid,articleID)
            ty1g += 1
            continue
        
        needUpdate = len(properties)

        lines = projizz.articleSimpleSentenceFileter(contenJson[articleID])
        text = ""
        for line in lines:
            text += (line + " ")

        observed = []
        for pro in properties:
            
            pitr = factCollection.find({"property":pro,"subject":articleName})
            if pitr.count() < 1:
                notNeed.append(pro)
                continue

            found = False
            for fact in pitr:
                tokens = projizz.getNamedEntityTokens(fact["object"])
                for token in tokens:
                    if token in text:
                        found = True
                        break
                if found:
                    break
            if found:
                observed.append(pro)
            
        if len(observed) > 0:
            articles.append(articleID)
            ans["observed"] = observed
            answerCollection.update({"revid":ans["revid"]},ans,upsert=False)
        else:
            ty2g += 1
            #print "#%d - give up %s (2)" % (jobid,articleID)

    print "#%d -> update %d (give up %d + %d)" % (jobid,len(articles),ty1g,ty2g)

    return (filename,articles)

def main(inputPath,inputPtnPath,outputPath,outputPtnPath):

    debug = True

    if not os.path.isdir(outputPath):
        os.mkdir(outputPath)
    if not os.path.isdir(outputPtnPath):
        os.mkdir(outputPtnPath)

    result = []
    count = 0

    # Update answer
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    t = 0
    for filename in os.listdir(inputPath):
        if ".json" in filename:
            t += 1
            if debug:
                result.append(updateAnswer(t,inputPath,filename))
            else:
                result.append(pool.apply_async(updateAnswer, (t,inputPath,filename)))
    
    if not debug:
        pool.close()
        pool.join()

    # Rebuild articles and patterns

    tmpArticle = {}
    tmpPtn = {}

    dataSize = 0
    for res in result:
        if debug:
            filename,articles = res
        else:
            filename,articles = res.get()

        print filename,len(articles)
        a = projizz.jsonRead(os.path.join(inputPath,filename))
        p = projizz.jsonRead(os.path.join(inputPtnPath,filename))

        for key in articles:
            dataSize += 1
            tmpArticle[key] = a[key]
            tmpPtn[key] = p[key]

            if len(tmpPtn) == 1000:
                print "write to %05d.json" % (count)
                projizz.jsonWrite(tmpArticle,os.path.join(outputPath,"%05d.json" % (count)))
                projizz.jsonWrite(tmpPtn,os.path.join(outputPtnPath,"%05d.json" % (count)))
                tmpArticle = {}
                tmpPtn = {}
                count += 1

    if len(tmpPtn) > 0:
        print "write to %05d.json" % (count)
        projizz.jsonWrite(tmpArticle,os.path.join(outputPath,"%05d.json" % (count)))
        projizz.jsonWrite(tmpPtn,os.path.join(outputPtnPath,"%05d.json" % (count)))
        tmpArticle = {}
        tmpPtn = {}
        count += 1

    print "write %d files. (%d)" % (count,dataSize)

    # Split to 5 
    splitTo5part("/tmp2/r01922024","y-all","/tmp2/r01922024","y")
    splitTo5part("/tmp2/r01922024","y-ptn-all","/tmp2/r01922024","y-ptn")


if __name__ == "__main__":
    if len(sys.argv) > 4:
        inputPath = sys.argv[1]
        inputPtnPath = sys.argv[2]
        outputPath = sys.argv[3]
        outputPtnPath = sys.argv[4]
        main(inputPath,inputPtnPath,outputPath,outputPtnPath)
    else:
        print "$ python ./update.rmNoMention.result.yago.answer.py inputPath inputPtnPath outputPath outputPtnPath"
