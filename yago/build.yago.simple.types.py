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

        prefix = "@prefix dbp: <http://dbpedia.org/ontology/> .\n@prefix owl: <http://www.w3.org/2002/07/owl#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."

        g = rdflib.Graph()
        r = g.parse(data=prefix+line,format="n3")
        for instance in r:
            j += 1

            yagoInstance    = "%s" % (instance[0][42:])
            yagoSimpleType  = "%s" % (instance[2][42:])

            inst = {"subject":yagoInstance,"type":yagoSimpleType}
            #print inst
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
    main("../../../YAGO/yagoSimpleTypes.ttl","projizz","yago.simple.types")
