"""Independent physical projection F=X+Y/4, depth G=Y-X/4.
Outer phase parametrizes height; all inner inverse brackets verified by Arb.
"""
from geometry import *
from fractions import Fraction as Fr
from functools import lru_cache
from scipy.optimize import brentq
import math,time,json
EPS=arb('1e-11'); factor=N*k/h
cf=[float(x) for x in coef[1]]; ph=[float(x) for x in phase]; ff=float(factor)
def height(u,j): return local(u,j)[0][2]*N/(lam*h)
def hfloat(u):
    r=sum(c*math.cos(m*u) for m,c in enumerate(cf))
    v=u+sum(c*math.sin(m*u) for m,c in enumerate(ph,1))
    return u-ff*r*math.sin(v)
@lru_cache(maxsize=200000)
def inverse(x):
    U=pi*Q(x); target=height(U,0); y=float(target.mid())
    w=brentq(lambda w:hfloat(w)-y,y-.1,y+.1,xtol=1e-12)
    center=arb(w); eps=EPS
    for _ in range(10):
        lo=center-eps; hi=center+eps
        if height(lo,1)<target and height(hi,1)>target:
            return lo.union(hi)
        eps*=10
    raise RuntimeError(('inverse',str(x),str(target),w))

def quantities(l,r):
    U=pi*box(l,r); W=inverse(l).union(inverse(r))
    A,VA,_=body(U,0); I,VI,_=body(W,1)
    du=VA[2]/VI[2]
    Fa=A[0]+A[1]/4; Fi=I[0]+I[1]/4
    Ga=A[1]-A[0]/4; Gi=I[1]-I[0]/4
    dFa=pi*(VA[0]+VA[1]/4); dFi=pi*(VI[0]+VI[1]/4)*du
    vals=[Fa-Fi,Fa+Fi,Fa,Fi]; deriv=[dFa-dFi,dFa+dFi,dFa,dFi]
    return vals,deriv,[-Gi,-Ga,Ga,Gi]

def sign(x):
    return 1 if x>0 else -1 if x<0 else 0

def isolate(kind,l,r):
    a=sign(quantities(l,l)[0][kind]); b=sign(quantities(r,r)[0][kind]); assert a*b==-1
    while r-l>Fr(1,10**8):
        m=(l+r)/2; sgn=sign(quantities(m,m)[0][kind])
        if not sgn:
            # retain a bracket strictly inside the existing one around an ambiguous midpoint.
            ml=(3*l+r)/4; mr=(l+3*r)/4
            al=sign(quantities(ml,ml)[0][kind]); ar=sign(quantities(mr,mr)[0][kind])
            if al*ar==-1: l,r,a,b=ml,mr,al,ar; continue
            raise RuntimeError(('root rounding',kind,l,r))
        if sgn==a: l,a=m,sgn
        else: r,b=m,sgn
    return l,r

def roots(kind):
    stack=[(Fr(0),Fr(662),0)]; result=[]; leaves=0; maxdepth=0
    while stack:
        l,r,d=stack.pop(); v,dv,_=quantities(l,r); f=v[kind]; der=dv[kind]
        if sign(f): leaves+=1; continue
        if sign(der):
            sl=sign(quantities(l,l)[0][kind]); sr=sign(quantities(r,r)[0][kind])
            if sl and sr:
                if sl!=sr:
                    a,b=isolate(kind,l,r); result.append((a,b,kind)); maxdepth=max(maxdepth,d)
                leaves+=1; continue
        if d>55: raise RuntimeError(('cover',kind,l,r,str(f),str(der)))
        m=(l+r)/2; stack.extend([(m,r,d+1),(l,m,d+1)])
    print('root kind',kind,'count',len(result),'leaves',leaves,'depth',maxdepth,flush=True)
    return result,leaves

if __name__=='__main__':
    start=time.time(); events=[]; counts=[]; leaf=[]
    for kind in range(4):
        rr,ll=roots(kind); events+=rr; counts.append(len(rr)); leaf.append(ll)
    events.sort()
    for a,b in zip(events,events[1:]): assert a[1]<b[0]
    pairs=[[(0,1),(2,3)],[(0,2),(1,3)],[(1,2)],[(0,3)]]
    lanes=list(range(4)); M=[[int(i==j) for j in range(4)] for i in range(4)]; word=[]
    for l,r,kind in events:
        _,_,depth=quantities(l,r)
        for a,b in pairs[kind]:
            ia,ib=lanes.index(a),lanes.index(b)
            assert abs(ia-ib)==1
            pos=min(ia,ib); left,right=lanes[pos:pos+2]
            sg=sign(depth[left]-depth[right]); assert sg
            x,y=M[pos:pos+2]
            if sg==1: M[pos:pos+2]=[[2*a-b for a,b in zip(x,y)],x]
            else: M[pos:pos+2]=[y,[2*b-a for a,b in zip(x,y)]]
            lanes[pos:pos+2]=[right,left]; word.append(sg*(pos+1))
    assert lanes==list(range(4))
    # Basis c=[p,0,-q,p-q] satisfies alternating sum zero.
    def apply(v): return [sum(a*b for a,b in zip(row,v)) for row in M]
    columns=[]
    for v in ([1,0,0,1],[0,0,-1,-1]):
        w=apply(v); columns.append([w[0]-w[1],w[1]-w[2]])
    action=[[columns[j][i] for j in range(2)] for i in range(2)]
    # Lower cap colors [a,b,3b-2a,2b-a]; impose upper cap, eliminate b.
    w=apply([1,0,-2,-1]); relations=[w[2]-w[0],w[3]-2*w[0]+w[1]]
    det=math.gcd(*relations)
    out=dict(root_counts=counts,leaves=leaf,events=len(events),crossings=len(word),positive=sum(x>0 for x in word),negative=sum(x<0 for x in word),permutation=lanes,matrix=M,action=action,relations=relations,determinant=det,seconds=time.time()-start,inverse_cache=str(inverse.cache_info()))
    print(json.dumps(out,indent=2),flush=True)
    json.dump(out,open('topology.json','w'),indent=2)
    json.dump(word,open('word.json','w'))
    json.dump([[str(l),str(r),k] for l,r,k in events],open('roots.json','w'))
    assert action==[[1,0],[1324,1]] and det==1327
