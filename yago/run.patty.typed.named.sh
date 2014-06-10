#!/bin/bash 

python ./eval.patty.naive.typed.named.py /tmp2/ccli/y-ptn-part-$1/ ./yagoPSv2/ps.$1.json /tmp2/ccli/patty.named.$1.out
mkdir -p ~/nas-3/patty-named
cp /tmp2/ccli/patty.named.$1.out ~/nas-3/patty-named

