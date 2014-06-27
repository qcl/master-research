#!/bin/bash 

# 2014.06.27
# run ./eval.py

python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-00-$1/ 0.0 /home/ccli/nas-3/vsm-00 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-70-$1/ 0.7 /home/ccli/nas-3/vsm-70 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-80-$1/ 0.8 /home/ccli/nas-3/vsm-80 $1.out
python ./eval.py /home/ccli/tmp2/y-part-$1/ /home/ccli/tmp2/y-ptn-part-$1/ /home/ccli/tmp2/tfidf-90-$1/ 0.9 /home/ccli/nas-3/vsm-90 $1.out
