"""Greedy hole filling: start from a configuration (JSON with Px, Py, pts), find the uncovered holes of the superlevel
set on a grid, add a tiny mass in a hole, re-optimize all parameters (Nelder-Mead), keep if better; repeat.
Usage: hf.py START.json OUT.json SEED [--rounds 20] [--n 500] [--maxit 400] [--tries 6]"""
import sys, os, json, math, time, argparse
import numpy as np
from scipy.optimize import minimize
from scipy.ndimage import label

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hleval import periodic_ratio, periodic_uncovered
from search import objective, encode, decode


def holes(Px, Py, pts, n):
    gx, gy, unc = periodic_uncovered(Px, Py, pts, n=n)
    lab, nl = label(unc)
    out = []
    for k in range(1, nl + 1):
        idx = np.argwhere(lab == k)
        cx, cy = gx[idx[:, 0]].mean(), gy[idx[:, 1]].mean()
        out.append((len(idx) * (Px / n) * (Py / n), cx, cy, gx[idx[:, 0]].min(), gx[idx[:, 0]].max(),
                    gy[idx[:, 1]].min(), gy[idx[:, 1]].max()))
    out.sort(key=lambda t: -t[0])
    return out, unc.mean()


def polish(x, k, maxit, reps=2):
    for _ in range(reps):
        x = minimize(lambda p: -objective(p, k), x, method='Nelder-Mead',
                     options=dict(maxiter=maxit * len(x), xatol=1e-12, fatol=1e-14, adaptive=True)).x
    return x, objective(x, k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('start'); ap.add_argument('out'); ap.add_argument('seed', type=int)
    ap.add_argument('--rounds', type=int, default=20); ap.add_argument('--n', type=int, default=500)
    ap.add_argument('--maxit', type=int, default=400); ap.add_argument('--tries', type=int, default=6)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    d = json.load(open(a.start))
    d = d.get('best', d)
    Px, Py, pts = d['Px'], d['Py'], [tuple(p) for p in d['pts']]
    k = len(pts)
    x = encode(Px, Py, pts)
    x, val = polish(x, k, a.maxit)
    print('start k=%d ratio %.10f' % (k, val), flush=True)
    t0 = time.time()
    for rnd in range(a.rounds):
        Px, Py, pts = decode(x, k)
        H, frac = holes(Px, Py, pts, a.n)
        print('round %d: %d holes, uncovered %.5f, largest %s' % (rnd, len(H), frac,
              ['%.4g' % h[0] for h in H[:6]]), flush=True)
        if not H:
            break
        improved = False
        for t in range(a.tries):
            h = H[min(t, len(H) - 1)] if t < len(H) else H[int(rng.integers(len(H)))]
            px_ = rng.uniform(h[3], h[4]) if t >= 2 else h[1]
            py_ = rng.uniform(h[5], h[6]) if t >= 2 else h[2]
            m0 = max(1e-4, min(0.05, h[0] * rng.uniform(0.05, 0.4)))
            pts2 = list(pts) + [(px_ % Px, py_ % Py, m0)]
            x2 = encode(Px, Py, pts2)
            x2, v2 = polish(x2, k + 1, a.maxit)
            print('  try %d: hole area %.3g at (%.4f, %.4f), m0 %.3g -> %.10f' % (t, h[0], px_, py_, m0, v2), flush=True)
            if v2 > val + 1e-9:
                x, val, k = x2, v2, k + 1
                improved = True
                break
        Px, Py, pts = decode(x, k)
        json.dump(dict(ratio=val, k=k, params=list(map(float, x)), Px=Px, Py=Py, pts=pts, round=rnd,
                       time=time.time() - t0), open(a.out, 'w'), indent=1)
        print('round %d done: k=%d ratio %.10f (t=%.0fs)' % (rnd, k, val, time.time() - t0), flush=True)
        if not improved:
            break


if __name__ == '__main__':
    main()
