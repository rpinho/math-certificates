"""Independent diagnostic test of the whole-disk coefficient transfer.
Laurent maps are scaled using boundary samples plus an angular Lipschitz
allowance. All arithmetic here is floating point: this is not a certificate.
"""
import json,numpy as np,time
from pathlib import Path
rng=np.random.default_rng(110468);c=.447;w=-np.log(c);Psi=(1+np.exp(-np.pi**2/w))**2/(8*np.exp(-np.pi**2/w));nang=4096
angles=2*np.pi*np.arange(nang)/nang
radii=np.r_[c+np.array([1e-9,1e-6,1e-4,.001]),np.linspace(c+.01,.99,25),1-1e-6]
minslack=1e9;minnorm=1e9;worst=None;count=0
for trial in range(1000):
    m=int(rng.integers(1,7));n=int(rng.integers(0,7));js=np.arange(-m,n+1)
    aa=(rng.normal(size=len(js))+1j*rng.normal(size=len(js)))
    aa*=np.where(js<0,c**(-js),1)
    if trial%5==0:aa[:]=0;aa[0]=c**m
    bound=0
    for r in (c,1.0):
        cc=aa*r**js;vals=cc@np.exp(1j*js[:,None]*angles[None,:])
        bound=max(bound,float(np.max(np.abs(vals))+np.pi/nang*np.sum(np.abs(js*cc))))
    aa/=bound*(1+1e-9)
    degree=int(rng.choice([0,1,4,12,32,64]));p=rng.normal(size=degree+1)+1j*rng.normal(size=degree+1)
    if trial%3==0:p=1/(np.arange(degree+1)+1)**.3
    f=np.convolve(aa,p);u=np.r_[np.zeros(m),p];u=np.pad(u,(0,len(f)-len(u)))
    diff=np.abs(f)**2-np.abs(u)**2;x=np.maximum(diff,0);y=np.maximum(-diff,0)
    norm=np.sum(-diff/(np.arange(len(diff))+1));scale=np.sum(np.abs(u)**2/(np.arange(len(u))+1))
    minnorm=min(minnorm,float(norm/scale));assert norm>-1e-10*scale
    for r in radii:
        t=r*r;ss=np.sin(np.pi*np.log(t)/(2*w))**2;H=np.sqrt(1+Psi/(2*ss));g=2/(1+H);eps=.115*g*(1-1/H)/2
        powers=t**np.arange(len(diff));X=x@powers;Y=y@powers
        slack=((1-g)*Y-eps*y[1]*t-X)/(X+Y+1e-300)
        assert slack>-1e-10,(trial,r,slack)
        if slack<minslack:minslack=float(slack);worst={'trial':trial,'r':float(r),'f':[[float(z.real),float(z.imag)] for z in f],'u':[[float(z.real),float(z.imag)] for z in u]}
        count+=1
out={'seed':110468,'pairs':1000,'radii_per_pair':len(radii),'radial_tests':count,'min_normalized_radial_slack':minslack,'min_normalized_squared_norm_gap':minnorm,'worst_radial_case':worst,'scope':'floating diagnostics, boundary-grid Lipschitz normalization of Laurent quotient; not proof','all_pass':True}
Path('results/transfer-attacks.json').write_text(json.dumps(out,indent=2));print(out['pairs'],out['radial_tests'],minslack,minnorm)
