#!/bin/bash 

# 2014.06.16
# run ./eval.py

python ./eval.py /tmp2/ccli/yago-ptn-part-$1/ /tmp2/ccli/yago-part-$1/ ./ps-c-0/ps.$1.json /home/ccli/nas-3 $1.out 0

