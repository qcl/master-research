# -*- coding:utf-8 -*-
# qcl

import projizz

dr = projizz.getYagoRelationDomainRange();

result = {}

for r in dr:
    if r == "produced":
        continue
    l = 0
    f = open("../patty/yagoSortedRela/%s.txt" % (r), "r")
    for line in f:
        l += 1
    f.close()
    domain = dr[r]["domain"]
    rang   = dr[r]["range"]
    
    if "wl:" in rang:
        rang = "Thing"

    if "wordnet_" in domain:
        domain = domain.split("_")
        domain = "%s\_%s" % (domain[0],domain[1])
    if "wordnet_" in rang:
        rang = rang.split("_")
        rang = "%s\_%s" % (rang[0],rang[1])
    
    result[r] = (domain,rang,l)

nr = sorted(result.items())

for r in nr:
    rela = r[0]
    d  = r[1][0]
    ra = r[1][1]
    co = r[1][2]
    print "%s & %s & %s & %d \\\\" % (rela,d,ra,co)
