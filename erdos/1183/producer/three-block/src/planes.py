"""Exact two-block slice catalogues. Each rejection stores actual sets."""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import gzip, json, subprocess
from math import prod

WORDS = ('0010011100101100011011','0011001011100010110011',
         '1100110100011101001100','1101100011010011100100')

def save(path, obj):
    with gzip.GzipFile(str(path), 'wb', mtime=0) as f:
        f.write(json.dumps(obj,separators=(',',':')).encode())

def read(path):
    with gzip.open(path,'rt') as f: return json.load(f)

def rankmap(shape):
    a,b,c=shape
    return [x+y+k for k in range(c+1) for y in range(b+1) for x in range(a+1)]

class Oracle:
    def __init__(self):
        self.proc=subprocess.Popen(['src/finder'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    @lru_cache(maxsize=32768)
    def query(self,shape,w,c,threshold):
        print(*shape,c,threshold,w,file=self.proc.stdin,flush=True)
        k,*family=map(int,self.proc.stdout.readline().split())
        assert k==len(family)
        return tuple(family)
    def close(self):
        self.proc.stdin.close()
        assert self.proc.wait()==0

@lru_cache(maxsize=None)
def rankinfo(shape):
    ranks=rankmap(shape)
    return ranks,[ranks.index(i) for i in range(sum(shape)+1)]

def rejection(oracle,shape,w,z):
    n=sum(shape)
    ranks,spine=rankinfo(shape)
    scalar=''.join(w[i] for i in spine)
    rank_only=all(w[i]==scalar[r] for i,r in enumerate(ranks))
    for c,ext in enumerate((z,23-n-z)):
        need=14-ext
        if need<=0:
            family=()
        elif rank_only:
            family=oracle.query((n,0,0),scalar,c,need)
        else:
            family=oracle.query(shape,w,c,need)
        if len(family)>=need:
            start=n+1+(z if c else 0)
            return list(family)+[(1<<i)-1 for i in range(start,start+max(0,14-len(family)))]
    return None

def plane_catalogue():
    cache={}
    oracle=Oracle()
    for n in range(22):
        for b in range(n//2+1):
            a=n-b
            bycontext=[]
            records=[]
            raw=0
            # In a one-row-thick strip, extend the long axis to retain overlap.
            along_x=b==0 or (b==1 and a>1)
            stride=b+1 if along_x else a+1
            def transpose(w,width):
                return ''.join(w[i::width] for i in range(width))
            for z in range(24-n):
                live=[]
                families=[]
                if n==0:
                    candidates=['0','1']
                else:
                    child=cache[a-1,b] if along_x else cache[a,b-1]
                    candidates=[]
                    for first in '01':
                        for last in '01':
                            left=child[z+(last=='0')]
                            right=child[z+(first=='0')]
                            ends=defaultdict(list)
                            for v in right:
                                if v[-1]!=last: continue
                                if along_x: v=transpose(v,a)
                                ends[v[:-stride]].append(v[-stride:])
                            for u in left:
                                if u[0]!=first: continue
                                if along_x: u=transpose(u,a)
                                for tail in ends.get(u[stride:],()):
                                    w=u+tail
                                    candidates.append(transpose(w,stride) if along_x else w)
                raw+=len(candidates)
                for w in sorted(candidates):
                    f=rejection(oracle,(a,b,0),w,z)
                    if f is None: live.append(w)
                    else: families.append(f)
                bycontext.append(live)
                records.append(families)
            cache[a,b]=bycontext
            save(Path(f'data/p-{a}-{b}.gz'),records)
            if n==21: assert bycontext==[[],sorted(''.join(w[t] for t in rankmap((a,b,0))) for w in WORDS),[]]
            print(a,b,'joined',raw,'live',sum(map(len,bycontext)),'families',sum(map(len,records)),flush=True)
    save(Path('data/planes-cache.gz'),{f'{a}-{b}':v for (a,b),v in cache.items()})
    oracle.close()

if __name__=='__main__': plane_catalogue()
