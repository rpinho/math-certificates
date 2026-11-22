import os
"""Rigorous (Arb, 256 bits) N0 ledger: provable lower expectation LB of int p Phi at m=0 from the documented component
rules, with each paid row charged its exact kappa plus its actual coefficient errors. Decides LB >= N0."""
import json
from fractions import Fraction as F
import flint
from flint import arb, fmpq
flint.ctx.prec = 256
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
w = json.load(open(I + 'wetch/central-certificate.json'), parse_float=str)
k = json.load(open(I + 'unktok/proof/data/selected-exact-kernel.json'), parse_float=str)
t = json.load(open(I + 'unktok/proof/data/target.json'), parse_float=str)
bf = json.load(open(I + 'unktok/proof/data/barrier-functional.json'), parse_float=str)
pr = json.load(open(I + 'unktok/proof/data/selected-paid-rows.json'), parse_float=str)
def A(x): x = F(x); return arb(fmpq(x.numerator, x.denominator))
def Bvec(n):
    a = F(2, n); return [F(1, 2) - a / 12] + [(2 - j * a) / 4 for j in range(1, n)] + [a / 24]
def bnd(n): return [F(1, 3)] + [F(1)] * (n - 1) + [F(1, 3)]
def dot(u, v): return sum((x * y for x, y in zip(u, v)), F(0))
rat = F(k['constant_exact']) + F(k['y2_exact']) * F(2, 3)
for f in w['families']:
    sb = sum(int(x) for x in f['b']); rat += F((sb * sb) // 4) * sum(F(v) for v in f['z'])
for r in w['functional_rows']:
    c = r['certificate']; n = int(c['cells']); B = Bvec(n)
    L0 = (dot([F(x) for x in c['functional_weights']], B) - dot([F(x) for x in c['diagonal']], bnd(n))
          - dot([F(x) for x in c['nonnegative']], B) - sum(F(x['multiplier']) for x in c['triangle_rows'])
          - F(c['mean_multiplier']) * F(c['mean_error_upper']))
    rat += F(r['multiplier']) * L0
g = [F(x) for x in bf['functional_weights']]
L2 = (dot(g, Bvec(240)) - dot([F(x) for x in bf['fine_diagonal']], bnd(240)) - dot([F(x) for x in bf['coarse_diagonal']], bnd(120))
      - F(bf['fine_eta']) / 12 - 2 * F(bf['fine_lambda']) / 19 - F(bf['coarse_eta']) / 12 - 2 * F(bf['coarse_lambda']) / 19
      - F(bf['fine_trace']) * 239 - F(bf['coarse_trace']) * 119
      - F(bf['coarse_fixed_scale']) * (dot([F(x) for x in bf['coarse_nonnegative']], Bvec(120)) + sum(F(x['multiplier']) for x in bf['coarse_triangle_rows'])))
rat += L2 / 2 ** 20
LB = A(rat)
for c in k['legacy_cos_retargeted']:
    z = F(c['z']); assert z <= 0
    xi = A(c['xi']); s = xi.sin() / xi; LB += A(z) * s * s
paid_exact = arb(0); paid_stored = F(0)
for r in pr['rows']:
    n = int(r['cells']); a = A(F(2, n)); xi = A(r['frequency_exact']); wt = A(r['weight_exact'])
    h_ = xi * a / 2; cc = (h_.sin() / h_) ** 2; sg = xi.sin() / xi
    W = [arb(1)] + [2 * (xi * a * j).cos() for j in range(1, n + 1)]
    kap = a * sum((Wj * A(Bj) for Wj, Bj in zip(W, Bvec(n))), arb(0)) - cc * sg * sg
    err = abs(A(r['cosine_coefficient_exact']) - cc) + sum((abs(A(hv) + a * W[j]) for j, hv in enumerate(r['hat_weights_exact'])), arb(0))
    paid_exact += wt * (kap + err)
    paid_stored += F(r['weight_exact']) * (F(r['paid_constant_exact']) + F(r['rationalization_payment_exact']))
N0 = A(t['N0_exact'])
for name, pay in [('exact kappa + actual errors', paid_exact), ('stored paid_constant + payment', A(paid_stored))]:
    d = LB - pay - N0
    print('%-32s LB - N0 in [%s, %s]   LB >= N0 proved: %s' % (name, d.lower().str(5, radius=False), d.upper().str(5, radius=False), bool(d > 0)))
