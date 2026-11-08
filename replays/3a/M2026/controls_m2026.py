import sys, json
sys.path.insert(0, '../Syl2026_k2k3')
from decimal import Decimal as D, getcontext
import ghr_check as g
G = [1518, 1524, 1587, 2024, 2032, 2116]
fn = 'hist_B17086.tsv'; x0 = D('0.9996683050229444')
res = {}
def at(name, **kw):
    a = dict(gens=G, B=17086, q=27995, k=1, xnum=0, xexp=0, ell=10**13, histpath=fn, c_h=None, claim='1.1923025406835', x_dec=x0)
    a.update(kw)
    try:
        r = g.run(**a); res[name] = {'PASS': r['PASS'], 'theta_lo': r['theta_lo'][:20]}
    except BaseException as e:
        res[name] = {'rejected_by': type(e).__name__ + ' ' + str(e)[:60]}
at('baseline'); at('claim_1.1923025408', claim='1.1923025408')
at('x_times_(1-1e-4)', x_dec=x0 * D('0.9999'))
at('ell_1e9', ell=10**9)
print(json.dumps(res, indent=1))
