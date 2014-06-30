#!/bin/bash 

# 2014.06.30
# run ./eval.py

python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-200-00-$1/ 0.0 ../selectPattern/ps-c-0/ps.$1.json /home/ccli/nas-3/vsm-00 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-200-70-$1/ 0.7 ../selectPattern/ps-c-7/ps.$1.json /home/ccli/nas-3/vsm-70 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-200-80-$1/ 0.8 ../selectPattern/ps-c-8/ps.$1.json /home/ccli/nas-3/vsm-80 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-200-90-$1/ 0.9 ../selectPattern/ps-c-9/ps.$1.json /home/ccli/nas-3/vsm-90 $1.out
