#!/usr/bin/env python3
"""Independent C82 referee. Standard library and python-flint only.

Exact hypotheses -> certified roots -> adaptive sign enclosures -> exact
logarithmic antiderivatives (Arb Li_2). No sampled quadrature is used.
See replay/report.md for the interval and branch arguments.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import time
from flint import arb, acb, fmpz_poly, ctx


def require(ok, message):
    if not ok:
        raise ValueError(message)


def A(q):
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def dyadic(x):
    m, e = x.man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def interval(x):
    require(x.is_finite(), 'nonfinite output')
    lo, hi = dyadic(x.lower()), dyadic(x.upper())
    return {'ball': str(x), 'lower': str(lo), 'upper': str(hi)}


def exact(c):
    den, num = [], []
    for section, out in [('denominator', den), ('numerator', num)]:
        require(isinstance(c[section], list), 'factor list required')
        for row in c[section]:
            coeffs = row['coeffs']
            require(isinstance(coeffs, list) and coeffs and
                    all(type(v) is int for v in coeffs) and coeffs[0] != 0,
                    'nonzero integer polynomial required')
            p = fmpz_poly(list(reversed(coeffs)))
            if section == 'denominator':
                require(p.degree() > 0 and coeffs[0] == 1, 'denominator must be nonconstant and monic')
                w = row['multiplicity']
                require(type(w) is int and w > 0, 'multiplicity must be positive integer')
            else:
                require(isinstance(row['q_rational'], str), 'exact rational string required')
                w = Fraction(row['q_rational'])
                require(w >= 0, 'negative exponent')
                if not w:
                    continue
            out.append((row['name'], p, w))
    D = sum(p.degree()*w for _, p, w in den)
    a = sum((p.degree()*w for _, p, w in num), Fraction(0))
    require(D > 0 and a < D, 'strict weighted degree inequality failed')
    for sn, s, _ in num:
        for rn, r, _ in den:
            require(s.gcd(r).degree() == 0, 'noncoprime active pair: '+sn+', '+rn)
    b = math.lcm(*(w.denominator for _, _, w in num)) if num else 1
    return den, num, D, a, b


class Replay:
    def __init__(self, certificate, quiet=False):
        den, num, D, a, b = exact(certificate)
        self.meta = {'D': D, 'a': str(a), 'slack': str(D-a), 'b': b,
                     'denominators': len(den), 'active_numerators': len(num),
                     'gcd_pairs': len(den)*len(num)}
        self.terms = []
        self.constant = arb(0)
        self.H = arb(0)
        self.numerator_mean = arb(0)
        self.root_records = []
        self.quiet = quiet
        self.pi2 = 2*arb.pi()
        T = fmpz_poly([0, 1, -1])
        for label, factors, sign in [('denominator', den, -1), ('numerator', num, 1)]:
            for name, p, weight in factors:
                P = p(T)
                require(P.degree() == 2*p.degree(), 'composition degree mismatch')
                roots = P.complex_roots()
                require(sum(m for _, m in roots) == P.degree(), 'incomplete certified root list')
                require(all(r.is_finite() and type(m) is int and m > 0 for r, m in roots), 'invalid root enclosure')
                lead = arb(abs(int(P.leading_coefficient()))).log()
                w = A(Fraction(sign*weight, D))
                self.constant += w*lead
                M = lead
                uncertain = 0
                for r, mult in roots:
                    rho = abs(r)
                    M += mult*rho.max(1).log()
                    mode = 'inside' if rho < 1 else 'outside' if rho > 1 else 'boundary'
                    uncertain += (mode == 'boundary')*mult
                    # A denominator root on the circle is not handled by this
                    # specialization; fail closed instead of silently dropping it.
                    require(label != 'denominator' or mode != 'boundary',
                            'denominator unit-circle separation not certified')
                    self.terms.append((r, w*mult, rho, mode))
                if label == 'denominator':
                    self.H += A(Fraction(weight, D))*M
                else:
                    self.numerator_mean += A(Fraction(weight, D))*M
                self.root_records.append({'kind': label, 'name': name, 'degree': P.degree(),
                                          'roots_with_multiplicity': sum(m for _, m in roots),
                                          'unit_modulus_unseparated': uncertain,
                                          'log_mahler': interval(M)})
                self.say('roots', label, name, P.degree(), 'boundary', uncertain)
        self.meta['composed_roots'] = sum(v['roots_with_multiplicity'] for v in self.root_records)
        self.say('H', self.H)

    def say(self, *args):
        if not self.quiet:
            print(*args, flush=True)

    def bounds(self, lo, hi):
        """Range of g over [lo,hi], with explicit singular upper bound.

        For theta displacement |s|<=h, |e^(i(theta+s))-e^itheta|<=h.
        If d=|z-r|-h>0, |d²/dtheta² log|e^itheta-r||<=|r|/d².
        Signed first derivatives are summed before taking absolute values.
        The independent direct distance bounds also handle numerator zeros.
        """
        mid = (lo+hi)/2
        h = A((hi-lo)/2)*self.pi2
        z = (acb(0, A(mid)*self.pi2)).exp()
        upper = self.constant.upper()
        lower = self.constant.lower()
        center = self.constant
        deriv = arb(0)
        second = arb(0)
        smooth = True
        for r, w, rho, mode in self.terms:
            dz = z-r
            distance = abs(dz)
            low = (distance-h).lower()
            high = (distance+h).upper()
            # Reverse triangle inequality gives an additional global bound.
            radial = abs(rho-1).lower()
            low = low.max(radial).max(0)
            loghi = high.log()
            loglo = low.log() if low > 0 else arb('-inf')
            if w > 0:
                upper += w*loghi
                lower += w*loglo
            else:
                upper += w*loglo
                lower += w*loghi
            if low > 0 and distance > 0:
                center += w*distance.log()
                deriv -= w*(r/dz).imag
                second += abs(w)*rho/(low*low)
            else:
                smooth = False
        if smooth:
            radius = abs(deriv)*h + second*h*h/2
            lower = lower.max((center-radius).lower())
            upper = upper.min((center+radius).upper())
        return lower.lower(), upper.upper()

    def primitive_integral(self, lo, hi):
        """Integral of g on a proved-positive interval, in turn coordinates."""
        a, b = A(lo)*self.pi2, A(hi)*self.pi2
        za, zb = acb(0,a).exp(), acb(0,b).exp()
        result = self.constant*A(hi-lo)
        for r, w, rho, mode in self.terms:
            if mode == 'outside':
                # |1/r|<1, hence the principal dilogarithm never crosses its cut.
                v = rho.log()*A(hi-lo) - ((zb/r).polylog(2)-(za/r).polylog(2)).imag/self.pi2
            else:
                if mode == 'boundary':
                    # Uniform branch proof even if the root ball straddles |r|=1.
                    arc = acb(0,-a.union(b)).exp()
                    image = r*arc
                    if not (not image.imag.contains(0) or image.real < 1):
                        # Split only the antiderivative evaluation; the sign proof
                        # for the parent remains valid for both children.
                        require(hi-lo > Fraction(1,2**180), 'unresolved dilogarithm branch')
                        m = (lo+hi)/2
                        return self.primitive_integral(lo,m)+self.primitive_integral(m,hi)
                v = ((r/zb).polylog(2)-(r/za).polylog(2)).imag/self.pi2
            require(v.is_finite(), 'nonfinite dilogarithm enclosure')
            result += w*v
        return result

    def run(self, cell_tolerance=Fraction(1,10**23), max_cells=1000000):
        stack = [(Fraction(0), Fraction(1,2), 0)]
        positive = []
        uncertain = arb(0)
        cells = negative = unresolved = 0
        max_depth = 0
        last = time.monotonic()
        while stack:
            lo, hi, depth = stack.pop()
            cells += 1
            require(cells <= max_cells and depth < 180, 'subdivision resource limit')
            lower, upper = self.bounds(lo,hi)
            max_depth = max(max_depth,depth)
            if upper <= 0:
                negative += 1
            elif lower >= 0:
                if positive and positive[-1][1] == lo:
                    positive[-1] = (positive[-1][0], hi)
                else:
                    positive.append((lo,hi))
            elif upper.is_finite() and upper*A(hi-lo) < A(cell_tolerance):
                uncertain += arb(0).union(upper*A(hi-lo))
                unresolved += 1
            else:
                m = (lo+hi)/2
                stack.append((m,hi,depth+1))
                stack.append((lo,m,depth+1))
            if time.monotonic()-last > 20:
                self.say('tiling', cells, 'position', float(lo), 'positive_runs', len(positive),
                         'negative', negative, 'unresolved', unresolved, 'depth',max_depth)
                last = time.monotonic()
        J = uncertain
        for k,(lo,hi) in enumerate(positive):
            J += self.primitive_integral(lo,hi)
            if time.monotonic()-last > 20:
                self.say('integrating positive runs',k+1,'/',len(positive))
                last=time.monotonic()
        J *= 2 # real-coefficient symmetry g(1-t)=g(t)
        require(J.is_finite(), 'nonfinite integral')
        self.meta.update(cells=cells, negative_cells=negative, positive_runs=len(positive),
                         unresolved_cells=unresolved, max_depth=max_depth,
                         unresolved_integral=interval(2*uncertain))
        self.say('J',J,'B',self.H+J)
        return self.H+J, J


def controls(c, original_B):
    outcomes = {}
    for name, change in [
        ('perturbed_coefficient', lambda x: x['denominator'][0]['coeffs'].__setitem__(0,2)),
        ('perturbed_exponent', lambda x: x['numerator'][0].__setitem__('q_rational','-1')),
        ('degree_violation', lambda x: x['numerator'][0].__setitem__('q_rational','100000000000000000000')),
        ('common_factor', lambda x: x['numerator'].append({'name':'gcd_control','coeffs':x['denominator'][0]['coeffs'],'q_rational':'1'}))]:
        bad=copy.deepcopy(c); change(bad)
        try:
            exact(bad)
        except (ValueError, ZeroDivisionError) as e:
            outcomes[name]={'status':'REJECTED','reason':str(e)}
        else:
            raise ValueError('control was not rejected: '+name)
    # Q(X)=X, A(X)=1: H=0, B=int log^+(2 sin(pi t))dt.
    # Its support is (1/6,5/6); B=Im Li_2(exp(i*pi/3))/pi.
    # For this analytic case only, Q(T) has a circle root, so exercise the
    # same integrator with the equivalent g=log|1-e^(2*pi*i*t)| and H=0.
    test=Replay.__new__(Replay)
    test.meta={}; test.constant=arb(0); test.H=arb(0); test.quiet=True
    test.pi2=2*arb.pi(); test.terms=[(acb(1),arb(1),arb(1),'boundary')]
    got,J=test.run(Fraction(1,10**24))
    known=acb(0,arb.pi()/3).exp().polylog(2).imag/arb.pi()
    require(got.overlaps(known) and got.rad() < arb('1e-20'), 'analytic control failed')
    outcomes['analytic_log_sine']={'status':'PASS','computed':interval(got),'known':interval(known),
                                  'formula':'Im Li_2(exp(i*pi/3))/pi'}
    # Full exact-algebra/root/integration pipeline: Q=X-3, A=1.
    # On the circle |3-z+z^2| >= 3-|z|-|z|^2=1, so J=0.
    # Both roots of z^2-z+3 have modulus sqrt(3), giving H=log(3).
    elementary={'denominator':[{'name':'X-3','coeffs':[1,-3],'multiplicity':1}],
                'numerator':[{'name':'one','coeffs':[1],'q_rational':'1'}]}
    synthetic=Replay(elementary, quiet=True)
    elem, _=synthetic.run()
    require(elem.overlaps(arb(3).log()) and elem.rad()<arb('1e-60'), 'elementary analytic case failed')
    outcomes['analytic_log3']={'status':'PASS','computed':interval(elem),'known':interval(arb(3).log())}
    # Valid, single-coefficient perturbation: P1=X becomes 2X. No monicity
    # restriction applies to numerators. Jensen gives B >= numerator mean.
    valid_coefficient=copy.deepcopy(c)
    require(valid_coefficient['numerator'][0]['coeffs']==[1,0], 'P1 control requires X')
    valid_coefficient['numerator'][0]['coeffs'][0]=2
    changed=Replay(valid_coefficient,quiet=True)
    require(changed.numerator_mean > original_B, 'valid coefficient change not separated')
    outcomes['valid_coefficient_change']={'status':'CHANGED','change':'P1: X -> 2X',
        'B_lower_bound':str(dyadic(changed.numerator_mean.lower())),
        'reason':'B is at least the numerator log-Mahler mean, now above original B'}
    # Valid exponent perturbation: q(P1)=0. An interval contribution alone
    # proves the new B exceeds the entire original enclosure.
    valid_exponent=copy.deepcopy(c)
    valid_exponent['numerator'][0]['q_rational']='0'
    changed=Replay(valid_exponent,quiet=True)
    for k in range(1,160):
        lo,hi=Fraction(k,1000),Fraction(k,1000)+Fraction(1,10000)
        lower,_=changed.bounds(lo,hi)
        bound=changed.H+2*A(hi-lo)*lower.max(0)
        if bound > original_B:
            outcomes['valid_exponent_change']={'status':'CHANGED','change':'q(P1) -> 0',
                'witness_interval':[str(lo),str(hi)],'g_lower_bound':str(dyadic(lower)),
                'B_lower_bound':str(dyadic(bound.lower()))}
            break
    require('valid_exponent_change' in outcomes, 'valid exponent change not separated')
    return outcomes


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=Path(__file__).resolve().parent.parent/'inputs/certificates/certificate.json')
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'result.json')
    parser.add_argument('--bits',type=int,default=256)
    parser.add_argument('--cell-tolerance',default='1e-23')
    parser.add_argument('--target',default='0.2520179248')
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    require(args.bits>=192,'precision below required 192 bits')
    ctx.prec=args.bits; ctx.threads=1
    started=time.monotonic()
    print('PID',os.getpid(),'precision',ctx.prec,'FLINT threads',ctx.threads,flush=True)
    data=args.certificate.read_bytes(); c=json.loads(data)
    obj=Replay(c)
    B,J=obj.run(Fraction(args.cell_tolerance))
    target=Fraction(args.target)
    passed=dyadic(B.upper())<target
    result={'status':'PASS' if passed else 'FAIL','precision_bits':ctx.prec,'pid':os.getpid(),
            'certificate_sha256':hashlib.sha256(data).hexdigest(),'exact':obj.meta,
            'H':interval(obj.H),'J':interval(J),'B':interval(B),'target':str(target),
            'target_margin_lower':str(target-dyadic(B.upper())),
            'roots':obj.root_records}
    if args.controls:
        result['controls']=controls(c,B)
        false=Fraction('0.2520179247')
        require(dyadic(B.lower())>false,'false target not conclusively rejected')
        result['controls']['false_target']={'status':'REJECTED','target':str(false),'reason':'target is below certified lower endpoint'}
    result['seconds']=time.monotonic()-started
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('FINAL',result['status'],json.dumps(result['B']), 'seconds',result['seconds'],flush=True)
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
