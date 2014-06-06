#!/bin/bash 

# 2014.06.01
# run ./eval.o.typed.py 

python ./eval.o.typed.named.py /tmp2/ccli/y-ptn-part-$1/ ./yagoPSv2/ps.$1.json /tmp2/ccli/o.named.$1.out
mkdir -p ~/nas-3/o-named
cp /tmp2/ccli/o.named.$1.out ~/nas-3/o-named

