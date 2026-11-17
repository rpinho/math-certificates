"""lem:words: every length-12 word over {R,B} contains a forbidden block (8 table words, reversals,
letter swaps); lem:gadgets checked separately by src/wp max on each table word."""
T = ["RRR", "RBRBR", "RBBRBBR", "RRBBRRBBR", "RBRRBRBBR", "RRBRBBRRBR", "RBRRBBRRBR", "RBBRRBRBBR"]
sw = lambda u: u.translate(str.maketrans("RB", "BR"))
F = set()
for t in T:
    for v in (t, t[::-1]):
        F |= {v, sw(v)}
from itertools import product
miss = [w for w in ("".join(p) for p in product("RB", repeat=12)) if not any(f in w for f in F)]
print("length 12 words without a forbidden block:", len(miss))
miss11 = [w for w in ("".join(p) for p in product("RB", repeat=11)) if not any(f in w for f in F)]
print("length 11 words without one:", len(miss11), "RRBRBBRRBBR among them:", "RRBRBBRRBBR" in miss11)
for t in T:
    print("GADGET", len(t) - 1, t.replace("R", "0").replace("B", "1"), t.count("R"))
