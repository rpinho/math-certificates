"""Exact prototype of the four-series strip encoding, without tilting.

Proposed method-2 marginal encoder: A,F,S,T,P are reconstructed from the
displayed equations, not taken as proved. Compare P at v=0 with direct actual
dominoes. u counts extra zero-pieces in closed nonempty leaf strips. A failed
coefficient comparison triggers the user's stop rule. This is not a bound.
"""
from collections import Counter
import argparse
import itertools
import json
from pathlib import Path
from audit_v2_marks import avoids


def plus(*items):
    out=Counter()
    for p in items:
        for k,x in p.items():out[k]+=x
    return out


def shift(p,du=0,dv=0,scale=1):
    return Counter({(u+du,v+dv):scale*x for (u,v),x in p.items()})


def mul(p,q):
    out=Counter()
    for (u,v),x in p.items():
        for (a,b),y in q.items():out[u+a,v+b]+=x*y
    return out


def product_at(arrays,n):
    acc=[Counter() for _ in range(n+1)]
    acc[0][0,0]=1
    for a in arrays:
        nxt=[Counter() for _ in range(n+1)]
        for j,p in enumerate(acc):
            if p:
                for k in range(min(n-j+1,len(a))):
                    if a[k]:nxt[j+k]=plus(nxt[j+k],mul(p,a[k]))
        acc=nxt
    return acc[n]


def lower(p):
    out=shift(p,scale=1)
    out=plus(out,shift(p,dv=1))
    for (u,v),x in p.items():
        if v:
            out[u,v-1]+=x
            out[u,v]+=x
    return out


def tower(N):
    one=Counter({(0,0):1})
    A=[one];F=[one];S=[Counter()];T=[Counter()];P=[Counter()]
    rows=[]
    for n in range(1,N+1):
        gA=Counter();gF=Counter();rT=Counter();upsP=Counter();rS=Counter();vT=Counter()
        for m in range(2,n+1):
            r=n-m
            gA=plus(gA,product_at([A]*m,r))
            gF=plus(gF,product_at([F]*m,r))
            upsP=plus(upsP,shift(product_at([A]*(m-1)+[P],r),scale=m))
            for a in range(m):
                rT=plus(rT,product_at([A]*a+[F]*(m-1-a)+[T],r))
                rS=plus(rS,product_at([A]*a+[F]*(m-1-a)+[S],r))
            # V = z^2 S/((1-zA)^2(1-zF)); coefficient of z^(m-2).
            for a in range(m-1):
                vT=plus(vT,shift(product_at([A]*a+[F]*(m-2-a)+[S,T],r),scale=a+1))
        A.append(plus(lower(A[-1]),A[-1],gA))
        F.append(plus(lower(F[-1]),shift(F[-1],du=1)))
        S.append(plus(lower(S[-1]),shift(S[-1],du=1),gA))
        T.append(plus(lower(T[-1]),T[-1],gF,rT))
        P.append(plus(lower(P[-1]),P[-1],upsP,rS,vT))
    return {'A':A,'F':F,'S':S,'T':T,'P':P}


def actual(n):
    out={x:Counter() for x in ['A','F','S','T','P']}
    witness={}
    for p in itertools.permutations(range(1,n+1)):
        if not avoids(p,(1,3,2,4)):continue
        for cut in range(n+1):
            low=tuple(x for x in p if x<=cut)
            top=tuple(x for x in p if x>cut)
            if not avoids(low,(1,3,2)) or not avoids(top,(2,1,3)):continue
            leaf={x for i,x in enumerate(top) if all(y<x for y in top[i+1:])}
            word=''.join('0' if x in leaf else '1' for x in sorted(top))
            out['A'][0]+=1
            if '1' not in word:
                out['F'][len(word)]+=1
                continue
            out['S'][word.index('1')]+=1
            # Blocks are maximal runs of ones, each followed by a leaf zero.
            runs=[]
            i=0
            while i<len(word):
                if word[i]=='0':i+=1;continue
                while i<len(word) and word[i]=='1':i+=1
                z=0
                while i<len(word) and word[i]=='0':z+=1;i+=1
                assert z>=1
                runs.append(z-1)
            out['T'][runs[-1]]+=1
            for extra in runs[:-1]:
                out['P'][extra]+=1
                witness.setdefault(extra,{'permutation':list(p),'cut':cut,'top':list(top),'word':word,'closed_strip_leaves':extra+1})
    return out,witness


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=7);args=ap.parse_args()
    encoded=tower(args.max_n)
    rows=[]
    for n in range(args.max_n+1):
        direct,witness=actual(n)
        row={'n':n,'series':{}}
        mismatch=False
        for name,arr in encoded.items():
            predicted=Counter({u:x for (u,v),x in arr[n].items() if v==0})
            differences={str(k):[predicted.get(k,0),direct[name].get(k,0)] for k in set(predicted)|set(direct[name]) if predicted.get(k,0)!=direct[name].get(k,0)}
            row['series'][name]={'matches':not differences,'differences':differences,'encoded':dict(predicted),'actual':dict(direct[name])}
            mismatch|=bool(differences)
        rows.append(row)
        Path('artifacts/strip_encoding_check.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if mismatch:
            Path('artifacts/strip_encoding_failure.json').write_text(json.dumps({'status':'FAILED; STOP','n':n,'comparison':row,'sample_actual_configurations':witness},indent=2)+'\n')
            raise SystemExit(2)
