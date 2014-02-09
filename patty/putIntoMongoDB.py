# qcl
# python ./putIntoMongoDB.py inputfile dbname collection
# inputfile format:
# line1: KeyName1 \t KeyName2 \t KeyName3 ...
# line2: Row1Value1 \t Row1Value2 \t Row1Value3 ...
# line3: Row2Value1 \t Row2Value2 \t Row2Value3 ...

import sys
from pymongo import Connection

def main(inputFile,dbName,collectionName):
    fp = open(inputFile,'r')

    line = fp.readline()[:-1]   # remove \n
    keys = line.split("\t")

    con = Connection()
    db = con[dbName]
    collection = db[collectionName]

    j = 0
    for line in fp:
        values = line[:-1].split("\t")
        j += 1
        if len(values) != len(keys):
            print "[ERROR] line",j,line
            continue

        instance = {}
        # FIXME
        for i in range(len(keys)):
            instance[keys[i]] = values[i]
        collection.insert(instance)

        if j%1000 == 0:
            print "[INFO] insert",j,"instances."

    print "Read",j,"lines. Finished."

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: python ./putIntoMongoDB.py [inputFile] [dbName] [collectionName]"
    else:
        print "Input file\t",sys.argv[1]
        print "DB name\t\t",sys.argv[2]
        print "Collection name\t",sys.argv[3]
        main(sys.argv[1],sys.argv[2],sys.argv[3])
