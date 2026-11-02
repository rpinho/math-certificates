"""Independent exact checker A: collapsed envelopes and integer recurrence rows.
No imports from generation, search, inherited verifier, or checker B.
Universal lemmas and external premises are in PROOF.md.
"""
import json,hashlib,math
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent

def floorq(x):return x.numerator//x.denominator

def verify(spec):
    assert spec['schema']=='c44-round6-v1' and spec['status']=='candidate, unrefereed'
    assert spec['horizon']==96 and spec['external_R3']==10
    raw=(P/spec['cap_source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==spec['cap_sha256']
    data=json.loads(raw)
    assert data['schema']=='c44-ternary-control-v1' and data['horizon']==96
    assert data['base_caps']=={'1':'1/2','2':'1','3':'5/4'}
    assert data['external_below_two']=='Kasami-Tokura 1970: lambda<2 implies lambda=2-2^(-j), j>=0'
    assert data['above_two']=='all values on the exact energy grid; no uncorrected KTA exclusion'
    results={}
    for mode in ('continuous','second','higher'):
        caps={1:Q(1,2),2:Q(1),3:Q(5,4)}
        assert [r['degree'] for r in data['modes'][mode]['rows']]==list(range(4,97))
        checks=[]
        for r in data['modes'][mode]['rows']:
            d=r['degree'];k=d-1;m=1<<k;c=caps[d-1];n=r['R']+1
            assert type(r['R'])==int and r['excluded']==n and r['R']>=3*m-2
            assert Q(r['previous'])==c and Q(1,2)<=c<=Q(k,2)
            t=Q(d*m,n)
            assert Q(r['lambda_limit'])==t
            # Optimize each floor cell correctly: the objective decreases
            # inside a cell, and its cell maxima increase in cell index.
            slope=2*c-1
            assert 0<=slope<=k-1
            choices=[]
            if mode=='continuous':
                h=floorq(2*k*t)
                if h>=2*k:choices.append(Q(h,2*k))
            elif mode=='second':
                if t>=1:choices.append(Q(1))
                h=floorq(2*k*t)
                if h>=3*k:choices.append(Q(h,2*k))
            else:
                choices=[2-Q(1,1<<j) for j in range(k) if 2-Q(1,1<<j)<=t]
                # The last energy-grid point below t identifies the rightmost
                # occupied cell. Its leftmost grid point maximizes that cell.
                e=floorq(t*m/2)
                if e>=m:
                    h=(4*k*e)//m
                    first=(h*m+4*k-1)//(4*k)
                    x=Q(2*first,m)
                    assert first<=e and floorq(2*k*x)==h
                    assert 1-slope*(Q(1,2*k)+Q(2,m))>0
                    choices.append(x)
            vals=[Q(2*m)*c+floorq(2*k*x)-slope*x for x in choices]
            maximum=max(vals,default=Q(-1))
            assert n>maximum
            # Check an explicit feasible scalar point at R. It need not be
            # realizable by a Boolean function: it proves this relaxation ends.
            w=r['relaxation_witness'];x=Q(w['lambda']);h=w['h']
            assert x>=1 and (n-1)*x<=d*m and h==floorq(2*k*x)
            if mode=='second':assert x==1 or x>=Q(3,2)
            if mode=='higher':
                assert (x*m/2).denominator==1
                if x<2:assert x in [2-Q(1,1<<j) for j in range(k)]
            value=Q(2*m)*c+h-slope*x
            assert value==Q(w['ceiling']) and value>=n-1
            caps[d]=Q(n-1,2*m)
            assert caps[d]==Q(r['cap']) and caps[d]>=c
            # Tail increment also applies to the feasible scalar witness.
            assert caps[d]-c<=Q(d*(d-1),1<<d)
            checks.append({'d':d,'first_excluded':n,'strict_gap':str(n-maximum)})
        assert data['modes'][mode]['caps']=={str(d):str(x) for d,x in caps.items()}
        tail=Q(96**2+3*96+4,1<<96)
        results[mode]={'cap96':str(caps[96]),'tail':str(tail),'bound':str(caps[96]+tail),
                      'checks':checks}
    assert spec['caps']==data['modes']['higher']['caps']
    upper=Q(results['higher']['bound'])
    assert upper<Q(spec['claim']) and Q(spec['baseline_claim'])-upper>Q(1,1000)
    # Re-evaluate the block recurrence with only elementary B_d<=d^2 as
    # a diagnostic. The accepted global proof uses the elementary cap tail.
    H=96;unit=1<<H;B=[0]+[d*d for d in range(1,H+1)]
    cap=[0]+[int(Q(spec['caps'][str(d)])*unit) for d in range(1,H+1)]
    charge=[0]+[d*(1<<(H-d)) for d in range(1,H+1)]
    prev=[0]*(H+1)
    for b in range(1,max(B)+1):
        out=[0]*(H+1);best=0
        for d in range(1,H+1):
            best=max(best,prev[d])
            out[d]=prev[d] if b>B[d] else min(cap[d],charge[d]+best)
        prev=out
    assert prev==cap
    return {'status':'PASS','implementation':'A','results':results,
            'bound':str(upper),'finite_columns':[str(Q(x,unit)) for x in prev[1:]],
            'gain_over_round5':str(Q(125475790246857326765951236155,39614081257132168796771975168)-upper)}

if __name__=='__main__':
    import sys
    s=json.loads((P/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json')).read_text())
    z=verify(s)
    (P/'verification_a.json').write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps({k:z[k] for k in ('status','bound','gain_over_round5')},indent=2))
