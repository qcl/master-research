#!/bin/bash 

# 2014.06.01
# run ./eval.naive.typed.py 

python ./eval.naive.typed.py /tmp2/ccli/yago-ptn-part-$1/ ./yagoPSv1/ps.$1.json /tmp2/ccli/typed.$1.out
mkdir -p ~/nas-3/typed
cp /tmp2/ccli/typed.$1.out ~/nas-3/typed

