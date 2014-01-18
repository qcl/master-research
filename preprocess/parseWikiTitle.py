# -*- coding: utf-8 -*-
# output the title from wiki-dump

import sys
import os

for line in sys.stdin:
    if "    <title>" in line:
        print line[11:-9]
