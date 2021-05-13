#!/bin/bash
# convert binary file to hex
# ./converttohex out.bin -> out.txt

file=$1
bn=$(echo "${file%.bin}")
cat $1 | xxd -c 40 -p | sed 's/.\{4\}/& /g' | tee $bn.txt
