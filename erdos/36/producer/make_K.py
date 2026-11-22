"""Search for type-K certificates (float g from Phi_Z.npy; the exact check is verify_K.py, written separately).
usage: E36_CACHE=DIR python -I make_K.py OUT.json [ratio] [safety_rel] [safety_abs]"""
import os, sys, json, math
import numpy as np
from fractions import Fraction as Fr

NC = 65536
out = sys.argv[1]
ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
srel = float(sys.argv[3]) if len(sys.argv) > 3 else 0.99
sabs = float(sys.argv[4]) if len(sys.argv) > 4 else 3e-7
g4 = np.load(os.path.join(os.environ.get('E36_CACHE', 'cache'), 'g_fine.npy')).reshape(NC, -1)
gs = np.maximum(srel * g4.min(axis=1) - sabs, 0.0)
pref = np.minimum.accumulate(gs)          # pref[k] = min gs[0..k]
N0 = 1.0000000000000004; C = -0.71989098445083919; Dup = 2.627239663352680428; L = 0.38062762587659104


def greedy_f(lam):
    u = 0.0; U = 0.0; w = 1.0 / NC
    for k in range(NC - 1, -1, -1):
        tg = u * NC
        if lam - gs[k] <= tg <= lam + gs[k]: s = tg; ul = 0.0
        else: s = min(max(tg, lam - gs[k]), lam + gs[k]); ul = u - s * w
        U += (abs(u) + abs(ul)) * w / 2 if u * ul >= 0 else (u * u + ul * ul) / (2 * abs(u - ul)) * w
        u = ul
        if u == 0.0 and (k == 0 or pref[k - 1] >= lam): return U, k
    return U + abs(u) * 0, 0


def greedy_exact(lam):
    lamF = Fr(lam); u = Fr(0); sl = []
    for k in range(NC - 1, -1, -1):
        g = Fr(float(gs[k]))
        s = min(max(u * NC, lamF - g), lamF + g); u = u - s / NC; sl.append(s)
        if u == 0 and (k == 0 or pref[k - 1] >= lam): return k, sl[::-1]
    raise RuntimeError('did not return to 0')


def score(lam, lo, hi):
    U, _ = greedy_f(lam)
    return min(C * lo * lo + lam * lo / 2, C * hi * hi + lam * hi / 2) - U


def best_lam(lo, hi):
    if lo == 0: return 0.0
    xs = np.geomspace(max(lo, 1e-6) * 0.2, max(hi, 1e-6) * 20, 40)
    v = [score(x, lo, hi) for x in xs]; j = int(np.argmax(v))
    a, b = xs[max(j - 1, 0)], xs[min(j + 1, len(xs) - 1)]
    for _ in range(30):  # golden section in log
        m1 = a * (b / a) ** 0.382; m2 = a * (b / a) ** 0.618
        if score(m1, lo, hi) > score(m2, lo, hi): b = m2
        else: a = m1
    return math.sqrt(a * b)


def dec(x, sig=6): return '%.*e' % (sig - 1, x)


# bins: [0, e0] core only, then geometric up to 1/160
edges = [Fr(1, 160)]
while edges[-1] > Fr('7e-5'):
    edges.append(Fr(dec(float(edges[-1]) / ratio, 4)))
edges[-1] = Fr('7e-5'); edges.append(Fr(0)); edges = edges[::-1]
bins = []
for lo, hi in zip(edges, edges[1:]):
    lam = best_lam(float(lo), float(hi))
    lamd = dec(lam, 8) if lam > 0 else '0'
    if lam > 0:
        k0, sl = greedy_exact(float(Fr(lamd)))
    else:
        k0, sl = NC, []
    sc = score(float(Fr(lamd)), float(lo), float(hi)) if lam > 0 else C * float(hi) ** 2
    est = (N0 + sc) / Dup
    print('%s %s lam=%s k0=%d est_margin=%.3e' % (lo, hi, lamd, k0, est - L), flush=True)
    bins.append({'lo': str(lo), 'hi': str(hi), 'lam': lamd, 'k0': k0, 'slopes': [str(s) for s in sl],
                 'est_margin_float': est - L})
json.dump({'type': 'K', 'target_lo': '0', 'target_hi': '1/160', 'ratio': ratio, 'safety': [srel, sabs], 'bins': bins},
          open(out, 'w'))
print('bins', len(bins), 'min est margin', min(b['est_margin_float'] for b in bins))
