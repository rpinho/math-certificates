"""Clean-room scalar GF(9), elimination, controls, and information sets."""
import hashlib, json, itertools, time
from pathlib import Path

def add(x,y): return ((x%3+y%3)%3)+3*((x//3+y//3)%3)
def neg(x): return (-x%3)+3*((-(x//3))%3)
def mul(x,y):
    a,b,c,d=x%3,x//3,y%3,y//3
    return (a*c-b*d)%3+3*((a*d+b*c)%3)
def inv(x): return next(y for y in range(1,9) if mul(x,y)==1)
def eliminate(g, order):
    a=[r[:] for r in g]; k=len(a); piv=[]
    for j in order:
        r=len(piv)
        p=next((i for i in range(r,k) if a[i][j]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        v=inv(a[r][j]); a[r]=[mul(v,x) for x in a[r]]
        for i in range(k):
            if i!=r and a[i][j]:
                v=neg(a[i][j]); a[i]=[add(x,mul(v,y)) for x,y in zip(a[i],a[r])]
        piv.append(j)
        if len(piv)==k: break
    return a,piv

def word(g,u):
    w=[0]*len(g[0])
    for x,r in zip(u,g): w=[add(a,mul(x,b)) for a,b in zip(w,r)]
    return w

def prepare(g,path):
    n=len(g[0]); k=len(g)
    _,piv=eliminate(g,range(n)); assert len(piv)==k
    unused=list(range(n)); sets=[]; mats=[]
    while len(unused)>=k:
        m,p=eliminate(g,unused)
        if len(p)<k: break
        assert all(m[i][p[j]]==int(i==j) for i in range(k) for j in range(k))
        sets.append(p); mats.append(m); unused=[j for j in unused if j not in p]
    assert sets
    data={'n':n,'k':k,'rank':len(piv),'information_sets_zero_based':sets,'unused':unused,'matrices':mats}
    Path(path+'.json').write_text(json.dumps(data,indent=2)+'\n')
    with open(path+'.dat','w') as f:
        print(n,k,len(sets),file=f)
        for m in mats:
            for r in m: print(*r,file=f)
    return data

def main():
    start=time.perf_counter()
    raw=Path('inputs/q9_n92_k13_d61.txt').read_bytes()
    expected=Path('inputs/SHA256SUMS').read_text().split()[0]
    digest=hashlib.sha256(raw).hexdigest(); assert digest==expected
    for x in range(9):
        assert add(x,0)==x and add(x,neg(x))==0 and mul(x,1)==x and mul(x,0)==0
        if x: assert mul(x,inv(x))==1
        for y in range(9):
            assert 0<=add(x,y)<9 and 0<=mul(x,y)<9
            assert add(x,y)==add(y,x) and mul(x,y)==mul(y,x)
            for z in range(9):
                assert add(add(x,y),z)==add(x,add(y,z))
                assert mul(mul(x,y),z)==mul(x,mul(y,z))
                assert mul(x,add(y,z))==add(mul(x,y),mul(x,z))
    assert mul(3,3)==2
    g=[[int(x) for x in r.split()] for r in raw.decode().splitlines() if r.strip()]
    assert len(g)==13 and all(len(r)==92 and all(0<=x<9 for x in r) for r in g)
    data=prepare(g,'candidate')
    # Evaluation RS code: all polynomials degree <3 at the nine field elements.
    rs=[[1]*9,list(range(9)),[mul(x,x) for x in range(9)]]
    control=prepare(rs,'rs_control')
    hist={}
    for u in itertools.product(range(9),repeat=3):
        if not any(u): continue
        w=sum(x!=0 for x in word(rs,u)); hist[w]=hist.get(w,0)+1
    assert min(hist)==7
    result={'sha256':digest,'hash_matches':True,'encoding':'a+3b; t^2=2',
            'field_axioms':'all 9 elements, 81 pairs, 729 triples passed',
            'rank':data['rank'],'information_sets':data['information_sets_zero_based'],
            'row_weights':[sum(x!=0 for x in r) for r in g],
            'control':{'parameters':[9,3,7],'scalar_exhaustive_nonzero_words':728,'weight_distribution':hist},
            'seconds':time.perf_counter()-start}
    Path('preparation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
