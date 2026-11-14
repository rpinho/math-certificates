"""Exact certificate checker, written separately from search (same agent).

An exact Cartesian partition accelerates exhaustive pair/triple existence tests.
For disjoint boxes, a sunflower with repeated global members would have a
containment; after checking Sperner, any cross-box sunflower is distinct.
Within one box we explicitly exclude triples with all entries equal.
No construction lemmas or trusted core/pedant validity are used here.
"""
import argparse,collections,itertools,json,math,resource,time
from fractions import Fraction
from pathlib import Path

class Invalid(Exception):pass

def partition(family,n):
    # Fixed low 8 bits, then 10 bits, then all remaining bits. Any n>=3 works.
    a=min(n,8); b=min(n-a,10)
    by=collections.defaultdict(lambda:collections.defaultdict(list))
    for x in family:by[x&((1<<a)-1)][(x>>a)&((1<<b)-1)].append(x>>(a+b))
    boxes=[]
    for c,uv in sorted(by.items()):
        groups=collections.defaultdict(list)
        for u,vs in uv.items():groups[tuple(sorted(vs))].append(u)
        for vs,us in groups.items():boxes.append((c,tuple(sorted(us)),vs))
    assert sum(len(u)*len(v) for c,u,v in boxes)==len(family)
    return boxes,a,b

def check_family(cert):
    n=cert['n']; ports=cert['ports']; fam=cert['masks']
    if not isinstance(n,int) or not 3<=n<=64:raise Invalid('ground set')
    if len(ports)!=2 or len(set(ports))!=2 or any(type(p)!=int or not 0<=p<n for p in ports):raise Invalid('ports')
    if any(type(x)!=int or not 0<=x<(1<<n) for x in fam):raise Invalid('mask range')
    if len(set(fam))!=len(fam):raise Invalid('duplicate mask')
    boxes,a,b=partition(fam,n)
    types=sorted({z for c,u,v in boxes for z in (u,v)})
    tid={x:i for i,x in enumerate(types)}
    subset={}; flowers={}
    def contain(s,t,strict=False):
        key=(s,t,strict)
        if key not in subset:
            subset[key]=next(((x,y) for x in types[s] for y in types[t] if x&y==x and (not strict or x!=y)),None)
        return subset[key]
    def flower(i,j,k,nonconstant=False):
        key=(i,j,k,nonconstant)
        if key not in flowers:
            ans=None
            for x in types[i]:
                if ans is not None:break
                for y in types[j]:
                    inter=x&y; forbidden=x^y
                    for z in types[k]:
                        if (z&inter)==inter and not z&forbidden and (not nonconstant or x!=y or y!=z):
                            ans=(x,y,z);break
                    if ans is not None:break
            flowers[key]=ans
        return flowers[key]
    encoded=[(c,tid[u],tid[v]) for c,u,v in boxes]
    for i,(c,u,v) in enumerate(encoded):
        if contain(u,u,True) or contain(v,v,True):raise Invalid(f'Sperner inside box {i}')
        for j,(d,s,t) in enumerate(encoded):
            if i!=j and c&d==c:
                wu=contain(u,s);wv=contain(v,t)
                if wu and wv:
                    x=c|(wu[0]<<a)|(wv[0]<<(a+b));y=d|(wu[1]<<a)|(wv[1]<<(a+b))
                    raise Invalid(f'Sperner violation {x} subset {y}')
    examined=0
    for i,(c,u,v) in enumerate(encoded):
        if flower(u,u,u,True) or flower(v,v,v,True):raise Invalid(f'sunflower inside box {i}')
        for j in range(i,len(encoded)):
            d,s,t=encoded[j]; inter=c&d
            for k in range(j,len(encoded)):
                if i==k:continue
                e,w,z=encoded[k]
                if c&e!=inter or d&e!=inter:continue
                examined+=1
                wu=flower(u,s,w)
                if wu is None:continue
                wv=flower(v,t,z)
                if wv is None:continue
                triple=[cc|(uu<<a)|(vv<<(a+b)) for cc,uu,vv in zip((c,d,e),wu,wv)]
                assert len(set(triple))==3
                raise Invalid('sunflower '+str(triple))
    counts=[0]*4
    for x in fam:counts[2*((x>>ports[0])&1)+((x>>ports[1])&1)]+=1
    if not all(counts):raise Invalid('nonpositive port count')
    n00,n01,n10,n11=counts
    trace=n10+n01; det=n10*n01-n11*n00
    return {'n':n,'members':len(fam),'boxes':len(boxes),'cross_box_triples_considered':examined,'port_counts':counts,'transfer_matrix':[[n10,n11],[n00,n01]],'trace':trace,'determinant':det,'exponent':n-2,'distinct':True,'Sperner':True,'sunflower_free':True}

def above_rational(trace,det,exp,x):
    # True iff the Perron rate exceeds the nonnegative rational x.
    y=x**exp
    if 2*y<=trace:return True
    return y*y-trace*y+det<0

def isolate(trace,det,exp,bits=220):
    lo=Fraction(0);hi=Fraction(2)
    while above_rational(trace,det,exp,hi):hi*=2
    for _ in range(bits):
        mid=(lo+hi)/2
        if above_rational(trace,det,exp,mid):lo=mid
        else:hi=mid
    return lo,hi

def decimal(frac,digits=60):
    s=10**digits;q=frac.numerator*s//frac.denominator
    return ('-' if q<0 else '')+str(abs(q)//s)+'.'+str(abs(q)%s).zfill(digits)

def verify(cert):
    out=check_family(cert)
    lo,hi=isolate(out['trace'],out['determinant'],out['exponent'])
    if cert.get('claimed_rate_lower') is not None:
        claim=Fraction(cert['claimed_rate_lower'])
        if not above_rational(out['trace'],out['determinant'],out['exponent'],claim):raise Invalid('raised claimed rate')
    blo,bhi=isolate(129456,64728**2-3018723123,26)
    equal=(out['trace'],out['determinant'],out['exponent'])==(129456,64728**2-3018723123,26)
    out.update(rate_interval_rational=[str(lo),str(hi)],rate_interval_decimal=[decimal(lo),decimal(hi+Fraction(1,10**60))],bar_comparison='equal' if equal else 'above' if lo>bhi else 'below' if hi<blo else 'unresolved',margin_interval_decimal=[decimal(lo-bhi),decimal(hi-blo+Fraction(1,10**60))])
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output');args=ap.parse_args()
    start=time.monotonic()
    try:
        out=verify(json.loads(Path(args.certificate).read_text()));out['verdict']='ACCEPT'
    except Invalid as e:out={'verdict':'REJECT','reason':str(e)}
    out.update(wall_seconds=time.monotonic()-start,cpu_seconds=time.process_time(),peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,checker_authorship='separately written (same agent)')
    txt=json.dumps(out,indent=2);print(txt)
    if args.output:Path(args.output).write_text(txt+'\n')
    return 0 if out['verdict']=='ACCEPT' else 1
if __name__=='__main__':raise SystemExit(main())
