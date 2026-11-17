"""Referee's direct check of the producer's listed witnesses (results.json used as data only),
plus corruption controls. Usage: python3 -I check_witnesses.py RESULTS_JSON"""
import json
import sys


def check(n, word, colour, fam):
    """Return (ok, reason). Distinct, in [n], all of `colour` by size, closed under pairwise union and intersection."""
    s = set(fam)
    if len(s) != len(fam):
        return False, "duplicate"
    if not fam:
        return False, "empty"
    for x in fam:
        if x < 0 or x >> n:
            return False, f"out of range {x}"
        if int(word[bin(x).count('1')]) != colour:
            return False, f"wrong colour {x}"
    for x in fam:
        for y in fam:
            if x | y not in s or x & y not in s:
                return False, f"not closed {x},{y}"
    return True, "ok"


d = json.load(open(sys.argv[1]))
for e in d:
    n, word = e["n"], e["word"]
    assert len(word) == n + 1, (n, word)
    for c in e["colours"]:
        ok, why = check(n, word, c["colour"], c["witness"])
        print(f"n={n} word={word} colour={c['colour']} claimed_max={c['maximum']} witness_size={len(c['witness'])} "
              f"direct_check={why} size_matches={len(c['witness']) == c['maximum']}")
    # controls on the colour-0 witness
    w = list(e["colours"][0]["witness"])
    bad1 = w[:]; bad1[len(w) // 2] ^= 1 << (n - 1)          # flip one coordinate of one member
    bad2 = w[:-2] + [w[-1]]                                  # delete a member
    bad3 = w[:]; bad3[0] = w[1]                              # duplicate
    print("  controls rejected:", [check(n, word, 0, b)[1] for b in (bad1, bad2, bad3)],
          "| wrong colour label:", check(n, word, 1, w)[1])
