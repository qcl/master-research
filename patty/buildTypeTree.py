# qcl

from pymongo import Connection

def main(dbName,collectionName):
    
    # Connection
    con = Connection()
    db = con[dbName]
    patterns = db[collectionName]
    yago = db["yago.taxonomy"]

    def gotoP(t):
        result = yago.find({"type":t})
        if result.count() > 0:
            hasP = False
            for i in range(0,result.count()):
                r = result[i]["subClassOf"]
                print t,"->",r
                if r == "wordnet_person_100007846":
                    return True
                rb = gotoP(r)
                if rb:
                    return True
            return False
        else:
            return False

    # Get types
    domains = patterns.distinct("domain")
    ranges  = patterns.distinct("range")

    print "DomainNumber:",len(domains)
    print "Range Number:",len(ranges)

    types = []
    for domain in domains:
        if not domain in types:
            types.append(domain)

    for r in ranges:
        if not r in types:
            types.append(r)

    types.sort()

    f = open("patty.wiki.pattern.domain.range.types.txt","w")
    for t in types:
        isP = gotoP(t)
        print "type:",t,isP,"\n\n"
        if isP:
            f.write("1\t%s\n" % (t) )
        else:
            f.write("0\t%s\n" % (t) )
    f.close()
    
    print "write",len(types),""

if __name__ == "__main__":
    main("projizz","patty.wiki.pattern")
