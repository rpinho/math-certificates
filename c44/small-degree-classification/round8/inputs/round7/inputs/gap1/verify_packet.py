"""Independent exact packet verifier. Imports no generator, search, or other verifier.

The direct C++ checker verifies the entire published catalogue by character sums.
This program checks affine kernels, covariance identities, finite equality budgets,
the polynomial witness, raw inherited duals, and independent rational columns.
The universal proof and external completeness assumptions remain in PROOF.md.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,itertools,json,math,subprocess,sys
R=Path(__file__).resolve().parent
def rank(a):
    a=[list(map(F,r)) for r in a];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[t/v for t in a[i]]
        for k in range(len(a)):
            if k!=i:
                v=a[k][j];a[k]=[u-v*w for u,w in zip(a[k],a[i])]
        i+=1
    return i
def covariance(a):
    n=len(a);k=len(a[0])
    return [[sum(F(row[i])*row[j] for row in a)/n for j in range(k)] for i in range(k)]
def verify_structure(c):
    # Independently enumerate all partitions of derivative degree three.
    types=[]
    for fixed in range(4):
        for b2 in range(4):
            for b3 in range(2):
                for b4 in range(2):
                    if fixed+b2+2*b3+3*b4==3:
                        types.append((fixed,tuple([2]*b2+[3]*b3+[4]*b4)))
    assert sorted(types)==sorted((t['fixed'],tuple(t['blocks'])) for t in c['types'])
    assert len(types)==7
    for fixed,blocks in types:
        h=fixed+sum(blocks);values=[]
        for x in itertools.product((-1,1),repeat=h):
            value=int(all(t==1 for t in x[:fixed]));offset=fixed
            for m in blocks:
                z=x[offset:offset+m];offset+=m
                value*=int(len(set(z))==1)*(z[0] if m%2==0 else 1)
            values.append(value)
        assert F(sum(t!=0 for t in values),len(values))==F(1,8)
        masks=[]
        for s in range(2**h):
            # product((-1,1)) indexing reverses signs relative to binary; support degrees are invariant.
            coefficient=sum(value*(-1 if (s&x).bit_count()%2 else 1) for x,value in enumerate(values))
            if coefficient:masks.append(s)
        assert max(s.bit_count() for s in masks)==3
        used=0
        for s in masks:used|=s
        assert used==(1<<h)-1 and h<=6
    records=[]
    for name,h in [('point_pair_pair',5),('pair_triple',5),('three_pairs',6)]:
        features=[];active=[];selected=[]
        for x in itertools.product((-1,1),repeat=h):
            if name=='point_pair_pair':
                u,s,t,v,w=x
                a=[F(1-u,2),F(s-t,2),F(v-w,2)]
                on=u==1 and s==t and v==w
                choose=u==-1 and s==-t and v==-w
            elif name=='pair_triple':
                s,t,u,v,w=x
                a=[F(s-t,2),F(u-w),F(v-w)]
                on=s==t and u==v==w
                choose=s==-t and not(u==v==w)
            else:
                s,t,u,v,w,z=x
                a=[F(s-t,2),F(u-v,2),F(w-z,2)]
                on=s==t and u==v and w==z
                choose=s==-t and u==-v and w==-z
            features.append(a)
            if on:active.append([1,*x]);assert all(v==0 for v in a)
            if choose:selected.append(a)
        # These independent affine forms span every affine function vanishing on active rows.
        assert rank(features)==3==h+1-rank(active)
        assert F(len(active),2**h)==F(1,8)
        C=covariance(features);S=covariance(selected)
        factor=F(3,4) if name=='pair_triple' else F(1,2)
        residual=[[factor*S[i][j]-C[i][j] for j in range(3)] for i in range(3)]
        assert all(residual[i][j]==(F(1,4) if name=='pair_triple' and i==j==0 else 0)
                   for i in range(3) for j in range(3))
        assert F(c['top_energy_caps'][name])==factor
        budget=F(h,16)+F(15,16)+factor/4
        assert budget==(F(22,16) if name=='point_pair_pair' else F(23,16))
        records.append({'type':name,'active':len(active),'kernel_dimension':3,
                        'energy_cap':str(factor),'count_budget':str(budget*16)})
    # Smaller supports, triple odd-sign obstruction, and exceptional equality cases.
    assert (F(4,16)+F(1,16)+F(7,8)*F(5,4))*16==F(45,2)<23
    assert all(a+b+d!=0 for a,b,d in itertools.product((-1,1),repeat=3))
    cases=[x for x in itertools.product((F(0),F(1,2),F(1)),repeat=3) if sum(x)==1]
    assert len(cases)==6 and all(sorted(x) in [[F(0),F(0),F(1)],[F(0),F(1,2),F(1,2)]] for x in cases)
    assert 2+2*c['external_R3']==22
    assert 2*9>23-6-1
    assert (F(1,4)+F(1,4)+F(1,8))/8==F(5,64)>F(1,16)
    # Walsh expansion of all eight full-mismatch norms determines cross inner products.
    signrows=list(itertools.product((-1,1),repeat=3))
    gramfeatures=[[1,s[0]*s[1],s[0]*s[2],s[1]*s[2]] for s in signrows]
    assert rank(gramfeatures)==4
    return records
def verify_witness(path):
    w=json.loads(path.read_text());assert w['schema']=='sign-fourier-integer-v1'
    assert w['variables']==22 and w['degree']==4 and w['denominator']==8
    p=dict(w['terms']);assert len(p)==len(w['terms'])==64
    union=0;conv={}
    for s,v in p.items():
        assert type(s)==type(v)==int and s>0 and abs(v)==1 and s.bit_count()==4
        union|=s
        for t,u in p.items():conv[s^t]=conv.get(s^t,0)+v*u
    assert union==(1<<22)-1
    assert {s:v for s,v in conv.items() if v}=={0:64}
    return {'variables':22,'degree':4,'Boolean_convolution':'PASS'}
def block_bounds(H):
    bs=[0]
    for d in range(1,H+1):
        b=math.isqrt(2*(d**4-d*d)//3)+1
        while 3*b*(b-1)>2*(d**4-d*d):b-=1
        assert 3*b*(b-1)<=2*(d**4-d*d)<3*b*(b+1)
        bs.append(b)
    epi=json.loads((R/'baseline/c44r5/epi_certificate.json').read_text())
    assert set(map(int,epi['certificates']))==set(range(1,49))
    for sd,z in epi['certificates'].items():
        d=int(sd);x=z['nodes'];w=list(map(F,z['weights']))
        assert x==sorted(set(x)) and x[0]==1 and len(x)==len(w)==d+1
        residues=[w[i]*x[i]*math.prod(x[i]-x[j] for j in range(d+1) if i!=j) for i in range(d+1)]
        assert residues[0]!=0 and len(set(residues))==1
        assert w[0]>0 and w[0]+sum(v for v in w[1:] if v<0)>0
        bs[d]=min(bs[d],x[-1]-1)
    sp=json.loads((R/'baseline/c44r5/spectral_certificate_round3.json').read_text())
    seen=set()
    for z in sp['certificates']:
        d,n=z['degree'],z['variables'];assert d not in seen;seen.add(d)
        a={int(k):F(v) for k,v in z['alpha'].items()};t=[F(0)]*(d+1)
        for x,v in a.items():
            K=[1,n-2*x]
            for j in range(1,d):
                m=(n-2*x)*K[-1]-(n-j+1)*K[-2];assert m%(j+1)==0;K.append(m//(j+1))
            for j in range(d+1):t[j]+=v*F(K[j],math.comb(n,j))
        M=2**(d-1)
        upper=F(M)
        for j,v in enumerate(t):
            k=v//2;upper+=F(math.comb(n,j),M)*max(v*k-k*k,v*(k+1)-(k+1)**2)
        lower=a.get(0,F(0))-a.get(1,F(0))-sum(abs(v) for x,v in a.items() if x>=2)
        assert lower>upper and z['block_bound']==n-1
        bs[d]=min(bs[d],n-1)
    assert len(seen)==37 and bs[8]==33
    return bs
def columns(caps,B,H):
    envelope=[F(0)]*(max(B)+1);values=[]
    for d in range(1,H+1):
        col=[F(0)];cost=F(d,2**d)
        for b in range(1,B[d]+1):col.append(min(caps.get(d,F(d,2)),cost+max(envelope[b-1],col[-1])))
        for b in range(len(envelope)):envelope[b]=max(envelope[b],col[min(b,B[d])])
        values.append(col[-1])
    tail=F(H**3+6*H**2+18*H+26,2**H)
    return max(values)+tail,values
def verify_caps(c):
    assert c['schema']=='quartic-envelope-cap-v1'
    assert c['quartic_R']==22 and c['external_R3']==10 and c['catalogue_classes']==761
    assert c['envelope']=='D<=1+E3/4'
    assert c['equality_signatures']==[[0,1,4,2],['1/2','9/8',9,3],[1,'5/4',10,3]]
    caps={1:F(1,2),2:F(1),3:F(5,4),4:F(11,8)}
    for d in range(5,13):
        minimum=2*d-1+(2**d-2)*caps[d-1];nonminimum=F(d*2**d,3)
        n=max(minimum.numerator//minimum.denominator,nonminimum.numerator//nonminimum.denominator)
        caps[d]=F(n,2**d)
        assert n+1>minimum and n+1>nonminimum
    assert c['caps']=={str(d):str(v) for d,v in caps.items()}
    assert [r['R'] for r in c['rows']]==[int(caps[d]*2**d) for d in range(4,13)]
    return caps
def main(H=96):
    s=json.loads((R/'candidate.json').read_text());assert s['schema']=='quartic22-bound-v1'
    assert H in (72,96)
    for name,sha in s['sources'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha
    c=json.loads((R/'certificate.json').read_text());assert c['quartic_R']==22 and c['external_R3']==10
    assert c['catalogue_classes']==761
    assert c['catalogue_sha256']=='d0ca4026c3bfa61f7c40945e4627feecd9264d7854114806c533d64e06836ba0'
    assert hashlib.sha256((R/c['catalogue_source']).read_bytes()).hexdigest()==c['catalogue_sha256']
    child=subprocess.Popen([str(R/'verify_catalogue'),str(R/c['catalogue_source'])],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    stdout,stderr=child.communicate()
    assert child.returncode==0,stderr
    catalogue=json.loads(stdout);assert catalogue['status']=='PASS'
    catalogue['verifier_pid']=child.pid
    structure=verify_structure(c);witness=verify_witness(R/c['witness_source'])
    caps=verify_caps(c)
    assert c['caps']==s['caps']
    B=block_bounds(H)
    assert B==s['B'][:H+1]
    value,values=columns(caps,B,H)
    old=caps.copy();old[4]=F(3,2);old[5]=F(27,16)
    baseline,_=columns(old,B,H)
    assert value<F(s['claim'])==F('3.1498761303')
    assert baseline-value==F(9,512)
    if H==96:
        assert value==F(s['bound']) and baseline==F(s['baseline'])
        assert values==[F(s['finite_degrees'][str(d)]) for d in range(1,H+1)]
    assert F(c['lower_recursion']['limit'])==F(22+2,2**4)==F(3,2)
    result={'status':'PASS','horizon':H,'R4':22,'R5_upper':53,'C44_upper':str(value),
            'gain_over_c44r5':str(baseline-value),'catalogue':catalogue,
            'control_checks':structure,'witness':witness}
    (R/f'verification_packet_H{H}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','horizon','R4','R5_upper','C44_upper','gain_over_c44r5']},indent=2))
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 96)
