"""Independent floating adversarial diagnostics, never proof of universal validity."""
import os,json,time
import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.linalg import solve_toeplitz, toeplitz, eigvalsh
from fractions import Fraction as F
from pathlib import Path
rng=np.random.default_rng(68110477);out=Path('results');out.mkdir(exist_ok=True);start=time.monotonic()
kap=.12;record={'seed':68110477,'status':'floating diagnostics only'}
# Genuine probability moments, with concentrated masses and near-antipodal supports.
mins={'row_minus_S':1e9,'row_minus_J':1e9,'support_M_bound':1e9,'psd':1e9}
worst={};count=0
for n in (2,3,4,8,32):
    for mode in range(4):
        for batch in range(10):
            B=1000
            theta=rng.uniform(-np.pi,np.pi,(B,n))
            if mode==1:theta=np.pi*rng.integers(0,2,(B,n))+rng.normal(0,10**rng.uniform(-8,-1),(B,n))
            if mode==2:theta=rng.normal(0,10**rng.uniform(-8,-.2),(B,n))
            weights=rng.dirichlet(np.full(n,.03 if mode==3 else 1),B)
            # Remove exact floating zeros from Dirichlet underflow from the support.
            z=np.exp(1j*theta);m1=np.sum(weights*z,axis=1);m2=np.sum(weights*z*z,axis=1);a=np.abs(m1)
            X=np.real(z*np.conj(m1[:,None]))/np.maximum(a[:,None],1e-300)
            M=np.max(np.where(weights>0,X,-np.inf),axis=1);q=np.sum(weights*X*X,axis=1)
            J=a*(q+a)/(1+a);S=a*a+2*kap*(1-np.abs(m2)**2)
            T=np.real(z*np.conj(m1[:,None]))+2*kap*(1-np.real(z*z*np.conj(m2[:,None])))
            maximum=np.max(np.where(weights>0,T,-np.inf),axis=1)
            b=np.abs(m2);rot=np.exp(-.5j*np.angle(m2));mr=m1*rot;x=mr.real;y=mr.imag
            vals={'row_minus_S':maximum-S,'row_minus_J':maximum-J,'support_M_bound':M-(q+a)/(1+a),'psd':1-b*b-2*(1-b)*x*x-2*(1+b)*y*y}
            for key,val in vals.items():
                idx=np.argmin(val)
                if val[idx]<mins[key]:mins[key]=float(val[idx]);worst[key]={'theta':theta[idx].tolist(),'weights':weights[idx].tolist()}
                assert val.min()>-2e-12,(key,val.min())
            count+=B
record['probability_moments']={'count':count,'minimum_slacks':mins,'worst':worst}
# Balanced image contacts: random triangles whose circular gaps are each <pi.
geom_min=1e9;row_identity=0;num=0
for batch in range(100):
    n=2000;phi=np.sort(rng.uniform(0,2*np.pi,(n,3)),axis=1)
    gaps=np.diff(np.c_[phi,phi[:,0]+2*np.pi],axis=1);phi=phi[np.max(gaps,axis=1)<np.pi]
    weights=np.column_stack((np.sin(phi[:,2]-phi[:,1]),np.sin(phi[:,0]-phi[:,2]),np.sin(phi[:,1]-phi[:,0])))
    weights/=weights.sum(axis=1)[:,None]
    theta=rng.uniform(-np.pi,np.pi,phi.shape);m1=np.sum(weights*np.exp(1j*theta),axis=1);m2=np.sum(weights*np.exp(2j*theta),axis=1)
    pdiff=phi[:,:,None]-phi[:,None,:];tdiff=theta[:,:,None]-theta[:,None,:]
    den=1-np.cos(pdiff);prof=(1-np.cos(tdiff))/2-kap*(1-np.cos(2*tdiff))
    pairs=[(0,1),(0,2),(1,2)];u=np.min(np.array([2*prof[:,i,j]/den[:,i,j] for i,j in pairs]),axis=0)
    assert np.min(u)>-1e-12
    # cosh(d_ij)=1+D*u*(1-v_i dot v_j); divide by D to avoid cancellation.
    rows=u[:,None]*np.sum(weights[:,None,:]*den,axis=2)
    row_identity=max(row_identity,float(np.max(np.abs(rows-u[:,None]))))
    T=np.real(np.exp(1j*theta)*np.conj(m1[:,None]))+2*kap*(1-np.real(np.exp(2j*theta)*np.conj(m2[:,None])))
    slack=1-np.max(T,axis=1)-u;geom_min=min(geom_min,float(slack.min()));assert slack.min()>-2e-12
    num+=len(phi)
record['balanced_geometric_contacts']={'count':num,'minimum_dimensionless_row_slack':geom_min,'maximum_row_identity_error':row_identity,'scope':'pairwise Fourier relaxation, not an annular interpolation claim'}
print('moments and geometry',count,num,mins,flush=True)
# scalar Schur criterion over the exact necessary PSD ellipse.
N=8192;theta=2*np.pi*(np.arange(N)+.5)/N;ct=np.cos(theta);st=np.sin(theta);ct2=np.cos(2*theta)
fevals=0

def param(v):
    b,rad,phi=v
    return np.sqrt((1+b)/2)*rad*np.cos(phi),np.sqrt((1-b)/2)*rad*np.sin(phi),b

def scalar_xyz(x,y,b,n=None):
    global fevals
    fevals+=1
    if n is None:cs,ss,cs2=ct,st,ct2
    else:
        th=2*np.pi*(np.arange(n)+.5)/n;cs,ss,cs2=np.cos(th),np.sin(th),np.cos(2*th)
    a=np.hypot(x,y);S=a*a+.24*(1-b*b)
    J=0 if a==0 else (a*a+((1+b)*x*x+(1-b)*y*y)/(2*a))/(1+a)
    W=np.maximum(np.maximum(S,J),x*cs+y*ss+.24*(1-b*cs2))
    logw=np.log(W);d=np.mean(logw*cs)+1j*np.mean(logw*ss)
    return float(np.exp(np.mean(logw))/(1+abs(d)**2))

opt=[]
for seed in range(6):
    res=differential_evolution(lambda v:scalar_xyz(*param(v)),[(.7,1),(0,.5),(0,np.pi/2)],seed=68110477+seed,popsize=20,maxiter=300,tol=1e-10,polish=True,workers=1)
    xyz=param(res.x);opt.append({'xyz':list(map(float,xyz)),'value':float(res.fun),'evaluations':res.nfev,'high_resolution_value':scalar_xyz(*xyz,n=262144)})
    print('scalar optimization',seed,opt[-1],flush=True)
# Endpoint and highly singular paths, not well represented by random continuous draws.
bound=[]
for a in [0,1e-12,1e-9,1e-6,1e-4,.001,.005,.01,.02,.04,.08,.16,.25,.34]:
    bound.append({'x':a,'y':0,'b':1,'value':scalar_xyz(a,0,1,n=262144)})
record['scalar_attack']={'evaluations':fevals,'optimizations':opt,'endpoint_samples':bound}
# Polynomial matrix minima test the actual one-coefficient inequality.
cases=[(0,0,1),(.02,0,1),(.1,0,1),(.01,.001,.999),(.05,.02,.99)]+[tuple(o['xyz']) for o in opt]
poly=[]
for x,y,b in cases:
    a=np.hypot(x,y);S=a*a+.24*(1-b*b);J=0 if a==0 else (a*a+((1+b)*x*x+(1-b)*y*y)/(2*a))/(1+a)
    n=131072;th=2*np.pi*np.arange(n)/n
    W=np.maximum(np.maximum(S,J),x*np.cos(th)+y*np.sin(th)+.24*(1-b*np.cos(2*th)))
    coeff=np.fft.fft(W)/n
    for deg in (16,64,256):
        col=coeff[:deg+1];rhs=np.zeros(deg+1);rhs[1]=1
        v=solve_toeplitz((col,np.conj(col)),rhs)
        energy=1/v[1].real;v=v/v[1]
        assert energy>.115-1e-8,(x,y,b,deg,energy)
        poly.append({'xyz':[float(x),float(y),float(b)],'degree':deg,'minimum_energy':float(energy)})
record['polynomial_attack']=poly;record['seconds']=time.monotonic()-start
(out/'contact-attacks.json').write_text(json.dumps(record,indent=2));print('DONE',record['seconds'],flush=True)
