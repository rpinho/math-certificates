"""Independent exact arithmetic, written from polynomial/Koszul definitions.

No submitted Python is imported or executed. Exponent pairs are (u, T^(1/6)).
Finite Laurent calculations are embedded in the full Novikov coefficient ring;
they are not a substitute for the universal categorical proof.
"""
import copy
import gzip
import hashlib
import json
import random
from pathlib import Path

ONE = {(0, 0): 1}
ZERO = {}

def tidy(a):
    return {e: c for e, c in a.items() if c}

def read_poly(raw):
    a = {}
    for u, t, c in raw:
        assert all(type(x) is int for x in (u, t, c))
        assert u >= 0
        a[u, t] = a.get((u, t), 0) + c
    return tidy(a)

def add(a, b):
    out = a.copy()
    for e, c in b.items():
        out[e] = out.get(e, 0) + c
    return tidy(out)

def neg(a):
    return {e: -c for e, c in a.items()}

def mul(a, b):
    out = {}
    for (u, t), c in a.items():
        for (v, s), d in b.items():
            e = (u+v, t+s)
            out[e] = out.get(e, 0) + c*d
    return tidy(out)

def exact_div(a, b):
    """Exact finite Laurent division by a coefficient polynomial, using Z only."""
    assert b and all(u == 0 for u, t in b)
    quot, rem = {}, a.copy()
    (_, bt), bc = max(b.items())
    floor = min((t for u, t in a), default=0) - min(t for u, t in b)
    for _ in range(10000):
        if not rem:
            return quot
        (u, t), c = max(rem.items())
        assert c % bc == 0, 'nonintegral division'
        assert t-bt >= floor, 'nonzero remainder'
        q = {(u, t-bt): c//bc}
        quot = add(quot, q)
        rem = add(rem, neg(mul(q, b)))
    raise AssertionError('division did not terminate')

def matrix(raw):
    return [[read_poly(a) for a in row] for row in raw]

def mm(a, b):
    assert len(a[0]) == len(b)
    return [[sum_poly(mul(a[i][k], b[k][j]) for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def sum_poly(polys):
    out = {}
    for a in polys:
        out = add(out, a)
    return out

def ident(n):
    return [[ONE.copy() if i == j else {} for j in range(n)] for i in range(n)]

def verify_case(c):
    p, f = read_poly(c['p']), read_poly(c['f'])
    assert p and all(u == 0 for u, t in p)
    lead_t = min(t for u, t in p)
    assert abs(p[0, lead_t]) > 1, 'coefficient must be a Novikov nonunit'
    degree = max(u for u, t in f)
    assert degree > 0 and degree == c['degree']
    assert {(u,t): v for (u,t),v in f.items() if u == degree} == {(degree,0):1}, 'not monic in u'
    U, V, d1, d2 = [matrix(c[k]) for k in ('U', 'Uinv', 'd1', 'd2')]
    assert mm(U,V) == mm(V,U) == ident(2), 'basis inverse'
    assert d1 == mm([[p,f]], U), 'wrong first differential'
    assert d2 == mm(V, [[neg(f)], [p]]), 'wrong second differential'
    assert mm(d1,d2) == [[{}]], 'd squared'
    # Recover the coefficient of a genuine syzygy after changing its basis.
    for h in [ONE, {(2,-3):7, (0,4):-11}, {(5,2):2, (1,-2):3, (0,0):-1}]:
        syz = mm(d2, [[h]])
        a, b = [row[0] for row in mm(U, syz)]
        recovered = exact_div(b,p)
        assert recovered == h and a == neg(mul(f,h))
    return {'id':c['id'], 'degree':degree, 'nonconstant_p':len(p)>1}

def pack_poly(p):
    return [[u,t,c] for (u,t),c in sorted(p.items())]

def pack_mat(m):
    return [[pack_poly(p) for p in row] for row in m]

def new_case(rng, idx):
    p = {(0,0):rng.choice([2,3,4,6,9])}
    if rng.randrange(2):
        p[0,rng.randrange(1,7)] = 1
    degree = rng.randrange(1,9)
    f = {(degree,0):1}
    for _ in range(7):
        f = add(f, {(rng.randrange(degree),rng.randrange(-3,5)):rng.randrange(-4,5)})
    a = {(rng.randrange(3),rng.randrange(-3,4)):rng.randrange(1,5)}
    b = {(rng.randrange(3),rng.randrange(-3,4)):rng.randrange(-4,0)}
    U = mm([[ONE,a],[{},ONE]], [[ONE,{}],[b,ONE]])
    V = mm([[ONE,{}],[neg(b),ONE]], [[ONE,neg(a)],[{},ONE]])
    return dict(id=f'independent_{idx}', p=pack_poly(p), f=pack_poly(f), degree=degree,
                U=pack_mat(U), Uinv=pack_mat(V), d1=pack_mat(mm([[p,f]],U)),
                d2=pack_mat(mm(V,[[neg(f)],[p]])))

def rejected(c):
    try:
        verify_case(c)
    except (AssertionError, KeyError, ValueError):
        return True
    return False

def main():
    raw = gzip.decompress(Path('submitted_certificate.json.gz').read_bytes())
    data = json.loads(raw)
    assert data['u_parity'] == 0 and data['no_field_inversion'] is True
    cases = [verify_case(c) for c in data['cases']]
    assert len(cases) == 24
    rng = random.Random(630211)
    independent = [verify_case(new_case(rng,i)) for i in range(200)]
    mutants = 0
    for c in data['cases']:
        for kind in ('d1', 'd2', 'Uinv', 'degree', 'unit_p', 'nonmonic_f'):
            bad = copy.deepcopy(c)
            if kind in ('d1','d2','Uinv'):
                bad[kind][0][0].append([0,0,1])
            elif kind == 'degree':
                bad['degree'] += 1
            elif kind == 'unit_p':
                bad['p'] = [[0,0,1]]
            else:
                bad['f'].append([c['degree'],0,1])
            assert rejected(bad), (c['id'],kind)
            mutants += 1
    # Paper's scalar action: S/(u-alpha) has u acting by alpha.
    scalar = data['printed_scalar_baseline']
    alpha = read_poly(scalar['alpha'])
    assert matrix(scalar['d1']) == [[add({(1,0):1},neg(alpha))]]
    assert read_poly(scalar['quotient_action']) == alpha
    scalar_tests = 0
    for _ in range(100):
        g = tidy({(rng.randrange(8), rng.randrange(-4,5)):rng.randrange(-7,8) for _ in range(15)})
        value = {}
        for (u,t), c in g.items():
            a = {(0,t):c}
            for _ in range(u):
                a = mul(a,alpha)
            value = add(value,a)
        product = mul(add({(1,0):1},neg(alpha)),g)
        evaluated = {}
        for (u,t), c in product.items():
            a = {(0,t):c}
            for _ in range(u):
                a = mul(a,alpha)
            evaluated = add(evaluated,a)
        assert not evaluated
        scalar_tests += 1
    # Verify the *literal* finite remainder, not an assertion of finite inversion.
    ser = data['unit_series']
    product = mul(read_poly(ser['unit']),read_poly(ser['inverse_truncation']))
    rem = add(product,neg(ONE))
    assert rem == read_poly(ser['remainder']) and rem
    assert min(t for u,t in rem) == ser['order']
    # Skeptical control: reduce the integer Koszul complex at (2,u).
    # In k=K_F2 its dual differential is zero, so Ext^2=k != 0.
    p, u = {(0,0):2}, {(1,0):1}
    koszul1, koszul2 = [[p,u]], [[neg(u)],[p]]
    def residue(a):
        return tidy({(0,t):c%2 for (v,t),c in a.items() if v == 0})
    assert residue(ONE) == ONE
    assert all(not residue(a) for row in koszul1+koszul2 for a in row)
    assert mm(koszul1,koszul2) == [[{}]]
    # Thus 1 cannot be in (2,u), and a length-one free resolution is impossible.
    report = dict(status='PASS', submitted_sha256=hashlib.sha256(raw).hexdigest(),
                  submitted_cases=cases, independent_cases=len(independent),
                  rejected_mutants=mutants, scalar_action_checks=scalar_tests,
                  unit_truncation_remainder=pack_poly(rem),
                  non_PID_control='1 survives mod (2,u); Ext^2(S/(2,u),K_F2)=K_F2',
                  scope='Exact finite algebra only; universal proof checked separately by reasoning and sources')
    Path('independent_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__ == '__main__':
    main()
