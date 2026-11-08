# Mechanical bundle of the real clean-room referee geometry.py and scalar.py.
# Only the now-redundant from geometry import * is removed.
"""Clean-room formulas from the stated cylindrical curve; no supplied code."""
import json
from flint import arb, arb_series, ctx
ctx.prec=160
ctx.cap=12
DATA=json.load(open('../candidate_high/CONSTRUCTION.json'))
p=DATA['parameters']; mod=DATA['modulation']
N,R,b,lam=[arb(p[k]) for k in ('N','R','reference_pitch','scale')]
h=(N-1)*b; s=(R*R+h*h).sqrt(); q=h/s; k=R/s
coef=[list(map(arb,mod['outer_cos'])),[-arb(v) for v in mod['inner_cos']]]
phase=list(map(arb,mod['phase_sin']))
pi=arb.pi()
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def sub(x,y): return [a-b for a,b in zip(x,y)]
def cross(x,y): return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def radius(u,j):
    r=coef[j][0]+0*u; rp=0*u; rpp=0*u
    for m,c in enumerate(coef[j][1:],1):
        r+=c*(m*u).cos(); rp-=m*c*(m*u).sin(); rpp-=m*m*c*(m*u).cos()
    return r,rp,rpp

def local(u,j):
    r,rp,rpp=radius(u,j); v=u; vp=1+0*u; vpp=0*u
    for m,c in enumerate(phase,1):
        v+=c*(m*u).sin(); vp+=m*c*(m*u).cos(); vpp-=m*m*c*(m*u).sin()
    cv,sv=v.cos(),v.sin()
    C=r*cv; D=r*sv
    Cp=rp*cv-r*sv*vp; Dp=rp*sv+r*cv*vp
    Cpp=(rpp-r*vp*vp)*cv-(2*rp*vp+r*vpp)*sv
    Dpp=(rpp-r*vp*vp)*sv+(2*rp*vp+r*vpp)*cv
    A=R-C; B=q*D
    pos=[A,B,h*u/N-k*D]
    vel=[-Cp-B/N,q*Dp+A/N,h/N-k*Dp]
    acc=[-Cpp-2*q*Dp/N-A/N**2,q*Dpp-2*Cp/N-B/N**2,-k*Dpp]
    return [[lam*x for x in vec] for vec in (pos,vel,acc)]

def rotate(vec,t,c=1):
    ct,st=t.cos(),t.sin()
    return [c*(vec[0]*ct-vec[1]*st),c*(vec[0]*st+vec[1]*ct),vec[2]]
def body(u,j,c=1): return [rotate(vec,u/N,c) for vec in local(u,j)]
def speed(u,j): return dot(local(u,j)[1],local(u,j)[1]).sqrt()
def curvature_F(u,j,rho=arb(1)):
    _,v,a=local(u,j); w=cross(v,a)
    return dot(v,v)**3-rho*rho*dot(w,w)
def Q(x): return arb(str(x))
def box(lo,hi): return Q((lo+hi)/2)+arb(0,Q((hi-lo)/2).upper())
def out(x): return str(x)
def endpoint(j):
    P,V,_=body(arb(0),j)
    vv=dot(V,V).sqrt(); pp=V[1]/vv; cc=V[2]/vv
    e=1 if j==0 else -1; Q=arb('15/2') if j==0 else arb('63/2')
    theta=cc.acos(); X=P[0]; Y=e*Q*(1-cc); Z=Q*e*pp; D=(X*X+Y*Y).sqrt()
    return dict(X=X,p=pp,c=cc,e=e,Q=Q,theta=theta,Y=Y,Z=Z,D=D)
ends=[endpoint(j) for j in range(2)]
def connector(l,j,c=1):
    a=ends[j]; Q,pp,cc,e=a['Q'],a['p'],a['c'],a['e']; t=l/Q
    P=[c*a['X'],c*Q*(pp*t.sin()+e*cc*(t.cos()-1)),Q*(e*pp*(1-t.cos())+cc*t.sin())]
    V=[arb(0),c*(pp*t.cos()-e*cc*t.sin()),e*pp*t.sin()+cc*t.cos()]
    return P,V

def oldcircle(t,j):
    a=ends[j]; X,Y,Z,D=[a[z] for z in ('X','Y','Z','D')]
    return [X*t.cos(),Y*t.cos(),Z+D*t.sin()],[-X*t.sin(),-Y*t.sin(),D*t.cos()]

def pair(u,d,j):
    P,V,_=local(u,0); W,T,_=local(u+d,j)
    W=rotate(W,d/N); T=rotate(T,d/N)
    z=sub(P,W)
    # Both move when u moves; in rotating first frame extra rotation is orthogonal to z.
    return dot(z,z),2*dot(z,sub(V,T)),-2*dot(z,T)

import time
res={}
def save(key,val):
    res[key]=({'ball':str(val),'lower':str(val.lower()),'upper':str(val.upper())} if isinstance(val,arb) else val)
    print(key,res[key],flush=True)

def bound(fun,lo,hi,test,limit=35):
    stack=[(lo,hi,0)]; acc=None; count=0
    while stack:
        l,r,d=stack.pop(); mid=(l+r)/2; U=box(l,r)
        v=fun(U)
        if not test(v):
            M=fun(Q(mid)); z=fun(arb_series([U,1],2)); v=M+z[1]*(U-Q(mid))
        if test(v):
            acc=v if acc is None else acc.union(v); count+=1
        else:
            if d>=limit: raise RuntimeError((l,r,str(v)))
            stack.extend([(l,mid,d+1),(mid,r,d+1)])
    return acc,count

if __name__=='__main__':
    from fractions import Fraction as F
    for j in range(2):
        z,n=bound(lambda u: local(u,j)[1][2],F(0),F(44,7),lambda x:x>arb('0.00000195') if j==0 else x>arb('0.30'))
        save('height_'+str(j),z); save('height_leaves_'+str(j),n)
        # natural uniform coarse bounds suffice for speed and radius
        rr=None; vv=None
        for i in range(2048):
            U=box(F(44*i,7*2048),F(44*(i+1),7*2048))
            ri=abs(radius(U,j)[0]); vi=speed(U,j)
            rr=ri if rr is None else rr.union(ri); vv=vi if vv is None else vv.union(vi)
        save('radius_'+str(j),rr); save('speed_'+str(j),vv)
        res['V'+str(j)]=str(vv.upper())
    # a'(u)=-sin(u) [a1+sum k ak U_(k-1)(cos u)].
    # |U_(k-1)| <= k, so this dominance proves max a=a(0).
    dominance=coef[0][1]-sum(m*m*abs(c) for m,c in enumerate(coef[0][2:],2))
    assert dominance>0
    save('outer_radius_dominance',dominance)
    amax=radius(arb(0),0)[0]
    save('outer_radius_max',amax)
    save('cross_bundle',lam*(2*R-2*amax)); assert lam*(2*R-2*amax)>2
    save('axis_h2_minus_R2',h*h-R*R)
    save('same_tail',lam*(9*h/N-2*amax*k))
    save('interface_tail',lam*(8*h/N-amax*k))
    save('outer_short',arb('3/2')*arb(res['V0']))
    save('inner_short',9*arb(res['V1']))
    # Independent eighth-order Taylor integration with full-cell derivative remainders.
    integrals=[]; errors=[]
    for j in range(2):
        total=arb(0); error=arb(0)
        for cell in range(512):
            m=pi*(2*cell+1)/512; d=pi/512; U=arb(m.mid(),(m.rad()+d).upper())
            a=speed(arb_series([m,1],9),j); B=speed(arb_series([U,1],9),j)
            total+=sum(2*d**(i+1)*a[i]/(i+1) for i in range(0,8,2))
            error+=2*d**9*abs(B[8])/9
        value=total+arb(0,error.upper())
        save('integral_'+str(j),value); integrals.append(value); errors.append(error)
    save('length_coefficient',(integrals[0]+integrals[1])/2)
    save('integration_remainder',(errors[0]+errors[1])/2)
    assert (integrals[0]+integrals[1])/2<arb('7.087559024')
    a,i=ends; Zstar=a['Z']+arb('21/10'); y=-i['Y']
    D=((a['X']+i['X'])**2+(a['Y']-y)**2).sqrt()/2
    E=4*(a['Q']*a['theta']+i['Q']*i['theta'])+pi*(a['D']+i['D']+2*D)+4*Zstar-2*(a['Z']+i['Z'])
    save('caps',E); assert E<150
    save('block_height',lam*2*pi*6*h)
    for j,a in enumerate(ends):
        for name,v in a.items(): save('end_'+str(j)+'_'+name,v)
    a,i=ends
    save('upper_circle_radius',D)
    save('plane_distance',(i['X']*a['Y']+a['X']*y)/D)
    save('nested_vertical_gap',a['Z']-i['Z']-i['D'])
    save('outer_Y_gap',a['Y']*arb(3).sqrt()/2)
    save('X_spacing',i['X']-a['X'])
    for j in range(2):
        save('connector_16_z_'+str(j),connector(arb(16),j)[0][2])
        save('connector_16_y_clear_'+str(j),abs(connector(arb(16),j)[0][1])-lam*(R+amax))
    cp=json.load(open('../candidate_high/CONTACT_POINT.json'))
    save('contact_input',cp)
    json.dump(res,open('scalar.json','w'),indent=2)
