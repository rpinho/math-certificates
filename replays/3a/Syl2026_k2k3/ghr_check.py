#!/usr/bin/env python3
"""Own checker (Python standard library only) for the C_3a lower bound
   theta = 1 + log(|V-V|/|V+V|) / log(2 max V + 1),  V = 2U,
for the controlled-carry block construction with a cost histogram.

Inputs from the constant page (3a): generators, B, q, k, x (dyadic), ell.
Data input: cost histogram (cost<TAB>multiplicity) = multiplicities of c_k(r)
over r in Z/q^k Z.  Everything else is recomputed here.

Bounds used (stated in the claimant's prose note; checked by brute force on
a toy instance in toy_test.py):
   |U-U| >= ell! / (N_0! prod_{r!=0,h} N_r!)
   |U+U| <= x^{-C} P(x)^{k ell},   P(x) = sum_{s in M+M} x^s
   2 max V + 1 <= 4 B q^{k ell}/(q-1) + 1
Rigour: decimal arithmetic at 120 digits; every transcendental value is
widened by a relative 1e-80 before use; ln n! uses Robbins' bounds.
"""
import sys, json, hashlib, time
from decimal import Decimal as D, getcontext
getcontext().prec = 120
PAD = D(10) ** -80


def pi_dec():
    prec = 140
    one = 10 ** prec
    def atan_inv(n):
        x = one // n; s = x; n2 = n * n; i = 1; sign = -1
        while x:
            x //= n2; i += 2
            s += sign * (x // i); sign = -sign
        return s
    p = 16 * atan_inv(5) - 4 * atan_inv(239)
    return D(p) / D(one)

PI = pi_dec()


def lo(v): return v * (1 - PAD) if v > 0 else v * (1 + PAD)
def hi(v): return v * (1 + PAD) if v > 0 else v * (1 - PAD)


def semigroup_mask(gens, B):
    ok = [False] * (B + 1); ok[0] = True
    for n in range(1, B + 1):
        for g in gens:
            if n >= g and ok[n - g]:
                ok[n] = True; break
    return [n for n in range(B + 1) if ok[n]]


def lnfact_bounds(n):
    """(lower, upper) for ln n!; Robbins: sqrt(2 pi n)(n/e)^n e^{1/(12n+1)} < n! < sqrt(2 pi n)(n/e)^n e^{1/(12n)}"""
    if n < 2:
        return D(0), D(0)
    N = D(n)
    base = (D(2) * PI * N).ln() / 2 + N * N.ln() - N
    return base + D(1) / (12 * N + 1) - PAD * abs(base), base + D(1) / (12 * N) + PAD * abs(base)


def read_hist(path):
    h = []
    for line in open(path):
        if line.startswith('#') or not line.strip():
            continue
        c, m = line.split(); h.append((int(c), int(m)))
    return h


def run(gens, B, q, k, xnum, xexp, ell, histpath, c_h, claim=None, x_dec=None):
    t0 = time.time()
    out = {}
    M = semigroup_mask(gens, B)
    MM = sorted({a + b for a in M for b in M})
    out['|M|'] = len(M); out['|M+M|'] = len(MM)
    Q = q ** k
    hist = read_hist(histpath)
    out['hist_sha256'] = hashlib.sha256(open(histpath, 'rb').read()).hexdigest()
    out['distinct_costs'] = len(hist)
    assert sum(m for _, m in hist) == Q
    assert sorted(c for c, m in hist if m % 2) == sorted([0] if c_h is None else [0, c_h]), 'odd classes'
    out['sum_multiplicities_equals_Q'] = True
    x = x_dec if x_dec is not None else D(xnum) / D(2) ** xexp          # exact
    pw = {c: x ** c for c, _ in hist}
    Z = sum(m * pw[c] for c, m in hist)
    out['Z'] = str(Z)[:40]
    Nc = {}; margin_min = D(1)
    for c, m in hist:
        if c == 0: continue
        v = ell * pw[c] / Z
        f = int(v); frac = v - f
        dist = min(frac, 1 - frac)
        if dist < D(10) ** -40: raise SystemExit('floor not robust at cost %d' % c)
        margin_min = min(margin_min, dist); Nc[c] = f
    out['min_floor_margin'] = str(margin_min)[:12]
    msz = {c: m - (1 if c == c_h else 0) for c, m in hist if c != 0}
    n0 = ell - sum(msz[c] * Nc[c] for c in Nc)
    assert n0 >= 0
    C = sum(msz[c] * Nc[c] * c for c in Nc)
    assert C % 2 == 0
    out['n0'] = n0; out['C'] = C
    out['min_Nc'] = min(Nc.values())
    lnl, _ = lnfact_bounds(ell)
    _, un0 = lnfact_bounds(n0)
    acc = sum(msz[c] * lnfact_bounds(Nc[c])[1] for c in Nc)
    logM_lo = lnl - un0 - acc * (1 + PAD)
    P = sum(x ** s for s in MM)
    P_hi = P * (1 + PAD)
    xl = x.ln()
    logS_hi = D(k) * ell * P_hi.ln() * (1 + PAD) + (-C * xl) * (1 + PAD)
    logDen_hi = (D(k) * ell * D(q).ln() + (D(4 * B) / D(q - 1)).ln()) * (1 + PAD) + D(10) ** -30
    num_lo = logM_lo - logS_hi
    out['numerator_positive'] = num_lo > 0
    theta_lo = 1 + num_lo * (1 - PAD) / logDen_hi
    out['logM_lo'] = str(logM_lo)[:50]; out['logS_hi'] = str(logS_hi)[:50]
    out['logDen_hi'] = str(logDen_hi)[:50]
    out['P_hi'] = str(P_hi)[:30]
    out['theta_lo'] = str(theta_lo)[:40]
    out['theta_infinity_info'] = str(1 + (Z.ln() / k - P.ln()) / D(q).ln())[:25]
    if claim is not None:
        out['claim'] = claim
        out['PASS'] = bool(theta_lo > D(claim))
    out['runtime_s'] = round(time.time() - t0, 1)
    return out


if __name__ == '__main__':
    inst, base = sys.argv[1], sys.argv[2]
    G = [1971, 2016, 2100, 2628, 2688, 2800]
    if inst == 'k2':
        r = run(G, 26972, 27022, 2, 9004870224628742, 53, 10 ** 18, base + '/data/k2_cost_hist.tsv', 24367, '1.19281555')
    else:
        r = run(G, 26972, 27022, 3, 9004879181054557, 53, 10 ** 24, base + '/k3/data/k3_cost_hist.tsv', 24367, '1.19359680')
    print(json.dumps(r, indent=1, default=str))
