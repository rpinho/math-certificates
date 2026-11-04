"""Referee implementation from PROOF formulas; no candidate code/data imports.

All acceptance decisions use python-flint Arb at 160 bits. Subdivision endpoints
are exact Fractions. A stack replaces each unresolved rectangle by both halves.
The program generates its own partition and never reads candidate certificates.
"""
from fractions import Fraction as F
from flint import arb, ctx
import json, time, os, sys

ctx.prec = 160
def A(x):
    if isinstance(x, arb): return x
    x = F(x)
    return arb(x.numerator) / x.denominator
def box(a,b):
    return A((a+b)/2) + arb(0, A((b-a)/2))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm2(v): return sum(x*x for x in v)
def rot(v,t,c=1):
    co,si=t.cos(),t.sin()
    return (c*(v[0]*co-v[1]*si),c*(v[0]*si+v[1]*co),v[2])

PI=arb.pi()
N=A('276/5'); R=A('293279789/100000000'); a=A('193279689/100000000')
i=A('3846709/50000000'); b=A('16209211/50000000')
lam=A('10001/10000'); h=(N-1)*b; s=(R*R+h*h).sqrt()
W=1-h/(s*N); B=h/s-1/N; C=R/s
rho=A('499951/500000'); target=1/rho
radii=[a,-i]

def body(r,c,u):
    sn,co=u.sin(),u.cos()
    p=rot((R-r*co,r*h/s*sn,h*u/N-r*C*sn),u/N,c)
    v=rot((r*W*sn,R/N+r*B*co,h/N-r*C*co),u/N,c)
    acc=rot((r*(W-B/N)*co-R/(N*N),r*(W/N-B)*sn,r*C*sn),u/N,c)
    return tuple(tuple(lam*x for x in z) for z in (p,v,acc))

caps=[]
for r,Q in [(a,A('15/2')),(-i,A('63/2'))]:
    yy=R-r+r*h/s*N; zz=h-r*C*N
    length=(yy*yy+zz*zz).sqrt()
    pp=yy/length; cc=zz/length; e=1 if pp>0 else -1
    theta=cc.acos(); X=lam*(R-r); Y=e*Q*(1-cc); Z=Q*abs(pp)
    D=(X*X+Y*Y).sqrt()
    V=lam*((s/N*(1+R/(s*s)*abs(r)))**2+(r*(N-h/s)/N)**2).sqrt()
    caps.append(dict(r=r,Q=Q,p=pp,c=cc,e=e,theta=theta,X=X,Y=Y,Z=Z,D=D,V=V))
cp,cm=caps; Zstar=cp['Z']+A('21/10')
Vnew=(cm['X']+cp['X'],cp['Y']+cm['Y'],A(0)); Dnew=norm2(Vnew).sqrt()/2

def connector(k,c,l):
    d=caps[k]; Q=d['Q']; p=d['p']; z=d['c']; e=d['e']; v=l/Q
    sn,co=v.sin(),v.cos()
    return ((c*d['X'],c*Q*(p*sn+e*z*(co-1)),Q*(e*p*(1-co)+z*sn)),
            (A(0),c*(p*co-e*z*sn),e*p*sn+z*co))

def semicircle(k,x):
    d=caps[k]; t=PI*x; sn,co=t.sin(),t.cos()
    return ((d['X']*co,d['Y']*co,d['Z']+d['D']*sn),
            (-PI*d['X']*sn,-PI*d['Y']*sn,PI*d['D']*co))

def same_bundle(r1,r2,u,d):
    """Relative rotation eliminates common axis phase before interval evaluation."""
    u2=u+d; sn,co=u.sin(),u.cos(); s2,c2=u2.sin(),u2.cos()
    p=(R-r1*co,r1*h/s*sn,-r1*C*sn)
    pu=(r1*sn,r1*h/s*co,-r1*C*co)
    q=rot((R-r2*c2,r2*h/s*s2,h*d/N-r2*C*s2),d/N)
    qu=rot((r2*s2,r2*h/s*c2,-r2*C*c2),d/N)
    qd=rot((r2*W*s2,R/N+r2*B*c2,h/N-r2*C*c2),d/N)
    v=sub(q,p); vu=sub(qu,pu)
    return lam*lam*norm2(v), (2*lam*lam*dot(v,vu),2*lam*lam*dot(v,qd))

def interface(kr,cr,kc,cc,u,l):
    p,v,_=body(radii[kr],cr,u); q,w=connector(kc,cc,l); d=sub(p,q)
    return norm2(d),(2*dot(d,v),-2*dot(d,w))

def cap_pair(c,x,y):
    L=cp['Q']*cp['theta']; p,v=connector(0,c,L*x); q,w=semicircle(1,y)
    d=sub(p,q)
    return norm2(d),(2*L*dot(d,v),-2*dot(d,w))

def cover(name,fun,domain,threshold,short=None):
    start=time.monotonic(); stack=[(tuple((F(a),F(b)) for a,b in domain),0)]
    nodes=leaves=arcs=0; maxdepth=0; worst=None
    while stack:
        bounds,depth=stack.pop(); nodes+=1; maxdepth=max(depth,maxdepth)
        if short and short(bounds): arcs+=1; leaves+=1; continue
        xs=[box(a,b) for a,b in bounds]
        val,grad=fun(*xs)
        lb=val.lower()
        if not lb>threshold:
            mids=[A((a+b)/2) for a,b in bounds]
            center,_=fun(*mids)
            taylor=center+sum(g*arb(0,A((b-a)/2)) for g,(a,b) in zip(grad,bounds))
            if taylor.lower()>lb: lb=taylor.lower()
        if lb>threshold:
            leaves+=1
            if worst is None or lb<worst: worst=lb
            continue
        if depth>=65:
            raise RuntimeError((name,'UNRESOLVED',bounds,str(val),str(threshold)))
        # Split the dimension contributing most to the mean-value error.
        scores=[float(abs(g).upper()*A(b-a)) for g,(a,b) in zip(grad,bounds)]
        j=max(range(len(bounds)),key=lambda j:scores[j])
        left=list(bounds); right=list(bounds); aa,bb=bounds[j]; mid=(aa+bb)/2
        left[j]=(aa,mid);right[j]=(mid,bb)
        stack.append((tuple(right),depth+1));stack.append((tuple(left),depth+1))
        if nodes%200000==0:
            print(json.dumps(dict(progress=name,nodes=nodes,stack=len(stack))),flush=True)
    out=dict(name=name,nodes=nodes,leaves=leaves,short_arc_leaves=arcs,maxdepth=maxdepth,
             lower=str(worst),threshold=str(threshold),seconds=round(time.monotonic()-start,3))
    print(json.dumps(out),flush=True)
    return out

def curvature_cover(k,lower):
    """Direct curvature-radius formula on a fresh dyadic phase subdivision."""
    stack=[(F(0),F(44,7),0)]; leaves=0; worst=None; maximum_depth=0
    while stack:
        lo,hi,depth=stack.pop(); u=box(lo,hi); sn,co=u.sin(),u.cos();r=radii[k]
        v=tuple(lam*x for x in (r*W*sn,R/N+r*B*co,h/N-r*C*co))
        aa=tuple(lam*x for x in (r*(W-B/N)*co-R/(N*N),r*(W/N-B)*sn,r*C*sn))
        vv=norm2(v); cr=norm2(cross(v,aa))
        margin=vv**3-lower*lower*cr
        if vv>0 and margin>0:
            rad=(vv**3/cr).sqrt()
            if worst is None or rad.lower()<worst: worst=rad.lower()
            leaves+=1;maximum_depth=max(depth,maximum_depth)
        else:
            assert depth<40,(k,lo,hi,str(margin))
            mid=(lo+hi)/2;stack.extend([(lo,mid,depth+1),(mid,hi,depth+1)])
    _,v0,a0=body(radii[k],1,A(0))
    sample_radius=(norm2(v0)**3/norm2(cross(v0,a0))).sqrt()
    out=dict(name='curvature_'+str(k),certified_radius_lower=str(lower),
             raw_interval_lower=str(worst),leaves=leaves,maxdepth=maximum_depth)
    out['sample_radius_upper']=str(sample_radius)
    print(json.dumps(out),flush=True);return out

def scalar_checks():
    checks={}
    def gt(name,lhs,rhs):
        assert lhs>rhs,(name,str(lhs),str(rhs))
        checks[name]={'lhs':str(lhs),'relation':'>','rhs':str(rhs)}
    # All clearances here are for the original curve at target radius 1/rho.
    t=target
    gt('full_phase_cover',A('44/7'),2*PI)
    gt('axis_pitch',h*h,R*R)
    gt('different_bundle_distance',2*lam*(R-a),2*t)
    gt('outer_short_arc',PI*t,A('3/2')*cp['V'])
    gt('inner_short_arc',PI*t,9*cm['V'])
    gt('same_bundle_vertical_tail',lam*(9*h/N-2*a*C),2*t)
    gt('interface_body_tail',lam*(8*h/N-a*C),2*t)
    gt('opposite_cap_separation_one_axis_turn',lam*2*PI*h,2*t)
    gt('inner_X',cm['X'],2*t)
    gt('middle_X_spacing',2*cp['X'],2*t)
    gt('adjacent_X_spacing',cm['X']-cp['X'],2*t)
    gt('lower_inner_height',cm['Z'],2*t)
    gt('lower_circle_height_separation',cp['Z']-cm['Z']-cm['D'],2*t)
    gt('outer_circle_radius',cp['D'],4*t)
    gt('inner_circle_radius',cm['D'],t)
    gt('outer_opposite_Y',cp['Y']*A(3).sqrt()/2,2*t)
    gt('upper_circle_radius',Dnew,4*t)
    gt('upper_connector_gap',Zstar-cp['Z'],2*t)
    plane=2*(cm['X']*cp['Y']-cp['X']*cm['Y'])/(2*Dnew)
    gt('upper_plane_separation',plane,2*t)
    gt('Y_sum_positive',cp['Y']+cm['Y'],A(0))
    for k,d in enumerate(caps):
        gt('height_derivative_'+str(k),h-abs(d['r'])*C*N,A(0))
        gt('connector_curvature_radius_'+str(k),d['Q'],t)
        gt('connector_c_positive_'+str(k),d['c'],A(0))
        gt('connector_c_less_than_one_'+str(k),A(1),d['c'])
        L=d['Q']*d['theta']
        if L>16:
            q,_=connector(k,1,A(16))
            if 16*d['c']>2*t: gt('connector_tail_'+str(k),16*d['c'],2*t)
            else: gt('connector_tail_'+str(k),abs(q[1])-lam*(R+a),2*t)
        else: gt('connector_covered_length_'+str(k),A(16),L)
        gt('upper_extension_positive_'+str(k),Zstar-d['Z'],A(0))
    means=[]
    for r in radii:
        means.append((s*s/(N*N)+r*r*W*W+r*r*R*R/(2*s*s*N*N)).sqrt())
    coefficient=lam*PI*sum(means)
    Elower=2*sum(d['Q']*d['theta'] for d in caps)+PI*(cp['D']+cm['D'])
    Eupper=2*sum(d['Q']*d['theta'] for d in caps)+4*Zstar-2*(cp['Z']+cm['Z'])+2*PI*Dnew
    gt('body_coefficient',A('3545553/500000'),coefficient)
    gt('cap_length',A(135),Elower+Eupper)
    # Independent tangent-point upper enclosure, using the exact points cited.
    p,v,_=body(a,-1,A('-6252895448239407/1000000000000000'))
    q,_,_=body(-i,-1,A('-970222336641621/200000000000000'))
    chord=sub(q,p); ds=norm2(chord);vs=norm2(v);dv=dot(chord,v)
    contact=(ds*ds*vs/(4*(ds*vs-dv*dv))).sqrt()
    gt('contact_upper',A('1000099/1000000'),contact)
    gt('contact_lower',contact,target)
    out=dict(checks=checks,body_coefficient=str(coefficient),lower_cap_length=str(Elower),
             upper_cap_length=str(Eupper),cap_length=str(Elower+Eupper),
             finite_length_n1=str(1104*coefficient+Elower+Eupper),
             scaled_coefficient=str(rho*coefficient),target_radius=str(target),
             contact_upper_enclosure=str(contact),caps=[{k:str(v) for k,v in d.items()} for d in caps],
             upper_circle_radius=str(Dnew))
    print(json.dumps(out),flush=True)
    return out

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    results=dict(pid=os.getpid(),precision_bits=ctx.prec,mode=mode,
                 actual_nice=os.getpriority(os.PRIO_PROCESS,0))
    if mode in ('all','scalars'):results['scalars']=scalar_checks()
    if mode in ('all','curvature'):
        results['curvatures']=[curvature_cover(0,A('1.98788')),curvature_cover(1,A('1.46347'))]
    if mode in ('all','body'):
        results['body']=[cover('outer_self',lambda u,d:same_bundle(a,a,u,d),
                              [(0,F(44,7)),(F(3,2),9)],4*target*target),
                         cover('outer_inner',lambda u,d:same_bundle(a,-i,u,d),
                              [(0,F(44,7)),(-9,9)],4*target*target)]
    if mode in ('all','caps'):
        results['caps']=[cover('lower_cross_'+str(c),lambda x,y:cap_pair(c,x,y),
                             [(0,1),(0,1)],4*target*target) for c in [-1,1]]
    if mode in ('all','interfaces'):
        out=[]
        # A half-turn about Z sends both labels c -> -c, leaving distances
        # unchanged, so eight covers exhaust the sixteen ordered choices.
        for kr in range(2):
          for kc in range(2):
            for cc in [-1,1]:
                short=None
                if kr==kc and cc==1:
                    short=lambda bds: -A(bds[0][0])*caps[kr]['V']+A(bds[1][1])<PI*target
                out.append(cover('interface_'+str((kr,1,kc,cc)),
                    lambda u,l:interface(kr,1,kc,cc,u,l),[(-8,0),(0,16)],4*target*target,short))
        results['interfaces']=out
    with open('geometry_'+mode+'.json','w') as f:json.dump(results,f,indent=2)

if __name__=='__main__':main()
