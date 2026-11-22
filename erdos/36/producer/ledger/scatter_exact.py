import os
import json
from fractions import Fraction as F
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
w = json.load(open(I + 'wetch/central-certificate.json'), parse_float=str)
p = json.load(open(I + 'unktok/proof/data/exact-periodic-offsets.json'), parse_float=str)
n = 131072
Zs = {int(i): F(v) for i, v in p['sparse']}
K = [F(0)] * n
for f in w['families']:
    x = [int(v) for v in f['positions']]; b = [int(v) for v in f['b']]
    zh = [F(v) * (n // 2) for v in f['z']]
    for a in range(3):
        for c in range(a + 1, 3):
            l = abs(x[a] - x[c]); s = F(b[a] * b[c], 2 * l)
            Zl = [sum(zh[(j + k * n) // l] for k in range(l)) for j in range(n)]
            for j in range(n): K[j] += s * (Zl[j] + Zl[n - 1 - j])
bad = sum(1 for j in range(n) if K[j] != Zs.get(j, F(0)))
print('cells where rebuilt != stored (exact rationals):', bad, 'of', n)
