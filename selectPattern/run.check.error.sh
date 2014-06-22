#!/bin/bash 

# 2014.06.22
# run ./errorChecking.py

python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-0/ps.$1.json /home/ccli/nas-3/e-c-00 $1.out 0
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-7/ps.$1.json /home/ccli/nas-3/e-c-70 $1.out 0.7
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-8/ps.$1.json /home/ccli/nas-3/e-c-80 $1.out 0.8
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-8/ps.$1.json /home/ccli/nas-3/e-c-88 $1.out 0.88
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ./ps-c-9/ps.$1.json /home/ccli/nas-3/e-c-90 $1.out 0.9
