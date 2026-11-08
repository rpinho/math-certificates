"""Clean-room GF(9) checker: polynomial encoding a+3b, t^2=-1."""
import hashlib, itertools, json, time
from pathlib import Path

def add(x,y): return (x%3+y%3)%3 + 3*((x//3+y//3)%3)
def neg(x): return (-x%3)%3 + 3*((-(x//3))%3)
def mul(x,y):
    a,b,c,d=x%3,x//3,y%3,y//3
    return (a*c-b*d)%3+3*((a*d+b*c)%3)
def power(x,e):
    r=1
    while e:
        if e&1:r=mul(r,x)
        x=mul(x,x);e//=2
    return r
def inv(x):
    assert x
    return power(x,7)
A=[[add(x,y) for y in range(9)] for x in range(9)]
M=[[mul(x,y) for y in range(9)] for x in range(9)]

def rref(G):
    R=[r[:] for r in G]; piv=[]; h=0
    for j in range(len(R[0])):
        p=next((i for i in range(h,len(R)) if R[i][j]),None)
        if p is None:continue
        R[h],R[p]=R[p],R[h]
        z=inv(R[h][j]);R[h]=[mul(z,x) for x in R[h]]
        for i in range(len(R)):
            if i!=h and R[i][j]:
                z=neg(R[i][j]);R[i]=[add(x,mul(z,y)) for x,y in zip(R[i],R[h])]
        piv.append(j);h+=1
        if h==len(R):break
    return R,piv

def field_check():
    for a in range(9):
        assert add(a,0)==a and mul(a,1)==a and add(a,neg(a))==0 and mul(a,0)==0
        if a: assert mul(a,inv(a))==1
        for b in range(9):
            assert add(a,b)==add(b,a) and mul(a,b)==mul(b,a)
            assert 0<=add(a,b)<9 and 0<=mul(a,b)<9
            for c in range(9):
                assert add(add(a,b),c)==add(a,add(b,c))
                assert mul(mul(a,b),c)==mul(a,mul(b,c))
                assert mul(a,add(b,c))==add(mul(a,b),mul(a,c))
    assert mul(3,3)==2
    return 'All field axioms checked exhaustively (729 triples); t^2=2.'

# Quadratic extension GF(81)=GF(9)[u]/(u^2-nonsquare).
NS=next(x for x in range(1,9) if x not in {mul(y,y) for y in range(9)})
def eadd(x,y):return add(x%9,y%9)+9*add(x//9,y//9)
def emul(x,y):
    a,b,c,d=x%9,x//9,y%9,y//9
    return add(mul(a,c),mul(NS,mul(b,d)))+9*add(mul(a,d),mul(b,c))
def epow(x,e):
    r=1
    while e:
        if e&1:r=emul(r,x)
        x=emul(x,x);e//=2
    return r
ALPHA=next(x for x in range(1,81) if epow(x,80)==1 and epow(x,40)!=1 and epow(x,16)!=1)
def evaluate(poly,x):
    r=0
    for c in reversed(poly):r=eadd(emul(r,x),c)
    return r

def roots(poly):return [i for i in range(80) if evaluate(poly,epow(ALPHA,i))==0]
def bch_bound(rr):
    rr=set(rr);best=(1,0,1)
    for step in range(1,80):
        if __import__('math').gcd(step,80)!=1:continue
        for start in rr:
            length=0
            while length<80 and (start+length*step)%80 in rr:length+=1
            if length+1>best[0]:best=(length+1,start,step)
    return best

def codeword(G,m):
    w=[0]*len(G[0])
    for c,row in zip(m,G):
        w=[add(x,mul(c,y)) for x,y in zip(w,row)]
    return w

def main():
    start=time.perf_counter()
    f=Path('inputs/q9_n85_k15_d54.txt'); digest=hashlib.sha256(f.read_bytes()).hexdigest()
    assert digest==Path('inputs/SHA256SUMS').read_text().split()[0]
    G=[list(map(int,r.split())) for r in f.read_text().splitlines()]
    assert len(G)==15 and all(len(r)==85 and all(0<=x<9 for x in r) for r in G)
    R,p=rref(G)
    result={'sha256':digest,'field':field_check(),'rank':len(p),'pivots':p,'extension_nonsquare':NS,'alpha':ALPHA}
    g=G[0][:66]
    result['shift_structure']=all(row[:80]==[0]*i+g+[0]*(14-i) for i,row in enumerate(G))
    rr=roots(g);result['roots']=rr;result['bch_bound']=bch_bound(rr)
    result['row_weights']=[sum(x!=0 for x in r) for r in G]
    result['g_at_1']=evaluate(g,1)
    result['seconds']=time.perf_counter()-start
    Path('initial_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
