# -*- coding: utf-8 -*-
# 2014.03.13
# provide api that return the abstract type of a wordnet type.

f = open("./patty.pattern.types")
types = {}
for line in f:
    l = line.split()
    types[l[0]] = l[1][:-1]
f.close()

def getAbstractTypeByWordnetType(t):
    return types[t]

if __name__ == '__main__':
    print getAbstractTypeByWordnetType("wordnet_academician_109759069")
