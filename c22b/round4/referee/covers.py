"""Adaptive interval proofs on full rational domains, regenerated here."""
from geometry import *
from fractions import Fraction as Fr
import sys,time,json

def one(j):
    rho=arb('1.98') if j==0 else arb('1.44'); stack=[(Fr(0),Fr(44,7),0)]; leaves=0; minf=None
    while stack:
        lo,hi,depth=stack.pop(); m=(lo+hi)/2; U=box(lo,hi)
        f=curvature_F(U,j,rho)
        if not f>0:
            jet=curvature_F(arb_series([U,1],2),j,rho)
            f=curvature_F(Q(m),j,rho)+jet[1]*(U-Q(m))
        if f>0:
            leaves+=1; minf=f.lower() if minf is None or f.lower()<minf else minf
        else:
            if depth>45: raise RuntimeError(('curvature',j,lo,hi,f))
            stack.extend([(lo,m,depth+1),(m,hi,depth+1)])
    return dict(radius_lower=str(rho),leaves=leaves,F_lower=str(minf))

def two(name,fn,root,short=None):
    stack=[(*root,0)]; count=0; shortcount=0; low=None; started=time.time(); maxdepth=0
    while stack:
        l,r,b,t,depth=stack.pop(); m=(l+r)/2; n=(b+t)/2
        if short is not None and short(l,r,b,t):
            shortcount+=1; continue
        U,D=box(l,r),box(b,t)
        val,du,dd=fn(U,D)
        if not val>4:
            f0=fn(Q(m),Q(n))[0]
            val=f0+du*(U-Q(m))+dd*(D-Q(n))
        if val>4:
            count+=1; maxdepth=max(maxdepth,depth)
            low=val.lower() if low is None or val.lower()<low else low
        else:
            if depth>60: raise RuntimeError((name,l,r,b,t,val))
            # gradient-scaled box widths choose refinement direction.
            wu=float(abs(du).upper())*float(r-l); wd=float(abs(dd).upper())*float(t-b)
            if wu>=wd: stack.extend([(l,m,b,t,depth+1),(m,r,b,t,depth+1)])
            else: stack.extend([(l,r,b,n,depth+1),(l,r,n,t,depth+1)])
        if (count+shortcount)%50000==0: print(name,count,shortcount,len(stack),round(time.time()-started,1),flush=True)
    return dict(distance_squared_lower=str(low),distance_leaves=count,short_leaves=shortcount,maxdepth=maxdepth,seconds=time.time()-started)

def interface_fn(j,c,k,d):
    def fn(u,l):
        P,V,_=body(u,j,c); W,T=connector(l,k,d); z=sub(P,W)
        return dot(z,z),2*dot(z,V),-2*dot(z,T)
    return fn

def lower_fn(c):
    def fn(x,y):
        ell=ends[0]['Q']*ends[0]['theta']; P,V=connector(x*ell,0,c); W,T=oldcircle(y*pi,1); z=sub(P,W)
        return dot(z,z),2*ell*dot(z,V),-2*pi*dot(z,T)
    return fn

if __name__=='__main__':
    task=sys.argv[1]; result={}; start=time.time()
    if task=='curvature':
        for j in range(2): result[str(j)]=one(j); print(j,result[str(j)],flush=True)
    elif task=='body':
        for j in range(2):
            root=(Fr(0),Fr(44,7),Fr(3,2) if j==0 else Fr(-9),Fr(9))
            result[str(j)]=two('body'+str(j),lambda u,d:pair(u,d,j),root)
            print(j,result[str(j)],flush=True)
    elif task=='interfaces':
        scal=json.load(open('scalar.json')); vs=[arb(scal['V'+str(j)]) for j in range(2)]
        # Z-axis half turn reduces the sixteen pairs to eight with body c=+1.
        for j in range(2):
            for k in range(2):
                for d in (-1,1):
                    name=f'{j}_{k}_{d}'
                    short=(lambda l,r,b,t: -Q(l)*vs[j]+Q(t)<pi) if j==k and d==1 else None
                    result[name]=two(name,interface_fn(j,1,k,d),(Fr(-8),Fr(0),Fr(0),Fr(16)),short)
                    print(name,result[name],flush=True)
    elif task=='lower':
        for c in (-1,1):
            result[str(c)]=two('lower'+str(c),lower_fn(c),(Fr(0),Fr(1),Fr(0),Fr(1)))
            print(c,result[str(c)],flush=True)
    result['seconds']=time.time()-start
    json.dump(result,open('cover_'+task+'.json','w'),indent=2)
