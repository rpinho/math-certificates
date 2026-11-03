"""Second exact implementation: power moments, direct binomial duals, integer rows.
The standalone independent checker is verify_exact.py. No cross-imports.
"""
import hashlib,json,math,sys,time
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent

def verify(s,ablations=False):
    assert s['schema']=='c44-reed-muller-bound-v1' and s['horizon']==96
    inputs={}
    for key in ['cap','epi','spectral']:
        b=(R/s[key+'_source']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==s[key+'_sha256']
        inputs[key]=json.loads(b)
    assert s['epi_sha256']=='ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49'
    assert s['spectral_sha256']=='1020ed20d078ec1fece41c643007426bc452fc3aeafc81761901b32ded4495ed'
    assert s['external_R3']==10 and s['external_bs_theorem']=='3b(b-1)<=2(d^4-d^2)'
    cap_packet=inputs['cap'];assert cap_packet['schema']=='c44-reed-muller-caps-v1'
    caps={1:F(1,2),2:F(1),3:F(5,4)}
    assert [r['degree'] for r in cap_packet['certificates']]==list(range(4,13))
    for z in cap_packet['certificates']:
        d=z['degree'];M=2**(d-1)
        assert z['M']==M and z['controls']==2*d-2 and F(z['lower_cap'])==caps[d-1]
        a=(2*d*M)//3
        minimum=F(2*d-2,2**d)+F(1,2*M)+F(M-1,M)*caps[d-1]
        b=int(minimum*2**d)
        assert a==z['nonminimum_R'] and b==z['minimum_R']
        assert z['R']==max(a,b) and F(z['minimum_potential'])==minimum
        caps[d]=F(z['R'],2**d)
        assert F(z['cap'])==caps[d] and F(z['nonminimum_influence'])==F(3,2*M)
    assert {str(d):str(c) for d,c in caps.items()}==s['caps']
    H=96;unit=2**H
    B=[0]
    for d in range(1,H+1):
        b=math.isqrt(2*(d**4-d*d)//3)+1
        while 3*b*(b-1)>2*(d**4-d*d):b-=1
        assert 3*b*(b-1)<=2*(d**4-d*d)<3*b*(b+1)
        B.append(b)
    epi=inputs['epi'];assert sorted(map(int,epi['certificates']))==list(range(1,49))
    for ds,z in epi['certificates'].items():
        d=int(ds);x=z['nodes'];w=[F(a) for a in z['weights']]
        assert len(x)==d+1==len(w) and x==sorted(set(x)) and x[0]==1 and all(type(a)==int and a>0 for a in x)
        for j in range(1,d+1):assert sum(a*b**j for a,b in zip(w,x))==0
        assert w[0]>0 and w[0]+sum(a for a in w[1:] if a<0)>0
        B[d]=min(B[d],x[-1]-1)
    duals=[]
    for z in inputs['spectral']['certificates']:
        assert z['schema']=='c44-spectral-lattice-dual-v3'
        d,n=z['degree'],z['variables'];a={int(k):F(v) for k,v in z['alpha'].items()}
        t=[]
        for l in range(d+1):
            value=F(0)
            for x,c in a.items():
                K=sum((-1)**j*math.comb(x,j)*math.comb(n-x,l-j)
                      for j in range(max(0,l-(n-x)),min(x,l)+1))
                value+=c*F(K,math.comb(n,l))
            t.append(value)
        M=2**(d-1);up=F(M)
        for l,c in enumerate(t):
            v=c.numerator//(2*c.denominator)
            up+=F(math.comb(n,l),M)*max(c*v-v*v,c*(v+1)-(v+1)*(v+1))
        low=a.get(0,F(0))-a.get(1,F(0))-sum(abs(c) for x,c in a.items() if x>=2)
        assert low>up and z['block_bound']==n-1
        B[d]=min(B[d],n-1);duals.append((d,str(low-up)))
    assert len(duals)==37 and len({d for d,_ in duals})==37 and B[8]==33
    def rows(c):
        ceilings=[0]+[int(c.get(d,F(d,2))*unit) for d in range(1,H+1)]
        assert all(F(ceilings[d],unit)==c.get(d,F(d,2)) for d in range(1,H+1))
        charge=[0]+[d*2**(H-d) for d in range(1,H+1)]
        prev=[0]*(H+1)
        for b in range(1,max(B)+1):
            out=[0]*(H+1);best=0
            for d in range(1,H+1):
                best=max(best,prev[d])
                out[d]=prev[d] if b>B[d] else min(ceilings[d],charge[d]+best)
            prev=out
        assert max(prev)==prev[-1]
        return prev
    new=rows(caps)
    oldcaps={3:F(5,4),4:F(25,16),5:F(71,32),6:F(45,16),7:F(447,128)}
    old=rows(oldcaps)
    tail=F(H**3+6*H**2+18*H+26,unit)
    bound=F(new[-1],unit)+tail
    assert bound<F(s['claim'])==F('3.1674542553')
    assert F(old[-1],unit)+tail==F(157739602520732550180509661243,39614081257132168796771975168)
    assert F(old[-1]-new[-1],unit)==F(417,512)
    out={'status':'PASS','horizon':H,'finite':str(F(new[-1],unit)),'tail':str(tail),
       'bound':str(bound),'gain':str(F(old[-1]-new[-1],unit)),'B':B,
       'finite_degrees':{str(d):str(F(new[d],unit)) for d in range(1,H+1)},'dual_gaps':duals}
    if ablations:
        tests={}
        for d in range(4,13):
            alone=oldcaps|{d:caps[d]}
            leave=caps.copy();leave[d]=oldcaps.get(d,F(d,2))
            tests[str(d)]={'alone_gain':str(F(old[-1]-rows(alone)[-1],unit)),
                           'loss_if_reverted':str(F(rows(leave)[-1]-new[-1],unit))}
        tests['caps4to6_gain']=str(F(old[-1]-rows(oldcaps|{d:caps[d] for d in range(4,7)})[-1],unit))
        tests['caps7and8_gain']=str(F(old[-1]-rows(oldcaps|{d:caps[d] for d in [7,8]})[-1],unit))
        out['ablations']=tests
    return out

if __name__=='__main__':
    s=json.loads((R/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json')).read_text())
    result=verify(s,'--ablations' in sys.argv)
    (R/'verification_rows.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','bound','gain']},indent=2))
