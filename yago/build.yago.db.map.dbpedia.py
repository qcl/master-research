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

        prefix = "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"

        g = rdflib.Graph()
        r = g.parse(data=prefix+line,format="n3")
        for instance in r:
            j += 1

            yagoInstance    = "%s" % (instance[0][42:])
            dbpediaInstance = "%s" % (instance[2])

            inst = {"yago":yagoInstance,"dbpedia":dbpediaInstance}
            c.append(inst)
            
            if j%1000 == 0:
                collection.insert(c)
                print "[INFO] insert",j,"instances."
                c = []
        
        #if j > 3:
        #    break

    if len(c) > 0:
        print "[INFO] insert the least",len(c),"instances."
        collection.insert(c)
    print "Read",j,"lines. Finished."

if __name__ == '__main__':
    main("../../../YAGO/yagoDBpediaInstances.ttl","projizz","yago.map.dbpedia")
