#!/usr/bin/env python3
"""Rejection controls for ghr_check.py (k=2 data). Each perturbed input must FAIL."""
import sys, json, shutil
sys.path.insert(0, '.')
import ghr_check as g
G = [1971, 2016, 2100, 2628, 2688, 2800]
H = '../_raw/syl/data/k2_cost_hist.tsv'
base = dict(gens=G, B=26972, q=27022, k=2, xnum=9004870224628742, xexp=53, ell=10**18, histpath=H, c_h=24367, claim='1.19281555')
res = {}
def attempt(name, **kw):
    a = dict(base); a.update(kw)
    try:
        r = g.run(**a); res[name] = {'PASS': r.get('PASS'), 'theta_lo': r['theta_lo'][:20], 'numerator_positive': r['numerator_positive']}
    except BaseException as e:
        res[name] = {'rejected_by': type(e).__name__ + ': ' + str(e)[:80]}
attempt('baseline')
attempt('claim_raised_to_1.19281556', claim='1.19281556')
attempt('x_scaled_by_(1-1e-4)', xnum=int(9004870224628742 * (1 - 1e-4)))
attempt('ell_1e9', ell=10**9)
# tampered histograms
lines = open(H).read().split('\n')
t = list(lines)
i = 10; c, m = t[i].split('\t'); t[i] = '%s\t%d' % (c, int(m) + 1)         # +1 multiplicity: sum != Q
open('/tmp/_t1.tsv', 'w').write('\n'.join(t)) if False else None
import os, tempfile
d = tempfile.mkdtemp(dir='.')
p1 = d + '/t1.tsv'; open(p1, 'w').write('\n'.join(t))
t2 = list(lines); a, ma = t2[10].split('\t'); b, mb = t2[11].split('\t')
t2[10] = '%s\t%d' % (a, int(ma) + 1); t2[11] = '%s\t%d' % (b, int(mb) - 1)  # sum kept, parity broken
p2 = d + '/t2.tsv'; open(p2, 'w').write('\n'.join(t2))
attempt('hist_multiplicity_plus1', histpath=p1)
attempt('hist_move_one_unit_between_classes', histpath=p2)
print(json.dumps(res, indent=1))
