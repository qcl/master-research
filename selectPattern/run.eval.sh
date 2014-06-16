#!/bin/bash 

# 2014.06.17
# run ./eval.py

python ./eval.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-0/ps.$1.json /home/ccli/nas-3 $1.out 0

