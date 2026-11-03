"""Multi-start local search over periodic point-mass configurations (rectangular cell, k points per cell, lam = 1).
Parameters: log Px, log Py, then for i = 1..k-1: x_i/Px, y_i/Py (mod 1), log m_i; point 0 = (0, 0) with mass 1.
Usage: search.py SEED K TRIALS OUT.json [--init lin|rand|file:PATH]"""
import sys, os, json, math, time, argparse
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hleval import periodic_ratio, lin_config


def decode(p, k):
    Px, Py = math.exp(p[0]), math.exp(p[1])
    pts = [(0.0, 0.0, 1.0)]
    for i in range(1, k):
        fx, fy, lm = p[2 + 3 * (i - 1): 5 + 3 * (i - 1)]
        pts.append(((fx % 1.0) * Px, (fy % 1.0) * Py, math.exp(lm)))
    return Px, Py, pts


def objective(p, k):
    try:
        Px, Py, pts = decode(p, k)
        if not (0.05 < Px < 50 and 0.05 < Py < 50) or any(not (1e-3 < q[2] < 1e3) for q in pts):
            return 0.0
        r, _, _ = periodic_ratio(Px, Py, pts, lam=1.0)
        return r
    except Exception:
        return 0.0


def encode(Px, Py, pts):
    p = [math.log(Px), math.log(Py)]
    for (x, y, m) in pts[1:]:
        p += [x / Px, y / Py, math.log(m)]
    return np.array(p)


def lin_start(k, rng):
    Px, Py, pts = lin_config()
    if k == 2:
        return encode(Px, Py, pts)
    # replicate Lin's cell r times in y (or x) to get >= k points, then keep k of them and perturb
    rep = int(math.ceil(k / 2))
    P2 = []
    for j in range(rep):
        P2 += [(x, y + j * Py, m) for (x, y, m) in pts]
    P2 = P2[:k]
    return encode(Px, rep * Py, P2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('seed', type=int); ap.add_argument('k', type=int); ap.add_argument('trials', type=int)
    ap.add_argument('out'); ap.add_argument('--init', default='mix'); ap.add_argument('--sigma', type=float, default=0.15)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    k = a.k
    best = None
    t0 = time.time()
    for trial in range(a.trials):
        mode = a.init if a.init != 'mix' else ('lin' if trial % 3 == 0 else 'rand')
        if mode == 'lin':
            p0 = lin_start(k, rng)
            p0 = p0 + a.sigma * rng.standard_normal(len(p0)) * np.r_[[0.3, 0.3], np.tile([0.2, 0.2, 1.0], k - 1)]
        elif mode.startswith('file:'):
            d = json.load(open(mode[5:]))
            p0 = np.array(d['params']) + a.sigma * rng.standard_normal(len(d['params']))
        else:
            Px, Py = math.exp(rng.uniform(0.0, 1.6)), math.exp(rng.uniform(0.0, 1.6))
            pts = [(0.0, 0.0, 1.0)] + [(rng.uniform(0, Px), rng.uniform(0, Py), math.exp(rng.normal(0, 0.8)))
                                       for _ in range(k - 1)]
            p0 = encode(Px, Py, pts)
        res = minimize(lambda p: -objective(p, k), p0, method='Nelder-Mead',
                       options=dict(maxiter=4000 * len(p0), xatol=1e-9, fatol=1e-12, adaptive=True))
        # one restart from the optimum (Nelder-Mead stalls on kinks)
        res2 = minimize(lambda p: -objective(p, k), res.x, method='Nelder-Mead',
                        options=dict(maxiter=4000 * len(p0), xatol=1e-10, fatol=1e-13, adaptive=True))
        val = -res2.fun
        if best is None or val > best['ratio']:
            Px, Py, pts = decode(res2.x, k)
            best = dict(ratio=val, k=k, params=list(map(float, res2.x)), Px=Px, Py=Py, pts=pts, trial=trial, mode=mode)
            json.dump(best, open(a.out, 'w'), indent=1)
        print('trial %d (%s) k=%d ratio %.10f best %.10f t=%.0fs' % (trial, mode, k, val, best['ratio'], time.time() - t0),
              flush=True)


if __name__ == '__main__':
    main()
