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
