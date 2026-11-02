"""Reviewer implementation. Reads only raw data; imports no target code.
Run on authorized pod, single process, standard library only.
"""
import json, math, hashlib, time
from fractions import Fraction as Q
from pathlib import Path
from decimal import Decimal, getcontext

ROOT=Path(__file__).resolve().parent
start=time.time()
inp=ROOT/'inputs'
receipt={'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inp.glob('*.json')}}
epi=json.loads((inp/'epi_certificate.json').read_text())
sp=json.loads((inp/'spectral_certificate_round3.json').read_text())
H=96
B={}
for d in range(1,H+1):
    # Exact binary search directly on the published quadratic inequality.
    lo,hi=0,d*d+1
    while hi-lo>1:
        m=(lo+hi)//2
        if 3*m*(m-1)<=2*(d**4-d*d):lo=m
        else:hi=m
    B[d]=lo

for ds,z in epi['certificates'].items():
    d=int(ds);nodes=z['nodes'];w=list(map(Q,z['weights']))
    assert len(nodes)==d+1 and len(set(nodes))==len(nodes)
    assert nodes[0]==1 and all(x>=1 for x in nodes)
    for j in range(1,d+1):assert sum(a*x**j for a,x in zip(w,nodes))==0
    assert w[0]+sum(a for a in w[1:] if a<0)>0
    B[d]=min(B[d],max(nodes)-1)

spectral=[]
for z in sp['certificates']:
    assert z['schema']=='c44-spectral-lattice-dual-v3'
    d,n=z['degree'],z['variables'];a={int(k):Q(v) for k,v in z['alpha'].items()}
    levels=[]
    for l in range(d+1):
        # Direct hypergeometric expectation of a character, no recurrence.
        val=Q(0)
        for k,c in a.items():
            numerator=sum((-1)**j*math.comb(k,j)*math.comb(n-k,l-j)
                          for j in range(max(0,l-(n-k)),min(l,k)+1))
            val+=c*Q(numerator,math.comb(n,l))
        levels.append(val)
    lower=a.get(0,0)-a.get(1,0)-sum(abs(v) for k,v in a.items() if k>=2)
    M=2**(d-1);penalty=Q(0)
    for l,c in enumerate(levels):
        t=c//2
        h=max(c*t-t*t,c*(t+1)-(t+1)**2)
        penalty+=math.comb(n,l)*h/M
    gap=lower-M-penalty
    assert gap>0,(d,gap)
    assert z['block_bound']==n-1
    B[d]=min(B[d],n-1)
    spectral.append({'degree':d,'excluded_blocks':n,'gap':str(gap)})
receipt['spectral']=spectral
receipt['block_bounds']=B

caps=[]
for d,c in [(4,Q(5,4)),(5,Q(31,16)),(6,Q(5,2))]:
    M=2**(d-1)
    nonminimum=d*M*M//(M+2)
    minimum=Q(2*d-2,2**d)+Q(1,2*M)+Q(M-1,M)*c
    r=max(nonminimum,minimum*2**d//1)
    caps.append({'d':d,'minimum_potential':str(minimum),'no_minimum_R':nonminimum,
                 'minimum_R':int(minimum*2**d//1),'R':int(r),'cap':str(Q(r,2**d))})
receipt['caps']=caps

def bound(caps,H):
    # Row induction in block budget; fixed scale gives exact integer arithmetic.
    unit=2**H
    C={d:int(caps.get(d,Q(d,2))*unit) for d in range(1,H+1)}
    cost={d:d*2**(H-d) for d in range(1,H+1)}
    row=[0]*(H+1)
    for b in range(1,max(B[d] for d in range(1,H+1))+1):
        best=0;new=[0]*(H+1)
        for d in range(1,H+1):
            best=max(best,row[d])
            new[d]=row[d] if b>B[d] else min(C[d],cost[d]+best)
        row=new
    finite=Q(max(row),unit)
    tail=Q(H**3+6*H**2+18*H+26,unit)
    return {'finite':str(finite),'tail':str(tail),'bound':str(finite+tail),
            'float':str(Decimal((finite+tail).numerator)/Decimal((finite+tail).denominator))}

getcontext().prec=85
base={3:Q(5,4),4:Q(31,16),7:Q(447,128)}
target=base|{4:Q(25,16),5:Q(71,32),6:Q(45,16)}
receipt['candidate']=bound(target,96)
receipt['baseline']=bound(base,96)
receipt['candidate_H72']=bound(target,72)
receipt['gain']=str(Q(receipt['baseline']['bound'])-Q(receipt['candidate']['bound']))
assert Q(receipt['candidate']['bound'])==Q(157739602520732550180509661243,39614081257132168796771975168)
assert Q(receipt['gain'])==Q(9,64)
assert Q(receipt['candidate']['bound'])<Q('3.9819073803')
receipt['seconds']=time.time()-start
receipt['status']='PASS'
(ROOT/'receipts'/'independent_bound.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','candidate','baseline','candidate_H72','gain','seconds']},indent=2))
