"""Exact verifier for type-K (core + odd-part capacity) certificates. Written separately from the search (make_K.py).

Lemma (REPORT_GAP.md section 3): for every measurable h with mean m,
    M >= [N0 + C m^2 + lam*m/2 - int_0^1 |u|] / D_up
for any real lam and any Lipschitz u on [0,1] with u(1) = 0 and |lam - u'(t)| <= g(t) := |Phi(t)| + |Phi(2-t)| a.e.

Certificate: per bin lo, hi, lam (exact decimals), k0, slopes s_k (exact fractions) for cells k0..65535 of width 1/65536;
slope 0 on cells < k0. u(1) = 0, u(k/65536) = u((k+1)/65536) - s_k/65536.

Checks (all exact rationals; g lower bounds are outward-rounded Arb endpoints converted to exact dyadics):
  (1) lam - s_k and s_k - lam both <= g_lb(cell k) for every cell k in [0, 65536)
  (2) U = int_0^1 |u| exactly (piecewise linear, zero crossings handled exactly)
  (3) num = min over m in {lo, hi} of N0 + C m^2 + lam m/2 - U ; bound = num / D_up > L strictly
  (4) cover: bins tile [A, B] with equal consecutive endpoints.
usage: E36_INPUTS=DIR python -I verify_K.py CERT.json [--raiseL 1e-6] [--flip BIN] [--drop BIN] [--nocap BIN]
"""
import sys, json, time, argparse, resource
from fractions import Fraction as Fr
import multiprocessing as mp
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'dint2'))
import flint
from flint import fmpq, arb
from load import load

flint.ctx.prec = 128
INPUTS = os.environ.get('E36_INPUTS', 'inputs')   # dir holding unktok/ and wetch/ (see README)
LNUM = 295115424188729399759259170770153384401616054763504786695772146837923638817310985375107967151349
LDEN = 775338951052420904588737482312221487781542035285383462905883789062500000000000000000000000000000
L = Fr(LNUM, LDEN)
NC = 65536


def Q(f): return fmpq(f.numerator, f.denominator)
def toF(x):  # exact Fraction of an arb point (arf)
    m, e = x.mid().man_exp(); m = int(m); e = int(e)
    return Fr(m * 2 ** e) if e >= 0 else Fr(m, 2 ** (-e))


# ---------------- kernel pieces (from primitive data, same construction as dint2) ----------------
d = load()
c0 = Q(d['c0']); y2 = Q(d['y2'])
COS = [(Q(a), Q(b)) for a, b in d['cos']]
H = [Q(x) for x in d['H']]
Zx = {i: Q(v) for i, v in d['Z'].items()}
rows = [(Q(mu), n, [Q(x) for x in g]) for mu, n, g in d['rows']]
macro = set(Fr(k, 120) for k in range(241))
for mu, n, g in rows:
    macro |= set(Fr(2 * k, n) for k in range(n + 1))
macro = sorted(macro)
mA = []; mB = []
for j in range(len(macro) - 1):
    lo, hi = macro[j], macro[j + 1]; mid = (lo + hi) / 2
    k = int(mid * 120); B = (H[k + 1] - H[k]) * 120; A = H[k] - B * fmpq(k, 120) + c0
    for mu, n, g in rows:
        a = fmpq(2, n); k = int(mid * n / 2)
        vk = g[0] / a if k == 0 else g[k] / (2 * a); vk1 = g[k + 1] / (2 * a)
        b = (vk1 - vk) / a; aa = vk - b * (k * a)
        A = A + mu * aa; B = B + mu * b
    mA.append(A); mB.append(B)
bps = sorted(set(Fr(i, NC) for i in range(2 * NC + 1)) | set(macro))
pieces = []  # (cell index, a, b, A, B)
mj = 0
for p in range(len(bps) - 1):
    lo, hi = bps[p], bps[p + 1]; mid = (lo + hi) / 2
    while macro[mj + 1] <= lo: mj += 1
    i = int(mid * NC)
    A = mA[mj] + Zx[i] if i in Zx else mA[mj]
    pieces.append((i, lo, hi, A, mB[mj]))
AXI = [arb(a) for a, b in COS]; AZ = [arb(b) for a, b in COS]
M3 = arb(sum((abs(b) * a ** 3 for a, b in COS), fmpq(0)))
AY2 = arb(y2)


def encl(job):
    """Arb enclosure of Phi on each piece: Phi(c)+Phi'(c)[-h,h]+Phi''(c)/2[0,h^2]+M3/6[-h^3,h^3]."""
    out = []
    for (i, a, b, A, B) in job:
        a_ = arb(Q(a)); b_ = arb(Q(b)); c = (a_ + b_) / 2; h = (b_ - a_) / 2
        S0 = arb(0); S1 = arb(0); S2 = arb(0)
        for x, z in zip(AXI, AZ):
            s_, c_ = (x * c).sin_cos(); S0 += z * c_; S1 += z * x * s_; S2 += z * x * x * c_
        Aa = arb(A); Ba = arb(B)
        p0 = Aa + Ba * c + AY2 * c * c + S0; p1 = Ba + 2 * AY2 * c - S1; p2 = 2 * AY2 - S2
        unit = arb(0, 1); half = arb(0.5, 0.5)  # [-1,1], [0,1]
        e = p0 + p1 * h * unit + p2 * h * h / 2 * half + M3 * h ** 3 / 6 * unit
        out.append((i, toF(e.lower()), toF(e.upper())))
    return out


def cell_bounds(nproc=4):
    jobs = [pieces[r::200] for r in range(200)]
    with mp.get_context('fork').Pool(nproc) as P:
        res = P.map(encl, jobs)
    lo = [None] * (2 * NC); hi = [None] * (2 * NC)
    for lst in res:
        for i, l, u in lst:
            lo[i] = l if lo[i] is None else min(lo[i], l)
            hi[i] = u if hi[i] is None else max(hi[i], u)
    def mig(l, u): return Fr(0) if l <= 0 <= u else min(abs(l), abs(u))
    return [mig(lo[k], hi[k]) + mig(lo[2 * NC - 1 - k], hi[2 * NC - 1 - k]) for k in range(NC)]


def intabs(ua, ub, w):
    if (ua >= 0 and ub >= 0) or (ua <= 0 and ub <= 0):
        return (abs(ua) + abs(ub)) * w / 2
    return (ua * ua + ub * ub) / (2 * abs(ua - ub)) * w


def check_bin(b, glb, N0, C, Dup, Lc, flip=False, nocap=False):
    lo = Fr(b['lo']); hi = Fr(b['hi']); lam = Fr(b['lam']); k0 = int(b['k0'])
    s = [Fr(x) for x in b['slopes']]
    assert len(s) == NC - k0
    if flip: lam = -lam
    if nocap: lam = Fr(0); s = [Fr(0)] * len(s)
    w = Fr(1, NC)
    bad = 0; worst = None
    for k in range(NC):
        sk = s[k - k0] if k >= k0 else Fr(0)
        sl = glb[k] - abs(lam - sk)
        if sl < 0: bad += 1
        if worst is None or sl < worst: worst = sl
    u = Fr(0); U = Fr(0)
    for k in range(NC - 1, k0 - 1, -1):
        ul = u - s[k - k0] * w
        U += intabs(ul, u, w); u = ul
    U += abs(u) * k0 * w          # u constant on [0, k0/NC]
    nums = [N0 + C * m * m + lam * m / 2 - U for m in (lo, hi)]
    num = min(nums)
    bound = num / Dup
    return {'lo': b['lo'], 'hi': b['hi'], 'lam': str(b['lam']), 'k0': k0, 'slope_violations': bad,
            'min_slope_slack': float(worst), 'U': float(U), 'u_at_k0': float(u),
            'bound': float(bound), 'margin': float(bound - Lc), 'pass': bool(bad == 0 and num > 0 and bound > Lc)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cert'); ap.add_argument('--raiseL', default=None)
    ap.add_argument('--flip', type=int, default=None); ap.add_argument('--drop', type=int, default=None)
    ap.add_argument('--nocap', type=int, default=None); ap.add_argument('--out', default=None); ap.add_argument('--N0shift', default=None)
    ap.add_argument('--dint2', default=None, help='D_up result json (default: dint2/res_main.json)')
    a = ap.parse_args(); T0 = time.time()
    cert = json.load(open(a.cert))
    tg = json.load(open(os.path.join(INPUTS, 'unktok/proof/data/target.json')))
    N0 = Fr(tg['N0_exact']) + (Fr(a.N0shift) if a.N0shift else 0); C = Fr(tg['C_exact'])
    dres = json.load(open(a.dint2 or os.path.join(HERE, 'dint2', 'res_main.json')))
    Dup = Fr(dres['D_up']) + Fr(1, 10 ** 22)   # printed 25 digits; pad outward
    Lc = L + (Fr(a.raiseL) if a.raiseL else 0)
    glb = cell_bounds()
    print('cell bounds done', round(time.time() - T0, 1), 's; min g_lb on [0,0.9]:', float(min(glb[:int(0.9 * NC)])), flush=True)
    bins = cert['bins']
    idx = [i for i in range(len(bins)) if i != a.drop]
    res = [check_bin(bins[i], glb, N0, C, Dup, Lc, flip=(i == a.flip), nocap=(i == a.nocap)) for i in idx]
    gaps = []
    for i, j in zip(idx, idx[1:]):
        if Fr(bins[i]['hi']) != Fr(bins[j]['lo']): gaps.append([bins[i]['hi'], bins[j]['lo']])
    cov = {'from': bins[idx[0]]['lo'], 'to': bins[idx[-1]]['hi'], 'gaps': gaps,
           'covers_target': (not gaps) and Fr(bins[idx[0]]['lo']) <= Fr(cert['target_lo']) and Fr(bins[idx[-1]]['hi']) >= Fr(cert['target_hi'])}
    mn = min(res, key=lambda r: r['margin'])
    out = {'cert': a.cert, 'N0_shift': a.N0shift, 'L_raised_by': a.raiseL, 'flip': a.flip, 'drop': a.drop, 'nocap': a.nocap,
           'D_up_used': str(Dup), 'n_bins': len(res), 'all_pass': all(r['pass'] for r in res), 'cover': cov,
           'n_fail': sum(not r['pass'] for r in res), 'min_margin': mn['margin'], 'min_margin_bin': [mn['lo'], mn['hi']],
           'runtime_s': round(time.time() - T0, 1),
           'maxrss_MB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20, 'bins': res}
    print(json.dumps({k: v for k, v in out.items() if k != 'bins'}, indent=1))
    if a.out: json.dump(out, open(a.out, 'w'), indent=1)


if __name__ == '__main__':
    main()
