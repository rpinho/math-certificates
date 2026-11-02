"""Standalone exact verifier, written separately from candidate generation.
Imports neither search/candidate code nor another verifier. Standard library.
Checks integer contradictions, raw duals, Lagrange identities, rational columns.
Universal mathematical lemmas and explicit external premises are in PROOF.md.
"""
import hashlib,json,math,sys,time
from fractions import Fraction as Q
from pathlib import Path
R=Path(__file__).resolve().parent
EPISHA='ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49'
SPSHA='1020ed20d078ec1fece41c643007426bc452fc3aeafc81761901b32ded4495ed'

def verify(spec,H=72):
    assert spec['schema']=='c44-reed-muller-bound-v1'
    assert spec['external_R3']==10 and spec['external_bs_theorem']=='3b(b-1)<=2(d^4-d^2)'
    assert spec['horizon']==96 and H in (72,96)
    blobs={}
    for key in ('cap','epi','spectral'):
        raw=(R/spec[key+'_source']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==spec[key+'_sha256']
        blobs[key]=json.loads(raw)
    assert spec['epi_sha256']==EPISHA and spec['spectral_sha256']==SPSHA
    cap=blobs['cap']
    assert cap['schema']=='c44-reed-muller-caps-v1' and cap['proof']=='PROOF.md'
    assert cap['external_weight_equivalence']=='CHS2020 Corollary 2.2'
    assert cap['external_structure']=='Valyuzhenich2023 Theorem 2(2)'
    assert cap['external_gap']=='binary RM(k,n) second weight >= 3*2^(n-k-1)'
    assert cap['base_caps']=={'1':'1/2','2':'1','3':'5/4'}
    assert [r['degree'] for r in cap['certificates']]==list(range(4,13))
    established={1:Q(1,2),2:Q(1),3:Q(5,4)}; contradictions=[]
    for r in cap['certificates']:
        d=r['degree'];m=1<<(d-1); n=r['R'];first=n+1
        assert type(n)==int and n>=3*m-2 and r['M']==m
        assert r['controls']==2*(d-1)
        assert Q(r['lower_cap'])==established[d-1]
        assert Q(r['nonminimum_influence'])==Q(3,2*m)
        # Prove impossibility at first excluded count, without trusting the floor.
        assert first*3>d*2*m
        minimum_n=2*d-1+(2*m-2)*established[d-1]
        assert first>minimum_n
        assert Q(r['minimum_potential'])*2**d==minimum_n
        assert r['nonminimum_R']*3<=d*2*m<(r['nonminimum_R']+1)*3
        assert r['minimum_R']<=minimum_n<r['minimum_R']+1
        assert n==max(r['nonminimum_R'],r['minimum_R'])
        established[d]=Q(n,2**d)
        assert established[d]==Q(r['cap'])
        contradictions.append({'d':d,'first_excluded':first,
          'nonminimum_excess':str(Q(3*first,2*m)-d),
          'minimum_excess':str(Q(first,2**d)-Q(r['minimum_potential']))})
    assert spec['caps']=={str(d):str(v) for d,v in established.items()}
    B=[0]
    for d in range(1,H+1):
        lo,hi=0,d*d+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if 3*mid*(mid-1)<=2*(d**4-d*d):lo=mid
            else:hi=mid
        assert 3*lo*(lo-1)<=2*(d**4-d*d)<3*lo*(lo+1)
        B.append(lo)
    epi=blobs['epi']
    assert sorted(map(int,epi['certificates']))==list(range(1,49))
    for ds,z in epi['certificates'].items():
        d=int(ds); x=z['nodes']; w=list(map(Q,z['weights']))
        assert len(x)==d+1 and x==sorted(set(x)) and len(w)==len(x)
        assert x[0]==1 and all(type(a)==int and a>=1 for a in x)
        # Common Lagrange residues certify all d positive-degree moments vanish.
        residues=[w[i]*x[i]*math.prod(x[i]-x[j] for j in range(len(x)) if j!=i) for i in range(len(x))]
        assert residues[0]!=0 and all(t==residues[0] for t in residues)
        assert w[0]>0 and w[0]+sum(t for t in w[1:] if t<0)>0
        B[d]=min(B[d],x[-1]-1)
    sp=blobs['spectral'];assert sp['schema']=='c44-spectral-bounds-v1'
    seen=set();dual_checks=[]
    for c in sp['certificates']:
        assert c['schema']=='c44-spectral-lattice-dual-v3'
        d,n=c['degree'],c['variables'];assert type(d)==type(n)==int and 1<=d<=48 and n>=d and d not in seen
        seen.add(d);a={int(k):Q(v) for k,v in c['alpha'].items()}
        assert len(a)==len(c['alpha']) and all(0<=k<=n for k in a)
        levels=[Q(0)]*(d+1)
        for x,t in a.items():
            kvals=[1,n-2*x]
            for j in range(1,d):
                v=(n-2*x)*kvals[-1]-(n-j+1)*kvals[-2]
                assert v%(j+1)==0;kvals.append(v//(j+1))
            for j in range(d+1):levels[j]+=t*Q(kvals[j],math.comb(n,j))
        lower=a.get(0,Q(0))-a.get(1,Q(0))-sum(abs(v) for k,v in a.items() if k>=2)
        penalty=Q(0);m=2**(d-1)
        for j,t in enumerate(levels):
            z=t//2
            h=max(t*z-z*z,t*(z+1)-(z+1)**2)
            assert h>=0
            penalty+=Q(math.comb(n,j),m)*h
        gap=lower-m-penalty
        assert gap>0 and c['block_bound']==n-1
        B[d]=min(B[d],n-1)
        dual_checks.append({'d':d,'B':n-1,'strict_gap':str(gap)})
    assert len(seen)==37 and B[8]==33
    def columns(caps):
        env=[Q(0)]*(max(B)+1);out=[]
        for d in range(1,H+1):
            col=[Q(0)];limit=caps.get(d,Q(d,2))
            for b in range(1,B[d]+1):
                col.append(min(limit,Q(d,2**d)+max(env[b-1],col[-1])))
            for b in range(len(env)):env[b]=max(env[b],col[min(b,B[d])])
            out.append(col[-1])
        assert max(out)==out[-1]==env[-1]
        return out
    new=columns(established)
    old_caps={3:Q(5,4),4:Q(25,16),5:Q(71,32),6:Q(45,16),7:Q(447,128)}
    old=columns(old_caps)
    # sum_{d>H} d^3/2^d, proved explicitly in PROOF.md.
    tail=Q(H**3+6*H**2+18*H+26,2**H)
    bound=new[-1]+tail
    assert Q(spec['claim'])==Q('3.1674542553') and bound<Q(spec['claim'])
    assert old[-1]-new[-1]==Q(417,512)>Q(1,10000)
    if H==96:assert old[-1]+tail==Q(157739602520732550180509661243,39614081257132168796771975168)
    return {'status':'PASS','horizon':H,'cap_checks':contradictions,'duals':dual_checks,
       'B':B,'finite':str(new[-1]),'tail':str(tail),'bound':str(bound),
       'baseline':str(old[-1]+tail),'gain':str(old[-1]-new[-1]),
       'finite_degrees':list(map(str,new))}

if __name__=='__main__':
    spec=json.loads((R/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json')).read_text())
    H=int(sys.argv[2]) if len(sys.argv)>2 else 72
    result=verify(spec,H)
    (R/f'verification_independent_H{H}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','horizon','bound','baseline','gain')},indent=2))
