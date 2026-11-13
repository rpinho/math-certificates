"""Our implementation of ordinary dual-weighted IRLS evaluation-lattice LLL.

Method credits: Doche auxiliary numerators, Pinho dual pricing, Patankar PR280
iterated numerator LLL. No third-party search code read or imported.
Integer coefficient lattice with weighted complex evaluations, exact Gram LLL,
irreducible factor extraction and pricing on the entire current LP dual.
"""
import argparse,hashlib,json,math,time
from pathlib import Path
import mpmath as mp
import numpy as np
from flint import ctx,fmpz_mat,fmpz_poly
from numerics import register,write_json,roots,root_logs,transformed_points

def coeffs(p):return tuple(int(c) for c in reversed(p.coeffs()))
def poly(c):return fmpz_poly(list(c)[::-1])
def evaluate(p,pts):
    c=coeffs(p);v=[mp.mpc(c[0]) for _ in pts]
    for a in c[1:]:v=[x*z+a for x,z in zip(v,pts)]
    return v

class Search:
    def __init__(self,a):
        self.a=a;self.start=time.monotonic();self.cpu=time.process_time();self.rng=np.random.default_rng(a.seed)
        mp.mp.prec=320;ctx.prec=256;ctx.threads=1
        self.state=json.loads(Path(a.state).read_text());d=np.load(a.dual)
        support=d['nu']>1e-18;self.t=d['t'][support];self.mass=d['nu'][support];self.eta=float(d['eta'])
        self.points=transformed_points(self.t);self.cdf=np.cumsum(self.mass);self.cdf/=self.cdf[-1]
        self.known={tuple(r['coeffs']) for r in self.state['numerator']}
        self.den=[poly(r['coeffs']) for r in self.state['denominator']]
        self.active=[poly(r['coeffs']) for r,w in zip(self.state['numerator'],self.state['w']) if w>1e-12]
        self.small=[p for p in self.active if p.degree()<=20]
        self.cache={};self.found={};self.stats=[];self.trials=0;self.priced=0;self.best=None;self.save()
    def save(self):
        write_json(self.a.out,{'candidate_unrefereed':True,'settings':vars(self.a),'elapsed':time.monotonic()-self.start,'cpu_seconds':time.process_time()-self.cpu,'trials':self.trials,'priced':self.priced,'negative_candidates':list(self.found.values()),'best':self.best,'iterations':self.stats})
    def price(self,p):
        c=coeffs(p)
        if c in self.cache:return self.cache[c]
        if any(p.gcd(q).degree()>0 for q in self.den):self.cache[c]=math.inf;return math.inf
        rc=float(self.mass@root_logs(c,self.points)+self.eta*p.degree());self.priced+=1;self.cache[c]=rc
        if c not in self.known and (self.best is None or rc<self.best['rc']):self.best={'coeffs':list(c),'rc':rc}
        if c not in self.known and rc< -1e-9 and c not in self.found:
            row={'name':'N82r10_'+hashlib.sha256(str(c).encode()).hexdigest()[:12],'coeffs':list(c),'rc':rc,'trial':self.trials}
            self.found[c]=row;self.save();print(json.dumps({'event':'negative','name':row['name'],'degree':p.degree(),'rc':rc}),flush=True)
        return rc
    def initial(self):
        # Direct warm starts and products of successful factors, with varied degree.
        if self.trials%3==0:return self.active[(self.trials//3)%len(self.active)]
        cap=int(self.rng.choice([24,32,40,48,56,64]));p=fmpz_poly([1])
        pool=self.active if self.trials%3==1 else self.small
        for _ in range(18):
            q=pool[int(self.rng.integers(len(pool)))]
            if p.degree()+q.degree()<=cap:p*=q
        return p
    def lattice(self,p,degree,pts,profile):
        values=evaluate(p,pts)
        # IRLS surrogate of integral log|P|: nu/|P0|^2.
        weights=[mp.mpf(float(v))/max(abs(z),mp.mpf('1e-80')) for v,z in zip(profile,values)]
        norm=max(weights);weights=[v/norm for v in weights]
        scale=mp.mpf(2)**200
        coefficient_norm=mp.sqrt(sum(mp.mpf(int(x))**2 for x in p.coeffs()))
        lam=mp.mpf(10)**float(self.rng.uniform(-6,-1))/max(coefficient_norm,1)
        ridge=max(1,int(mp.nint(scale*lam/norm)))
        n=degree+1;powers=[mp.mpc(1) for _ in pts];rows=[]
        for j in range(n):
            v=[z*w*scale for z,w in zip(powers,weights)]
            rows.append([ridge if k==j else 0 for k in range(n)]+[int(mp.nint(z.real)) for z in v]+[int(mp.nint(z.imag)) for z in v])
            powers=[z*x for z,x in zip(powers,pts)]
        basis=fmpz_mat(rows);gram=basis*basis.transpose()
        reduced,change=gram.lll(delta=.99,rep='gram',transform=True)
        assert change*gram*change.transpose()==reduced
        k=min(8,n);vectors=[[int(change[i,j]) for j in range(n)] for i in range(k)]
        candidates=list(vectors)
        for i in range(k):
            for j in range(i):
                candidates.append([x+y for x,y in zip(vectors[i],vectors[j])])
                candidates.append([x-y for x,y in zip(vectors[i],vectors[j])])
        return [fmpz_poly(v) for v in candidates]
    def trial(self):
        begun=time.monotonic();p=self.initial();old=math.inf
        quantiles=(np.arange(self.a.points)+self.rng.uniform(.1,.9,self.a.points))/self.a.points
        ts=self.t[np.searchsorted(self.cdf,quantiles)]
        pts=[]
        for t in ts:
            z=mp.expjpi(2*mp.mpf(float(t)));pts.append(z*(1-z))
        profile=np.exp(self.rng.normal(0,.3 if self.trials%2 else 0,len(pts)))
        extra=int(self.rng.integers(0,7));d=min(80,p.degree()+extra)
        for it in range(self.a.iterations):
            if time.monotonic()-self.start>self.a.seconds:break
            candidates=self.lattice(p,d,pts,profile);best=None;seen=set()
            for q in candidates:
                if time.monotonic()-self.start>self.a.seconds:break
                if q.degree()<1:continue
                if int(q.leading_coefficient())<0:q=-q
                c=coeffs(q)
                if c in seen:continue
                seen.add(c)
                # Price factors as columns; the complete product guides IRLS.
                total=0.;valid=True
                for f,m in q.factor()[1]:
                    if f.degree()<1:continue
                    r=self.price(f);total+=m*r
                    if not math.isfinite(r):valid=False
                if valid and (best is None or total<best[0]):best=(total,q)
            if best is None:break
            row={'trial':self.trials,'iteration':it,'degree':d,'best_rc':best[0],'negative':len(self.found),'priced':self.priced,'elapsed':time.monotonic()-self.start}
            self.stats.append(row);self.save();print(json.dumps(row),flush=True)
            if best[0]>=old-1e-10:break
            old,p=best;profile=np.ones(len(pts))
        self.trials+=1;self.save()
        print(json.dumps({'event':'trial_done','trials':self.trials,'seconds':time.monotonic()-begun,'negative':len(self.found)}),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',required=True);ap.add_argument('--dual',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--seconds',type=int,default=240);ap.add_argument('--seed',type=int,default=8111);ap.add_argument('--points',type=int,default=256);ap.add_argument('--iterations',type=int,default=8)
    a=ap.parse_args();register('lll_numerator_search');s=Search(a)
    while time.monotonic()-s.start<a.seconds:s.trial()
    s.save()
