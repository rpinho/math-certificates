#!/bin/bash
# (1) exact maxima of every n=22 survivor at T=13; (2) single-letter flips of the best words
echo "== n=22 survivors (first letter 0) exact maxima"
for w in $(awk '{print $3}' out/screen_T13_good.txt); do
  a=$(./src/wp max 22 $w 0 | grep -o "max=[0-9]*"); b=$(./src/wp max 22 $w 1 | grep -o "max=[0-9]*"); echo "$w $a $b"; done
echo "== single-letter flips: n word pos value(max of the two colour maxima)"
for p in "21 0010011100101100011011" "22 00100111010011100110100" "23 001001110010110001101101" "24 0011010011101001101010010"; do
  set -- $p; n=$1; w=$2; line="n=$n"
  for ((k=0;k<=n;k++)); do b=${w:$k:1}; f="${w:0:$k}$((1-b))${w:$((k+1))}"
    a=$(./src/wp max $n $f 0 | sed 's/.*max=\([0-9]*\).*/\1/'); c=$(./src/wp max $n $f 1 | sed 's/.*max=\([0-9]*\).*/\1/')
    v=$(( a>c ? a : c )); line="$line $k:$a/$c"; done; echo "$line"; done
