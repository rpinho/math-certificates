"""Fixture test of every link of the type-K chain on lawful step functions h (direct computation).
Links: (a) core  int p Phi >= N0 + C m^2              [round-1 S12, claimant's]
       (b) e/d   int p Phi <= M D - int_0^1 |d| g     [our lemma, part 1]
       (c) dual  int_0^1 |d| g >= lam m/2 - U          [our lemma, part 2, with the bin's certificate]
       (d) final M >= bound of the bin containing |m|
Near-extremal fixtures: sequential LP (as round-1 nearext.py) with the mean pinned to a target."""
import json, sys, os
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.environ.get('E36_CACHE', 'cache').rstrip('/') + '/'   # float caches + outputs (see build_float_cache.py)
VK = os.environ.get('E36_VK', os.path.join(HERE, '..', 'results', 'vK_main.json'))   # verify_K.py output for the certificate
CERT = os.path.join(HERE, '..', 'certificates', 'certK_r105.json')
Phi = np.load(W + 'Phi_Z.npy'); NP = len(Phi); dtp = 4 / NP; tp = (np.arange(NP) + .5) * dtp - 2
g = np.load(W + 'g_fine.npy'); NG = len(g); tg = (np.arange(NG) + .5) / NG
N0 = 1.0000000000000004; C = -0.71989098445083919; D = float(np.sum(np.maximum(Phi, 0)) * dtp); L = 0.38062762587659104
cert = json.load(open(VK))['bins']
certin = json.load(open(CERT))['bins']


def pk(h, w):  # p at t = k w, k = -(n-1)..n-1 ; p piecewise linear in between
    return np.correlate(1 - h, h, mode='full') * w


def near(n, mt, seed):
    w = 2 / n; x = (np.arange(n) + .5) * w; rng = np.random.default_rng(seed)
    def jac(h):
        gg = 1 - h; J = np.zeros((2 * n - 1, n))
        for k in range(-(n - 1), n):
            r = k + n - 1
            i = np.arange(max(0, -k), min(n, n - k)); j = i + k
            J[r, i] += w * gg[j]; J[r, j] -= w * h[i]
        return J
    h = np.clip(0.5 + 0.4 * np.sin(np.pi * x * rng.integers(1, 4)) + 0.1 * rng.normal(size=n), 0, 1)
    h = h / h.sum() / w; h = np.clip(h, 0, 1); rho = 0.2
    for it in range(200):
        p = pk(h, w); J = jac(h)
        c = np.zeros(n + 1); c[-1] = 1
        A = np.hstack([J, -np.ones((2 * n - 1, 1))])
        Aeq = np.zeros((2, n + 1)); Aeq[0, :n] = w; Aeq[1, :n] = x * w
        beq = [1 - h.sum() * w, (2 - mt) / 2 - (h * x).sum() * w]
        bnd = [(max(-rho, -hi), min(rho, 1 - hi)) for hi in h] + [(None, None)]
        res = linprog(c, A_ub=A, b_ub=-p, A_eq=Aeq, b_eq=beq, bounds=bnd, method='highs')
        if not res.success: rho /= 2; continue
        hn = np.clip(h + res.x[:n], 0, 1)
        if pk(hn, w).max() < p.max() + 1e-12 or it < 5: h = hn; rho = min(rho * 1.2, 0.3)
        else: rho /= 2
        if rho < 1e-8: break
    return h


def evaluate(name, h):
    n = len(h); w = 2 / n; x = (np.arange(n) + .5) * w
    mass = h.sum() * w; m = 2 - 2 * (h * x).sum() * w
    P = pk(h, w); M = P.max(); tk = np.arange(-(n - 1), n) * w
    p = np.interp(tp, tk, P, left=0, right=0)
    Ip = np.sum(p * Phi) * dtp
    # d(t) = H(t)+H(2-t)-1, H piecewise linear
    Hn = np.concatenate([[0], np.cumsum(h) * w]); xs = np.arange(n + 1) * w
    d = np.interp(tg, xs, Hn) + np.interp(2 - tg, xs, Hn) - 1
    Idg = np.sum(np.abs(d) * g) / NG
    sgn = 1 if m >= 0 else -1; am = abs(m)
    # reflection: |m| bin; d of reflected h is -d, same |d|
    j = [i for i, b in enumerate(cert) if Fr(b['lo']) <= Fr(am) <= Fr(b['hi'])]
    out = {'name': name, 'n': n, 'mass': mass, 'm': m, 'M': M, 'm_check_2int_d': 2 * np.sum(d) / NG * sgn * sgn,
           'core_slack': Ip - (N0 + C * m * m), 'ed_slack': M * D - Idg - Ip}
    if j:
        b = cert[j[0]]; bi = certin[j[0]]
        lam = float(Fr(bi['lam'])); U = b['U']
        out.update({'bin': [b['lo'], b['hi']], 'dual_slack': Idg - (lam * am / 2 - U), 'Idg': Idg,
                    'final_slack': M - b['bound'], 'bound': b['bound']})
    return out


if __name__ == '__main__':
    res = []
    hne = np.load(os.path.join(HERE, 'data', 'nearext_h128.npy')); res.append(evaluate('nearext128', hne)); res.append(evaluate('nearext128_reflected', hne[::-1]))
    res.append(evaluate('constant_half', np.full(200, 0.5)))
    x = (np.arange(400) + .5) / 200
    res.append(evaluate('three_block', ((x < 0.5) | ((x > 1.0) & (x < 1.5))).astype(float)))
    for mt in [1.5e-4, 3e-4, 1e-3, 2.5e-3, 6e-3, -1e-3]:
        for seed in (1, 2):
            h = near(128, mt, seed); res.append(evaluate('near_m%.1e_s%d' % (mt, seed), h))
            np.save(W + 'fix_m%.1e_s%d.npy' % (mt, seed), h)
    for r in res:
        print(json.dumps({k: (round(v, 10) if isinstance(v, float) else v) for k, v in r.items()}))
    json.dump(res, open(W + 'fixtures_K.json', 'w'), indent=1)
    keys = ['core_slack', 'ed_slack', 'dual_slack', 'final_slack']
    print('MIN', {k: min(r[k] for r in res if k in r) for k in keys})
