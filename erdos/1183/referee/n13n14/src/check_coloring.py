import json, sys, hashlib
p=sys.argv[1]; raw=open(p,'rb').read(); d=json.loads(raw)
n=d['n']; col=d['colors']; word=d['rank_word']
assert len(col)==1<<n, len(col)
derived=['']*(n+1); ok=True
for S,c in enumerate(col):
    k=bin(S).count('1'); ch=str(c)
    if derived[k]=='': derived[k]=ch
    elif derived[k]!=ch: ok=False
w=''.join(derived)
print(f"{p}: sha256={hashlib.sha256(raw).hexdigest()} n={n} entries={len(col)} values={sorted(set(col))} size-only={ok} derived_word={w} matches_claimed={w==word}")
print("keys:", sorted(d.keys()))
for fam_s in sys.argv[2:]:
    fam=[int(x) for x in fam_s.split(',')]; F=set(fam)
    cl=all((a|b) in F and (a&b) in F for a in F for b in F)
    print(f"family {fam}: distinct={len(F)} closed={cl} colours={sorted({col[S] for S in F})} sizes={[bin(S).count('1') for S in fam]}")
