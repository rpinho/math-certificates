"""Separately written (same agent) two-sided interval replay of the fixed PR301 construction.

Imports no search, baseline, submitted checker, or prior review code.
Exact Z[z] composition and certified FLINT root isolation; four-node Gaussian
quadrature on proven-positive cells; clipped-affine integration on crossings.
See NUMERICS.md for the proof of every panel enclosure.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import time
import flint
from flint import acb, arb, ctx, fmpz_poly

EXPECTED = '520d8104d9c64137f6d436e365ad9b5c6b6a36ed1abb34f32a5dcb9b2e69c5cd'

def ball(q):
    q = Fraction(q)
    return arb(q.numerator)/q.denominator

def exact_endpoint(x):
    m, e = x.man_exp()
    return {'mantissa': str(m), 'exponent': int(e)}

def describe(x):
    assert x.is_finite()
    return {'ball': str(x), 'lower': exact_endpoint(x.lower()),
            'upper': exact_endpoint(x.upper())}

class Replay:
    def __init__(self, path, precision, offset):
        assert precision >= 256
        ctx.prec = precision
        ctx.threads = 1
        self.raw = Path(path).read_bytes()
        self.sha = hashlib.sha256(self.raw).hexdigest()
        if self.sha != EXPECTED:
            raise ValueError('REJECT: certificate SHA256 differs from pinned packet')
        cert = json.loads(self.raw)
        den, num = [], []
        for kind, dest in [('denominator', den), ('numerator', num)]:
            for rec in cert[kind]:
                a = rec['coeffs']
                assert len(a)>1 and all(type(v) is int for v in a) and a[0]
                p = fmpz_poly(a[::-1])
                if kind == 'denominator':
                    q = rec['multiplicity']
                    assert abs(a[0]) == 1 and type(q) is int and q>0
                    q = Fraction(q)
                else:
                    q = Fraction(rec['q_rational'])
                    assert q>=0
                if q:
                    dest.append((p, q))
        self.D = sum(p.degree()*q for p,q in den)
        self.A = sum(p.degree()*q for p,q in num)
        assert self.D>0 and self.A<self.D
        pairs = 0
        for p,q in num:
            for r,m in den:
                assert p.gcd(r).degree() == 0
                pairs += 1
        self.groups = []
        self.constant = ball(offset)
        self.mahler = arb(0)
        self.tau = 2*arb.pi()
        root_count = 0
        T = fmpz_poly([0,1,-1])
        for sign, group in [(-1, den), (1, num)]:
            for p, q in group:
                composed = fmpz_poly([0])
                for coefficient in reversed(p.coeffs()):
                    composed = composed*T+coefficient
                assert composed.degree() == 2*p.degree()
                roots = composed.complex_roots()
                assert sum(m for r,m in roots) == composed.degree()
                w = ball(sign*q/self.D)
                leading_log = arb(abs(int(composed.leading_coefficient()))).log()
                self.constant += w*leading_log
                data = []
                for r,m in roots:
                    assert r.is_finite()
                    ar = abs(r)
                    # Positive-coefficient Eulerian polynomial A_7(ar).
                    e7 = 1+120*ar+1191*ar**2+2416*ar**3+1191*ar**4+120*ar**5+ar**6
                    data.append((r, m, ar,
                                 abs(w)*m*self.tau**2*ar,
                                 abs(w)*m*self.tau**8*ar*e7))
                    if sign == -1:
                        self.mahler -= w*m*ar.max(1).log()
                if sign == -1:
                    self.mahler -= w*leading_log
                self.groups.append((w, data))
                root_count += composed.degree()
        s = arb(30).sqrt()
        self.nodes = [((15-2*s)/35).sqrt(), ((15+2*s)/35).sqrt()]
        self.weights = [(18+s)/36, (18-s)/36]
        self.audit = dict(D=int(self.D), degree_A=str(self.A),
                          coprimality_pairs=pairs, composed_roots=root_count,
                          denominator_factors=len(den), numerator_factors=len(num))

    def value(self, t):
        u = acb(0,self.tau*t).exp()
        g = self.constant
        for w, data in self.groups:
            product = arb(1)
            for r,m,ar,c2,c8 in data:
                product *= abs(u-r)**m
            g += w*product.log()
        return g

    def panel(self, k, depth, tolerance):
        width = arb(1)/(1<<depth)
        h = width/2
        mid = arb(2*k+1)/(1<<(depth+1))
        u = acb(0,self.tau*mid).exp()
        displacement = self.tau*h
        upper = self.constant
        center = self.constant
        derivative = acb(0)
        m2, m8 = arb(0), arb(0)
        separated = True
        valid_upper = True
        for w, data in self.groups:
            product = arb(1)
            far_product = arb(1)
            near_product = arb(1)
            group_separated = True
            for r,m,ar,c2,c8 in data:
                difference = u-r
                distance = abs(difference)
                near = distance-displacement
                far_product *= (distance+displacement)**m
                product *= distance**m
                if near>0:
                    near_product *= near**m
                    m2 += c2/near**2
                    m8 += c8/near**8
                    derivative += w*m*acb(0,self.tau)*u/difference
                else:
                    group_separated = False
                    separated = False
            if w>0:
                upper += w*far_product.log()
            elif group_separated:
                upper += w*near_product.log()
            else:
                valid_upper = False
            center += w*product.log()
        if valid_upper and upper<0:
            return arb(0), 'negative'
        if not separated:
            return None, None
        assert center.is_finite() and derivative.is_finite()
        slope = derivative.real
        reach = abs(slope)*h+m2*h*h/2
        if center+reach<0:
            return arb(0), 'negative'
        if center-reach>0:
            error = m8*width**9/1778112000
            if not error < tolerance*width/8:
                return None, None
            quadrature = arb(0)
            for node, weight in zip(self.nodes,self.weights):
                quadrature += weight*(self.value(mid+h*node)+self.value(mid-h*node))
            estimate = quadrature*h
            enclosure = estimate + arb(0,error.upper())
            kind = 'gauss_positive'
        else:
            # Integrate the positive part of the affine Taylor polynomial
            # exactly (with ball parameters); positive part is 1-Lipschitz.
            error = m2*width**3/24
            if slope>0 or slope<0:
                left = (center-slope*h).max(0)
                right = (center+slope*h).max(0)
                estimate = (right**2-left**2)/(2*slope)
            else:
                estimate = width*center.max(0)
                error += abs(slope)*width**2/4
            enclosure = estimate + arb(0,error.upper())
            kind = 'clipped_affine'
        if not enclosure.is_finite() or not enclosure.rad()<tolerance*width:
            return None, None
        return enclosure, kind

    def integrate(self, tolerance):
        answer = arb(0)
        counts = Counter()
        maxdepth, visited = 1, 0
        last = time.monotonic()
        # Real coefficients imply g(1-t)=g(t); exact half-circle tiling.
        stack = [(0,1)]
        while stack:
            k,depth = stack.pop()
            maxdepth = max(maxdepth,depth)
            enclosure,kind = self.panel(k,depth,tolerance)
            visited += 1
            if enclosure is None:
                if depth>=70:
                    raise RuntimeError('REJECT: unresolved panel at depth limit')
                stack.extend([(2*k+1,depth+1),(2*k,depth+1)])
            else:
                answer += enclosure
                counts[kind] += 1
            if time.monotonic()-last>30:
                print(json.dumps(dict(event='progress',visited=visited,counts=dict(counts),
                                      t=float(arb(k)/(1<<depth)),max_depth=maxdepth)),flush=True)
                last = time.monotonic()
        return 2*answer, dict(visited=visited,counts=dict(counts),max_depth=maxdepth)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',default='pinned/certificate.json')
    p.add_argument('--precision',type=int,default=256)
    p.add_argument('--tol',default='1e-17')
    p.add_argument('--target',default='0.253091834')
    p.add_argument('--offset',default='0',help='artificial integrand shift for controls')
    p.add_argument('--out',default='interval_256.json')
    a = p.parse_args()
    started = time.monotonic()
    print(json.dumps(dict(event='start',pid=os.getpid(),nice=os.getpriority(os.PRIO_PROCESS,0),
                          settings=vars(a))),flush=True)
    r = Replay(a.certificate,a.precision,a.offset)
    print(json.dumps(dict(event='initialized',audit=r.audit,mahler=str(r.mahler),
                          seconds=time.monotonic()-started)),flush=True)
    tolerance = ball(a.tol)
    assert tolerance>0
    integral, panels = r.integrate(tolerance)
    bound = r.mahler+integral
    margin = ball(a.target)-bound
    passed = bool(margin>0)
    rejected = bool(margin<0)
    result = dict(status='PASS' if passed else 'REJECT' if rejected else 'INCONCLUSIVE',
                  candidate_unrefereed=True, artificial_integrand_offset=a.offset,
                  certificate_sha256=r.sha, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  precision_bits=a.precision,tolerance=a.tol,target=a.target,
                  pid=os.getpid(), python_flint=flint.__version__,
                  audit=r.audit,panels=panels,mahler_normalized=describe(r.mahler),
                  integral_normalized=describe(integral),integral_unnormalized=describe(integral*ball(r.D)),
                  bound=describe(bound),margin=describe(margin),seconds=time.monotonic()-started)
    Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return 0 if passed else 1

if __name__ == '__main__':
    raise SystemExit(main())
