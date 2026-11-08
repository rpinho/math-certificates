#!/usr/bin/env python3
"""Partial independent check of the k=3 cost histogram (the full rebuild is too slow in pure Python).
 (1) exact: every residue r with c_3(r) <= T is hit by a lift triple (d0,d1,d2) in D^3 with kappa-sum <= T, so
     enumerating all such triples and keeping the minimum per residue gives m(c) exactly for c <= T.  Compared
     with the claimant's histogram for all c <= T.
 (2) Lemma 0 (carry automaton) vs these exact minima on a sample of residues.
 (3) statistical: random residues, automaton cost, cumulative frequencies vs histogram.
"""
import sys, random, math, time
from collections import Counter
sys.path.insert(0, '.')
import rebuild_hist as R
B, q = R.B, R.q
T = int(sys.argv[1]); NS = int(sys.argv[2])
hist = {}
for line in open('../_raw/syl/k3/data/k3_cost_hist.tsv'):
    if line[0] == '#': continue
    c, m = line.split(); hist[int(c)] = int(m)
M = R.mask(); tab = R.kappa_table(M); kap = R.make_kap(tab)
Dk = sorted(((kap(d), d) for d in range(-B, B + 1) if kap(d) < R.INF))
# count triples
cnt = Counter(k for k, d in Dk)
ks = sorted(cnt)
# number of ordered triples with sum <= T
c2 = Counter()
for a in ks:
    for b in ks:
        if a + b <= T: c2[a + b] += cnt[a] * cnt[b]
n3 = sum(c2[s] * cnt[c] for s in c2 for c in ks if s + c <= T)
print('T', T, 'ordered triples with sum <=T:', n3, flush=True)
Q = q ** 3
best = {}
t0 = time.time()
L = [(k, d) for k, d in Dk if k <= T]
for k0, d0 in L:
    for k1, d1 in L:
        s01 = k0 + k1
        if s01 > T: break
        base = d0 + d1 * q
        for k2, d2 in L:
            s = s01 + k2
            if s > T: break
            r = (base + d2 * q * q) % Q
            v = best.get(r)
            if v is None or s < v: best[r] = s
print('enumerated in', round(time.time() - t0, 1), 's; residues hit', len(best), flush=True)
mine = Counter(best.values())
bad = [(c, mine.get(c, 0), hist.get(c, 0)) for c in sorted(set(hist) | set(mine)) if c <= T and mine.get(c, 0) != hist.get(c, 0)]
print('costs <= T compared:', sum(1 for c in hist if c <= T), 'mismatches:', len(bad), bad[:5])
# (2) Lemma 0 on enumerated residues
def c_auto(r):
    digs = [r % q, (r // q) % q, r // (q * q)]
    best = R.INF
    for gs in range(8):
        g = [0, -(gs & 1), -((gs >> 1) & 1), -((gs >> 2) & 1)]
        tot = 0
        for i in range(3):
            tot += kap(digs[i] - g[i] + q * g[i + 1])
            if tot >= R.INF: break
        best = min(best, tot)
    return best
rnd = random.Random(7)
keys = rnd.sample(sorted(best), min(20000, len(best)))
print('Lemma0 (automaton) vs exact enumeration on', len(keys), 'residues: mismatches', sum(1 for r in keys if c_auto(r) != best[r]), flush=True)
# (3) sampling
cum = []
tot = 0
for c in sorted(hist):
    tot += hist[c]; cum.append((c, tot / Q))
sample = [c_auto(rnd.randrange(Q)) for _ in range(NS)]
sample.sort()
import bisect
print('sample size', NS)
worst = 0
for p in (0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99):
    # threshold t = hist quantile
    t = next(c for c, F in cum if F >= p)
    F = dict(cum)[t]
    emp = bisect.bisect_right(sample, t) / NS
    z = (emp - F) / math.sqrt(F * (1 - F) / NS)
    worst = max(worst, abs(z))
    print('  quantile %.3f: threshold cost %d  hist F=%.5f  sample F=%.5f  z=%.2f' % (p, t, F, emp, z))
print('max |z| =', round(worst, 2))
