"""Produce 180-bit Arb profile-cover certificates for the (9, 10)-bidegree model at c = 99/20 = 4.95."""

import argparse
from fractions import Fraction
import gzip
import itertools
import json
import math
from pathlib import Path
import resource
import time

from flint import arb, ctx
import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import xlogy

ctx.prec = 180

GRID = 10_000 * 2**20
CAP = 4_001 * 2**20
GAP = GRID * 3 // 20  # exact 3/20
SCALE = 10**12
CLAIM = 1_500_000_000  # target rate <= -3/2000 = -0.0015
N0 = 450_000

# Exact rational endpoints for alpha_9(n) = 2*ceil(n/20)/n over all integers n >= N0:
# alpha_9(n) in [1/10, 1/10 + 19/(10*N0)]
ALPHA9_LO_FRAC = Fraction(1, 10)
ALPHA9_HI_FRAC = Fraction(1, 10) + Fraction(19, 10 * N0)
THETA_LO_FRAC = 1 - ALPHA9_HI_FRAC
THETA_HI_FRAC = 1 - ALPHA9_LO_FRAC
DBAR_LO_FRAC = 10 - ALPHA9_HI_FRAC
DBAR_HI_FRAC = 10 - ALPHA9_LO_FRAC  # 99/10

ALPHA9_LO_F = float(ALPHA9_LO_FRAC)
ALPHA9_HI_F = float(ALPHA9_HI_FRAC)
DBAR_LO_F = float(DBAR_LO_FRAC)
DBAR_HI_F = float(DBAR_HI_FRAC)

ALLOWED = np.array([[(j - i) % 5 in (0, 2, 3) for j in range(5)] for i in range(5)], dtype=float)
BLUE = tuple((i, j) for i in range(5) for j in range(5) if (j - i) % 5 in (0, 2, 3))
CORNERS = list(itertools.product((0, 1), repeat=4))
VERTEX_SELECTORS = [
    (i, [j for j in range(5) if i != j], np.array(CORNERS).T)
    for i in range(5)
]


def arb_frac(fr: Fraction) -> arb:
    return arb(fr.numerator) / arb(fr.denominator)


ALPHA9_IV = arb_frac(ALPHA9_LO_FRAC).union(arb_frac(ALPHA9_HI_FRAC))
THETA_IV = arb(1) - ALPHA9_IV
DBAR_IV = arb(10) - ALPHA9_IV
ALPHA9_HI_ARB = arb_frac(ALPHA9_HI_FRAC)
THETA_HI_ARB = arb_frac(THETA_HI_FRAC)
DBAR_LO_ARB = arb_frac(DBAR_LO_FRAC)
DBAR_HI_ARB = arb_frac(DBAR_HI_FRAC)


def arb_ent(x: arb) -> arb:
    if x.is_zero():
        return arb(0)
    return x * x.log()


# Precompute alpha_9*log(alpha_9) + theta*log(theta) enclosure on ALPHA9_IV:
# Note x -> x log x + (1-x) log(1-x) is strictly decreasing on (0, 1/2), so max on [lo, hi] <= 0.5 is at lo!
# Evaluating directly in Arb on ALPHA9_IV also encloses it tightly; let's use direct Arb evaluation so verifier is 1-line!
SPLIT_ENT_IV = ALPHA9_IV * ALPHA9_IV.log() + THETA_IV * THETA_IV.log()


def narrow(lo, hi, order):
    lo, hi = list(lo), list(hi)
    if order == "a":
        relations = [(0, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)]
    else:
        relations = [(j, k, 0) for j in (0, 2) for k in (1, 3, 4)] + [(3, 4, 0)]
        if order == "c":
            relations += [(0, 3, GAP), (2, 3, GAP)]
    for _ in range(3):
        for j, k, gap in relations:
            lo[j] = max(lo[j], lo[k] + gap)
            hi[k] = min(hi[k], hi[j] - gap)
        for j in range(5):
            lo[j] = max(lo[j], GRID - sum(hi[k] for k in range(5) if j != k))
            hi[j] = min(hi[j], GRID - sum(lo[k] for k in range(5) if j != k))
        if any(a > b for a, b in zip(lo, hi)) or sum(lo) > GRID or sum(hi) < GRID:
            return None
    if order == "b" and min(lo[0], lo[2]) - hi[3] > GAP:
        return None
    return lo, hi


def vertices(lo, hi):
    lo_a, hi_a = np.array(lo), np.array(hi)
    out = []
    for free, fixed, patterns in VERTEX_SELECTORS:
        block = np.empty((5, 16), dtype=np.int64)
        block[fixed] = np.where(patterns, hi_a[fixed, None], lo_a[fixed, None])
        block[free] = GRID - block[fixed].sum(axis=0)
        out.append(block[:, (lo_a[free] <= block[free]) & (block[free] <= hi_a[free])].T)
    return np.unique(np.concatenate(out), axis=0)


def solve_naive_point(a):
    """Fast saddlepoint (t, eta) for naive bidegree rate at profile a."""
    a = np.maximum(a, 1e-12)
    a /= a.sum()
    alpha9 = 0.5 * (ALPHA9_LO_F + ALPHA9_HI_F)
    d_bar = 10.0 - alpha9
    a9 = alpha9 * a
    t = np.sqrt(a)
    eta = 0.0
    for _ in range(12):
        s_tilde = (9.0 * a9 + 10.0 * (a - a9)) / d_bar
        # 6 Newton steps for Sinkhorn scaling ALLOWED * t_i * t_j
        u = np.maximum(t, 1e-15)
        for _ in range(8):
            mu = ALLOWED @ u
            f = u * mu - s_tilde
            if np.max(np.abs(f)) < 1e-12:
                break
            J = np.diag(mu) + u[:, None] * ALLOWED
            du = np.linalg.solve(J, f)
            step = 1.0
            while np.min(u - step * du) <= 0:
                step *= 0.5
            u = u - step * du
        t = u

        def sum_xi(e_val):
            lk = np.clip(np.log(d_bar * t / a) + e_val - 1.0, -200.0, 200.0)
            k = np.exp(lk)
            y = 18.0 / ((8.0 + k) + np.sqrt((8.0 + k) ** 2 + 36.0))
            return float(np.dot(a, 1.0 - y)) - alpha9

        eta = brentq(sum_xi, -150.0, 150.0, xtol=1e-10)
        lk = np.clip(np.log(d_bar * t / a) + eta - 1.0, -200.0, 200.0)
        k = np.exp(lk)
        y = 18.0 / ((8.0 + k) + np.sqrt((8.0 + k) ** 2 + 36.0))
        new_a9 = a * (1.0 - y)
        if np.max(np.abs(new_a9 - a9)) < 1e-10:
            break
        a9 = new_a9
    # Normalize t so geometric mean or max is ~1
    t = t / np.max(t)
    # Adjust eta since kappa_i uses t_i * exp(eta - 1): scaling t by 1/c shifts eta by +log(c)!
    # Recompute exact eta for normalized t:
    def sum_xi_norm(e_val):
        lk = np.clip(np.log(d_bar * t / a) + e_val - 1.0, -200.0, 200.0)
        k = np.exp(lk)
        y = 18.0 / ((8.0 + k) + np.sqrt((8.0 + k) ** 2 + 36.0))
        return float(np.dot(a, 1.0 - y)) - alpha9

    eta = brentq(sum_xi_norm, -150.0, 150.0, xtol=1e-11)
    t_int = [max(1, round(float(val) * SCALE)) for val in t]
    eta_int = round(float(eta) * SCALE)
    return t_int, eta_int


def eval_U_float_vertices(verts_f, t, eta, s03=1.0, s02=1.0, lin0=0.0, lin2=0.0):
    """Evaluate max over vertices and alpha9 endpoints in float."""
    S_mat = np.ones((5, 5))
    S_mat[0, 3] = S_mat[3, 0] = s03
    S_mat[0, 2] = S_mat[2, 0] = s02
    W = ALLOWED * (t[:, None] * t) * S_mat
    Z = float(np.sum(W))
    logZ = math.log(Z)
    worst = -1e9
    for alpha9 in (ALPHA9_LO_F, ALPHA9_HI_F):
        theta = 1.0 - alpha9
        d_bar = 10.0 - alpha9
        c0 = xlogy(alpha9, alpha9) + xlogy(theta, theta) + 0.5 * d_bar * logZ - eta * alpha9
        # Vectorized over (N_verts, 5)
        pos = verts_f > 0
        vals = np.full(len(verts_f), c0)
        for i in range(5):
            vi = verts_f[:, i]
            m = vi > 0
            if not np.any(m):
                continue
            vm = vi[m]
            lk = np.clip(np.log(d_bar * t[i] / vm) + eta - 1.0, -250.0, 250.0)
            k = np.exp(lk)
            r = np.sqrt((8.0 + k) ** 2 + 36.0)
            y = 18.0 / ((8.0 + k) + r)
            xi = 2.0 * k / ((10.0 + k) + r)
            vals[m] += vm * (9.0 * np.log(vm) - 10.0 * math.log(d_bar * t[i]) + 10.0 * np.log(9.0 + y) - np.log(y) + xi)
        if lin0 != 0.0:
            vals += verts_f[:, 0] * lin0
        if lin2 != 0.0:
            vals += verts_f[:, 2] * lin2
        worst = max(worst, float(np.max(vals)))
    return worst, W / Z


def arb_eval_vertices(verts, t_int, eta_int, s03=None, s02=None, lin0=None, lin2=None):
    """Rigorous 180-bit Arb upper bound over all vertices on ALPHA9_IV."""
    t = [arb(x) / SCALE for x in t_int]
    eta = arb(eta_int) / SCALE
    exp_eta_m1 = (eta - 1).exp()
    z = arb(0)
    for i, j in BLUE:
        term = t[i] * t[j]
        if s03 is not None and ((i == 0 and j == 3) or (i == 3 and j == 0)):
            term = term * s03
        elif s02 is not None and ((i == 0 and j == 2) or (i == 2 and j == 0)):
            term = term * s02
        z += term
    const_base = SPLIT_ENT_IV + (DBAR_IV / 2) * z.log() - eta * ALPHA9_IV
    c_ti = [-10 * (DBAR_IV * ti).log() for ti in t]
    cache = {}

    def f_term(i, x_int):
        if x_int == 0:
            return arb(0)
        key = (i, x_int)
        if key not in cache:
            a_i = arb(x_int) / GRID
            kappa = (DBAR_IV * t[i] * exp_eta_m1) / a_i
            rad = ((8 + kappa) ** 2 + 36).sqrt()
            y = arb(18) / ((8 + kappa) + rad)
            xi = (2 * kappa) / ((10 + kappa) + rad)
            val = a_i * (9 * a_i.log() + c_ti[i] + 10 * (9 + y).log() - y.log() + xi)
            if i == 0 and lin0 is not None:
                val += a_i * lin0
            elif i == 2 and lin2 is not None:
                val += a_i * lin2
            cache[key] = val
        return cache[key]

    max_ub = arb(-1000)
    for v in verts:
        tot = const_base
        for i in range(5):
            tot += f_term(i, int(v[i]))
        max_ub = max_ub.max(tot.upper())
    return max_ub, t, z


def rho_float(a_lo_int):
    a_lo = a_lo_int / GRID
    if a_lo <= ALPHA9_HI_F:
        return 1.0 / 9.0
    return a_lo / (10.0 * a_lo - ALPHA9_HI_F)


def rho_arb(a_lo_int):
    a_lo_fr = Fraction(a_lo_int, GRID)
    if a_lo_fr <= ALPHA9_HI_FRAC:
        return arb(1) / arb(9)
    a_lo = arb(a_lo_int) / GRID
    return a_lo / (10 * a_lo - ALPHA9_HI_ARB)


def try_case1(boxlo, boxhi, verts, verts_f):
    """Optimize 1D-concave product parameters (t, eta, u1, u2, u3) for Case I on box."""
    if boxlo[0] <= 0 or boxlo[2] <= 0:
        return None
    r0 = rho_float(boxlo[0])
    r2 = rho_float(boxlo[2])
    a_mid = verts_f.mean(axis=0)
    a_mid /= a_mid.sum()
    t_init_int, eta_init_int = solve_naive_point(a_mid)
    t0 = np.array(t_init_int, dtype=float) / SCALE
    lt_init = np.log(np.maximum(t0 / t0[0], 1e-12))[1:]
    eta0 = eta_init_int / SCALE

    # Fast optimization at centroid a_mid first!
    a_mid_2d = a_mid[None, :]

    def mid_obj(p):
        t = np.exp([0.0, p[0], p[1], p[2], p[3]])
        eta = p[4]
        u1 = 1.0 / (1.0 + math.exp(-np.clip(p[5], -20, 20)))
        u2 = 1.0 / (1.0 + math.exp(-np.clip(p[6], -20, 20)))
        u3 = 1.0 / (1.0 + math.exp(-np.clip(p[7], -20, 20)))

        def fg(u):
            f = 1.0 - (1.0 - u) ** 10
            b = 10.0 * ((1.0 - u) ** 9) / f
            return math.log(f) - b * u, b

        g1, b1 = fg(u1)
        g2, b2 = fg(u2)
        g3, b3 = fg(u3)
        s03 = math.exp(min(50.0, r0 * b1))
        s02 = math.exp(min(50.0, r0 * b2 + r2 * b3))
        val, _ = eval_U_float_vertices(a_mid_2d, t, eta, s03=s03, s02=s02, lin0=g1 + g2, lin2=g3)
        return val

    res = minimize(mid_obj, [*lt_init, eta0, -1.5, -0.2, -0.2], method="BFGS", options={"gtol": 1e-5, "maxiter": 35})
    p = res.x
    if res.fun > -CLAIM / SCALE + 5e-4:
        return None

    # Evaluate on actual box vertices!
    def box_obj(q):
        t = np.exp([0.0, q[0], q[1], q[2], q[3]])
        eta = q[4]
        u1 = 1.0 / (1.0 + math.exp(-np.clip(q[5], -20, 20)))
        u2 = 1.0 / (1.0 + math.exp(-np.clip(q[6], -20, 20)))
        u3 = 1.0 / (1.0 + math.exp(-np.clip(q[7], -20, 20)))

        def fg(u):
            f = 1.0 - (1.0 - u) ** 10
            b = 10.0 * ((1.0 - u) ** 9) / f
            return math.log(f) - b * u, b

        g1, b1 = fg(u1)
        g2, b2 = fg(u2)
        g3, b3 = fg(u3)
        s03 = math.exp(min(50.0, r0 * b1))
        s02 = math.exp(min(50.0, r0 * b2 + r2 * b3))
        val, _ = eval_U_float_vertices(verts_f, t, eta, s03=s03, s02=s02, lin0=g1 + g2, lin2=g3)
        return val

    bval = box_obj(p)
    if bval > -CLAIM / SCALE - 2e-4 and bval < -CLAIM / SCALE + 5e-4:
        res2 = minimize(box_obj, p, method="Nelder-Mead", options={"maxiter": 80, "fatol": 1e-5})
        p, bval = res2.x, float(res2.fun)
    if bval > -CLAIM / SCALE - 1.2e-4:
        return None

    t_raw = np.exp([0.0, p[0], p[1], p[2], p[3]])
    c_scale = float(np.max(t_raw))
    t_norm = t_raw / c_scale
    eta_norm = p[4] + math.log(c_scale)
    t_int = [max(1, round(float(v) * SCALE)) for v in t_norm]
    eta_int = round(float(eta_norm) * SCALE)
    u_ints = [min(SCALE - 1, max(1, round((1.0 / (1.0 + math.exp(-float(p[k])))) * SCALE))) for k in (5, 6, 7)]

    # Verify in 180-bit Arb!
    r0_a = rho_arb(boxlo[0])
    r2_a = rho_arb(boxlo[2])
    bgs = []
    for ui in u_ints:
        u_a = arb(ui) / SCALE
        f_a = 1 - (1 - u_a) ** 10
        b_a = 10 * ((1 - u_a) ** 9) / f_a
        g_a = f_a.log() - b_a * u_a
        if not (b_a > 0 and g_a < 0):
            return None
        bgs.append((b_a, g_a))
    (b1_a, g1_a), (b2_a, g2_a), (b3_a, g3_a) = bgs
    s03_a = (r0_a * b1_a).exp()
    s02_a = (r0_a * b2_a + r2_a * b3_a).exp()
    if not (s03_a > 1 and s02_a > 1):
        return None
    max_ub, _, _ = arb_eval_vertices(verts, t_int, eta_int, s03=s03_a, s02=s02_a, lin0=g1_a + g2_a, lin2=g3_a)
    if max_ub <= arb(-CLAIM) / SCALE:
        return ["C1", t_int, eta_int, u_ints, -CLAIM]
    return None


def binary_kl_f(x, b):
    return float(xlogy(x, x / b) + xlogy(1.0 - x, (1.0 - x) / (1.0 - b)))


def upper_limit_f(two_b, budget):
    if binary_kl_f(1.0, two_b) <= budget:
        return 1.0
    return brentq(lambda x: binary_kl_f(x, two_b) - budget, two_b, 1.0, xtol=1e-14)


def q_cap_frac(hi_i_int, hi_j_int):
    s_i = min(Fraction(10 * hi_i_int, GRID), Fraction(9 * hi_i_int, GRID) + THETA_HI_FRAC)
    s_j = min(Fraction(10 * hi_j_int, GRID), Fraction(9 * hi_j_int, GRID) + THETA_HI_FRAC)
    return min(s_i, s_j) / DBAR_LO_FRAC


def kl1d_min_f(lo_q, hi_q, b_ij):
    if lo_q <= b_ij <= hi_q:
        return 0.0
    two_q = 2.0 * hi_q if hi_q < b_ij else 2.0 * lo_q
    two_q = min(1.0 - 1e-15, max(1e-15, two_q))
    return binary_kl_f(two_q, 2.0 * b_ij)


def arb_kl_cell_lb(lo_num: int, hi_num: int, denom: int, two_b: arb) -> arb:
    """Rigorous lower bound on D(2*Q, 2*B) for Q in [lo_num/denom, hi_num/denom]."""
    two_lo = arb(2 * lo_num) / arb(denom)
    two_hi = arb(2 * hi_num) / arb(denom)
    if two_lo > two_b and two_lo <= 1:
        comp = 1 - two_lo
        val = arb_ent(two_lo) + arb_ent(comp) - two_lo * two_b.log() - comp * (1 - two_b).log()
        return val if val > 0 else arb(0)
    if two_hi < two_b and two_hi >= 0:
        comp = 1 - two_hi
        val = arb_ent(two_hi) + arb_ent(comp) - two_hi * two_b.log() - comp * (1 - two_b).log()
        return val if val > 0 else arb(0)
    return arb(0)


def try_case2(boxlo, boxhi, verts, t_int, eta_int, raw_int, B_f):
    if boxlo[0] <= 0 or boxlo[2] <= 0:
        return None
    upper_f = raw_int / SCALE
    # Use generous tail budget so h02, h24 easily clear the far tails, while 8x8 KL+M10 handles [0, h02] x [0, h24]!
    budget = max(1e-7, (upper_f + CLAIM / SCALE + 5e-4) / (0.5 * DBAR_LO_F))
    cap02_int = math.ceil(float(q_cap_frac(boxhi[0], boxhi[2])) * GRID)
    cap24_int = math.ceil(float(q_cap_frac(boxhi[2], boxhi[4])) * GRID)

    h02_int = max(1, min(cap02_int, math.ceil(GRID * upper_limit_f(2.0 * B_f[0, 2], budget) / 2.0)))
    h24_int = max(1, min(cap24_int, math.ceil(GRID * upper_limit_f(2.0 * B_f[2, 4], budget) / 2.0)))

    s2_min_fr = max(Fraction(9 * boxlo[2], GRID), Fraction(10 * boxlo[2], GRID) - ALPHA9_HI_FRAC)
    s2_min_f = float(s2_min_fr)
    r0_f = rho_float(boxlo[0])
    a0_lo_f = boxlo[0] / GRID
    a2_lo_f = boxlo[2] / GRID
    a2_hi_f = boxhi[2] / GRID

    g02 = np.linspace(0.0, h02_int / GRID, 9)
    g24 = np.linspace(0.0, h24_int / GRID, 9)
    kl02_arr = np.array([kl1d_min_f(g02[i], g02[i + 1], B_f[0, 2]) for i in range(8)])
    kl24_arr = np.array([kl1d_min_f(g24[j], g24[j + 1], B_f[2, 4]) for j in range(8)])
    kl_pen_mat = 0.5 * DBAR_LO_F * np.maximum(kl02_arr[:, None], kl24_arr[None, :])
    q0_hi_arr = np.minimum(1.0, (DBAR_HI_F * g02[1:]) / s2_min_f)[:, None]
    q4_hi_arr = np.minimum(1.0, (DBAR_HI_F * g24[1:]) / s2_min_f)[None, :]

    def occ_f(u):
        f = 1.0 - (1.0 - u) ** 10
        b = 10.0 * ((1.0 - u) ** 9) / f
        g = math.log(f) - b * u
        w = math.exp(min(40.0, b * r0_f))
        m_vals = ((1.0 + (w - 1.0) * q0_hi_arr) ** 10
                  - (1.0 - q4_hi_arr + (w - 1.0) * q0_hi_arr) ** 10
                  + (1.0 - q4_hi_arr) ** 10
                  - (1.0 - q0_hi_arr) ** 10)
        log_m = np.log(np.maximum(m_vals, 1e-300))
        a2_term = np.maximum(a2_lo_f * log_m, a2_hi_f * log_m)
        return float(a0_lo_f * g + np.max(-kl_pen_mat + a2_term))

    fit = minimize_scalar(occ_f, bounds=(0.03, 0.90), method="bounded")
    if upper_f + float(fit.fun) > -CLAIM / SCALE - 1e-6:
        return None
    u_int = min(SCALE - 1, max(1, round(float(fit.x) * SCALE)))

    # Verify in 180-bit Arb!
    max_ub, t_a, z_a = arb_eval_vertices(verts, t_int, eta_int)
    upper_a = arb(raw_int) / SCALE
    if not (max_ub <= upper_a):
        return None

    limit_a = arb(-CLAIM) / SCALE
    for i, j, h_int in ((0, 2, h02_int), (2, 4, h24_int)):
        if Fraction(h_int, GRID) < q_cap_frac(boxhi[i], boxhi[j]):
            th = 2 * arb(h_int) / GRID
            prob = 2 * t_a[i] * t_a[j] / z_a
            if not (th > prob and th <= 1):
                return None
            comp = 1 - th
            div = arb_ent(th) + arb_ent(comp) - th * prob.log() - comp * (1 - prob).log()
            if not (upper_a - (DBAR_LO_ARB / 2) * div <= limit_a):
                return None

    s2_min_a = arb_frac(s2_min_fr)
    u_a = arb(u_int) / SCALE
    f_a = 1 - (1 - u_a) ** 10
    b_a = 10 * ((1 - u_a) ** 9) / f_a
    g_a = f_a.log() - b_a * u_a
    if not (b_a > 0 and g_a < 0):
        return None
    r0_a = rho_arb(boxlo[0])
    w_a = (b_a * r0_a).exp()
    a0_a = arb(boxlo[0]) / GRID
    a2_iv = (arb(boxlo[2]) / GRID).union(arb(boxhi[2]) / GRID)
    two_b02 = 2 * t_a[0] * t_a[2] / z_a
    two_b24 = 2 * t_a[2] * t_a[4] / z_a

    kl02_a = [arb_kl_cell_lb(i * h02_int, (i + 1) * h02_int, 8 * GRID, two_b02) for i in range(8)]
    kl24_a = [arb_kl_cell_lb(j * h24_int, (j + 1) * h24_int, 8 * GRID, two_b24) for j in range(8)]
    q0_hi_a = []
    for i in range(8):
        q_fr = DBAR_HI_FRAC * Fraction((i + 1) * h02_int, 8 * GRID)
        q0_hi_a.append(arb(1) if q_fr >= s2_min_fr else (DBAR_HI_ARB * arb((i + 1) * h02_int) / arb(8 * GRID)) / s2_min_a)
    q4_hi_a = []
    for j in range(8):
        q_fr = DBAR_HI_FRAC * Fraction((j + 1) * h24_int, 8 * GRID)
        q4_hi_a.append(arb(1) if q_fr >= s2_min_fr else (DBAR_HI_ARB * arb((j + 1) * h24_int) / arb(8 * GRID)) / s2_min_a)

    for i in range(8):
        q0_c = q0_hi_a[i]
        for j in range(8):
            q4_c = q4_hi_a[j]
            m_val = ((1 + (w_a - 1) * q0_c) ** 10
                     - (1 - q4_c + (w_a - 1) * q0_c) ** 10
                     + (1 - q4_c) ** 10
                     - (1 - q0_c) ** 10)
            if not (m_val > 0):
                return None
            base_02 = upper_a - (DBAR_LO_ARB / 2) * kl02_a[i]
            base_24 = upper_a - (DBAR_LO_ARB / 2) * kl24_a[j]
            base_cell = base_02 if base_02.upper() <= base_24.upper() else base_24
            cell_rate = base_cell + a0_a * g_a + a2_iv * m_val.log()
            if not (cell_rate <= limit_a):
                return None
    return ["C2", t_int, eta_int, raw_int, [h02_int, h24_int, u_int], -CLAIM]
    return None


def build(case, out_dir: Path, max_seconds=1200):
    start = time.monotonic()
    deadline = start + max_seconds
    records = []
    totals = {"split": 0, "empty": 0, "naive": 0, "occupancy": 0}

    def visit(lo, hi, depth):
        if time.monotonic() >= deadline:
            raise TimeoutError((case, depth, totals))
        if depth > 110:
            raise ArithmeticError((case, "depth", lo, hi, totals))
        if case == "naive_ab":
            boxes = [box for order in ("a", "b") if (box := narrow(lo, hi, order))]
        else:
            box = narrow(lo, hi, "c")
            boxes = [box] if box else []
        if not boxes:
            records.append(["X"])
            totals["empty"] += 1
            return

        boxlo = [min(b[0][i] for b in boxes) for i in range(5)]
        boxhi = [max(b[1][i] for b in boxes) for i in range(5)]
        verts = vertices(boxlo, boxhi)
        verts_f = verts / GRID

        # 1. Try Naive leaf
        a_mid = verts_f.mean(axis=0)
        t_int, eta_int = solve_naive_point(a_mid)
        t_f = np.array(t_int, dtype=float) / SCALE
        rate_f, B_f = eval_U_float_vertices(verts_f, t_f, eta_int / SCALE)
        raw_est = math.ceil((rate_f + 2e-4) * SCALE)
        if rate_f <= -CLAIM / SCALE + 1e-4:
            max_ub, _, _ = arb_eval_vertices(verts, t_int, eta_int)
            if max_ub <= arb(-CLAIM) / SCALE:
                # Extract exact ceiling integer of max_ub * SCALE in Arb with +10 safety margin:
                scaled_ub = (max_ub * SCALE).ceil()
                base_raw = int(scaled_ub.unique_fmpz()) if scaled_ub.unique_fmpz() is not None else math.ceil(float(max_ub) * SCALE)
                raw_int = min(-CLAIM, base_raw + 10)
                if max_ub <= arb(raw_int) / SCALE and raw_int <= -CLAIM:
                    records.append(["N", t_int, eta_int, raw_int, -CLAIM])
                    totals["naive"] += 1
                    return

        # 2. Try Kempe-swap occupancy leaf
        if case == "case1" and raw_est < int(0.06 * SCALE):
            rec = try_case1(boxlo, boxhi, verts, verts_f)
            if rec is not None:
                records.append(rec)
                totals["occupancy"] += 1
                return
        elif case == "case2" and raw_est < int(0.06 * SCALE):
            max_ub, _, _ = arb_eval_vertices(verts, t_int, eta_int)
            ub_ceil = (max_ub * SCALE).ceil()
            raw_int = (int(ub_ceil.unique_fmpz()) if ub_ceil.unique_fmpz() is not None else math.ceil(float(max_ub) * SCALE)) + 10
            while not (max_ub <= arb(raw_int) / SCALE):
                raw_int += 10
            rec = try_case2(boxlo, boxhi, verts, t_int, eta_int, raw_int, B_f)
            if rec is not None:
                records.append(rec)
                totals["occupancy"] += 1
                return

        # 3. Split widest tightened coordinate
        widths = [boxhi[i] - boxlo[i] for i in range(5)]
        j = widths.index(max(widths))
        cut = (boxlo[j] + boxhi[j]) // 2
        if not lo[j] < cut < hi[j]:
            raise ArithmeticError(("inconclusive", case, lo, hi, rate_f))
        records.append(["S", j, cut])
        totals["split"] += 1
        if totals["split"] % 2048 == 0:
            print(case, "checkpoint", totals, "elapsed", round(time.monotonic() - start, 2), flush=True)
        upper = list(hi)
        upper[j] = cut
        visit(lo, upper, depth + 1)
        lower = list(lo)
        lower[j] = cut
        visit(lower, hi, depth + 1)

    visit([0] * 5, [CAP] * 5, 0)
    elapsed = round(time.monotonic() - start, 3)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    stats = dict(totals, elapsed_seconds=elapsed, peak_rss_bytes=rss)
    print(case, stats, flush=True)

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = {
        "format": 3,
        "model": "bidegree_9_10",
        "c_num": 99,
        "c_den": 20,
        "n0": N0,
        "case": case,
        "root": [[0] * 5, [CAP] * 5],
        "grid": GRID,
        "tilt_scale": SCALE,
        "claim": -CLAIM,
        "records": records,
    }
    out_path = out_dir / f"cert_{case}.json.gz"
    with gzip.GzipFile(out_path, "wb", mtime=0) as f:
        f.write((json.dumps(doc, separators=(",", ":")) + "\n").encode())
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["naive_ab", "case1", "case2", "all"], default="all", nargs="?")
    parser.add_argument("--out-dir", type=Path, default=Path("certificates"))
    parser.add_argument("--seconds", type=int, default=1200)
    args = parser.parse_args()
    t0 = time.monotonic()
    cases = ("naive_ab", "case1", "case2") if args.case == "all" else (args.case,)
    all_stats = {}
    for c in cases:
        all_stats[c] = build(c, args.out_dir, max_seconds=args.seconds - (time.monotonic() - t0))
    (args.out_dir / "producer_stats.json").write_text(json.dumps(all_stats, indent=2) + "\n")
