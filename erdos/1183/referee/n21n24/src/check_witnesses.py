"""Direct closure check of the producer's witness families (data only), plus corruption controls.
Usage: python3 check_witnesses.py ../e1183n21/certificates/upper_n2{1,2,3,4}.json"""
import json, sys, random


def check(n, word, colour, fam):
    """Return (ok, reason). ok iff distinct masks in [n], every member's size coloured `colour`,
    closed under union and intersection."""
    s = set(fam)
    if len(s) != len(fam):
        return False, "duplicate"
    for x in fam:
        if x < 0 or x >> n:
            return False, f"mask {x} outside [n]"
        if int(word[bin(x).count("1")]) != colour:
            return False, f"mask {x} rank {bin(x).count('1')} wrong colour"
    for x in fam:
        for y in fam:
            if (x | y) not in s or (x & y) not in s:
                return False, f"not closed at {x},{y}"
    return True, "ok"


rng = random.Random(1183)
for path in sys.argv[1:]:
    d = json.load(open(path))
    n, w = d["n"], d["word"]
    assert len(w) == n + 1
    for c in d["colours"]:
        fam = c["witness"]
        ok, why = check(n, w, c["colour"], fam)
        print(f"n={n} word={w} colour={c['colour']} claimed_max={c['maximum']} members={len(fam)} {why}")
        # corruption controls: flip one coordinate of one member; drop the top member
        bad = list(fam)
        i = rng.randrange(len(bad))
        bad[i] ^= 1 << rng.randrange(n)
        print("   corrupt(flip a bit):", check(n, w, c["colour"], bad)[1])
        bad = sorted(fam)[:-1] + [sorted(fam)[-1] ^ (1 << (n - 1))] if sorted(fam)[-1] >> (n - 1) & 1 else None
        bad2 = [x for x in fam if x != (max(fam, key=lambda v: bin(v).count('1')))]
        # removing the top is still closed only if the top is not a join; report whatever happens
        print("   drop top member:", check(n, w, c["colour"], bad2)[1], f"(members={len(bad2)})")
        flipw = w[: n] + str(1 - int(w[n]))
        print("   word with last letter flipped:", check(n, flipw, c["colour"], fam)[1])
