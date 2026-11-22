import os
"""Rebuild the periodic-offset step function from Wetch's 9 families (ANALYTIC-REVIEW 'periodic components') and compare
with exact-periodic-offsets.json. z(t) = (n/2) z_i on cell i (width 2/n, n = 131072 on [0,2]);
int_0^2 z(t) q(l t) dt = int_0^2 q(s) Z_l(s) ds, Z_l[j] = (1/l) sum_{k<l} zh[floor((j + k n)/l)];
q(s) = p_e(s) + p_e(2-s)  ->  kernel on |t|:  1/2 sum_fam sum_{i<j} b_i b_j (Z_l[j] + Z_l[n-1-j])."""
import json
import numpy as np
from fractions import Fraction as F
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
w = json.load(open(I + 'wetch/central-certificate.json'), parse_float=str)
p = json.load(open(I + 'unktok/proof/data/exact-periodic-offsets.json'), parse_float=str)
n = 131072
Zd = np.zeros(n); 
for i, v in p['sparse']: Zd[int(i)] = float(F(v))
K = np.zeros(n)
j = np.arange(n)
for f in w['families']:
    x = [int(v) for v in f['positions']]; b = [int(v) for v in f['b']]
    zh = np.array([float(F(v)) for v in f['z']]) * (n / 2)
    for a in range(3):
        for c in range(a + 1, 3):
            l = abs(x[a] - x[c]); Zl = np.zeros(n)
            for k in range(l): Zl += zh[(j + k * n) // l]
            Zl /= l
            K += 0.5 * b[a] * b[c] * (Zl + Zl[::-1])
print('rebuilt: min %.4e max %.4e nnz(|K|>1e-15) %d ; stored: nnz %d min %.4e max %.4e' % (K.min(), K.max(), np.sum(np.abs(K) > 1e-15), np.sum(Zd != 0), Zd.min(), Zd.max()))
for name, cand in [('K', K), ('-K', -K), ('K - mean', K - K.mean()), ('-(K - mean)', -(K - K.mean()))]:
    print('%-12s max|Zstored - cand| = %.3e' % (name, np.max(np.abs(Zd - cand))))
print('first cells stored', Zd[:4], 'rebuilt', K[:4])
