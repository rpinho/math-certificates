"""Independent checker B: exhaustive floor-cell inequalities and rational columns.
Written separately. Imports no search code and no other verifier.
"""
from pathlib import Path
from fractions import Fraction
import json,hashlib,math,sys
P=Path(__file__).resolve().parent
Q=Fraction

def check(path):
    spec=json.loads(path.read_text())
    assert spec['schema']=='c44-round6-v1' and spec['horizon']==96 and spec['external_R3']==10
    assert spec['status']=='candidate, unrefereed'
    blob=(P/spec['cap_source']).read_bytes()
    assert hashlib.sha256(blob).hexdigest()==spec['cap_sha256']
    packet=json.loads(blob)
    assert packet['schema']=='c44-ternary-control-v1' and packet['horizon']==96
    assert packet['base_caps']=={'1':'1/2','2':'1','3':'5/4'}
    assert packet['external_below_two']=='Kasami-Tokura 1970: lambda<2 implies lambda=2-2^(-j), j>=0'
    assert packet['above_two']=='all values on the exact energy grid; no uncorrected KTA exclusion'
    answer={}
    for name in ['higher','second','continuous']:
        caps={1:Q(1,2),2:Q(1),3:Q(5,4)};records=packet['modes'][name]['rows']
        assert len(records)==93
        for degree,record in zip(range(4,97),records):
            k=degree-1;den=2**k;previous=caps[k];ceiling=record['R'];n=ceiling+1
            assert record['degree']==degree and record['excluded']==n
            assert type(ceiling)==int and ceiling>=3*den-2
            assert Q(record['previous'])==previous
            assert Q(1,2)<=previous<=Q(k,2)
            ratio=Q(degree*den,n)
            assert Q(record['lambda_limit'])==ratio
            allowed=[]
            if name=='continuous':
                # Enumerate every cell, not just the final maximizing cell.
                for h in range(2*k,int(2*k*ratio)+1):allowed.append(Q(h,2*k))
            elif name=='second':
                if ratio>=1:allowed.append(Q(1))
                for h in range(3*k,int(2*k*ratio)+1):allowed.append(Q(h,2*k))
            else:
                for j in range(k):
                    value=Q(2*2**j-1,2**j)
                    if value<=ratio:allowed.append(value)
                # lambda=2z/den. For each h, choose the smallest allowed
                # z satisfying h<=2k lambda. It gives the largest budget
                # throughout that cell because previous>=1/2.
                for h in range(4*k,int(2*k*ratio)+1):
                    z=-((-h*den)//(4*k))
                    value=Q(2*z,den)
                    if 2*k*value<h+1 and value<=ratio:allowed.append(value)
            if name=='higher':assert record['case_count']==len(allowed)
            budgets=[Q(2*den)*previous+int(2*k*x)+(1-2*previous)*x for x in allowed]
            assert all(v<n for v in budgets)
            w=record['relaxation_witness'];x=Q(w['lambda'])
            assert x>=1 and x*ceiling<=degree*den and w['h']==int(2*k*x)
            if name=='second':assert x==1 or x>=Q(3,2)
            if name=='higher':
                assert (x*den).denominator==1 and int(x*den)%2==0
                if x<2:assert any(x==Q(2*2**j-1,2**j) for j in range(k))
            potential=Q(2*den)*previous+w['h']+(1-2*previous)*x
            assert potential>=ceiling and potential==Q(w['ceiling'])
            caps[degree]=Q(ceiling,2*den)
            assert caps[degree]==Q(record['cap']) and caps[degree]>=previous
            assert caps[degree]-previous<=Q(degree*(degree-1),2**degree)
            # Frozen explanatory cases must be genuine inequalities.
            for case in record['cases']:
                y=Q(case['lambda']);assert 1<=y<=ratio
                assert case['h']==int(2*k*y)
                assert Q(case['ceiling'])==Q(2*den)*previous+case['h']+(1-2*previous)*y<n
        assert packet['modes'][name]['caps']=={str(i):str(v) for i,v in caps.items()}
        # Independently sum the tail by multiplying geometric series:
        # sum d(d-1)2^-d after H = (H(H-1)+4H+4)2^-H.
        H=96;tail=Q(H*(H-1)+4*H+4,2**H)
        answer[name]={'finite':str(caps[H]),'tail':str(tail),'bound':str(caps[H]+tail)}
    assert spec['caps']==packet['modes']['higher']['caps']
    upper=Q(answer['higher']['bound'])
    assert upper<Q(spec['claim']) and Q(spec['baseline_claim'])-upper>Q(1,1000)
    # Independently verify inherited block inputs before using them diagnostically.
    epi_raw=(P/'baseline/epi_certificate.json').read_bytes()
    sp_raw=(P/'baseline/spectral_certificate_round3.json').read_bytes()
    assert hashlib.sha256(epi_raw).hexdigest()=='ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49'
    assert hashlib.sha256(sp_raw).hexdigest()=='1020ed20d078ec1fece41c643007426bc452fc3aeafc81761901b32ded4495ed'
    B=[0]
    for d in range(1,97):
        a,b=0,d*d+1
        while b-a>1:
            mid=(a+b)//2
            if 3*mid*(mid-1)<=2*(d**4-d*d):a=mid
            else:b=mid
        B.append(a)
    for ds,certificate in json.loads(epi_raw)['certificates'].items():
        d=int(ds);nodes=certificate['nodes'];weights=list(map(Q,certificate['weights']))
        assert len(nodes)==len(weights)==d+1 and nodes[0]==1 and nodes==sorted(set(nodes))
        assert all(type(x)==int and x>0 for x in nodes)
        constant=weights[0]*nodes[0]*math.prod(nodes[0]-x for x in nodes[1:])
        assert constant!=0
        for i in range(len(nodes)):
            assert weights[i]*nodes[i]*math.prod(nodes[i]-nodes[j] for j in range(len(nodes)) if i!=j)==constant
        assert weights[0]>0 and weights[0]+sum(w for w in weights[1:] if w<0)>0
        B[d]=min(B[d],nodes[-1]-1)
    duals=json.loads(sp_raw)['certificates'];assert len(duals)==37
    for z in duals:
        d,n=z['degree'],z['variables'];m=2**(d-1);a={int(i):Q(v) for i,v in z['alpha'].items()}
        level=[Q(0)]*(d+1)
        for x,coefficient in a.items():
            ks=[1,n-2*x]
            for j in range(1,d):
                num=(n-2*x)*ks[j]-(n-j+1)*ks[j-1]
                assert num%(j+1)==0;ks.append(num//(j+1))
            for j in range(d+1):level[j]+=coefficient*Q(ks[j],math.comb(n,j))
        left=a.get(0,0)-a.get(1,0)-sum(abs(v) for x,v in a.items() if x>=2)
        right=Q(m)
        for j,t in enumerate(level):
            lower=t//2
            right+=Q(math.comb(n,j),m)*max(t*lower-lower**2,t*(lower+1)-(lower+1)**2)
        assert left>right and z['block_bound']==n-1
        B[d]=min(B[d],n-1)
    assert B[8]==33
    caps={int(d):Q(v) for d,v in spec['caps'].items()}
    envelope=[Q(0)]*(max(B)+1);end=[];saturation=[]
    for d in range(1,97):
        column=[Q(0)]
        for b in range(1,B[d]+1):
            column.append(min(caps[d],Q(d,2**d)+max(envelope[b-1],column[-1])))
        assert column[-1]==caps[d]
        saturation.append(next(b for b,v in enumerate(column) if v==caps[d]))
        for b in range(len(envelope)):envelope[b]=max(envelope[b],column[min(b,B[d])])
        end.append(column[-1])
    return {'status':'PASS','implementation':'B','bound':str(upper),'modes':answer,
       'B':B,'saturation':saturation,'finite_columns':list(map(str,end)),
       'gain_over_round5':str(Q(125475790246857326765951236155,39614081257132168796771975168)-upper)}

if __name__=='__main__':
    result=check(P/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json'))
    (P/'verification_b.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','bound','gain_over_round5')},indent=2))
