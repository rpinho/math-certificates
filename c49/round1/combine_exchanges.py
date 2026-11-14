"""Exact enumeration of deletion-domain unions with a monotone count upper bound."""
import argparse,collections,itertools,json,math,subprocess,sys,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--radius',type=int,default=4);ap.add_argument('--suffix',default='');ap.add_argument('--certificate');args=ap.parse_args()
start=time.monotonic();r=args.radius;suffix=args.suffix or f'_r{r}'
records=json.loads(Path(f'logs/deletion_covers{suffix}.json').read_text())
# Every minimal cover is certified by exhaustive concrete-witness branching.
cover_to_candidates=collections.defaultdict(set)
for e in records:
    for rem in e['minimal_removals']:cover_to_candidates[frozenset(rem)].add(e['candidate'])
covers=list(cover_to_candidates);regions=set(covers);front=set(covers)
while front:
    new=set()
    for a in front:
        for b in covers:
            c=a|b
            if len(c)<=r and c not in regions:new.add(c)
    regions.update(new);front=new
base=[33969,64728,64728,88867]
if args.certificate:
    cert=json.loads(Path(args.certificate).read_text());assert cert['ports']==[0,1];base=[0]*4
    for m in cert['masks']:base[2*(m&1)+((m>>1)&1)]+=1
def rho(count):
    a,b,c,d=count
    return (b+c+math.sqrt((b-c)**2+4*a*d))/2
bar=rho(base);max_upper=0;promising=[]
for rem in regions:
    add=set.union(*(cover_to_candidates[c] for c in covers if c<=rem))
    counts=base[:]
    for m in rem:counts[2*(m&1)+((m>>1)&1)]-=1
    for m in add:counts[2*(m&1)+((m>>1)&1)]+=1
    upper=rho(counts);max_upper=max(max_upper,upper)
    if upper>bar+1e-8:promising.append({'remove':sorted(rem),'candidate_pool':sorted(add),'upper_port_counts':counts,'upper_rho':upper})
# Float is only a screening tool; each supposedly excluded count vector is
# checked with an exact comparison of quadratic surds against the same bar.
# Rational isolating intervals are computed here independently of checker.py.
from fractions import Fraction
from math import isqrt
S=10**50
assert base[1]==base[2]
barlo=base[1]*S+isqrt(base[0]*base[3]*S*S);barhi=barlo+1
exact_excluded=0
for rem in regions:
    add=set.union(*(cover_to_candidates[c] for c in covers if c<=rem))
    c=base[:]
    for m in rem:c[2*(m&1)+((m>>1)&1)]-=1
    for m in add:c[2*(m&1)+((m>>1)&1)]+=1
    a,b,d,e=c;disc=(b-d)**2+4*a*e
    hi=(b+d)*S+isqrt(disc*S*S)+1
    if hi<2*barlo:exact_excluded+=1
    elif c==base:exact_excluded+=1
    else:assert any(p['remove']==sorted(rem) for p in promising),('unresolved exact upper',c)
out={'radius':r,'candidates':len(records),'minimal_covers':len(covers),'removal_regions':len(regions),'exactly_excluded_by_monotone_count_bound':exact_excluded,'promising':promising,'seconds':time.monotonic()-start}
Path(f'logs/exchange_combined{suffix}.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v if k!='promising' else len(v) for k,v in out.items()},indent=2))
