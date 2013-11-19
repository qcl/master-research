# -*- coding: utf-8 -*-
# qcl
#
import sys
import os
import gc

def main(templateListFilename):

    # initialize template lists
    
    tempList = []

    f = open(templateListFilename,'r')
    for lines in f:
        tempList.append(lines.split(':')[1][:-1])
    sys.stderr.write("Read templates list.\n")
    f.close()

    c = 0
    fp = 0
    inPage = False
    found = False
    content = []
    for line in sys.stdin:
        if line[:-1] == '  <page>':
            inPage = True
            found = False
            content = []
            gc.collect()
        elif line[:-1] == '  </page>':
            inPage = False
            c = c + 1
            if found:
                print line[:-1]
                fp = fp + 1
            sys.stderr.write("read "+str(c)+" pages.\n")

        if inPage:
            if not found:
                content.append(line)
                
                if "{{" in line: 
                    for temp in tempList:
                        if temp in line:
                            found = True
                            for l in content:
                                print l[:-1]
            else:
                print line[:-1]
        
    sys.stderr.write("found "+str(fp)+" pages.\n")
    print '<!-- ',fp,'/',c,'-->'




if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'Usage: python templateUsedParser.py <templates list> < <input xml> > <output xml>'
    else:
        main(sys.argv[1])
    
