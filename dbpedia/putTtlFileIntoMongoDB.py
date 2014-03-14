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
        if line[0] == "#":
            continue

        g = rdflib.Graph()
        r = g.parse(data=line,format="n3")
        #print len(r)
        for instance in r:
            j += 1
            
            resourceName  = "%s" % (instance[0])
            propertyName  = "%s" % (instance[1])
            propertyValue = "%s" % (instance[2])

            inst = {"resource":resourceName,"property":propertyName,"value":propertyValue}
            c.append(inst)
            #if type(instance[0]) == type(instance[2]) and "ontology" in instance[1]:
            #    print "%s %s %s" % (instance[0],instance[1],instance[2])
            
            if j%1000 == 0:
                collection.insert(c)
                print "[INFO] insert",j,"instances."
                c = []

        
    if len(c) > 0:
        print "[INFO] insert the least",len(c),"instances."
        collection.insert(c)
    print "Read",j,"lines. Finished."

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: python ./putIntoMongoDB.py [inputFile] [dbName] [collectionName]"
    else:
        print "Input file\t",sys.argv[1]
        print "DB name\t\t",sys.argv[2]
        print "Collection name\t",sys.argv[3]
        main(sys.argv[1],sys.argv[2],sys.argv[3])
