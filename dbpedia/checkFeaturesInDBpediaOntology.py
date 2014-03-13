# -*- coding: utf-8 -*-
# 2014.03.13
# 檢查是否PATTY的Features都在DBpedia的Ontology裡面

import simplejson as json

pattyFeaturesFile = open("./../patty/patty.dbpedia.Relations.json","r")
pattyFeatures = json.load(pattyFeaturesFile)
pattyFeaturesFile.close()

dbpediaOntologyFile = open("./dbpedia.ontology.txt")
for ontology in dbpediaOntologyFile:
    o = ontology.split("/")[-1][:-1]
    if o in pattyFeatures:
        pattyFeatures.remove(o)
        print o,len(pattyFeatures)

print pattyFeatures
        
