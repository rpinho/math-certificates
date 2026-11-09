"""Closed support cover using its own Taylor/concavity enclosures.
The density is represented by its exact slope jumps. Far terms use a power
series with an explicit geometric remainder. Near density terms use chords
or tangents of H, and near roots use a second derivative or max-distance bound.
"""
import argparse, json, time, multiprocessing as mp, os
from fractions import Fraction as F
from flint import arb, acb, arb_poly, arb_series, acb_series, ctx
from referee_check import A,H,HP,Certificate

ORDER=32

def model(c,left,right):
    mid=(left+right)/2; half=(right-left)/2
    a,h=A(mid),A(half)
    n=ORDER;ctx.cap=n+1
    total=arb_series([-c.loglc],n+1); err=arb(0)
    near=[]; roots=[]
    for e,s in c.jumps:
        d=a-e
        if abs(d)>4*h:
            ds=arb_series([d,h],n+1)
            positive=ds if d>0 else -ds
            total+=s*ds*ds*(positive.log()/2-arb(3)/4)
            ratio=h/abs(d)
            err+=abs(s)*d*d*ratio**(n+1)/((n+1)*n*(n-1)*(1-ratio))
        else:
            assert abs(d)+h<1, 'near H concavity domain'
            near.append((d,s))
    for root,b in c.roots:
        d=acb(a)-root
        if abs(d)>4*h:
            if d.imag.is_zero():
                dr=d.real
                ds=arb_series([dr,h],n+1)
                ls=(ds if dr>0 else -ds).log()
            else:
                zs=acb_series([d,acb(h)],n+1).log()
                ls=arb_series([v.real for v in zs.coeffs()],n+1)
            total-=b*ls
            ratio=h/abs(d)
            err+=b*ratio**(n+1)/((n+1)*(1-ratio))
        else: roots.append((d,b))
    p=arb_poly(total.coeffs());p0=p[0]+arb(0,err.upper());p[0]=p0
    return p,p.derivative(),p.derivative().derivative(),near,roots,h,err

def lower(mod,l,r):
    p,p1,p2,near,roots,h,err=mod
    v=A((l+r)/2);rad=A((r-l)/2);iv=arb(v,rad.upper())
    value=p(v);slope=p1(v);curv=p2(iv)
    for d,s in near:
        u=d+h*v
        if s>0:
            # H''=log|x|<=0 on this entire local domain: chord is a lower bound.
            hl=H(d+h*A(l));hr=H(d+h*A(r))
            value+=s*(hl+hr)/2
            slope+=s*(hr-hl)/(2*rad)
        else:
            # Negative multiple of H is convex, so its tangent is a lower bound.
            value+=s*H(u);slope+=s*h*HP(u)
    for d,b in roots:
        z=d+acb(h*v);zi=d+acb(h*iv)
        if abs(zi)>0:
            value-=b*abs(z).log()
            slope-=b*h*(1/z).real
            curv+=b*h*h*(1/(zi*zi)).real
        else:
            # This covers the root itself: -log|x-root| is +infinity there.
            value-=b*abs(zi).upper().log()
    low=value-abs(slope)*rad
    if not curv>=0: low+=curv.lower()*rad*rad/2
    return low.lower()

_C=None

def init(path):
    global _C
    ctx.prec=192;ctx.threads=1
    _C=Certificate(json.load(open(path)))

def cell_task(task):
    i,left,right=task;st=time.time();mod=model(_C,left,right)
    stack=[(F(-1),F(1),0)];leaves=[];worst=None;worstwhere=None;depth=0
    while stack:
        l,r,d=stack.pop();bound=lower(mod,l,r)
        if bound>A('1e-15'):
            x0=(left+right)/2+(right-left)*l/2;x1=(left+right)/2+(right-left)*r/2
            leaves.append([str(x0),str(x1),str(bound)])
            if worst is None or bound<worst:worst=bound;worstwhere=[str(x0),str(x1)]
            depth=max(depth,d)
        else:
            if d>=36 or len(leaves)>200000:
                raise RuntimeError(f'unresolved cell {i}, interval {l},{r}, bound {bound}, error {mod[-1]}')
            m=(l+r)/2;stack.extend([(m,r,d+1),(l,m,d+1)])
    return dict(cell=i,left=str(left),right=str(right),leaves=leaves,minimum=str(worst),where=worstwhere,depth=depth,seconds=time.time()-st,remainder=str(mod[-1]),near_nodes=len(mod[3]),near_roots=len(mod[4]))

def tasks(c):
    for i in c.cells:
        stack=[(c.x[i],c.x[i+1])]
        while stack:
            a,b=stack.pop()
            if b-a>F(1,256):
                m=(a+b)/2;stack.extend([(m,b),(a,m)])
            else:yield i,a,b

def run():
    ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--workers',type=int,default=4);ap.add_argument('--limit',type=int);ap.add_argument('--output',default='cover.jsonl');args=ap.parse_args()
    assert 1<=args.workers<=4
    c=Certificate(json.load(open(args.certificate)));c.check_point(F(3));todo=list(tasks(c))
    if args.limit:todo=todo[:args.limit]
    start=time.time();count=0;leaves=0;minimum=None;where=None;depth=0
    with open(args.output,'w') as out,mp.Pool(args.workers,initializer=init,initargs=(args.certificate,)) as pool:
        print('START',len(todo),'pieces',os.getpid(),flush=True)
        for res in pool.imap_unordered(cell_task,todo,chunksize=1):
            out.write(json.dumps(res)+'\n');out.flush();count+=1;leaves+=len(res['leaves'])
            lo=A(res['minimum'])
            if minimum is None or lo<minimum:minimum=lo;where=res['where'];mincell=res['cell']
            depth=max(depth,res['depth'])
            if count%50==0 or count==len(todo):print(count,'/',len(todo),'leaves',leaves,'seconds',round(time.time()-start,1),'min',str(minimum),flush=True)
    summary=dict(pieces=count,leaves=leaves,minimum=str(minimum),where=where,cell=mincell,maximum_depth=depth,seconds=time.time()-start,order=ORDER,prec=ctx.prec,complete=args.limit is None)
    json.dump(summary,open(args.output+'.summary.json','w'),indent=2);print(summary,flush=True)

if __name__=='__main__':run()
