# -*- coding: utf-8 -*-
# qcl
import sys
import simplejson as json

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        f = open(sys.argv[1],"r")
        dic = json.load(f)
        f.close()

        sorted_dic = sorted(dic.iteritems(), key = lambda x:x[1])
        sorted_dic.reverse()

        for item in sorted_dic:
            print "%s\t%s" % (item[0],str(item[1]))
