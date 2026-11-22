"""Rigorous upper bound on D = int_{-2}^{2} max(Phi,0) dt.  See README.md.
usage: python -I dint.py [--zscale 1.001] [--tau 1e-9] [--out name]"""
import sys, time, json, math, argparse, resource
import os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
from fractions import Fraction as Fr
import numpy as np
import flint
from flint import fmpq, arb
from load import load
T0=time.time()
ap=argparse.ArgumentParser(); ap.add_argument('--zscale',default=None); ap.add_argument('--tau',type=float,default=1e-9)
ap.add_argument('--out',default='main'); ap.add_argument('--maxdepth',type=int,default=36)
args=ap.parse_args()
flint.ctx.prec=128
def Q(fr): return fmpq(fr.numerator, fr.denominator)
def fl(q):  # correctly rounded float of fmpq (CPython int/int true division is correctly rounded)
    return int(q.p)/int(q.q)
d=load()
c0=Q(d['c0']); y2=Q(d['y2'])
cos=[(Q(a),Q(b)) for a,b in d['cos']]
ctrl=None
if args.zscale is not None:
    j=max(range(len(cos)),key=lambda i: abs(cos[i][1]))
    s=Q(Fr(args.zscale)); cos[j]=(cos[j][0],cos[j][1]*s); ctrl=dict(index=j,xi=str(cos[j][0]),scale=args.zscale)
H=[Q(x) for x in d['H']]
Zx={i:Q(v) for i,v in d['Z'].items()}
rows=[(Q(mu),n,[Q(x) for x in g]) for mu,n,g in d['rows']]
# ---------- breakpoints & exact piece coefficients Phi_piece(t)=A+B t+y2 t^2+sum z cos(xi t)
macro=set(Fr(k,120) for k in range(241))
for mu,n,g in rows:
    macro|=set(Fr(2*k,n) for k in range(n+1))
macro=sorted(macro)
mA=[];mB=[]
for j in range(len(macro)-1):
    lo,hi=macro[j],macro[j+1]; mid=(lo+hi)/2
    k=int(mid*120); B=(H[k+1]-H[k])*120; A=H[k]-B*fmpq(k,120)
    A=A+c0
    for mu,n,g in rows:
        a=fmpq(2,n); k=int(mid*n/2)
        vk=g[0]/a if k==0 else g[k]/(2*a); vk1=g[k+1]/(2*a)
        b=(vk1-vk)/a; aa=vk-b*(k*a)
        A=A+mu*aa; B=B+mu*b
    mA.append(A);mB.append(B)
bps=sorted(set(Fr(i,65536) for i in range(131073))|set(macro))
NP=len(bps)-1
pA=[];pB=[]; mj=0
for p in range(NP):
    lo,hi=bps[p],bps[p+1]; mid=(lo+hi)/2
    while macro[mj+1]<=lo: mj+=1
    assert macro[mj]<=lo and hi<=macro[mj+1]
    i=int(mid*65536); A=mA[mj]+Zx[i] if i in Zx else mA[mj]
    pA.append(A); pB.append(mB[mj])
bpq=[fmpq(b.numerator,b.denominator) for b in bps]
bpf=np.array([b.numerator/b.denominator for b in bps])
Af=np.array([fl(a) for a in pA]); Bf=np.array([fl(b) for b in pB])
print('pieces',NP,'macro',len(macro),'t',round(time.time()-T0,1),flush=True)
# ---------- float data
xi=np.array([fl(a) for a,b in cos]); z=np.array([fl(b) for a,b in cos]); y2f=fl(y2)
NT=len(cos)
zxi=z*xi; zxi2=zxi*xi
Sz0=fl(sum((abs(b) for a,b in cos),fmpq(0)))*(1+1e-15); Sz1=fl(sum((abs(b)*a for a,b in cos),fmpq(0)))*(1+1e-15)
Sz2=fl(sum((abs(b)*a*a for a,b in cos),fmpq(0)))*(1+1e-15); Sz3=fl(sum((abs(b)*a**3 for a,b in cos),fmpq(0)))*(1+1e-15)
ay2=abs(y2f)*(1+1e-15)
u=2.0**-53; NN=NT+3
print('Sz0..3',Sz0,Sz1,Sz2,Sz3,flush=True)
def evalf(pid,c):
    X=np.multiply.outer(c,xi); C=np.cos(X); S=np.sin(X)
    A=Af[pid];B=Bf[pid]
    p0=A+B*c+y2f*c*c+C@z
    p1=B+2*y2f*c-S@zxi
    p2=2*y2f-C@zxi2
    aA=np.abs(A);aB=np.abs(B)
    E0=1.1*u*(NN*(aA+aB*c+ay2*c*c+Sz0)+3*c*Sz1+7*Sz0)
    E1=1.1*u*(NN*(aB+2*ay2*c+Sz1)+3*c*Sz2+8*Sz1)
    E2=1.1*u*(NN*(2*ay2+Sz2)+3*c*Sz3+9*Sz2)
    return p0,p1,p2,E0,E1,E2
def decide(p0,p1,p2,E0,E1,E2,h):
    """returns lo,hi enclosure of Phi_piece on [c-h,c+h]"""
    h2=h*h
    rnd=8*u*(np.abs(p0)+np.abs(p1)*h+np.abs(p2)*h2)
    slack=E0+E1*h+E2*h2/2+Sz3*h2*h/6+rnd+1e-300
    lo=p0-np.abs(p1)*h+np.minimum(0,p2)*h2/2-slack
    hi=p0+np.abs(p1)*h+np.maximum(0,p2)*h2/2+slack
    dsl=np.abs(p2)*h+Sz3*h2/2+E1+E2*h+8*u*(np.abs(p1)+np.abs(p2)*h)
    mono=(p1-dsl>0)|(p1+dsl<0)
    fL=p0-p1*h+p2*h2/2; fR=p0+p1*h+p2*h2/2
    lo2=np.minimum(fL,fR)-slack; hi2=np.maximum(fL,fR)+slack
    lo=np.where(mono,np.maximum(lo,lo2),lo); hi=np.where(mono,np.minimum(hi,hi2),hi)
    return lo,hi
# pieces: pid, fa, fb, exact endpoint ids (-1 => exact value is the float)
pid=np.arange(NP); fa=bpf[:-1].copy(); fb=bpf[1:].copy(); ia=np.arange(NP); ib=np.arange(1,NP+1); dep=np.zeros(NP,int)
final=[]  # tuples of arrays: pid,fa,fb,ia,ib,status(1 pos,-1 neg,0 bracket),lo,hi
level=0
while len(pid):
    n=len(pid); lo=np.empty(n); hi=np.empty(n)
    for s in range(0,n,8192):
        sl=slice(s,s+8192)
        c=(fa[sl]+fb[sl])/2; h=(fb[sl]-fa[sl])/2*(1+4*u)+1e-15
        r=evalf(pid[sl],c); lo[sl],hi[sl]=decide(*r,h)
    st=np.zeros(n,int); st[lo>=0]=1; st[hi<=0]=-1
    und=st==0
    canspl=und&(dep<args.maxdepth)&((fb-fa)>1e-13)&((fb-fa)*np.maximum(hi,0)>1e-18)
    done=~canspl
    final.append((pid[done],fa[done],fb[done],ia[done],ib[done],st[done],lo[done],hi[done]))
    print('level',level,'n',n,'pos',(st==1).sum(),'neg',(st==-1).sum(),'split',canspl.sum(),'bracket',(und&~canspl).sum(),'t',round(time.time()-T0,1),flush=True)
    m=canspl; c=(fa[m]+fb[m])/2
    pid=np.concatenate([pid[m],pid[m]]); nfa=np.concatenate([fa[m],c]); nfb=np.concatenate([c,fb[m]])
    ia=np.concatenate([ia[m],-np.ones(m.sum(),int)]); ib=np.concatenate([-np.ones(m.sum(),int),ib[m]])
    dep=np.concatenate([dep[m],dep[m]])+1; fa=nfa; fb=nfb; level+=1
P=[np.concatenate([f[k] for f in final]) for k in range(8)]
o=np.argsort(P[1],kind='stable'); P=[x[o] for x in P]
fpid,ffa,ffb,fia,fib,fst,flo,fhi=P
assert np.all(ffb[:-1]==ffa[1:]) and ffa[0]==0 and ffb[-1]==2
print('final pieces',len(fpid),'pos',(fst==1).sum(),'neg',(fst==-1).sum(),'bracket',(fst==0).sum(),flush=True)
def ex(fv,idx): return bpq[idx] if idx>=0 else fmpq(Fr(float(fv)).numerator,Fr(float(fv)).denominator)
# ---------- arb re-verification of small-margin decisions
axi=[arb(a) for a,b in cos]; az=[arb(b) for a,b in cos]
ay2a=arb(y2)
M3=arb(sum((abs(b)*a**3 for a,b in cos),fmpq(0)))
def arb_encl(p,a,b):
    a=arb(a); b=arb(b); c=(a+b)/2; h=(b-a)/2
    S0=arb(0);S1=arb(0);S2=arb(0)
    for x,zz in zip(axi,az):
        s_,c_=(x*c).sin_cos(); S0+=zz*c_; S1+=zz*x*s_; S2+=zz*x*x*c_
    A=arb(pA[p]);B=arb(pB[p])
    p0=A+B*c+ay2a*c*c+S0; p1=B+2*ay2a*c-S1; p2=2*ay2a-S2
    s=arb(0,1)  # [-1,1]
    R=M3*h**3/6*s
    full=p0+p1*h*s+p2*(h*h*arb(0.5,0.5))/2*2*0  # placeholder
    # centered form: p0 + p1*[-h,h] + p2*[0,h^2/2] + R
    q=p2*h*h/2; full=p0+p1*h*s+q*arb(0.5,0.5)+R
    dphi=p1+p2*h*s+M3*h*h/2*s
    if not (dphi>0 or dphi<0): return full
    fL=p0-p1*h+q+R; fR=p0+p1*h+q+R
    lo=min(fL.lower(),fR.lower()); hi=max(fL.upper(),fR.upper())
    lo2=max(lo,full.lower()); hi2=min(hi,full.upper())
    return arb(lo2).union(arb(hi2))
import multiprocessing as mp
def _ex2(v,i): return ex(v,i)
def _verify(ks):
    out=[]
    for k in ks:
        e=arb_encl(int(fpid[k]),ex(ffa[k],fia[k]),ex(ffb[k],fib[k]))
        okk=(fst[k]==1 and e.lower()>=0) or (fst[k]==-1 and e.upper()<=0)
        out.append((int(k),bool(okk)))
    return out
def _brk(ks):
    S=arb(0)
    for k in ks:
        a=ex(ffa[k],fia[k]); b=ex(ffb[k],fib[k])
        e=arb_encl(int(fpid[k]),a,b); up=e.upper()
        if up>0: S+=arb(b-a)*up
    m,e_=S.upper().mid().man_exp()
    return int(m),int(e_)
chk=np.nonzero(fst!=0)[0]
print('arb re-verify ALL',len(chk),'decided pieces',flush=True)
P_=mp.get_context('fork').Pool(4)
nfail=0
for lst in P_.map(_verify,[chk[i::50] for i in range(50)]):
    for k,okk in lst:
        if not okk: nfail+=1; fst[k]=0
print('arb failures (demoted to bracket):',nfail,'t',round(time.time()-T0,1),flush=True)
brk=np.nonzero(fst==0)[0]
print('brackets',len(brk),flush=True)
Bsum=arb(0)
for m,e_ in P_.map(_brk,[brk[i::50] for i in range(50)]):
    Bsum+=arb(m)*arb(2)**e_
P_.close()
arbhi={}
# ---------- antiderivative F and runs of positive pieces
# G(t)=int_0^t (A_p+B_p s)ds piecewise, exact prefix at breakpoints
Gc=[fmpq(0)]
for p in range(NP):
    a,b=bpq[p],bpq[p+1]; Gc.append(Gc[-1]+pA[p]*(b-a)+pB[p]*(b*b-a*a)/2)
def Fx(t,p):  # t exact fmpq inside piece p
    a=bpq[p]; G=Gc[p]+pA[p]*(t-a)+pB[p]*(t*t-a*a)/2
    ta=arb(t); s=arb(0)
    for x,zz in zip(axi,az): s+=zz/x*(x*ta).sin()
    return arb(G)+ay2a*ta**3/3+s
pos=fst==1
runs=[]; k=0; n=len(fst)
while k<n:
    if pos[k]:
        j=k
        while j+1<n and pos[j+1]: j+=1
        runs.append((k,j)); k=j+1
    else: k+=1
print('runs',len(runs),flush=True)
Dpos=arb(0)
for k,j in runs:
    Dpos+=Fx(ex(ffb[j],fib[j]),int(fpid[j]))-Fx(ex(ffa[k],fia[k]),int(fpid[k]))
Dup=2*(Dpos+Bsum); Dlo=2*Dpos
N0=fmpq(141670994486089423037343024410866487501393222560969,141670994486089356410880000000000000000000000000000)
L=fmpq(295115424188729399759259170770153384401616054763504786695772146837923638817310985375107967151349,775338951052420904588737482312221487781542035285383462905883789062500000000000000000000000000000)
Lt=fmpq(295115424188729399759259170770153384401616054763504786695772146837923638817310985375107967151349,775338951268261542560203221298558473843677269760519266128540039062500000000000000000000000000000)
Dupper=arb(Dup.upper()); Dlower=arb(Dlo.lower())
ratio=arb(N0)/Dupper   # rigorous lower bound on N0/D lies at ratio.lower()
rlo=arb(ratio.lower())
meas=2*float(sum((ffb-ffa)[pos])); measbr=2*float(sum((ffb-ffa)[fst==0]))
res=dict(control=ctrl,tau=args.tau,maxdepth=args.maxdepth,smooth_pieces=NP,final_pieces=int(len(fst)),
 n_pos=int(pos.sum()),n_neg=int((fst==-1).sum()),n_bracket=int(len(brk)),n_arb_checked=int(len(chk)),n_arb_fail=nfail,runs=len(runs),
 bracket_total_width=measbr,bracket_contribution_upper=(2*Bsum).upper().str(20,radius=False),
 measure_certified_positive=meas,
 D_up=Dupper.str(25,radius=False),D_lo=Dlower.str(25,radius=False),Dup_minus_Dlo=(Dupper-Dlower).str(5,radius=False),
 N0_over_Dup_lower=rlo.str(25,radius=False),
 margin_vs_Ltarget=(rlo-arb(Lt)).str(8,radius=False), N0_over_Dup_ge_Ltarget=bool(rlo>arb(Lt)),
 margin_vs_L=(rlo-arb(L)).str(8,radius=False), N0_over_Dup_ge_L=bool(rlo>arb(L)),
 Ltarget_float=arb(Lt).str(25,radius=False), L_float=arb(L).str(25,radius=False),
 N0_over_L=(arb(N0)/arb(L)).str(25,radius=False), N0_over_Ltarget=(arb(N0)/arb(Lt)).str(25,radius=False),
 margin_vs_038062762=(rlo-arb('0.38062762')).str(8,radius=False),
 runtime_s=round(time.time()-T0,1), maxrss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20)
print(json.dumps(res,indent=1))
json.dump(res,open(os.path.join(HERE,f'res_{args.out}.json'),'w'),indent=1)
