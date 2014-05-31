# qcl

import sys
import rdflib
from pymongo import Connection

def main(inputFile,dbName,collectionName):
    fp = open(inputFile,'r')

    # connect to database
    con = Connection()
    db = con[dbName]
    collection = db[collectionName]

    c = []
    j = 0
    for line in fp:
        if line[0] == "#" or line[0] == "@" or line[0] == "\n":
            continue
        #if line[0:29] != "<http://dbpedia.org/resource/":
        #    continue

        g = rdflib.Graph()
        r = g.parse(data=line,format="n3")
        for instance in r:
            j += 1

            yagoSubject     = "%s" % (instance[0][42:])
            yagoProperty    = "%s" % (instance[1][42:])
            yagoObject      = "%s" % (instance[2][42:])

            inst = {"subject":yagoSubject,"property":yagoProperty,"object":yagoObject}
            c.append(inst)
            
            if j%1000 == 0:
                collection.insert(c)
                print "[INFO] insert",j,"instances."
                c = []
        
    if len(c) > 0:
        print "[INFO] insert the least",len(c),"instances."
        collection.insert(c)
    print "Read",j,"lines. Finished."

if __name__ == '__main__':
    main("../../../YAGO/yagoFacts.ttl","projizz","yago.facts")
