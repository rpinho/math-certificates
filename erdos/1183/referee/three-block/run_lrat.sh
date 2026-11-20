#!/bin/sh
# check all 144 LRATs with my checker and with drat-trim lrat-check
py="${PYTHON:-python3}"
checker="${LRAT_CHECK:-ext/lrat-check}"
n=0; a=0; b=0
for c in ../data/face/*.cnf ../data/split23/*.cnf ../data/split22/*.cnf; do
  l=${c%.cnf}.lrat; n=$((n+1))
  r1=$("$py" -I lrat.py "$c" "$l")
  r2=$("$checker" "$c" "$l" 2>&1 | grep -c 'c VERIFIED')
  [ "$r1" = VERIFIED ] && a=$((a+1)) || echo "own: $c $r1"
  [ "$r2" -ge 1 ] && b=$((b+1)) || echo "drat-trim: $c"
done
echo "LRAT files $n own-verified $a drat-trim-verified $b"
[ "$n" -eq 144 ] && [ "$a" -eq "$n" ] && [ "$b" -eq "$n" ]
