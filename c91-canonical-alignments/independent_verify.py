"""Independent exact/Arb verifier. Imports no search or inherited verifier code.

The artifact contains patterns and a vector, not a trusted transition graph.
Both automata are reconstructed in prescribed breadth-first column order.
"""
import array,gzip,hashlib,json,sys,time
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from flint import arb,ctx

COL=((0,0),(1,1),(0,1),(1,0),(0,None),(1,None),(None,0),(None,1))

def check_noncanonical(word,length):
    symbols=[]
    for _ in range(length):symbols.append(COL[word%8]);word//=8
    symbols.reverse();assert word==0
    x=tuple(a for a,b in symbols if a is not None)
    y=tuple(b for a,b in symbols if b is not None)
    # Forward DAG shortest paths, ordered by (cost,gaps,whole operation string).
    best={(0,0):(0,0,b'')}
    def relax(i,j,value):
        old=best.get((i,j))
        if old is None or value<old:best[i,j]=value
    for i in range(len(x)+1):
        for j in range(len(y)+1):
            cost,gaps,ops=best[i,j]
            if i<len(x) and j<len(y):relax(i+1,j+1,(cost+(x[i]!=y[j]),gaps,ops+b'0'))
            if i<len(x):relax(i+1,j,(cost+1,gaps+1,ops+b'1'))
            if j<len(y):relax(i,j+1,(cost+1,gaps+1,ops+b'2'))
    actual=(sum(a!=b for a,b in symbols),sum(a is None or b is None for a,b in symbols),
            bytes(50 if a is None else 49 if b is None else 48 for a,b in symbols))
    assert actual!=best[len(x),len(y)],('forbidding a canonical word',symbols)

def memory_step(state,c):
    # last: -1 start, 0..3 diagonal label, 4 D, 5 I.
    last,letters,ban,prior=state;a,b=COL[c]
    if c<4:
        if last in (4,5):
            if a!=b or a in letters:return None
            prior=last
        else:prior=-1
        return c,(),None,prior
    direction=4 if b is None else 5;letter=a if b is None else b
    if last in (4,5):
        if direction!=last:return None
        newletters=tuple(sorted(set(letters+(letter,))));newban=ban
    else:
        if prior!=-1 and prior!=direction:return None
        newletters=(letter,)
        newban=(COL[last][1] if direction==4 else COL[last][0]) if last in (2,3) else None
    if letter==newban:return None
    return direction,newletters,newban,-1

def original_automaton(patterns,L,starttime):
    forbidden=set();prefix={(0,0)}
    for k,(n,w) in enumerate(patterns,1):
        assert type(n)is int and type(w)is int and 2<=n<=L and 0<=w<8**n
        assert (w,n) not in forbidden
        check_noncanonical(w,n);forbidden.add((w,n))
        for length in range(n):prefix.add((w//8**(n-length),length))
        if k%200000==0:print('checked forbidden',k,'seconds',time.time()-starttime,flush=True)
    # Finite run-memory machine, separately enumerated from semantic tuples.
    memories=[(-1,(),None,-1)];mid={memories[0]:0};mtable=[]
    for state in memories:
        row=[]
        for c in range(8):
            nxt=memory_step(state,c)
            if nxt is None:row.append(-1)
            else:
                if nxt not in mid:mid[nxt]=len(memories);memories.append(nxt)
                row.append(mid[nxt])
        mtable.append(row)
    def next_prefix(w,n,c):
        z=w*8+c;chosen=None
        for length in range(n+1,-1,-1):
            key=z%8**length,length
            if key in forbidden:return None
            if chosen is None and key in prefix:chosen=key
        assert chosen is not None
        return chosen
    states=[(0,0,0)];ids={states[0]:0};edges=array.array('i')
    for i,(w,n,m) in enumerate(states):
        for c in range(8):
            nm=mtable[m][c]
            p=next_prefix(w,n,c) if nm>=0 else None
            if p is None:edges.append(-1);continue
            key=p[0],p[1],nm
            target=ids.get(key)
            if target is None:target=len(states);ids[key]=target;states.append(key)
            edges.append(target)
        if i and i%500000==0:print('reconstructed original',i,'reachable',len(states),'seconds',time.time()-starttime,flush=True)
    print('complete original automaton',len(states),'run memories',len(memories),flush=True)
    return edges,len(states)

def input_features(hx,hy,c,K):
    result=[0]*K
    for history,bit in ((hx,COL[c][0]),(hy,COL[c][1])):
        if bit is None:continue
        for lag in range(1,min(K,3)+1):
            if len(history)>=lag:result[lag-1]+=1 if history[-lag]==bit else -1
        if K==4 and len(history)>=3:result[3]+=(-1)**(sum(history[-3:])+bit)
    return tuple(result)

def strip_step(hx,hy,ds,ins,c,W,B):
    """Maintain exact cost differences of pure diagonal competitors.

    Histories and score tuples have a semantic representation independent of
    the generator's bit histories and radix packing.
    """
    a,b=COL[c];op=0 if a is not None and b is not None else 1 if b is None else 2
    transformed=[]
    for direction,scores,history,other in ((1,ds,hx,b),(2,ins,hy,a)):
        pending=[None]*W
        for r,s in enumerate(scores,1):
            if s is None:continue
            assert len(history)>=r
            if op==0:
                rnew=r;value=s+int(history[-r]!=other)-int(a!=b)
            elif op==direction:
                rnew=r+1;value=s
            else:
                rnew=r-1;value=s+int(history[-r]!=other)-2
            if op!=direction and value<=0:return None
            if 1<=rnew<=W and value<=B:
                old=pending[rnew-1]
                pending[rnew-1]=value if old is None else min(old,value)
        if op==direction:pending[0]=0
        transformed.append(tuple(pending))
    nx=hx if a is None else (hx+(a,))[-4:]
    ny=hy if b is None else (hy+(b,))[-4:]
    return nx,ny,transformed[0],transformed[1]

def main():
    begun=time.time();path=Path(sys.argv[1]);cert=json.loads(gzip.open(path,'rt').read())
    assert cert['schema']=='c91-typical-strip-v1'
    assert cert['status'].startswith('candidate')
    L,W,B,K=(cert[z] for z in ('L','W','B','K'))
    assert all(type(z)is int for z in (L,W,B,K)) and 2<=L<=15 and 1<=W<=4 and 1<=B<=12 and K in (2,4)
    vec=cert['vector'];assert len(vec)>0 and all(type(v)is int and v>0 for v in vec)
    p,q=cert['x'];r,s=cert['t'];zs=cert['z']
    assert len(zs)==K
    assert all(type(z)is int and z>0 for z in (p,q,r,s)) and p>q and r<s
    assert all(len(z)==2 and all(type(v)is int and v>0 for v in z) for z in zs)
    denominator=4*q*q*s
    for u,v in zs:denominator*=u*u*v*v
    @lru_cache(maxsize=None)
    def coefficient(cclass,feature):
        value=(p*p*s,p*p*r,2*p*q*r)[cclass]
        for h,(u,v) in zip(feature,zs):
            assert -2<=h<=2
            value*=u**(2+h)*v**(2-h)
        return value
    old,N=original_automaton(cert['forbidden_patterns'],L,begun)
    assert N==cert['original_states']
    blank=(None,)*W;initial=(0,(),(),blank,blank)
    states=[initial];ids={initial:0};minimum=None
    for i,(o,hx,hy,ds,ins) in enumerate(states):
        assert i<len(vec),('extra reachable state',i)
        total=0
        for c in range(8):
            destination=old[8*o+c]
            if destination<0:continue
            other=strip_step(hx,hy,ds,ins,c,W,B)
            if other is None:continue
            key=(destination,)+other
            j=ids.get(key)
            if j is None:j=len(states);ids[key]=j;states.append(key)
            assert j<len(vec),('missing vector entry',j)
            total+=coefficient(0 if c<2 else 1 if c<4 else 2,input_features(hx,hy,c,K))*vec[j]
        slack=denominator*vec[i]-total
        assert slack>0,('Av<v failed',i,slack)
        minimum=slack if minimum is None else min(minimum,slack)
        if i and i%500000==0:print('exact rows',i,'reachable',len(states),'seconds',time.time()-begun,flush=True)
    assert len(states)==len(vec),('vector has unreachable entries',len(vec),len(states))
    a,b=cert['bound'];assert type(a)is int and type(b)is int and a>0 and b>0
    ctx.prec=256;x=arb(p)/q;t=arb(r)/s
    margin=2*x.log()+(arb(a)/b)*t.log();assert margin>0,('exponent failed',margin)
    print('PASS: complete independent reconstruction and every exact AV<V row.')
    print('original_states',N,'product_states',len(states),'minimum_integer_slack',minimum)
    print('x',Fraction(p,q),'t',Fraction(r,s),'z',[str(Fraction(*z)) for z in zs])
    print('Arb expression',-2*x.log()/t.log(),'positive exponent',margin)
    print('CERTIFIED CANDIDATE, UNREFEREED: C91 >=',Fraction(a,b),'=',float(Fraction(a,b)))
    print('artifact_sha256',hashlib.sha256(path.read_bytes()).hexdigest())
    print('elapsed_seconds',time.time()-begun)

if __name__=='__main__':
    if not __debug__:raise RuntimeError('assertions must remain enabled')
    main()
