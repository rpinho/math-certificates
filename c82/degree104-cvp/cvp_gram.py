"""Local C82 feasibility experiment; all reduced costs are heuristic.

Fresh implementation of the method described by vidigoat PR280/v2 README:
complementary-measure IRLS, independent LLL of H*X^j evaluations,
and budgeted Schnorr--Euchner CVP enumeration. No claimant code is imported.
Uses our inherited core.py only for root-based floating pricing.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import time

import mpmath as mp
import numpy as np
from flint import ctx, fmpz_mat, fmpz_poly
from numba import njit
from core import roots, logabs, logmahlerT


@njit
def enumerate_cvp(R, y, keep, limit):
    """Search projected Euclidean CVP; bounded nodes, no optimality claim."""
    n = len(y)
    z = np.zeros(n, np.int64)
    for k in range(n-1, -1, -1):
        s = y[k]
        for j in range(k+1, n):
            s -= R[k,j]*z[j]
        z[k] = int(np.rint(s/R[k,k]))
    # A finite starting radius from Babai and its coordinate neighbours.
    pool = np.zeros((keep,n), np.int64)
    costs = np.full(keep, np.inf)
    count = 0
    for j in range(2*n+2):
        zz = np.zeros(n,np.int64) if j==2*n+1 else z.copy()
        if j and j<=2*n:
            zz[(j-1)//2] += 1 if j%2 else -1
        diff = R @ zz.astype(np.float64)-y
        cost = diff @ diff
        worst = np.argmax(costs)
        if cost < costs[worst]:
            pool[worst] = zz
            costs[worst] = cost
    radius = np.max(costs)*(1+1e-12)
    partial = np.zeros(n+1)
    center = np.zeros(n)
    step = np.ones(n,np.int64)
    k = n-1
    entering = True
    nodes = 0
    while nodes < limit:
        if entering:
            s = y[k]
            for j in range(k+1,n):
                s -= R[k,j]*z[j]
            center[k] = s/R[k,k]
            z[k] = int(np.rint(center[k]))
            step[k] = 1 if center[k] >= z[k] else -1
        nodes += 1
        err = R[k,k]*(z[k]-center[k])
        distance = partial[k+1]+err*err
        if distance <= radius:
            if k == 0:
                duplicate = False
                for j in range(keep):
                    if np.isfinite(costs[j]) and np.all(pool[j] == z):
                        duplicate = True
                        break
                worst = np.argmax(costs)
                if not duplicate and distance < costs[worst]:
                    pool[worst] = z
                    costs[worst] = distance
                    radius = np.max(costs)*(1+1e-12)
            else:
                partial[k] = distance
                k -= 1
                entering = True
                continue
        else:
            k += 1
            if k == n:
                return pool, costs, nodes, True
        z[k] += step[k]
        step[k] = -step[k]-(1 if step[k]>0 else -1)
        entering = False
    return pool, costs, nodes, False


def coeffs(p):
    return tuple(int(x) for x in reversed(p.coeffs()))


def cvp_self_test():
    import itertools
    R = np.array([[1., .3, -.2], [0., 1.2, .1], [0.,0.,.9]])
    y = np.array([.61, -.77, .45])
    pool,costs,nodes,complete = enumerate_cvp(R,y,8,100000)
    truth = sorted((float(np.sum((R@np.array(z)-y)**2)),z)
                   for z in itertools.product(range(-3,4),repeat=3))[:8]
    assert complete
    assert np.allclose(sorted(costs),[x[0] for x in truth],rtol=1e-12,atol=1e-12)
    return {'status':'PASS','nodes':nodes,'nearest_squared_distance':float(min(costs))}


class Experiment:
    def __init__(self, args):
        self.a = args
        self.start = time.monotonic()
        self.rng = np.random.default_rng(args.seed)
        ctx.prec = 256
        ctx.threads = 1
        mp.mp.prec = 360
        self.state = json.loads(Path(args.state).read_text())
        dual = np.load(args.dual)
        self.t = dual['t']
        self.nu = dual['nu']
        self.lam = float(dual['lam'])
        support = self.nu > 1e-18
        self.ts = self.t[support]
        self.ns = self.nu[support]
        self.nums = [fmpz_poly(r['coeffs'][::-1]) for r in self.state['numerator']]
        self.known = {tuple(r['coeffs']) for r in self.state['denominator']}
        self.warm = [fmpz_poly(r['coeffs'][::-1]) for r in self.state['denominator']]
        old = json.loads(Path(args.library).read_text())
        self.library = [fmpz_poly(r['coeffs'][::-1]) for r in old['denominator']]
        self.public_bank = {coeffs(p) for p in self.library}
        p4 = next(r for r in self.state['numerator'] if r['name']=='P4')
        self.H = fmpz_poly([0,-1,1])*fmpz_poly(p4['coeffs'][::-1])
        assert self.H.degree() == 6
        self.cache = {}
        self.seen = set()
        self.records = []
        self.found = []
        self.best = None
        self.trials = 0
        self.evaluated = 0
        self.iterations = 0
        self.stats = []
        self.selftest = cvp_self_test()
        self.save()
        self.emit('setup', degree=args.degree, samples=args.points,
                  dual_support=len(self.ts), dual_mass=float(self.ns.sum()),
                  lambda_=self.lam, selftest=self.selftest)

    def emit(self, event, **data):
        print(json.dumps(dict(event=event,seconds=time.monotonic()-self.start,**data)),flush=True)

    def score(self,p,source):
        c = coeffs(p)
        if c in self.cache:
            return self.cache[c]
        stamp = time.monotonic()
        rr = roots(c)
        lm = float(logmahlerT(c,rr))
        rc = float(lm-self.ns@logabs(c,self.ts,rr)-self.lam*p.degree())
        result = dict(coeffs=list(c),degree=p.degree(),rc=rc,
                      rc_per_degree=rc/p.degree(),height=lm/p.degree(),
                      source=source,known=c in self.known,
                      public_bank=c in self.public_bank,
                      score_seconds=time.monotonic()-stamp)
        self.evaluated += 1
        allowed = not any(p.gcd(s).degree()>0 for s in self.nums)
        self.cache[c] = rc if allowed else math.inf
        result['coprime_to_numerators'] = allowed
        if allowed and c not in self.known and (self.best is None or rc<self.best['rc']):
            self.best = result
            self.emit('best',degree=p.degree(),rc=rc,rc_per_degree=rc/p.degree())
        if allowed and rc < -2e-8 and c not in self.known:
            # Exact factorisation distinguishes usable new factors from products.
            fac = p.factor()[1]
            result['factors'] = [dict(coeffs=list(coeffs(f)),degree=f.degree(),multiplicity=int(m)) for f,m in fac]
            self.found.append(result)
            self.emit('negative_candidate',degree=p.degree(),rc=rc,
                      factor_degrees=[f.degree() for f,m in fac])
        self.records.append({k:v for k,v in result.items() if k!='coeffs'})
        return rc if allowed else math.inf

    def sampled_powers(self,d):
        # Stratified sampling of uniform minus the re-solved LP dual.
        mass = np.maximum(1/len(self.t)-self.nu,0)
        cdf = np.cumsum(mass)
        cdf /= cdf[-1]
        q = (np.arange(self.a.points)+self.rng.uniform(.15,.85,self.a.points))/self.a.points
        idx = np.searchsorted(cdf,q)
        P = []
        for tt in self.t[idx]:
            z = mp.expjpi(2*mp.mpf(float(tt)))
            w = z*(1-z)
            row = [mp.mpc(1)]
            for j in range(d):
                row.append(row[-1]*w)
            P.append(row)
        return P

    @staticmethod
    def values(p,P):
        cs = [int(x) for x in p.coeffs()]
        return [sum((row[j]*c for j,c in enumerate(cs)),mp.mpc(0)) for row in P]

    def lattice_step(self,current,P,profile):
        start = time.monotonic()
        d = current.degree()
        n = d-self.H.degree()
        bits = self.a.bits
        scale = mp.mpf(2)**bits
        vals = self.values(current,P)
        # High-degree evaluations span many orders of magnitude. A median-
        # relative floor (e.g. 1e-14) would suppress entire arcs and invalidate
        # the IRLS majorisation. Sampling avoids exact zeros; retain all scales.
        floor = min(abs(v) for v in vals)*mp.mpf('1e-30')
        assert floor>0
        weights = [mp.mpf(float(noise))/max(abs(v),floor) for v,noise in zip(vals,profile)]
        # Normalisation rescales the entire objective without changing CVP.
        normal = max(weights)
        weights = [w/normal for w in weights]
        hvals = self.values(self.H,P)
        identity = 1 << max(0,bits-self.a.ridge_bits)
        rows = []
        for j in range(n):
            evaluated = [h*row[j]*w*scale for h,row,w in zip(hvals,P,weights)]
            rows.append([identity if i==j else 0 for i in range(n)]
                        +[int(mp.nint(v.real)) for v in evaluated]
                        +[int(mp.nint(v.imag)) for v in evaluated])
        build_seconds = time.monotonic()-start
        stamp = time.monotonic()
        # Exact Gram-form LLL avoids repeatedly updating 2*points columns.
        # It is the same integer evaluation lattice, with an exact unimodular
        # transformation; no CVP target or polynomial is embedded into LLL.
        matrix = fmpz_mat(rows)
        gram = matrix*matrix.transpose()
        reduced_gram, transform = gram.lll(delta=.99,rep='gram',transform=True)
        assert transform*gram*transform.transpose()==reduced_gram
        red = transform*matrix
        lll_seconds = time.monotonic()-stamp
        # Float QR/enumeration only proposes integer candidates; all polynomial
        # construction stays exact, and full-grid root pricing screens proposals.
        C = [[int(red[j,i])//identity for i in range(n)] for j in range(n)]
        assert all(int(red[j,i])%identity==0 for i in range(n) for j in range(n))
        B = np.ldexp(np.array([[float(red[j,k]) for k in range(red.ncols())] for j in range(n)]),-bits)
        targetvals = [-v*w for v,w in zip(vals,weights)]
        target = np.concatenate([np.zeros(n),[float(v.real) for v in targetvals],
                                 [float(v.imag) for v in targetvals]])
        objective_scale = np.linalg.norm(target)
        B /= objective_scale
        target /= objective_scale
        Q,R = np.linalg.qr(B.T,mode='reduced')
        y = Q.T@target
        z,costs,nodes,complete = enumerate_cvp(R,y,self.a.keep,self.a.nodes)
        proposals = []
        for zz in z:
            if np.max(np.abs(zz))>10**12:
                continue
            u = [sum(int(zz[j])*C[j][i] for j in range(n)) for i in range(n)]
            p = current+self.H*fmpz_poly(u)
            assert p.degree()==d and p.leading_coefficient()==1
            proposals.append(p)
        stat = dict(build_seconds=build_seconds,lll_seconds=lll_seconds,
                    total_seconds=time.monotonic()-start,nodes=int(nodes),
                    enumeration_completed=bool(complete),
                    qr_diagonal_min=float(min(abs(np.diag(R)))),
                    qr_diagonal_max=float(max(abs(np.diag(R)))),
                    unique_proposals=len({coeffs(p) for p in proposals}),
                    dimension=n,ambient_dimension=B.shape[1])
        stat['target_norm_before_rescale'] = float(objective_scale)
        stat['nearest_projected_squared_distance'] = float(min(costs))
        stat['current_projected_squared_distance'] = float(y@y)
        # Diagnostic sampled objectives use independently evaluated polynomials.
        if self.trials==0:
            best_index = int(np.argmin(costs))
            if best_index<len(proposals):
                vv = self.values(proposals[best_index],P)
                stat['exact_sampled_l2_ratio'] = float(sum(abs(x*w)**2 for x,w in zip(vv,weights))/sum(abs(x*w)**2 for x,w in zip(vals,weights)))
                stat['sampled_log_difference'] = float(sum(mp.log(abs(x)/abs(v)) for x,v in zip(vv,vals))/len(P))
        return proposals,stat

    def product_start(self):
        if self.a.degree==104:
            if self.trials%4==0:
                return self.warm[(self.trials//4)%len(self.warm)]
            if self.trials%4==1:
                choices = [p for p in self.library if p.degree()==104]
                return choices[int(self.rng.integers(len(choices)))]
            left = [p for p in self.library if p.degree()==44]
            right = [p for p in self.library if p.degree()==60]
            return left[int(self.rng.integers(len(left)))]*right[int(self.rng.integers(len(right)))]
        # Requested higher degree 120: a public 104 factor times our degree16 P9.
        choices = [p for p in self.library if p.degree()==self.a.degree-104]
        if choices:
            if self.trials%3==2 and self.a.degree==120:
                sixty = [p for p in self.library if p.degree()==60]
                return sixty[int(self.rng.integers(len(sixty)))]*sixty[int(self.rng.integers(len(sixty)))]
            warm = self.warm if self.trials%3==0 else [p for p in self.library if p.degree()==104]
            return warm[int(self.rng.integers(len(warm)))]*choices[int(self.rng.integers(len(choices)))]
        raise ValueError('No exact-degree product start in local library')

    def trial(self):
        started = time.monotonic()
        p = self.product_start()
        d = p.degree()
        P = self.sampled_powers(d)
        # Optional unit shifts change the residue mod P4 while preserving
        # values at 0 and 1. Inverse X and inverse (X-1) exist modulo P4.
        shift = [0,0]
        if self.a.unit_shifts and self.trials%3==2:
            X = fmpz_poly([0,1]); Xm1 = X-1
            C = self.H//(X*Xm1)
            invx = -((C-int(C[0]))//X)*int(C[0])
            invxm1 = -((C-int(C(1)))//Xm1)*int(C(1))
            aa,bb = [int(v) for v in self.rng.integers(-4,5,2)]
            unit = ((X if aa>=0 else invx)**abs(aa)*(Xm1 if bb>=0 else invxm1)**abs(bb))%C
            correction = (((p*unit-p)%C)*invx*invxm1)%C
            p += X*Xm1*correction
            shift = [aa,bb]
        source = dict(trial=self.trials,degree=d,seed=self.a.seed,residue_shift=shift)
        current_rc = self.score(p,dict(source,iteration=-1))
        mode = self.trials%4
        # Independent perturbation profiles; subsequent iterations use exact IRLS.
        if mode==0:
            profile = np.ones(len(P))
        elif mode in (1,2):
            profile = np.exp(self.rng.normal(0,.35 if mode==1 else .9,len(P)))
        else:
            v = self.values(p,P)
            exponent = float(self.rng.uniform(-.3,.3))
            med = sorted(abs(x) for x in v)[len(v)//2]
            profile = np.array([float((max(abs(x),med*mp.mpf('1e-14'))/med)**exponent) for x in v])
        for it in range(self.a.iterations):
            if time.monotonic()-self.start>self.a.seconds:
                break
            proposals,stat = self.lattice_step(p,P,profile)
            self.iterations += 1
            scored = [(current_rc,p)]
            for candidate in proposals:
                try:
                    rc = self.score(candidate,dict(source,iteration=it))
                    scored.append((rc,candidate))
                except (ValueError,RuntimeError,OverflowError) as exc:
                    self.emit('pricing_error',error=repr(exc))
            scored.sort(key=lambda x:x[0])
            rc,new = scored[0]
            stat.update(trial=self.trials,iteration=it,current_rc=current_rc,
                        best_rc=rc,degree=d)
            self.stats.append(stat)
            self.emit('iteration',**stat)
            self.save()
            # Always allow one unperturbed retry if the first perturbed step stalls.
            if coeffs(new)==coeffs(p) or rc>=current_rc-1e-10:
                if it==0 and mode:
                    profile = np.ones(len(P))
                    continue
                break
            p,current_rc = new,rc
            profile = np.ones(len(P))
        self.trials += 1
        self.emit('trial_done',trial=self.trials,degree=d,rc=current_rc,
                  trial_seconds=time.monotonic()-started,evaluated=self.evaluated)
        self.save()

    def save(self):
        result = dict(candidate_unrefereed=True,settings=vars(self.a),
                      elapsed_seconds=time.monotonic()-self.start,pid=os.getpid(),
                      trials=self.trials,iterations=self.iterations,
                      polynomials_scored=self.evaluated,best=self.best,
                      negative_candidates=self.found,iteration_stats=self.stats,
                      score_records=self.records,cvp_selftest=self.selftest,
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        path=Path(self.a.out)
        tmp=path.with_suffix('.tmp')
        tmp.write_text(json.dumps(result,indent=1)+'\n')
        tmp.replace(path)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--state',default='runs/baseline.json')
    ap.add_argument('--dual',default='runs/baseline-dual.npz')
    ap.add_argument('--library',default='prior_sources/final_state_lp.json')
    ap.add_argument('--degree',type=int,default=104)
    ap.add_argument('--points',type=int,default=720)
    ap.add_argument('--seconds',type=int,default=600)
    ap.add_argument('--seed',type=int,default=1104)
    ap.add_argument('--nodes',type=int,default=40000)
    ap.add_argument('--keep',type=int,default=16)
    ap.add_argument('--iterations',type=int,default=8)
    ap.add_argument('--bits',type=int,default=260)
    ap.add_argument('--ridge-bits',type=int,default=190)
    ap.add_argument('--unit-shifts',action='store_true')
    ap.add_argument('--out',default='runs/cvp104.json')
    a=ap.parse_args()
    with open('evidence/pids.jsonl','a') as f:
        f.write(json.dumps(dict(kind='cvp_search',pid=os.getpid(),settings=vars(a)))+'\n')
    e=Experiment(a)
    while time.monotonic()-e.start<a.seconds:
        e.trial()
    e.save()
    e.emit('finished',trials=e.trials,evaluated=e.evaluated)


if __name__=='__main__':
    main()
