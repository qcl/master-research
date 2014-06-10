#!/bin/bash 

# 2014.06.10
# run ./eval.o.typed.py 

python ./eval.patty.naive.typed.py /tmp2/ccli/y-ptn-part-$1/ ./yagoPSv2/ps.$1.json /tmp2/ccli/patty.typed.$1.out
mkdir -p ~/nas-3/patty-typed
cp /tmp2/ccli/patty.typed.$1.out ~/nas-3/patty-typed

