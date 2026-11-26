"""Referee's numerical (NOT rigorous) rate functions, from the referee's own derivation.

L(a,Q) = 9 sum a log a - 5 sum_{ij ordered} Q log Q, Q symmetric, blue support, rows a.
Off-diagonal ordered entries x = (q02, q03, q13, q14, q24); diag Q_ii = a_i - sum_j Q_ij.
Naive rate:   N(a)  = max_Q L
Case I rate:  R1(a) = max_Q L + a0 log f(q03/a0),  f(p) = 1-(1-p)^10
Case II rate (referee's version of LEMMAS §4 bound, optimised over the free parameter u):
  R2(a) = max_Q [ L + a0*(log f(u) - beta u) + 90 q24 log(1 + p (e^{beta/10}-1)) ],  p = q02/(a2-q24)
  (this is an upper bound on the true Case II exponent; minimised over u.)
"""
import numpy as np
from scipy.optimize import minimize

PAIRS = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 4)]
d = 10


def xlogx(x):
    x = np.asarray(x, float)
    return np.where(x > 0, x * np.log(np.where(x > 0, x, 1)), 0.0)


def diag(a, x):
    s = np.zeros(5)
    for k, (i, j) in enumerate(PAIRS):
        s[i] += x[k]; s[j] += x[k]
    return a - s


def L(a, x):
    dg = diag(a, x)
    if np.any(dg < -1e-15) or np.any(x < -1e-15):
        return -np.inf
    return 9 * xlogx(a).sum() - 5 * (xlogx(dg).sum() + 2 * xlogx(x).sum())


def f(p):
    return 1 - (1 - p) ** d


def obj_case1(a, x):
    v = L(a, x)
    if not np.isfinite(v):
        return v
    p = min(1.0, x[1] / a[0])
    return v + a[0] * np.log(max(f(p), 1e-300))


def inner_max(a, obj, x0=None, extra_dim=0, extra_bounds=()):
    """maximise concave-ish obj over feasible x (and optional extra params)"""
    cons = [{"type": "ineq", "fun": (lambda z, i=i: diag(a, z[:5])[i])} for i in range(5)]
    best = (-np.inf, None)
    starts = []
    # start: independent-ish
    for s in range(4):
        rng = np.random.default_rng(s)
        z = np.array([min(a[i], a[j]) for i, j in PAIRS]) * rng.uniform(0.05, 0.3, 5)
        if extra_dim:
            z = np.concatenate([z, [np.mean(b) for b in extra_bounds]])
        starts.append(z)
    if x0 is not None:
        starts.append(x0)
    bnds = [(0, min(a[i], a[j])) for i, j in PAIRS] + list(extra_bounds)
    for z0 in starts:
        r = minimize(lambda z: -obj(a, z), z0, method="SLSQP", bounds=bnds, constraints=cons,
                     options={"ftol": 1e-13, "maxiter": 500})
        if r.success or True:
            v = obj(a, r.x)
            if np.isfinite(v) and v > best[0] and np.all(diag(a, r.x[:5]) > -1e-9):
                best = (v, r.x)
    return best


def naive(a):
    return inner_max(a, lambda a, x: L(a, x))


def case1(a):
    return inner_max(a, obj_case1)


A = np.zeros((5, 5))
for i in range(5):
    for j in range(5):
        if (j - i) % 5 in (0, 2, 3):
            A[i, j] = 1


def scale_t(a, iters=20000, tol=1e-15):
    """t with t_i (A t)_i / (t^T A t) = a_i (max-entropy blue type with rows a)."""
    t = np.sqrt(np.maximum(a, 1e-300))
    for _ in range(iters):
        At = A @ t
        tn = np.where(a > 0, a / At, 0.0)
        tn = np.sqrt(tn * t)  # damped
        tn /= tn.sum()
        if np.max(np.abs(tn - t)) < tol:
            t = tn; break
        t = tn
    return t


def U_t(a, t):
    Z = t @ A @ t
    return 9 * xlogx(a).sum() - 10 * np.sum(np.where(a > 0, a * np.log(np.where(t > 0, t, 1)), 0)) + 5 * np.log(Z)


def naive_exact(a):
    t = scale_t(a)
    Q = A * np.outer(t, t) / (t @ A @ t)
    return U_t(a, t), t, Q


def scale_ts(a, s, iters=40000, tol=1e-15):
    As = A.copy(); As[0, 3] = As[3, 0] = s
    t = np.sqrt(np.maximum(a, 1e-300))
    for _ in range(iters):
        tn = np.where(a > 0, a / (As @ t), 0.0)
        tn = np.sqrt(tn * t); tn /= tn.sum()
        if np.max(np.abs(tn - t)) < tol:
            t = tn; break
        t = tn
    Q = As * np.outer(t, t) / (t @ As @ t)
    return Q


def L_Q(a, Q):
    return 9 * xlogx(a).sum() - 5 * xlogx(Q).sum()


def case1_exact(a):
    """max over Q of L + a0 log f(Q03/a0): concave in Q; optimum is in the s-tilted family. 1-D search in log s."""
    from scipy.optimize import minimize_scalar
    def g(ls):
        Q = scale_ts(a, np.exp(ls))
        return -(L_Q(a, Q) + a[0] * np.log(f(min(1.0, Q[0, 3] / a[0]))))
    r = minimize_scalar(g, bounds=(-3, 6), method="bounded", options={"xatol": 1e-9})
    Q = scale_ts(a, np.exp(r.x))
    return -r.fun, np.exp(r.x), Q


def scale_ts_t(a, s, iters=40000, tol=1e-15):
    As = A.copy(); As[0, 3] = As[3, 0] = s
    t = np.sqrt(np.maximum(a, 1e-300))
    for _ in range(iters):
        tn = np.where(a > 0, a / (As @ t), 0.0)
        tn = np.sqrt(tn * t); tn /= tn.sum()
        if np.max(np.abs(tn - t)) < tol:
            t = tn; break
        t = tn
    return t
