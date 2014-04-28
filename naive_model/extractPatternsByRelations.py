# -*- coding: utf-8 -*-
# qcl
# extract patterns by relationship then output to ./PbR

import sys
from pymongo import Connection

# build connection
con = Connection()
db = con.projizz
collection = db.patty.dbpedia.relation

dbpr = collection

# query relations
relations = dbpr.distinct("relation")

# for each relation, do...
for relation in  relations:
    f = open("./PbR/%s.txt" % (relation) , "w")

    patterns = dbpr.find({"relation":relation})

    for pattern in patterns:
        f.write("%s\n" % (pattern["pattern"]))

    print "%s\t%d" % (relation,patterns.count())

    f.close()
