"""Clean-room C86 checker, written by the referee from the mathematical formulas.
No producer program is used. Rational certificate data and standard FLINT only.
"""
import argparse, json, hashlib, time, os
from fractions import Fraction as F
from flint import fmpz
from functools import reduce
from flint import arb, acb, arb_poly, arb_series, acb_series, fmpz_poly, ctx
ctx.prec=192
ctx.threads=1

def A(q):
    return arb(str(q))

def H(t):
    """Real continuous twice-primitive of log|t|, H(0)=0."""
    if t.is_zero(): return arb(0)
    if t.contains(0):
        u=abs(t).upper()
        assert u < 1
        return arb(0, (u*u*(abs(u.log())/2+1)).upper())
    return t*t*(abs(t).log()/2-arb(3)/4)

def HC(z):
    if z.imag.is_zero(): return H(z.real)
    return (z*z*(z.log()/2-acb(arb(3)/4))).real

def HP(t):
    if t.is_zero(): return arb(0)
    assert not t.contains(0)
    return t*(abs(t).log()-1)

class Certificate:
    def __init__(self, data):
        self.data=data
        self.x=list(map(F,data['edges']))
        self.y=list(map(F,data['node_densities']))
        self.b=list(map(F,data['b']))
        self.q=data['A']
        self.bound=F(data['bound'])
        assert len(self.x)==len(self.y) and len(self.x)>1
        assert all(u<v for u,v in zip(self.x,self.x[1:])), 'node order'
        assert all(t>=0 for t in self.y), 'negative density'
        assert self.y[0]==self.y[-1]==0, 'density must join zero outside'
        assert self.x[0]>F(1,1000) and self.x[-1]<13, 'positive support'
        assert len(self.b)==len(self.q) and all(b>0 for b in self.b), 'weights'
        assert len(set(tuple(q) for q in self.q))==len(self.q), 'duplicate auxiliary'
        self.mass=sum((v-u)*(a+b)/2 for u,v,a,b in zip(self.x,self.x[1:],self.y,self.y[1:]))
        self.moment=sum((v-u)*((2*u+v)*a+(u+2*v)*b)/6 for u,v,a,b in zip(self.x,self.x[1:],self.y,self.y[1:]))
        assert self.mass>0
        assert self.bound==self.moment/self.mass, 'declared bound differs from normalized first moment'
        self.degree=sum(b*(len(q)-1) for b,q in zip(self.b,self.q))
        assert self.degree<self.mass, 'weighted degree is not below mass'
        slopes=[(b-a)/(v-u) for u,v,a,b in zip(self.x,self.x[1:],self.y,self.y[1:])]
        jumps=[slopes[0]]+[b-a for a,b in zip(slopes,slopes[1:])]+[-slopes[-1]]
        assert sum(jumps)==0 and sum(j*x for j,x in zip(jumps,self.x))==0
        self.jumps=[(A(x),A(s)) for x,s in zip(self.x,jumps) if s]
        self.roots=[]
        self.aux=[]
        for i,(q,b) in enumerate(zip(self.q,self.b)):
            assert len(q)>1 and all(type(t) is int for t in q) and q[-1]>0
            assert reduce(lambda a, b: int(fmpz(a).gcd(b)), q)==1, 'not primitive'
            p=fmpz_poly(q)
            content,factors=p.factor()
            assert content==1 and len(factors)==1 and factors[0][0]==p and factors[0][1]==1, 'not irreducible'
            roots=p.complex_roots()
            assert len(roots)==p.degree() and all(m==1 for r,m in roots)
            real=sum(r.imag.is_zero() for r,m in roots)
            nonreal=sum(not r.imag.contains(0) for r,m in roots)
            assert real+nonreal==p.degree(), 'root classification unresolved'
            self.roots.extend((r,A(b)) for r,m in roots)
            self.aux.append(dict(index=i,coefficients=q,degree=p.degree(),leading_coefficient=q[-1],weight=str(b),real_roots=real,nonreal_roots=nonreal,roots=[str(r) for r,m in roots]))
        self.loglc=sum((A(b)*A(q[-1]).log() for b,q in zip(self.b,self.q)),arb(0))
        self.cells=[i for i,(a,b) in enumerate(zip(self.y,self.y[1:])) if a or b]

    def potential(self,z):
        return sum((s*HC(z-e) for e,s in self.jumps),arb(0))

    def check_point(self, x):
        """A failed necessary point inequality rejects with a rigorous witness."""
        x=F(x)
        vals=[sum(t*x**i for i,t in enumerate(q)) for q in self.q]
        if any(t==0 for t in vals): return None  # f=+infinity at an auxiliary root
        val=self.potential(acb(A(x)))-sum((A(b)*A(abs(t)).log() for b,t in zip(self.b,vals)),arb(0))
        assert val>=0, f'potential at x={x} is negative or unresolved: {val}'
        return val

    def integrals(self):
        for info,q in zip(self.aux,self.q):
            roots=fmpz_poly(q).complex_roots()
            val=A(self.mass)*A(q[-1]).log()+sum((self.potential(r) for r,m in roots),arb(0))
            info['log_integral']=str(val)
            assert val>0, f'nonpositive or unresolved log integral Q{info["index"]}: {val}'
        return self.aux

    def metadata(self):
        return dict(nodes=len(self.x),positive_nodes=sum(y>0 for y in self.y),positive_cells=len(self.cells),mass=str(self.mass),moment=str(self.moment),bound=str(self.bound),weighted_degree=str(self.degree),degree_slack=str(self.mass-self.degree),support_enclosing_grid=[str(self.x[0]),str(self.x[-1])],auxiliaries=self.aux)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('certificate');ap.add_argument('--output',default='structure.json')
    args=ap.parse_args()
    start=time.time(); raw=open(args.certificate,'rb').read(); c=Certificate(json.loads(raw));c.integrals();c.check_point(F(3))
    out=c.metadata();out.update(sha256=hashlib.sha256(raw).hexdigest(),seconds=time.time()-start,prec=ctx.prec)
    json.dump(out,open(args.output,'w'),indent=2);print('PASS structure and integrals',out['seconds'],flush=True)

if __name__=='__main__': main()
