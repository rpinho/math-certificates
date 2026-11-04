"""Fresh certified projection at horizontal coordinate 5X+Y, depth Y.

Only referee geometry is imported. Candidate projection certificates and words
are never read. Floating-point inversion proposes brackets; every inverse and
every crossing is accepted exclusively by Arb inequalities.
"""
from independent_geometry import *
from functools import lru_cache
from math import sin, pi, floor, gcd
from scipy.optimize import brentq
from flint import fmpz_mat
from itertools import combinations

ecc=[N*r*C/h for r in radii]
K=2*PI*276
for e in ecc: assert abs(e)<1

@lru_cache(None)
def inverse(k,x):
    z=K*A(x); zfloat=float(z); e=ecc[k]; ef=float(e)
    root=brentq(lambda u:u-ef*sin(u)-zfloat,zfloat-1.01,zfloat+1.01,
                xtol=1e-13,rtol=1e-15)
    # Exact binary rational proposed endpoints, with generous room for libm.
    unit=F(1,2**36); center=F(floor(root*2**36),2**36); step=unit*4
    while True:
        lo=center-step;hi=center+step
        flo=A(lo)-e*A(lo).sin()-z;fhi=A(hi)-e*A(hi).sin()-z
        if flo<0 and fhi>0:return lo,hi
        step*=2
        assert step<1

def projected(k,left,right):
    lo,_=inverse(k,left);_,hi=inverse(k,right);u=box(lo,hi)
    p,v,_=body(radii[k],1,u)
    du=K/(1-ecc[k]*u.cos())
    return 5*p[0]+p[1],p[1],(5*v[0]+v[1])*du

def functions(left,right):
    fa,ga,da=projected(0,left,right);fi,gi,di=projected(1,left,right)
    return {'m':(fa-fi,da-di),'p':(fa+fi,da+di),
            'a':(fa,da),'i':(fi,di)},(ga,gi)

def sgn(x):
    if x>0:return 1
    if x<0:return -1
    return 0

def root_bracket(kind,left,right):
    sl=sgn(functions(left,left)[0][kind][0]);sr=sgn(functions(right,right)[0][kind][0])
    assert sl*sr==-1
    while right-left>F(1,2**38):
        mid=(left+right)/2;sm=sgn(functions(mid,mid)[0][kind][0])
        if sm==sl:left=mid
        elif sm==sr:right=mid
        else:
            # Do not rely on a sign at an unresolved midpoint; bracket it.
            l=(left+mid)/2;r=(mid+right)/2
            if sgn(functions(l,l)[0][kind][0])==sl and sgn(functions(r,r)[0][kind][0])==sr:
                left,right=l,r
            else: raise RuntimeError('root midpoint unresolved')
    return left,right

def all_roots():
    roots=[];stats={}
    for kind in ['m','p','a','i']:
        stack=[(F(0),F(1),0)];empty=one=nodes=0;maxdepth=0
        while stack:
            left,right,depth=stack.pop();nodes+=1;maxdepth=max(depth,maxdepth)
            value,derivative=functions(left,right)[0][kind]
            if sgn(value):empty+=1;continue
            if sgn(derivative):
                sl=sgn(functions(left,left)[0][kind][0]);sr=sgn(functions(right,right)[0][kind][0])
                if sl*sr==-1:
                    lo,hi=root_bracket(kind,left,right)
                    roots.append((lo,hi,kind));one+=1;continue
                if sl!=0 and sl==sr:empty+=1;continue
            assert depth<45,(kind,left,right,str(value),str(derivative))
            mid=(left+right)/2
            stack.extend([(mid,right,depth+1),(left,mid,depth+1)])
        stats[kind]=dict(empty=empty,one_root=one,nodes=nodes,maxdepth=maxdepth)
        print(json.dumps({kind:stats[kind]}),flush=True)
    roots.sort()
    for l,r in zip(roots,roots[1:]):assert l[1]<r[0],(l,r)
    return roots,stats

def derive_word(roots):
    order=[0,1,2,3];word=[];events=[]
    pairs={'m':[(0,1),(2,3)],'p':[(0,2),(1,3)],'a':[(1,2)],'i':[(0,3)]}
    signed_counts={}
    for lo,hi,kind in roots:
        _,(ga,gi)=functions(lo,hi);depths=[-gi,-ga,ga,gi]
        generators=[]
        for a,b in pairs[kind]:
            j,k=order.index(a),order.index(b)
            assert abs(j-k)==1,(kind,order,a,b)
            if j>k:j,k=k,j
            sign=sgn(depths[order[j]]-depths[order[k]])
            assert sign!=0
            generators.append(sign*(j+1))
        assert len({abs(g) for g in generators})==len(generators)
        for gen in sorted(generators,key=abs):
            j=abs(gen)-1;order[j],order[j+1]=order[j+1],order[j]
            word.append(gen);signed_counts[gen]=signed_counts.get(gen,0)+1
        events.append(dict(lo=str(lo),hi=str(hi),kind=kind,generators=generators))
    assert order==[0,1,2,3]
    return word,events,signed_counts

def color_matrix(word):
    cols=[[int(i==j) for j in range(4)] for i in range(4)]
    for gen in word:
        j=abs(gen)-1;x,y=cols[j],cols[j+1]
        if gen>0:cols[j]=[2*a-b for a,b in zip(x,y)];cols[j+1]=x
        else:cols[j]=y;cols[j+1]=[2*b-a for a,b in zip(x,y)]
    return cols

def determinant(C4):
    # Lower cap: c2=3c1-2c0, c3=2c1-c0. Upper: d2=d0,
    # d3=2d0-d1, with d=C4*c. These are full Fox integer relations.
    rows=[[2,-3,1,0],[1,-2,0,1],
          [C4[2][j]-C4[0][j] for j in range(4)],
          [C4[3][j]-2*C4[0][j]+C4[1][j] for j in range(4)]]
    minors=[]
    for rs in combinations(range(4),3):
      for cs in combinations(range(4),3):
        minors.append(abs(int(fmpz_mat([[rows[r][c] for c in cs] for r in rs]).det())))
    g=0
    for d in minors:g=gcd(g,d)
    return g,rows,minors,str(fmpz_mat(rows).snf())

def reduced_action(C4):
    # c=(p+q,q,0,p) has c0-c1+c2-c3=0, with c0-c1=p,c1-c2=q.
    vectors=[[1,0,0,1],[1,1,0,0]];out=[]
    for v in vectors:
        d=[sum(c*x for c,x in zip(row,v)) for row in C4]
        assert d[0]-d[1]+d[2]-d[3]==0
        out.append([d[0]-d[1],d[1]-d[2]])
    return [[out[j][i] for j in range(2)] for i in range(2)]

def main():
    start=time.monotonic();roots,stats=all_roots();word,events,counts=derive_word(roots)
    C4=color_matrix(word);M=reduced_action(C4);det,rows,minors,snf=determinant(C4)
    assert M==[[1,0],[1104,1]],M
    assert det==1107,det
    result=dict(pid=os.getpid(),precision_bits=ctx.prec,projection='F=5X+Y, depth=Y',
                independent_partition=stats,event_count=len(events),crossing_count=len(word),
                signed_generator_counts=counts,full_color_matrix=C4,reduced_action=M,
                fox_relations=rows,fox_3x3_minors=minors,smith_normal_form=snf,determinant=det,
                seconds=time.monotonic()-start,inverse_cache=str(inverse.cache_info()))
    with open('topology_results.json','w') as f:json.dump(result,f,indent=2)
    with open('independent_braid.json','w') as f:json.dump(dict(word=word,events=events),f)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
