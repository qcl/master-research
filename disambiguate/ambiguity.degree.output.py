# -*- coding: utf-8 -*-
# qcl
# Read the output ./ambiguity.degree.statistics.py generate

import sys
import projizz

def outputStatistics(jsonPath):

    # Read file in.
    properties = projizz.jsonRead(jsonPath)

    for degree in range(1,18):
        degree = "%d" % (degree)
        if not degree in properties:
            print "%s\t%d" % (degree,0)
        else:
            print "%s\t%d" % (degree,len(properties[degree]))
if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonPath = sys.argv[1]
        outputStatistics(jsonPath)
    else:
        print "$ python ./ambiguity.degree.output.py [jsonPath]"
