"""Proof replay using integer tables. No producer, finder, or SAT library imports."""
import gzip
import json
import sys
from functools import lru_cache
from itertools import combinations
from math import prod
from pathlib import Path
from collections import defaultdict,Counter

DATA=Path('data')
WORDS=['0010011100101100011011','0011001011100010110011',
       '1100110100011101001100','1101100011010011100100']
stats=Counter()

def read(path):
    with gzip.open(path,'rt') as f:return json.load(f)

def key(shape):return '-'.join(map(str,shape))
def index(p,s):return p[0]+(s[0]+1)*(p[1]+(s[1]+1)*p[2])
def positions(s):
    return [(i,j,k) for k in range(s[2]+1) for j in range(s[1]+1) for i in range(s[0]+1)]
def string(w,n):return format(w,f'0{n}b')[::-1]
def pack(w):return int(w[::-1],2)

def family_image(f,s,z,ambient=23,target=14):
    d=sum(s)
    assert type(f)==list and all(type(x)==int and 0<=x<1<<ambient for x in f),'invalid set'
    F=set(f)
    assert len(F)==len(f) and len(F)>=target,'witness size/distinctness'
    for x,y in combinations(F,2):
        assert x&y in F and x|y in F,'witness closure'
    cols=set(); cells=0
    for x in f:
        if x>>d:
            assert x==(1<<x.bit_length())-1,'exterior prefix'
            cols.add(int(x.bit_length()>d+z))
        else:
            counts=[]
            for width in s:
                counts.append((x%2**width).bit_count())
                x>>=width
            cells |= 1<<index(counts,s)
    assert len(cols)<=1,'exterior colours'
    return cells,cols or {0,1}

def direction(s):
    a,b,c=s
    if c:
        for i in (2,1,0):
            if s[i]>1:return i
        return 2
    return 1 if b>1 or a==b else 0

def joins(s,ax,child):
    length=prod(x+1 for x in s)
    domain=(1<<(24-sum(s)))-1
    stride=prod(x+1 for x in s[:ax])
    chunk=stride*s[ax]
    part=(1<<chunk)-1
    repeats=prod(x+1 for x in s[ax+1:])
    def scatter(w):
        return sum(((w>>(chunk*j))&part)<<((chunk+stride)*j) for j in range(repeats))
    bot=scatter((1<<(chunk*repeats))-1)
    overlap=bot&(bot<<stride)
    groups=defaultdict(list)
    lifts=[(scatter(w),contexts) for w,contexts in child.items()]
    for word,ctx in lifts:
        high=word<<stride
        groups[high&overlap].append((high,ctx))
    for low,lc in lifts:
        for high,hc in groups[low&overlap]:
            w=low|high
            budgets=domain & (lc>>(1-(w>>(length-1)))) & (hc>>(1-(w&1)))
            if budgets:yield w,budgets

def restrictions(s,cache):
    # Group consecutive source cells so a plane projection uses shifts and masks.
    points=positions(s)
    for ax,capacity in enumerate(s):
        free=tuple(x for j,x in enumerate(s) if j!=ax)+(0,)
        for k in range(capacity+1):
            source=[index(p,s) for p in points if p[ax]==k]
            runs=[]
            for out,idx in enumerate(source):
                if runs and runs[-1][2]+runs[-1][0]==idx:runs[-1][2]+=1
                else:runs.append([idx,out,1])
            fields=[(((1<<length)-1)<<start,start-dest) for start,dest,length in runs]
            ext=0
            for j in range(capacity+1):
                if j==k:continue
                p=[0,0,0] if j<k else list(s)
                p[ax]=j
                ext|=1<<index(p,s)
            yield cache[free],fields,ext

def face_path(s):
    if s[2]:return DATA/f't-{key(s)}.gz'
    return DATA/f'p-{s[0]}-{s[1]}.gz'

def eliminate(s,possible,records):
    assert len(records)==24-sum(s),'context count'
    for z,families in enumerate(records):
        rejected=defaultdict(set)
        for f in families:
            mask,cols=family_image(f,s,z)
            for c in cols:rejected[c].add(mask)
        eligible=[w for w,ctx in possible.items() if ctx>>z&1]
        stats['families']+=len(families)
        for w in eligible:
            if (any(w&m==0 for m in rejected[0]) or
                any(w&m==m for m in rejected[1])):
                possible[w] &= ~(1<<z)
    return {w:v for w,v in possible.items() if v}

def cnf_bytes(n,rows):
    return (f'p cnf {n} {len(rows)}\n'+''.join(' '.join(str(i) for i in r)+' 0\n' for r in rows)).encode()

def verify_face_cnf(s,ax,child,words,directory=DATA):
    p=directory/'face'/key(s)
    size=[x+1 for x in s]
    ch=list(s);ch[ax]-=1
    grid=positions(s)
    ids={pt:i for i,pt in enumerate(positions(ch))}
    shared=[]
    for pt in grid:
        if 0<pt[ax]<s[ax]:
            other=list(pt);other[ax]-=1
            shared.append((ids[pt],ids[tuple(other)]))
    leftidx=[]; rightidx=[]
    for pt in grid:
        if pt[ax]<s[ax]:leftidx.append(ids[pt]);rightidx.append(None)
        else:
            other=list(pt);other[ax]-=1
            leftidx.append(None);rightidx.append(ids[tuple(other)])
    claims={string(w,len(grid)) for w in words}
    cuts=read(p.with_suffix('.cuts.gz'))
    rows=[[1,2,3]]; n=3; labels={}
    for z in range(3):
        allowed=sorted((string(w,len(ids)),b) for w,b in child.items() if (b>>z)&3)
        m=len(allowed)
        rows.extend([[-1-z]+list(range(n+1,n+m+1)),[-1-z]+list(range(n+m+1,n+2*m+1))])
        for i,(left,lc) in enumerate(allowed,n+1):
            for j,(right,rc) in enumerate(allowed,n+m+1):
                bad=(not (lc>>(z+int(right[-1]=='0'))&1) or
                     not (rc>>(z+int(left[0]=='0'))&1) or
                     any(left[x]!=right[y] for x,y in shared))
                if not bad:
                    w=''.join(left[k] if k is not None else right[l] for k,l in zip(leftidx,rightidx))
                    bad=z==1 and w in claims
                    labels[z,w]=i,j
                if bad:rows.append([-i,-j])
        n+=2*m
    for z,w,f in cuts:
        m,cs=family_image(f,s,z)
        assert any((pack(w)&m)==(m if c else 0) for c in cs)
        i,j=labels[z,w]
        rows.append([-i,-j])
    assert p.with_suffix('.cnf').read_bytes()==cnf_bytes(n,rows),'face DIMACS regeneration'

def replay():
    cache={}
    @lru_cache(maxsize=None)
    def work(s):
        ax=direction(s)
        if sum(s):
            ch=list(s);ch[ax]-=1
            child=work(tuple(ch))
            possible=dict(joins(s,ax,child))
        else:possible={0:(1<<24)-1,1:(1<<24)-1}
        stats['joined_contexts']+=sum(m.bit_count() for m in possible.values())
        if s[2]:
            for ax2 in range(3):
                work(tuple(v for j,v in enumerate(s) if j!=ax2)+(0,))
            for tables,fields,ext in restrictions(s,cache):
                for w,ctx in list(possible.items()):
                    projected=sum((w&m)>>drop for m,drop in fields)
                    extra=ext.bit_count()-(w&ext).bit_count()
                    opt=ctx & (tables.get(projected,0)>>extra)
                    if opt:possible[w]=opt
                    else:del possible[w]
        result=eliminate(s,possible,read(face_path(s)))
        cache[s]=result
        stats['shapes']+=1
        stats['surviving_contexts']+=sum(m.bit_count() for m in result.values())
        if sum(s)==21:
            g=positions(s)
            claimed={pack(''.join(v[sum(p)] for p in g)):2 for v in WORDS}
            assert result==claimed,('face classification',s)
            if s[2]:
                file_words=read(DATA/f'live-{key(s)}.gz')
                assert file_words==[[],sorted(string(w,len(g)) for w in result),[]],'changed survivor cell'
            verify_face_cnf(s,ax,child,result)
            print('verified face',s,'z=1 exactly four words',flush=True)
        return result
    for c in range(8):
        for b in range(c,(21-c)//2+1): work((21-b-c,b,c))
    print(dict(stats),flush=True)
    return cache

if __name__=='__main__':replay()
