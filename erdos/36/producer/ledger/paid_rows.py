import os
"""Rebuild each paid row from COUPLING-LEMMAS' J formula and compare with the stored exact data (within error bounds).
J(t) = c cos(xi t) - a K_W(t) + a(W.B) - c sigma^2,  c = sinc^2(xi a/2), W_0=1, W_k = 2cos(xi a k), sigma = sin(xi)/xi."""
import json
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 50
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
pr = json.load(open(I + 'unktok/proof/data/selected-paid-rows.json'), parse_float=str)
k = json.load(open(I + 'unktok/proof/data/selected-exact-kernel.json'), parse_float=str)
t = json.load(open(I + 'unktok/proof/data/target.json'), parse_float=str)
def q(x): x = F(x); return mp.mpf(x.numerator) / x.denominator
def Bvec(n):
    a = F(2, n); return [F(1, 2) - a / 12] + [(2 - j * a) / 4 for j in range(1, n)] + [a / 24]
worst = {'cos': 0, 'hat': 0, 'const': 0}; viol = 0
for r in pr['rows']:
    n = int(r['cells']); a = mp.mpf(2) / n; xi = q(r['frequency_exact'])
    c = (mp.sin(xi * a / 2) / (xi * a / 2)) ** 2; sg = mp.sin(xi) / xi
    W = [mp.mpf(1)] + [2 * mp.cos(xi * a * j) for j in range(1, n + 1)]
    B = [q(x) for x in Bvec(n)]
    kap = a * sum(x * y for x, y in zip(W, B)) - c * sg * sg
    eb = [q(x) for x in r['coefficient_error_bounds_exact']]   # [cos, hats..., ] length n+2
    dc = abs(q(r['cosine_coefficient_exact']) - c); dh = [abs(q(h) - (-a * W[j])) for j, h in enumerate(r['hat_weights_exact'])]
    dk = abs(q(r['paid_constant_exact']) - kap)
    worst['cos'] = max(worst['cos'], dc); worst['hat'] = max(worst['hat'], max(dh)); worst['const'] = max(worst['const'], dk)
    if dc > eb[0] or any(dh[j] > eb[1 + j] for j in range(n + 1)): viol += 1
print('52 paid rows vs J formula: max |cos coef diff| %s, max |hat diff| %s, max |paid_constant - kappa| %s' % tuple(mp.nstr(worst[x], 3) for x in ('cos', 'hat', 'const')))
print('rows with a coefficient difference above its stored error bound:', viol)
# per-row validity of the payment: paid_constant + rationalization >= kappa + |dc|*1 + sum |dh_j| * (hat-moment bound 1)
tot_short = mp.mpf(0); nshort = 0; tot_slack = mp.mpf(0)
for r in pr['rows']:
    n = int(r['cells']); a = mp.mpf(2) / n; xi = q(r['frequency_exact'])
    c = (mp.sin(xi * a / 2) / (xi * a / 2)) ** 2; sg = mp.sin(xi) / xi
    W = [mp.mpf(1)] + [2 * mp.cos(xi * a * j) for j in range(1, n + 1)]
    B = [q(x) for x in Bvec(n)]
    kap = a * sum(x * y for x, y in zip(W, B)) - c * sg * sg
    err = abs(q(r['cosine_coefficient_exact']) - c) + sum(abs(q(h) + a * W[j]) for j, h in enumerate(r['hat_weights_exact']))
    s = q(r['paid_constant_exact']) + q(r['rationalization_payment_exact']) - kap - err
    w_ = q(r['weight_exact']); tot_slack += w_ * s
    if s < 0: nshort += 1; tot_short += w_ * s
print('rows where paid_constant+payment < kappa+actual errors:', nshort, ' weighted shortfall', mp.nstr(tot_short, 4), ' total weighted slack', mp.nstr(tot_slack, 4))
