#!/bin/bash 

# 2014.06.01
# run ./eval.naive.t5.typed.py 

python ./eval.naive.t5.typed.py /tmp2/ccli/yago-ptn-part-$1/ ./yagoPSv1/ps.$1.json /tmp2/ccli/typed.t5.$1.out
mkdir -p ~/nas-3/t5-typed
cp /tmp2/ccli/typed.t5.$1.out ~/nas-3/t5-typed

