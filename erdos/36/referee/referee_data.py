"""Exact inputs, ledger, and affine part of the kernel on [0,2]."""
import hashlib
import json
import re
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import os
from pathlib import Path

from flint import arb, fmpq

INPUTS = Path(os.environ.get("E36_INPUTS", "inputs"))   # dir holding unktok/ and wetch/ (see README)
DATA = INPUTS / "unktok" / "proof" / "data"
WETCH = INPUTS / "wetch"
GRID = 65536


def read(path):
    return json.loads(path.read_bytes(), parse_float=str)


def ball(x):
    q = F(x)
    return arb(fmpq(q.numerator, q.denominator))


def bounds(a):
    def endpoint(x):
        m, e = x.man_exp()
        return F(int(m)) * F(2) ** int(e)
    return endpoint(a.lower()), endpoint(a.upper())


def targets():
    target = read(DATA / "target.json")
    result = (DATA.parent.parent / "RESULT.md").read_text()
    full = F(re.search(r"`{3}text\s+(\d+/\d+)", result)[1])
    assert full > F(target['uniform_lower_exact']) and full > F('0.38062762')
    return F(target['N0_exact']), F(target['C_exact']), full


def hat_base(n):
    a = F(2, n)
    return [F(1, 2) - a/12, *[(2-k*a)/4 for k in range(1, n)], a/24]


def dot(xs, ys):
    return sum(x*y for x, y in zip(xs, ys, strict=True))


def diagonal_payment(ds):
    return sum(ds[1:-1]) + (ds[0]+ds[-1])/3


def heights(gamma):
    n = len(gamma)-1
    return [gamma[0]*n/2] + [x*n/4 for x in gamma[1:]]


def lagrange_to_fine(h, n):
    assert n % (len(h)-1) == 0
    scale = n // (len(h)-1)
    return [(h[i//scale]*(scale-i%scale) + h[min(i//scale+1, len(h)-1)]*(i%scale))/scale
            for i in range(n+1)]


def scatter(families, n):
    # A single occupied input cell i maps to lag consecutive grid cells
    # starting at lag*i (mod n), each with Jacobian 1/lag.
    output = defaultdict(F)
    scalar = F(0)
    for fam in families:
        pos, b, zz = fam['positions'], fam['b'], fam['z']
        assert len(pos) == len(set(pos)) == len(b) == 3 and set(b) <= {-1, 1}
        assert len(zz) == n
        weights = {}
        for i, raw in enumerate(zz):
            if raw not in (0, '0', '0.0'):
                z = F(raw)
                assert z <= 0
                if z:
                    weights[i] = z
        scalar += (sum(b)**2 // 4) * sum(weights.values())
        for i, j in combinations(range(3), 2):
            lag = abs(pos[i]-pos[j])
            factor = F(n*b[i]*b[j], 4*lag)
            for k, z in weights.items():
                term = factor*z
                for u in range(lag*k, lag*(k+1)):
                    cell = u % n
                    output[cell] += term
                    output[n-1-cell] += term
    return {k:v for k,v in output.items() if v}, scalar


def rebuild():
    for entry in read(DATA.parent.parent/'UPSTREAM.json')['inputs']:
        assert hashlib.sha256((WETCH/entry['name']).read_bytes()).hexdigest() == entry['sha256']
    manifest = read(DATA.parent/'MANIFEST.json')['files']
    for path in DATA.glob('*.json'):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest['data/'+path.name]['sha256']
    raw = read(WETCH/'central-certificate.json')
    ker = read(DATA/'selected-exact-kernel.json')
    barrier = read(DATA/'barrier-functional.json')
    c0, y2 = F(ker['constant_exact']), F(ker['y2_exact'])
    cosines = {F(r['xi']):F(r['z']) for r in ker['legacy_cos_retargeted']}
    assert len(cosines) == 314 and max(cosines.values()) <= 0
    fourier = sum(ball(z)*ball(x).sinc()**2 for x,z in cosines.items())
    offsets, periodic = scatter(raw['families'], raw['cells'])
    off = read(DATA/'exact-periodic-offsets.json')
    assert raw['cells'] == off['cells'] == 2*GRID
    assert sorted(offsets.items()) == sorted((k,F(v)) for k,v in off['sparse'])

    grids = []
    rows = F(0)
    C = y2/2
    for row in raw['functional_rows']:
        w = F(row['multiplier'])
        r = row['certificate']
        n = r['cells']
        gamma, z, diag = [list(map(F,r[k])) for k in ('functional_weights','nonnegative','diagonal')]
        eta = F(r['mean_multiplier'])
        tris = [F(t['multiplier']) for t in r['triangle_rows']]
        assert min([w,eta,*z,*diag,*tris]) >= 0 and not r['circle_rows']
        B = hat_base(n)
        rows += w*(dot(gamma,B)-dot(z,B)-diagonal_payment(diag)-sum(tris)-eta/12)
        C -= w*eta/F(2,n)**2
        grids.append([w*v for v in heights(gamma)])

    nf = barrier['fine_cells']
    paid_h = [F(0)]*(nf+1)
    paid_store = F(0)
    paid_true = arb(0)
    excesses = []
    maxerr = [arb(0) for _ in range(3)]
    paid_rows = read(DATA/'selected-paid-rows.json')['rows']
    for row in paid_rows:
        n = row['cells']
        a = F(2,n)
        xi, w, cz, stored, payment = [F(row[k]) for k in ('frequency_exact','weight_exact',
            'cosine_coefficient_exact','paid_constant_exact','rationalization_payment_exact')]
        assert row['kind']=='jensen' and w>=0
        wg = list(map(F,row['hat_weights_exact']))
        hh = lagrange_to_fine(heights(wg), nf)
        paid_h = [x+w*y for x,y in zip(paid_h, hh, strict=True)]
        cosines[xi] += w*cz
        exact_c = ball(xi*a/2).sinc()**2
        W = [arb(1)] + [2*ball(xi*a*k).cos() for k in range(1,n+1)]
        kappa = ball(a)*dot(W, map(ball,hat_base(n))) - exact_c*ball(xi).sinc()**2
        cerr = abs(ball(cz)-exact_c)
        herr = [abs(ball(g)+ball(a)*v) for g,v in zip(wg,W,strict=True)]
        errors = [cerr, *herr]
        assert all(err <= ball(limit) for err,limit in
                   zip(errors,row['coefficient_error_bounds_exact'],strict=True))
        # Each |E cos| and each normalized hat moment is at most one.
        actual_charge = kappa + cerr + sum(herr)
        paid_true -= ball(w)*actual_charge
        paid_store -= w*(stored+payment)
        excesses.append(ball(w)*(ball(stored+payment)-actual_charge))
        for i, err in enumerate([cerr,max(herr,key=lambda v: v.upper()),abs(kappa-ball(stored))]):
            maxerr[i] = max(maxerr[i],err,key=lambda v:v.upper())
    assert all(v>=0 for v in excesses)
    assert cosines == {F(r['xi']):F(r['z']) for r in ker['merged_cos']}
    fh = list(map(F,ker['fine_hat_heights_exact']))
    gamma = list(map(F,barrier['functional_weights']))
    bh = heights(gamma)
    scale = (fh[0]-paid_h[0])/bh[0]
    assert scale == F(1,2**20)
    assert fh == [p+scale*q for p,q in zip(paid_h,bh,strict=True)]
    grids.append(fh)

    L0 = dot(gamma,hat_base(nf))
    for side in ('fine','coarse'):
        n = barrier[side+'_cells']
        eta, joint, beta = [F(barrier[side+'_'+k]) for k in ('eta','lambda','trace')]
        ds = list(map(F,barrier[side+'_diagonal']))
        assert min([eta,joint,beta,*ds])>=0
        L0 -= diagonal_payment(ds)+eta/12+2*joint/19+beta*(n-1)
        C -= scale*(eta+joint)/F(2,n)**2
    tau = F(barrier['coarse_fixed_scale'])
    z = list(map(F,barrier['coarse_nonnegative']))
    tris = [F(t['multiplier']) for t in barrier['coarse_triangle_rows']]
    assert min([tau,*z,*tris])>=0
    L0 -= tau*(dot(z,hat_base(barrier['coarse_cells']))+sum(tris))
    terms = dict(constant=c0, second_moment=y2*F(2,3), legacy_cos=fourier, periodic=periodic,
                 wetch_rows=rows, two_scale=scale*L0, paid_stored=paid_store)
    base = sum(ball(v) if isinstance(v,F) else v for k,v in terms.items() if k!='paid_stored')
    N0, C_target, L = targets()
    slack = base+paid_true-ball(N0)
    stored_slack = base+ball(paid_store)-ball(N0)
    assert C == C_target and slack > 0
    # With c0 already in the kernel its lower expectation is exactly c0.
    # This extra comparison tests the reported interpretation of L0.
    c0_residual = (c0 - F(ker['legacy_y0_exact_decimal'])
        - sum(F(r['weight_exact'])*F(r['paid_constant_exact']) for r in paid_rows)+scale*L0)
    ledger = dict(terms={k:str(v) for k,v in terms.items()}, C=str(C), N0=str(N0),
        c0_residual=str(c0_residual), stored_minus_N0=str(stored_slack), actual_minus_N0=str(slack),
        paid_savings=str(sum(excesses)), paid_max_errors=list(map(str,maxerr)),
        paid_rows=len(paid_rows), wetch_rows=len(raw['functional_rows']), families=len(raw['families']),
        offsets=len(offsets), cosines=len(cosines), fine_heights=len(fh), scale=str(scale))
    return c0, y2, cosines, grids, offsets, ledger
