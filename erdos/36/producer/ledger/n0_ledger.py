import os
"""N0 ledger from primitive data, using only the conventions written in ANALYTIC-REVIEW.md / COUPLING-LEMMAS.md.
Each line is a named scalar contribution to N0 (lower expectation of int p Phi at m=0)."""
import json
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 60
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
w = json.load(open(I + 'wetch/central-certificate.json'), parse_float=str)
k = json.load(open(I + 'unktok/proof/data/selected-exact-kernel.json'), parse_float=str)
t = json.load(open(I + 'unktok/proof/data/target.json'), parse_float=str)
bf = json.load(open(I + 'unktok/proof/data/barrier-functional.json'), parse_float=str)
pr = json.load(open(I + 'unktok/proof/data/selected-paid-rows.json'), parse_float=str)
N0 = F(t['N0_exact']); C = F(t['C_exact'])
two20 = F(1, 2 ** 20)
def sig2(xi): x = mp.mpf(xi.numerator) / xi.denominator; return (mp.sin(x) / x) ** 2
def Bvec(n):
    a = F(2, n); return [F(1, 2) - a / 12] + [(2 - j * a) / 4 for j in range(1, n)] + [a / 24]
def bounds(n): return [F(1, 3)] + [F(1)] * (n - 1) + [F(1, 3)]
led = []
led.append(('constant c0 (E 1 = 1)', mp.mpf(F(k['constant_exact']).numerator) / F(k['constant_exact']).denominator))
y2 = F(k['y2_exact']); led.append(('y2 * 2/3 (exact moment)', mp.mpf(y2.numerator) / y2.denominator * 2 / 3))
# cosines: legacy (z<=0) via sigma^2 ; paid frequencies separately
leg = sum((mp.mpf(F(c['z']).numerator) / F(c['z']).denominator) * sig2(F(c['xi'])) for c in k['legacy_cos_retargeted'])
led.append(('legacy cos: sum z sigma^2 (z<=0)', leg))
mer = 0; npos = 0
for c in k['merged_cos']:
    z = F(c['z']); xi = F(c['xi'])
    if z <= 0: mer += mp.mpf(z.numerator) / z.denominator * sig2(xi)
    else: npos += 1; mer += mp.mpf(z.numerator) / z.denominator * (2 * sig2(xi) - 1)
print('merged cos naive (z>0 via 2s^2-1, %d positive):' % npos, mp.nstr(mer, 15), ' (not used: paid rows carry E>=0 instead)')
# periodic families (Wetch): floor((sum b)^2/4) * sum z
fam = 0
for f in w['families']:
    sb = sum(int(x) for x in f['b']); zz = f['z']
    zs = sum(F(v[1]) if isinstance(v, list) else F(v) for v in (zz if isinstance(zz, list) else [zz]))
    fam += F((sb * sb) // 4) * zs
led.append(('periodic families: floor((sum b)^2/4) sum z', mp.mpf(fam.numerator) / fam.denominator))
# Wetch 17 rows: L0 = gamma.B - d.bounds - z.B - sum w - eta/12 (joint lambda = 0)
rows = F(0)
for r in w['functional_rows']:
    c = r['certificate']; n = int(c['cells']); mu = F(r['multiplier'])
    g = [F(x) for x in c['functional_weights']]; d = [F(x) for x in c['diagonal']]; z = [F(x) for x in c['nonnegative']]
    B = Bvec(n); bd = bounds(n)
    tri = sum(F(x['multiplier']) for x in c['triangle_rows'])
    L0 = sum(a * b for a, b in zip(g, B)) - sum(a * b for a, b in zip(d, bd)) - sum(a * b for a, b in zip(z, B)) - tri - F(c['mean_multiplier']) * F(c['mean_error_upper'])
    rows += mu * L0
led.append(('17 Wetch rows: sum mu (gamma.B - d.bnd - z.B - sum w - eta/12)', mp.mpf(rows.numerator) / rows.denominator))
# two-scale (weight 2^-20, established by the C ledger)
g = [F(x) for x in bf['functional_weights']]; Bf_ = Bvec(240)
df = [F(x) for x in bf['fine_diagonal']]; dc = [F(x) for x in bf['coarse_diagonal']]
zc = [F(x) for x in bf['coarse_nonnegative']]; Bc = Bvec(120)
tau = F(bf['coarse_fixed_scale'])
trc = sum(F(x['multiplier']) for x in bf['coarse_triangle_rows'])
L2 = (sum(a * b for a, b in zip(g, Bf_)) - sum(a * b for a, b in zip(df, bounds(240))) - sum(a * b for a, b in zip(dc, bounds(120)))
      - F(bf['fine_eta']) / 12 - 2 * F(bf['fine_lambda']) / 19 - F(bf['coarse_eta']) / 12 - 2 * F(bf['coarse_lambda']) / 19
      - F(bf['fine_trace']) * 239 - F(bf['coarse_trace']) * 119 - tau * (sum(a * b for a, b in zip(zc, Bc)) + trc))
L2w = L2 * two20
led.append(('two-scale functional x 2^-20 (our reading of the prose)', mp.mpf(L2w.numerator) / L2w.denominator))
# paid rows: E J >= 0 ; payments
pay_c = sum(F(r['weight_exact']) * F(r['paid_constant_exact']) for r in pr['rows'])
pay_r = sum(F(r['weight_exact']) * F(r['rationalization_payment_exact']) for r in pr['rows'])
print('paid rows: sum w*paid_constant = %s ; sum w*rationalization = %s' % (float(pay_c), float(pay_r)))
for key in ['coupling_core_canonical_fourier_rhs_lower_exact', 'coupling_new_canonical_fourier_rhs_lower_exact',
            'coupling_old_canonical_fourier_rhs_lower_exact', 'coupling_nonnegative_scalar_surplus_lower_exact', 'delta_constant_exact']:
    print('stored', key, float(F(k[key])))
tot = sum(v for _, v in led)
for n_, v in led: print('%-70s %+.15f' % (n_, float(v)))
print('%-70s %+.15f' % ('SUM of specified terms', float(tot)))
print('%-70s %+.15f' % ('N0 (target.json)', float(N0)))
print('%-70s %+.3e' % ('N0 - SUM (unexplained: paid rows / payments / conventions)', float(mp.mpf(N0.numerator) / N0.denominator - tot)))
res = mp.mpf(N0.numerator) / N0.denominator - (tot - mp.mpf(pay_c.numerator) / pay_c.denominator - mp.mpf(pay_r.numerator) / pay_r.denominator)
print('%-70s %+.15f' % ('paid rows: - sum w*(paid_constant + rationalization_payment)', -float(pay_c + pay_r)))
print('N0 - [SUM - paid payments] = %s   (negative => N0 is below our recomputed lower expectation, i.e. conservative)' % mp.nstr(res, 6))
# sensitivity: drop the two-scale term, drop families
print('if two-scale term omitted, residual would be', mp.nstr(res + led[5][1], 6), '; if families omitted:', mp.nstr(res + led[3][1], 6))
