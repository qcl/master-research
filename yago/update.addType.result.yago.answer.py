# -*- coding: utf-8 -*-
# qcl
# python ./putIntoMongoDB.py inputfile dbname collection

import sys
from pymongo import Connection

def main():

    count = 0

    taxonomy = {}
    
    # connect to database
    con = Connection()
    db = con["projizz"]

    simpleType = db["yago.taxonomy"]
    collectionType = db["yago.simple.types"]
    answerCollection = db["result.yago.answer"]

    def getTypes(ty):
        if ty in taxonomy:
            pass
            #print "hit",ty
        else:
            #print "query",ty
            it = simpleType.find({"type":ty})
            taxonomy[ty] = []
            for t in it:
                taxonomy[ty].append(t["subClassOf"])
        
        result = [ty]
        types = taxonomy[ty]
        for t in types:
            if not t in result:
                result.append(t)
            r = getTypes(t)
            for st in r:
                if not st in result:
                    result.append(st)

        return result

    # testing
    #print getTypes(u"wordnet_site_108651247")
    #print getTypes(u"yagoGeoEntity")

    #ita = answerCollection.find({"_id":"Aruba"})
    ita = answerCollection.find()

    for yagoAns in ita:
        count += 1
        name = yagoAns["_id"]
        it = collectionType.find({"subject":name})
        types = []
        for t in it:
            for st in getTypes(t["type"]):
                if not st in types:
                    types.append(st)

        yagoAns["type"] = types
        answerCollection.update({"_id":name},yagoAns,upsert=False)

        if count % 1000 == 0:
            print "update",count,"instances."


if __name__ == "__main__":
    main()
