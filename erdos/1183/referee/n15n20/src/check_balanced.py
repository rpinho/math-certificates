"""Independent re-check of the balanced-word witness file written by wps bal.
Each line: WORD COLOUR mask... . Checks: the words are exactly all words of length n+1 with (n+1)/2 ones,
and every witness has >= (n+3)/2 distinct members of that colour, inside [n], closed under union and intersection.
Usage: python3 -I check_balanced.py N FILE"""
import sys
from itertools import combinations

n = int(sys.argv[1])
m, thr = (n + 1) // 2, (n + 3) // 2
seen, bad = set(), 0
for line in open(sys.argv[2]):
    p = line.split()
    word, c = p[0], p[1]
    if c == "NONE":
        bad += 1
        continue
    c, fam = int(c), [int(x) for x in p[2:]]
    s = set(fam)
    ok = (len(word) == n + 1 and word.count("1") == m and len(s) == len(fam) >= thr
          and all(0 <= x < (1 << n) and int(word[bin(x).count("1")]) == c for x in fam)
          and all((x | y) in s and (x & y) in s for x in fam for y in fam))
    bad += not ok
    seen.add(word)
expected = {"".join("1" if i in S else "0" for i in range(n + 1)) for S in map(set, combinations(range(n + 1), m))}
print(f"n={n} balanced_words_expected={len(expected)} lines_with_witness={len(seen)} all_covered={seen == expected} bad={bad} threshold={thr}")
