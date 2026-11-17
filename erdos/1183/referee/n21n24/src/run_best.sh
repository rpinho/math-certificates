#!/bin/bash
# exact maxima of the producer's best words (data only) and the n=11..20 controls
for p in "21 0010011100101100011011" "21 0011001011100010110011" "22 00100111010011100110100" "23 001001110010110001101101" "24 0011010011101001101010010" $(awk '/^max n=/{sub("n=","",$2);sub("word=","",$3);print $2":"$3}' ../e1183n1520_referee/out/max_words.txt | sort -u | tr '\n' ' '); do
  p=${p/:/ }; set -- $p
  for c in 0 1; do s=$(date +%s.%N); nice -n 10 ./src/wp max $1 $2 $c; e=$(date +%s.%N); echo "  time=$(echo "$e - $s" | bc)"; done
done
