"""Generate finite scalar certificates. No output is accepted without both verifiers."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
H=96

def options(d,n,mode='higher'):
    k=d-1;M=2**k;t=F(d*M,n)
    if mode=='continuous':
        a=int(2*k*t)
        return [F(a,2*k)] if a>=2*k else []
    low=[F(1)]
    if mode=='second':
        a=int(2*k*t)
        return [x for x in low if x<=t]+([F(a,2*k)] if a>=3*k else [])
    low += [2-F(1,2**j) for j in range(1,k)]
    low=[x for x in low if x<=t]
    # Real degree-d Boolean Fourier granularity plus energy parity:
    # lambda in (2/M) Z. Enumerate each possible floor of 2k lambda.
    high=[]
    for h in range(4*k,int(2*k*t)+1):
        e=(h*M+4*k-1)//(4*k)
        x=F(2*e,M)
        if x<=t and int(2*k*x)==h:high.append(x)
    return low+high

def budget(d,c,x):return int(2*(d-1)*x)+x+(2**d-2*x)*c

def row(d,c,mode):
    def feasible(n):return any(n<=budget(d,c,x) for x in options(d,n,mode))
    lo=3*2**(d-1)-2;hi=d*2**(d-1)+1
    assert feasible(lo) and not feasible(hi)
    while hi-lo>1:
        m=(lo+hi)//2
        if feasible(m):lo=m
        else:hi=m
    return {'degree':d,'previous':str(c),'R':lo,'cap':str(F(lo,2**d)),
       'excluded':hi,'lambda_limit':str(F(d*2**(d-1),hi)),
       'case_count':len(options(d,hi,mode)),
       'cases':[{'lambda':str(x),'h':int(2*(d-1)*x),'ceiling':str(budget(d,c,x))}
                for x in sorted(options(d,hi,mode),key=lambda x:budget(d,c,x),reverse=True)[:1]],
       'relaxation_witness':next({'lambda':str(x),'h':int(2*(d-1)*x),'ceiling':str(budget(d,c,x))}
                              for x in options(d,lo,mode) if lo<=budget(d,c,x))}

allmodes={}
for mode in ['continuous','second','higher']:
    caps={1:F(1,2),2:F(1),3:F(5,4)};rows=[]
    for d in range(4,H+1):
        r=row(d,caps[d-1],mode);rows.append(r);caps[d]=F(r['cap'])
    allmodes[mode]={'caps':{str(d):str(x) for d,x in caps.items()},'rows':rows}
packet={'schema':'c44-ternary-control-v1','status':'candidate, unrefereed',
 'horizon':H,'proof':'PROOF.md','base_caps':{'1':'1/2','2':'1','3':'5/4'},
 'external_below_two':'Kasami-Tokura 1970: lambda<2 implies lambda=2-2^(-j), j>=0',
 'above_two':'all values on the exact energy grid; no uncorrected KTA exclusion',
 'modes':allmodes}
(P/'caps.json').write_text(json.dumps(packet,indent=2)+'\n')
spec={'schema':'c44-round6-v1','status':'candidate, unrefereed','horizon':H,
 'claim':'2.1974348818','baseline_claim':'3.1674542553','cap_source':'caps.json',
 'caps':allmodes['higher']['caps'],'external_R3':10}
spec['cap_sha256']=hashlib.sha256((P/'caps.json').read_bytes()).hexdigest()
(P/'candidate.json').write_text(json.dumps(spec,indent=2)+'\n')
print(json.dumps({mode:{'cap96':m['caps']['96'],'caps':{d:m['caps'][d] for d in map(str,range(4,13))}}
                 for mode,m in allmodes.items()},indent=2))
