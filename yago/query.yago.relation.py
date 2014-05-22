# -*- coding: utf-8 -*-
# qcl
# python ./putIntoMongoDB.py inputfile dbname collection

import sys
from pymongo import Connection

def main():
    # connect to database
    con = Connection()
    db = con["projizz"]
    collection = db["patty.yago.relation"]

    a = collection.distinct("relation")

    for relation in a:
        f = open("./yagoRelation/%s.txt" % (relation), "w")
        print relation

        it = collection.find({"relation":relation})
        for i in it:
            f.write("%s\n" % (i["pattern"]))

        f.close()

if __name__ == "__main__":
    main()
