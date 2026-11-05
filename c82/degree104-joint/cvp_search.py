"""Fresh weighted-evaluation LLL/CVP column generator for degree 104.

Method: Patankar PR280; residue restriction and prices: Pinho PR301.
Written for c82r5, without importing/copying old search/helper modules.
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
from flint import ctx,fmpz_mat,fmpz_poly
from numba import njit
from numerics import register,write_json,roots,root_logs,mahler_T,transformed_points

@njit
def nearest_points(triangle,target,keep,budget):
    """Budgeted Schnorr–Euchner depth-first enumeration, retaining distinct points."""
    n=len(target)
    babai=np.zeros(n,np.int64)
    for level in range(n-1,-1,-1):
        babai[level]=int(np.rint((target[level]-np.dot(triangle[level,level+1:],babai[level+1:].astype(np.float64)))/triangle[level,level]))
    bank=np.zeros((keep,n),np.int64)
    loss=np.full(keep,np.inf)
    # Distinct Babai neighbours provide a finite radius without duplicate slots.
    seed_count=2*n*(keep//(2*n)+2)+1
    for seed in range(seed_count+1):
        v=babai.copy()
        if 1<=seed<=seed_count-1:
            axis=((seed-1)//2)%n
            magnitude=(seed-1)//(2*n)+1
            v[axis]+=magnitude if seed%2 else -magnitude
        if seed==seed_count:v[:]=0
        duplicate=False
        for j in range(keep):
            if np.isfinite(loss[j]) and np.all(bank[j]==v):duplicate=True
        if duplicate:continue
        residual=triangle@v.astype(np.float64)-target
        cost=np.dot(residual,residual)
        worst=np.argmax(loss)
        if cost<loss[worst]:bank[worst]=v;loss[worst]=cost
    vector=np.zeros(n,np.int64)
    partial=np.zeros(n+1)
    centers=np.zeros(n)
    pivots=np.zeros(n,np.int64)
    offsets=np.zeros(n,np.int64)
    lower=np.zeros(n,np.int64);upper=np.zeros(n,np.int64)
    level=n-1;enter=True;nodes=0
    while level<n and nodes<budget:
        radius=np.max(loss)*(1+1e-12)+1e-30
        if enter:
            rhs=target[level]
            for j in range(level+1,n):rhs-=triangle[level,j]*vector[j]
            centers[level]=rhs/triangle[level,level]
            available=max(0.,radius-partial[level+1])
            spread=math.sqrt(available)/abs(triangle[level,level])
            # Bounds only guide proposals; invalid ill-conditioned cases are skipped.
            if abs(centers[level])+spread>1e12:return bank,loss,nodes,False
            lower[level]=math.ceil(centers[level]-spread)
            upper[level]=math.floor(centers[level]+spread)
            pivots[level]=int(np.rint(centers[level]));offsets[level]=0
        off=offsets[level]
        direction=1 if centers[level]>=pivots[level] else -1
        v=pivots[level]
        if off>0:v+=direction*((off+1)//2)*(1 if off%2 else -1)
        offsets[level]+=1
        maxdistance=max(abs(upper[level]-pivots[level]),abs(lower[level]-pivots[level]))
        if off>2*maxdistance+2 or lower[level]>upper[level]:
            level+=1;enter=False;continue
        nodes+=1
        if v<lower[level] or v>upper[level]:enter=False;continue
        vector[level]=v
        error=triangle[level,level]*(v-centers[level])
        total=partial[level+1]+error*error
        if total>radius:enter=False;continue
        if level>0:
            partial[level]=total;level-=1;enter=True;continue
        duplicate=False
        for j in range(keep):
            if np.all(bank[j]==vector):duplicate=True;break
        worst=np.argmax(loss)
        if not duplicate and total<loss[worst]:bank[worst]=vector;loss[worst]=total
        enter=False
    return bank,loss,nodes,level==n


def descending(p):return tuple(int(c) for c in reversed(p.coeffs()))
def polynomial(c):return fmpz_poly(list(c)[::-1])

def enumeration_check():
    import itertools
    rng=np.random.default_rng(9831)
    errors=[]
    for case in range(12):
        R=np.triu(rng.normal(0,.25,(3,3)))
        for j in range(3):R[j,j]=rng.choice([-1,1])*rng.uniform(.7,1.4)
        y=rng.uniform(-1,1,3)
        _,cost,_,complete=nearest_points(R,y,16,100000)
        truth=sorted(float(np.sum((R@np.array(v)-y)**2)) for v in itertools.product(range(-7,8),repeat=3))[:16]
        errors.append(float(np.max(np.abs(np.sort(cost)-truth))))
        assert complete and np.allclose(np.sort(cost),truth,atol=1e-12,rtol=1e-12)
    return {'cases':12,'maximum_distance_error':max(errors)}

class Search:
    def __init__(self,a):
        self.a=a;self.wall=time.monotonic();self.cpu=time.process_time();self.rng=np.random.default_rng(a.seed)
        ctx.prec=256;ctx.threads=1;mp.mp.prec=380
        self.state=json.loads(Path(a.state).read_text());dual=np.load(a.dual)
        self.t=dual['t'];self.nu=dual['nu'];self.lam=float(dual['lam'])
        positive=self.nu>1e-18
        self.price_points=transformed_points(self.t[positive]);self.price_mass=self.nu[positive]
        self.cdf=np.cumsum(np.maximum(1/len(self.t)-self.nu,0));self.cdf/=self.cdf[-1]
        self.bank=json.loads(Path(a.bank).read_text())
        self.warm=[polynomial(r['coeffs']) for r in self.state['denominator']]
        self.archive=[polynomial(r['coeffs']) for r in self.bank['denominator']]
        self.numerators=[polynomial(r['coeffs']) for r in self.state['numerator']]
        self.known={tuple(r['coeffs']) for r in self.state['denominator']}
        self.H=fmpz_poly([0,-1,1])*polynomial(next(r['coeffs'] for r in self.state['numerator'] if r['name']=='P4'))
        assert self.H.degree()==6
        self.cache={};self.found=[];self.stats=[];self.trials=0;self.priced=0;self.best=None
        self.selftest=enumeration_check();self.save()
        self.emit('start',pid=os.getpid(),settings=vars(a),enumeration=self.selftest)

    def emit(self,event,**kw):print(json.dumps({'event':event,'elapsed':time.monotonic()-self.wall,**kw}),flush=True)
    def save(self):
        write_json(self.a.out,{'candidate_unrefereed':True,'settings':vars(self.a),'pid':os.getpid(),
            'elapsed':time.monotonic()-self.wall,'cpu_seconds':time.process_time()-self.cpu,
            'trials':self.trials,'priced':self.priced,'negative_candidates':self.found,
            'best':self.best,'iterations':self.stats,'enumeration_check':self.selftest})

    def price(self,p):
        c=descending(p)
        if c in self.cache:return self.cache[c]
        rr=roots(c);rc=mahler_T(c,rr)-self.price_mass@root_logs(c,self.price_points,rr)-p.degree()*self.lam
        self.priced+=1
        if any(p.gcd(q).degree()>0 for q in self.numerators):rc=math.inf
        self.cache[c]=float(rc)
        if c not in self.known and math.isfinite(rc) and (self.best is None or rc<self.best['rc']):
            self.best={'coeffs':list(c),'rc':float(rc),'trial':self.trials}
            self.emit('best',rc=float(rc),priced=self.priced)
        if rc< -2e-8 and c not in self.known:
            fs=p.factor()[1]
            record={'coeffs':list(c),'rc':float(rc),'trial':self.trials,
                'name':'C82r6_'+hashlib.sha256(str(c).encode()).hexdigest()[:12],
                'factors':[{'coeffs':list(descending(f)),'multiplicity':int(m)} for f,m in fs]}
            self.found.append(record);self.emit('negative',rc=float(rc),factor_degrees=[f.degree() for f,m in fs]);self.save()
        return float(rc)

    def start_polynomial(self):
        mode=self.trials%4
        if mode==0:return self.warm[(self.trials//4)%len(self.warm)]
        if mode==1:
            choices=[p for p in self.archive if p.degree()==104]
            return choices[int(self.rng.integers(len(choices)))]
        left=[p for p in self.archive if p.degree()==44];right=[p for p in self.archive if p.degree()==60]
        return left[int(self.rng.integers(len(left)))]*right[int(self.rng.integers(len(right)))]

    def samples(self):
        quantiles=(np.arange(self.a.points)+self.rng.uniform(.15,.85,self.a.points))/self.a.points
        indices=np.searchsorted(self.cdf,quantiles)
        ts=self.t[indices]
        pts=[]
        for t in ts:
            z=mp.expjpi(2*mp.mpf(float(t)));pts.append(z*(1-z))
        powers=[[mp.mpc(1) for _ in pts]]
        for j in range(104):powers.append([v*z for v,z in zip(powers[-1],pts)])
        return pts,powers

    @staticmethod
    def eval_poly(p,pts):
        c=descending(p);v=[mp.mpc(c[0]) for _ in pts]
        for coefficient in c[1:]:v=[x*z+coefficient for x,z in zip(v,pts)]
        return v

    def propose(self,p,pts,powers,profile):
        begun=time.monotonic();n=p.degree()-self.H.degree()
        values=self.eval_poly(p,pts);hvalues=self.eval_poly(self.H,pts)
        weights=[mp.mpf(float(a))/abs(b) for a,b in zip(profile,values)]
        norm=max(weights);weights=[w/norm for w in weights]
        scale=mp.mpf(2)**260;ridge=1<<70
        real_rows=[]
        for j in range(n):
            v=[h*x*w*scale for h,x,w in zip(hvalues,powers[j],weights)]
            real_rows.append([ridge if k==j else 0 for k in range(n)]+
                             [int(mp.nint(x.real)) for x in v]+[int(mp.nint(x.imag)) for x in v])
        lattice=fmpz_mat(real_rows);gram=lattice*lattice.transpose()
        reduced,change=gram.lll(delta=.99,rep='gram',transform=True)
        assert change*gram*change.transpose()==reduced
        lattice=change*lattice
        transform=[[int(change[i,j]) for j in range(n)] for i in range(n)]
        floats=np.array([[float(lattice[i,j]) for j in range(lattice.ncols())] for i in range(n)])*2.**-260
        target=np.r_[np.zeros(n),[float(-v.real*w) for v,w in zip(values,weights)],
                                  [float(-v.imag*w) for v,w in zip(values,weights)]]
        normalization=np.linalg.norm(target);floats/=normalization;target/=normalization
        Q,R=np.linalg.qr(floats.T,mode='reduced');y=Q.T@target
        vectors,costs,nodes,finished=nearest_points(R,y,self.a.keep,self.a.nodes)
        result=[]
        for v in vectors:
            if np.max(np.abs(v))>1e12:continue
            u=[sum(int(v[i])*transform[i][j] for i in range(n)) for j in range(n)]
            q=p+self.H*fmpz_poly(u)
            assert q.degree()==104 and int(q.leading_coefficient())==1
            result.append(q)
        stat={'seconds':time.monotonic()-begun,'nodes':int(nodes),'completed':bool(finished),
              'nearest_projected':float(min(costs)),'current_projected':float(y@y),
              'unique_proposals':len(set(descending(q) for q in result))}
        return result,stat

    def trial(self):
        p=self.start_polynomial();current=self.price(p);pts,powers=self.samples()
        mode=self.trials%4
        profile=np.ones(len(pts)) if mode==0 else np.exp(self.rng.normal(0,.35 if mode==1 else .9,len(pts)))
        for iteration in range(self.a.iterations):
            if time.monotonic()-self.wall>self.a.seconds:break
            candidates,stat=self.propose(p,pts,powers,profile)
            best=p;best_rc=current
            for q in candidates:
                rc=self.price(q)
                if rc<best_rc-1e-10:best=q;best_rc=rc
            stat.update({'trial':self.trials,'iteration':iteration,'current_rc':current,'best_rc':best_rc})
            self.stats.append(stat);self.emit('iteration',**stat);self.save()
            if descending(best)==descending(p):
                if iteration==0 and mode:profile=np.ones(len(pts));continue
                break
            p=best;current=best_rc;profile=np.ones(len(pts))
        self.trials+=1;self.save();self.emit('trial_done',trials=self.trials,priced=self.priced,rc=current)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',default='runs/baseline.json');ap.add_argument('--dual',default='runs/baseline-dual.npz')
    ap.add_argument('--bank',default='prior_sources/factor-bank.json');ap.add_argument('--points',type=int,default=1024)
    ap.add_argument('--seconds',type=int,default=600);ap.add_argument('--seed',type=int,default=5104)
    ap.add_argument('--iterations',type=int,default=8);ap.add_argument('--keep',type=int,default=16);ap.add_argument('--nodes',type=int,default=4000000)
    ap.add_argument('--out',default='runs/search-0.json');a=ap.parse_args();register('cvp')
    experiment=Search(a)
    while time.monotonic()-experiment.wall<a.seconds:experiment.trial()
    experiment.emit('finished',trials=experiment.trials,priced=experiment.priced);experiment.save()
