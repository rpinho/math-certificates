"""Independent scalar-cover replay with a custom Decimal interval kernel.
The first harmonic uses exact cell integrals of exp(-i theta), not the
submission's midpoint phase-error estimate. Data-only certificate import.
"""
import json, pathlib, time, hashlib, collections
from fractions import Fraction as F
from intervals import I,PI,DN,UP,RN,D,imax,imin,sincos
Z=I('23/200');KAP=I('3/25');DELTA=F('1/1000000')
OUT=pathlib.Path('results');OUT.mkdir(exist_ok=True)

def floors(box):
    xl,xh,yl,yh,bl,bh=map(I,box)
    al=(xl**2+yl**2).sqrt();ah=(xh**2+yh**2).sqrt()
    slo=xl**2+yl**2+2*KAP*(1-bh**2)
    shi=xh**2+yh**2+2*KAP*(1-bl**2)
    if ah.hi==0:jl=jh=I(0)
    else:
        jl=(al**2+((1+bl)*xl**2+(1-bh)*yl**2)/(2*ah))/(1+ah)
        jh=ah if al.lo==0 else imin(ah,(ah**2+((1+bh)*xh**2+(1-bl)*yh**2)/(2*al))/(1+al))
    return imax(slo,jl).lo,imax(shi,jh).hi

CACHE={}
def angles(n):
    if n in CACHE:return CACHE[n]
    h=PI/n;s,c=sincos(h);ss,cc=sincos(2*h);sinc=s/h
    arr=[]
    for j in range(n):
        c2=c*c-s*s;s2=2*s*c
        rc=s.abs()*h+h*h/2;rs=c.abs()*h+h*h/2;r2=2*s2.abs()*h+2*h*h
        cb=I(max(D(-1),(c-rc).lo),min(D(1),(c+rc).hi))
        sb=I(max(D(-1),(s-rs).lo),min(D(1),(s+rs).hi))
        c2b=I(max(D(-1),(c2-r2).lo),min(D(1),(c2+r2).hi))
        arr.append((c,s,cb,sb,c2b))
        s,c=s*cc+c*ss,c*cc-s*ss
    # All centers produced by interval-enclosed exact rotations, no float trig.
    CACHE[n]=(arr,sinc)
    return CACHE[n]

def grid(box,n):
    xl,xh,yl,yh,bl,bh=map(I,box)
    x=I(xl.lo,xh.hi);y=I(yl.lo,yh.hi);b=I(bl.lo,bh.hi)
    low,high=floors(box);floor=I(low,high)
    arr,sinc=angles(n)
    slog=I(0);dc=I(0);ds=I(0);err=I(0)
    for c,s,cb,sb,c2b in arr:
        W=imax(floor,x*cb+y*sb+2*KAP*(1-b*c2b))
        if W.lo<=0:return None
        ll=W.log();mid=(I(ll.lo)+I(ll.hi))/2;rad=(I(ll.hi)-I(ll.lo))/2
        slog+=I(ll.lo);dc+=mid*c;ds+=mid*s;err+=rad
    harmonic=( (sinc*dc/n)**2+(sinc*ds/n)**2 ).sqrt()+err/n
    gap=(slog/n).exp()-Z*(1+harmonic**2)
    return gap

def small_region():
    # For b<=.999, A0^2 >= .12-delta/2. For b>=.999 use h_a.
    delta=I(DELTA);ell=I('2997/6250')
    assert (I('3/25')-delta/2-Z).lo>0
    assert (I('6/25')*(1-I('999/1000'))-delta).lo>0
    assert (4*ell-(1+delta)**2).lo>0
    d0=delta*(1+delta)/(2*ell)
    assert (1-2*d0).lo>0
    endpoints=[F(1,2**j) for j in range(17,0,-1)]+[F(16383,16384)]
    total=I(0);count=0;previous=None;mingamma=None
    for left,right in zip(endpoints,endpoints[1:]):
        for j in range(512):
            u=left+(right-left)*F(j,512);v=left+(right-left)*F(j+1,512)
            if previous is not None:assert u==previous
            previous=v
            assert (I(u)-d0).lo>0 and u>2*DELTA/F('2997/6250')
            gamma=1/v-DELTA/(F('2997/6250')*v*v);assert gamma>1
            mingamma=gamma if mingamma is None else min(mingamma,gamma)
            # Exact density for X=sin²(theta) is 1/(pi sqrt(X(1-X))).
            maxquad=F(1,4) if u<=F(1,2)<=v else max(u*(1-u),v*(1-v))
            masslower=I(v-u)/(PI*I(maxquad).sqrt())
            total+=masslower*I(gamma).log();count+=1
    gap=(ell/16).log()+total-Z.log();assert gap.lo>0,gap
    return {'bins':count,'log_margin':gap.pair(),'method':'density lower bound in each rational bin; no asin quadrature','min_gamma':str(mingamma)}

def run():
    path='../c68r3/certificates/row-cover.json';data=json.load(open(path))
    assert data['model']=='contact_row_v1' and F(data['zeta'])==F('23/200') and F(data['delta'])==DELTA and F(data['kappa'])==F('3/25')
    root=list(map(F,data['root']));assert root==[F(0),F('17/50'),F(0),F('17/50'),F('7/10'),F(1)]
    leaves=[]
    def walk(node,box,address):
        if 'kind' in node:
            assert set(node)<= {'kind','n'};leaves.append((address,box,node));return
        assert set(node)=={'axis','mid','left','right'}
        a=node['axis'];assert type(a) is int and 0<=a<=2
        m=F(node['mid']);assert box[2*a]<m<box[2*a+1]
        left=box.copy();right=box.copy();left[2*a+1]=m;right[2*a]=m
        walk(node['left'],left,address+'L');walk(node['right'],right,address+'R')
    walk(data['tree'],root,'')
    volume=lambda box:(box[1]-box[0])*(box[3]-box[2])*(box[5]-box[4])
    assert sum(volume(b) for _,b,_ in leaves)==volume(root)
    records=[];start=time.monotonic();small=small_region();print('small',small,flush=True)
    for i,(address,box,node) in enumerate(leaves):
        kind=node['kind'];xl,xh,yl,yh,bl,bh=box;rec={'address':address,'box':list(map(str,box)),'kind':kind}
        if kind=='psd':
            peak=1-bl*bl-2*(1-bl)*xl*xl-2*(1+bl)*yl*yl
            assert peak<0;rec['upper_psd']=str(peak)
        elif kind=='constant':
            low,_=floors(box);assert low>Z.hi;rec['lower_floor']=str(low)
        elif kind=='small':assert xh*xh+yh*yh<=DELTA*DELTA
        else:
            assert kind=='grid';n=node['n'];assert type(n) is int and n>=16
            gap=grid(box,n);assert gap is not None and gap.lo>0,(address,box,n,gap)
            rec.update(n=n,margin=gap.pair())
        records.append(rec)
        if i%10==0 or i==len(leaves)-1:
            print(i+1,len(leaves),kind,rec.get('margin'),round(time.monotonic()-start,2),flush=True)
            (OUT/'scalar-progress.json').write_text(json.dumps({'done':i+1,'total':len(leaves),'last':rec},indent=2))
    gridmin=min((D(r['margin'][0]),r['address']) for r in records if 'margin' in r)
    result={'input':path,'sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),'arithmetic':'independent directed Decimal, 65 digits','coverage':'exact rational split reconstruction plus exact volume identity','counts':dict(collections.Counter(r['kind'] for r in records)),'small':small,'minimum_grid_margin':[str(gridmin[0]),gridmin[1]],'leaves':records,'seconds':time.monotonic()-start,'all_pass':True}
    (OUT/'scalar-cover.json').write_text(json.dumps(result,indent=2));print('PASS',result['minimum_grid_margin'],flush=True)
if __name__=='__main__':run()
