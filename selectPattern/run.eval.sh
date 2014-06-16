#!/bin/bash 

# 2014.06.17
# run ./eval.py

python ./eval.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-0/ps.$1.json /home/ccli/nas-3/confidence-0 $1.out 0
python ./eval.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-7/ps.$1.json /home/ccli/nas-3/confidence-7 $1.out 0.7
python ./eval.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-8/ps.$1.json /home/ccli/nas-3/confidence-8 $1.out 0.8
python ./eval.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-9/ps.$1.json /home/ccli/nas-3/confidence-9 $1.out 0.9

