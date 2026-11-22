import os
"""Does the kernel's data equal the sum of the certified components used in the N0 ledger?"""
import json
from fractions import Fraction as F
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
k = json.load(open(I + 'unktok/proof/data/selected-exact-kernel.json'), parse_float=str)
bf = json.load(open(I + 'unktok/proof/data/barrier-functional.json'), parse_float=str)
pr = json.load(open(I + 'unktok/proof/data/selected-paid-rows.json'), parse_float=str)
w = json.load(open(I + 'wetch/central-certificate.json'), parse_float=str)
# (i) cosines
leg = {F(c['xi']): F(c['z']) for c in k['legacy_cos_retargeted']}
mer = {F(c['xi']): F(c['z']) for c in k['merged_cos']}
paid = {}
for r in pr['rows']:
    xi = F(r['frequency_exact']); paid[xi] = paid.get(xi, 0) + F(r['weight_exact']) * F(r['cosine_coefficient_exact'])
print('cos freqs: legacy', len(leg), 'merged', len(mer), 'paid', len(paid), 'same freq sets:', set(leg) == set(mer), set(paid) <= set(mer))
dev = [abs(mer[x] - leg[x] - paid.get(x, 0)) for x in mer]
print('(i) max |merged - legacy - sum w*cos_coef| =', float(max(dev)), ' bound sum w*err_cos =',
      float(sum(F(r['weight_exact']) * F(r['coefficient_error_bounds_exact'][0]) for r in pr['rows'])))
# (ii) fine hats: H = two-scale hats*2^-20 + sum w*hat_weights ?
H = [F(x) for x in k['fine_hat_heights_exact']]; dH = [F(x) for x in k['delta_fine_hat_heights_exact']]
g = [F(x) for x in bf['functional_weights']]; b = F(2, 240)
hat2 = [g[0] / b] + [x / (2 * b) for x in g[1:]]
def heights(gam, a): return [gam[0] / a] + [x / (2 * a) for x in gam[1:]]
def to240(hc): return [hc[j // 2] if j % 2 == 0 else (hc[j // 2] + hc[j // 2 + 1]) / 2 for j in range(241)]
ph = [F(0)] * 241
for r in pr['rows']:
    n = int(r['cells']); wgt = F(r['weight_exact']); hw = [F(x) for x in r['hat_weights_exact']]
    hh = heights(hw, F(2, n)); hh = hh if n == 240 else to240(hh)
    ph = [ph[j] + wgt * hh[j] for j in range(241)]
hat2 = heights(g, b)
for name, cand in [('2^-20*twoscale + paid', [hat2[j] / 2 ** 20 + ph[j] for j in range(241)]),
                   ('delta + paid', [dH[j] + ph[j] for j in range(241)]), ('paid only', ph), ('2^-20*twoscale', [x / 2 ** 20 for x in hat2])]:
    print('(ii) max |H - (%s)| =' % name, float(max(abs(H[j] - cand[j]) for j in range(241))))
print('    max|H| =', float(max(abs(x) for x in H)), '; H - delta =', float(max(abs(H[j]-dH[j]) for j in range(241))))
# (iii) constant: c0 vs legacy y0 (+ two-scale/paid constants?)
c0 = F(k['constant_exact']); y0 = F(k['legacy_y0_exact_decimal']); dc = F(k['delta_constant_exact'])
print('(iii) c0 - legacy_y0 =', float(c0 - y0), ' delta_constant =', float(dc), ' c0 - y0 - delta_constant =', float(c0 - y0 - dc))
print('     sum w*paid_constant =', float(sum(F(r['weight_exact']) * F(r['paid_constant_exact']) for r in pr['rows'])))
print('     wetch y0 =', w['y0'], ' legacy y0 =', k['legacy_y0_exact_decimal'])
