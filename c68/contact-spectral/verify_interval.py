#!/usr/bin/env python3
"""Second C68 checker, written independently of search and the Arb checker.

Uses mpmath's outward interval arithmetic, unnormalized moment recurrences,
and exact Fraction checks for structure. No flint and no search imports.
The analytic reductions are in ANGULAR_LEMMA.md and GREEN_FLUX_PROOF.md.
"""
import argparse
import hashlib
import json
import time
from fractions import Fraction as Q
from pathlib import Path
from mpmath import iv

if not __debug__:
    raise SystemExit('Refusing Python -O: structural assertions are required')


def interval(q):
    q = Q(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def require_positive(x, label):
    if not x.a > 0:
        raise ArithmeticError(f'{label}: {x}')


def cosh(x):
    return (iv.exp(x) + iv.exp(-x)) / 2


def sinh(x):
    return (iv.exp(x) - iv.exp(-x)) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate')
    ap.add_argument('--bits', type=int, default=340)
    ap.add_argument('--output')
    args = ap.parse_args()
    started = time.monotonic()
    iv.prec = args.bits
    raw = Path(args.certificate).read_bytes()
    d = json.loads(raw)
    assert d['model'] in ('fourier_majorant_low_coefficient_v1','spectral_geometric_mean_v2','contact_spectral_v3')
    zeta = {'fourier_majorant_low_coefficient_v1':Q(9,320),'spectral_geometric_mean_v2':Q(3,50),'contact_spectral_v3':Q(7,100)}[d['model']]
    assert Q(d['kappa']) == Q(3, 25) and Q(d['zeta']) == zeta
    spectral = None
    if d['model']=='spectral_geometric_mean_v2':
        from verify_spectral_interval import verify_cover
        spectral = verify_cover(Path(args.certificate).parent/'spectral-cover.json')
    if d['model']=='contact_spectral_v3':
        from verify_contact_interval import verify_cover
        spectral = verify_cover(Path(args.certificate).parent/'contact-cover.json')
    c, R = Q(d['c']), Q(d['R'])
    nodes, weights = [list(map(Q, d[key])) for key in ('nodes', 'weights')]
    cuts = list(map(Q, d['tail_partition']))
    assert 0 < c < 1 and c*c < R < 1 and c <= R
    assert len(nodes) == len(weights) >= 2
    assert nodes[0] == c*c and nodes[-1] == R
    assert all(x > 0 for x in weights) and sum(weights) == R
    assert all(x < y for x, y in zip(nodes, nodes[1:]))
    assert cuts[0] == R and cuts[-1] == 1
    assert all(x < y for x, y in zip(cuts, cuts[1:]))
    K1, K2 = d['first_tail_k'], d['second_tail_k']
    assert isinstance(K1, int) and isinstance(K2, int)
    assert 1 < K1 < 1000000 and 1 < K2 < 1000000
    assert weights[-1]*(K1+1) >= R

    w = -iv.log(interval(c))
    A = iv.pi**2 / w
    q = iv.exp(-A)
    Psi = (1+q)**2 / (8*q)
    kappa = interval(Q(3,25))
    tanhA8 = sinh(A/8)/cosh(A/8)
    hypotheses = {
        'flux': interval(Q(1,3))-1/cosh(A/2)**2,
        'small_arc': 2*(1-8*kappa)*Psi-16*sinh(A/4)**2,
        'near_midpoint': tanhA8**2-(1+8*kappa)*iv.pi**2/64,
        'middle_arc': (1-4*kappa)/2-1/cosh(A/8)**2,
        'beta1_positive': Psi-6,
    }
    for name, value in hypotheses.items():
        require_positive(value, name)
    # Rational hypotheses in the low-coefficient polynomial argument.
    assert Q(17,100)**2 > Q(9,320)
    assert 2*Q(3,25)*(1-Q(15,16)**2) > Q(9,320)
    assert 4*Q(3,25)*Q(15,16) == Q(9,20)
    assert Q(9,5) > Q(117,100)**2
    assert Q(17,100)*Q(117,100) < Q(9,20)

    beta, beta1 = [], []
    atomic_g, atomic_e = [], []
    for t in nodes:
        if t == c*c:
            g = epsilon = iv.mpf(0)
        else:
            sigma = iv.sin(iv.pi*iv.log(interval(t))/(2*w))**2
            # Rationalized form differs from the Arb checker's evaluation.
            h_inverse = iv.sqrt(2*sigma/(Psi+2*sigma))
            g = 2*h_inverse/(1+h_inverse)
            epsilon = interval(zeta/2)*g*(1-h_inverse)
            require_positive(g, 'atomic g')
            require_positive(1-g-epsilon, 'atomic beta1')
        beta.append(1-g)
        beta1.append(1-g-epsilon)
        atomic_g.append(str(g))
        atomic_e.append(str(epsilon))

    def slope(a, b):
        # g(t) >= l*(1-t) throughout [a,b]. Derivation is in PROOF.md.
        a, b = interval(a), interval(b)
        angle = -iv.pi*iv.log(a)/(2*w)
        require_positive(angle, 'positive tail angle')
        require_positive(6-angle**2, 'tail sine truncation')
        B = iv.pi/(2*w)*(1+(1-b)/2)*(1-angle**2/6)
        require_positive(B, 'tail B')
        l = 2*iv.sqrt(2)*B/(iv.sqrt(2)*B*(1-a)+iv.sqrt(2*B**2*(1-a)**2+Psi))
        require_positive(l, 'tail slope')
        # Freeze a downward endpoint; this can only weaken the claim.
        return iv.mpf(l.a)

    cells = [(a,b,slope(a,b)) for a,b in zip(cuts,cuts[1:])]
    ta, tb = Q(d['second_tail_a']), Q(d['second_tail_b'])
    assert R <= ta < tb < 1
    l = slope(ta,tb)
    tail_good = l*interval((1-tb)*(tb-ta))*interval(ta)**K2
    tail_bad = sum(interval(v)*interval(t)**K2 for t,v in zip(nodes,weights))
    tail_gap = tail_good-tail_bad
    require_positive(tail_gap, 'all k >= second tail')

    W, T = list(map(interval,weights)), list(map(interval,nodes))
    atom_powers = [iv.mpf(1) for _ in nodes]
    C = {a:interval(a) for a in cuts}
    cut_powers = C.copy()  # powers of degree k+1 after k updates
    Rpower = interval(R)
    minA = minB = None
    minAk = minBk = None
    for k in range(1,max(K1,K2)):
        atom_powers = [p*t for p,t in zip(atom_powers,T)]
        Rpower *= interval(R)
        if k < K1:
            residual = sum(v*p for v,p in zip(W,atom_powers))-Rpower/(k+1)
            require_positive(residual, ('ordinary moment',k))
            relative = residual*(k+1)/Rpower
            if minA is None or relative.a < minA.a:
                minA, minAk = relative, k
        if k < K2:
            for a in cuts:
                cut_powers[a] *= C[a]
            integral_g = iv.mpf(0)
            for a,b,l in cells:
                # Antiderivative of (1-t)*t**k, evaluated at both endpoints.
                lower = cut_powers[a]/(k+1)-cut_powers[a]*C[a]/(k+2)
                upper = cut_powers[b]/(k+1)-cut_powers[b]*C[b]/(k+2)
                integral_g += l*(upper-lower)
            bs = beta1 if k == 1 else beta
            residual = Rpower/(k+1)+integral_g-sum(v*b*p for v,b,p in zip(W,bs,atom_powers))
            require_positive(residual, ('weighted moment',k))
            relative = residual*(k+1)/Rpower
            if minB is None or relative.a < minB.a:
                minB, minBk = relative, k
    out = dict(status='PASS', backend='mpmath.iv', bits=iv.prec, c=str(c),
               certificate_sha256=hashlib.sha256(raw).hexdigest(),
               hypothesis_margins={k:str(v) for k,v in hypotheses.items()},
               first_finite_through=K1-1, first_tail_from=K1,
               second_finite_through=K2-1, second_tail_from=K2,
               first_min_relative=str(minA), first_min_k=minAk,
               second_min_relative=str(minB), second_min_k=minBk,
               second_infinite_tail_gap=str(tail_gap),
               atomic_g=atomic_g, atomic_epsilon=atomic_e,
               seconds=time.monotonic()-started)
    if spectral is not None:
        out['spectral_scalar_verification']=spectral
    result = json.dumps(out,indent=2)+'\n'
    print(result)
    if args.output:
        Path(args.output).write_text(result)


if __name__ == '__main__':
    main()
