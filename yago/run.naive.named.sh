#!/bin/bash 

# 2014.06.02
# run ./eval.naive.typed.named.py

python ./eval.naive.typed.named.py /tmp2/ccli/yago-ptn-part-$1/ /tmp2/ccli/yago-part-$1/ ./yagoPSv1/ps.$1.json /tmp2/ccli/named.$1.out
mkdir -p ~/nas-3/named
cp /tmp2/ccli/named.$1.out ~/nas-3/named

