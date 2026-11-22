"""Build the float-grid caches used only by the SEARCH (make_K.py) and the fixtures (fixtures_K.py):
Phi_Z.npy (float kernel on 2^20 midpoints of [-2,2]) and g_fine.npy (folded weight g on [0,1]).
Not needed to check the certificate (verify_K.py rebuilds the kernel exactly from the inputs).
Combines round-1's kernel_var.py (base, Zp), kernel_var2.py (rowk), kernel_norm.py (Phi = base+rowk+Zp+const)
and the g-map step. usage: E36_INPUTS=DIR python -I build_float_cache.py CACHE_DIR"""
import os, sys, json
import numpy as np
from fractions import Fraction as F
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
D = I + 'unktok/proof/data/'
k = json.load(open(D + 'selected-exact-kernel.json'))
po = json.load(open(D + 'exact-periodic-offsets.json'))
c = json.load(open(I + 'wetch/central-certificate.json'))
per = np.zeros(po['cells'])
for i, v in po['sparse']: per[i] = float(F(v))
const = float(F(k['constant_exact'])); y2 = float(k['y2_exact'])
H = np.array([float(F(x)) for x in k['fine_hat_heights_exact']])
cos = [(float(F(q['xi'])), float(F(q['z']))) for q in k['merged_cos']]
N = 2 ** 20; t = (np.arange(N) + 0.5) * 4 / N - 2; at = np.abs(t)
base = y2 * t * t + np.interp(at, np.arange(241) / 120, H)
for xi, z in cos: base += z * np.cos(xi * t)
Zp = per[np.clip((at * 65536).astype(int), 0, 131071)]
rowk = np.zeros(N)
for r in c['functional_rows']:
    mu = r['multiplier']; mu = float(F(mu)) if isinstance(mu, str) else float(mu)
    g = np.array([float(F(x)) if isinstance(x, str) else float(x) for x in r['certificate']['functional_weights']])
    nc = r['certificate']['cells']; a = 2 / nc; knots = np.arange(nc + 1) * a
    hts = np.concatenate([[g[0] / a], g[1:] / (2 * a)])
    rowk += mu * np.interp(at, knots, hts, right=0)
Phi = (base + rowk + Zp) + const
np.save(os.path.join(out, 'Phi_Z.npy'), Phi)
P = Phi; i0 = N // 2; K = N // 4
A = P[i0:i0 + K]; B = P[i0 + N // 2 - 1 - np.arange(K)]
np.save(os.path.join(out, 'g_fine.npy'), np.abs(A) + np.abs(B))
print('wrote Phi_Z.npy, g_fine.npy to', out)
