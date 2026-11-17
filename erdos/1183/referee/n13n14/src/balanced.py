import sys, itertools, collections
sys.path.insert(0, sys.argv[0].rsplit('/',1)[0])
from poset_search import search, realise, closed
n=13; out=open(sys.argv[1],'w'); stats=collections.Counter(); fails=0; cnt=0
for ones in itertools.combinations(range(n+1),(n+1)//2):
    w=''.join('1' if i in ones else '0' for i in range(n+1)); cnt+=1
    done=False
    for c in '01':
        R={i for i,ch in enumerate(w) if ch==c}
        r,_=search(n,R,8)
        if r:
            fam=realise(n,*r); sz=[bin(S).count('1') for S in fam]
            assert len(fam)>=8 and closed(fam) and all(s in R for s in sz)
            # describe poset: number of elements, base size, weights, preds
            shape=f"|P|={len(r[1])} base={r[0]} elems={[(bin(d)[2:],wt) for d,wt in r[1]]}"
            out.write(f"{w} colour={c} sizes={sz} masks={fam} {shape}\n")
            stats[(c,len(r[1]))]+=1; done=True; break
    if not done: fails+=1; out.write(f"{w} NOT REJECTED\n")
print(f"balanced words: {cnt}; rejected: {cnt-fails}; not rejected: {fails}; by (colour,|P|): {dict(sorted(stats.items()))}")
