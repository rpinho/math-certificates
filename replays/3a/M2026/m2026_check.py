#!/usr/bin/env python3
"""Replay of 3a M2026 from the constant page text only (no claimant data, no claimant code).
Builds: M = <gens> ∩ [0,B]; kappa(d) = min{a+b: a-b=d}; c(r) = min kappa(d) over d in M-M, d = r mod q (q odd);
histogram of c over Z/qZ; type N_r = floor(ell x^c(r)/Z) (r != 0), N_0 = ell - sum; C = sum N_r c(r); L = C/2;
then the bound of ghr_check.run with block length k=1 and no self-inverse residue other than 0."""
import sys, json
sys.path.insert(0, '../Syl2026_k2k3')
from decimal import Decimal as D, getcontext
import ghr_check as g
from collections import Counter
G = [1518, 1524, 1587, 2024, 2032, 2116]; q = 27995; ell = 10 ** 13
def build(B):
    M = g.semigroup_mask(G, B)
    kap = {}
    for a in M:
        for b in M:
            d = a - b; s = a + b
            if d not in kap or s < kap[d]: kap[d] = s
    c = {}
    for d, s in kap.items():
        r = d % q
        if r not in c or s < c[r]: c[r] = s
    assert len(c) == q
    assert all(c[r] == c[(-r) % q] for r in c)          # symmetry
    hist = Counter(c.values())
    fn = 'hist_B%d.tsv' % B
    with open(fn, 'w') as f:
        f.write('# cost\tmultiplicity\n')
        for cc in sorted(hist): f.write('%d\t%d\n' % (cc, hist[cc]))
    return fn, len(M)
out = {}
for B, claim, xs in [(17086, '1.1923025406835', '0.9996683050229444'), (17032, '1.1922990483828', '0.9996683050229444')]:
    fn, nM = build(B)
    getcontext().prec = 120
    x_decimal = D(xs)
    x_double = D(float(xs))
    for label, xd in [('x=decimal literal', x_decimal), ('x=binary64 nearest', x_double)]:
        r = g.run(G, B, q, 1, 0, 0, ell, fn, None, claim, x_dec=xd)
        out['B=%d %s' % (B, label)] = {k: r[k] for k in ('|M|', '|M+M|', 'n0', 'C', 'theta_lo', 'claim', 'PASS', 'min_floor_margin', 'numerator_positive', 'theta_infinity_info')}
        out['B=%d %s' % (B, label)]['L'] = r['C'] // 2
print(json.dumps(out, indent=1))
