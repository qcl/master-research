# -*- coding: utf-8 -*-
# qcl
# Read the output ./ambiguity.degree.statistics.py generate

import sys
import projizz

def outputStatistics(jsonPath):

    # Read file in.
    properties = projizz.jsonRead(jsonPath)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonPath = sys.argv
        outputStatistics(jsonPath)
    else:
        print "$ python ./ambiguity.degree.output.py [jsonPath]"
