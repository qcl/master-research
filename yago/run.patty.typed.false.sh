#!/bin/bash 

# 2014.06.10
# run ./eval.o.typed.py 

python ./eval.patty.naive.typed.usefalse.py /tmp2/ccli/y-ptn-part-$1/ ./yagoPSv2/ps.$1.json /tmp2/ccli/patty.typed.false.$1.out
mkdir -p ~/nas-3/patty-typed-false
cp /tmp2/ccli/patty.typed.false.$1.out ~/nas-3/patty-typed-false

