import rdflib

g = rdflib.Graph()
g.load("../../../dbpedia/dbpedia_3.9.owl")

for s,p,o in g:
    #print s,p,o
    print s

