#!/bin/bash 

# 2014.07.04
# run ./errorChecking.py

python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ../selectPattern/ps-c-0/ps.$1.json /home/ccli/nas-3/ecnbc-00 $1.out 0 /tmp2/ccli/nbc-00-$1
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ../selectPattern/ps-c-7/ps.$1.json /home/ccli/nas-3/ecnbc-70 $1.out 0.7 /tmp2/ccli/nbc-70-$1
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ../selectPattern/ps-c-8/ps.$1.json /home/ccli/nas-3/ecnbc-80 $1.out 0.8 /tmp2/ccli/nbc-80-$1
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ../selectPattern/ps-c-8/ps.$1.json /home/ccli/nas-3/ecnbc-88 $1.out 0.88 /tmp2/ccli/nbc-80-$1
python ./errorChecking.py /tmp2/ccli/y-ptn-part-$1/ /tmp2/ccli/y-part-$1/ ../selectPattern/ps-c-9/ps.$1.json /home/ccli/nas-3/ecnbc-90 $1.out 0.9 /tmp2/ccli/nbc-90-$1
