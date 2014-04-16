# -*- coding: utf-8 -*-
# qcl
# Build naive model, only tf, no idf =w=, and pattern has no weight
import operator

f = open("./patternsByRelations.log","r")
for line in f:
    pattern = line.split("\t")[0]
    g = open("./PbR/%s.txt" % (pattern),"r")

    print pattern

    words = {}
    count = 0
    for l in g:
        ws = l.split()
        for word in ws:
            if len(word) > 2 and word[0:2] == "[[":
                continue

            if word[-1] == ";":
                word = word[:-1]

            if not word in words:
                words[word] = 0

            words[word] += 1
            count+=1

    for word in words:
        words[word] /= float(count)
   
    h = open("./naiveModel/%s.json" % (pattern),"w")
    sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1))
    sorted_words.reverse()

    h.write("{\n")

    for w in sorted_words:
        h.write("\"%s\":\"%s\"\n" % (w[0],str(w[1])))

    h.write("}")
    h.close()
    

    g.close()
f.close()

