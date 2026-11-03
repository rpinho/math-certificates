"""Exact packet verifier A: rational exclusions and canonical case coverage.
No generator, search or verifier-B imports. Native verify_third_a.cpp
performs the separately replayed finite minimum-partial exclusions.
"""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
import hashlib, json, pathlib, sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
C=R/'certificates'
T=json.loads((C/'third_weight.json').read_text())
assert T['schema']=='c44-third-weight-v2' and T['status']=='candidate, unrefereed'
assert (T['degree'],T['normalized_weight'],T['denominator'],T['numerator_norm'])==(5,'7/4',32,56)
assert (T['minimum_partial_energy'],T['next_partial_energy'],T['conclusion'])==(16,24,'controls <= 13')
assert T['template_counts']=={'13':359502,'15':1479478,'16':2757118,'17':4910178,'14':752752}
expected=[]
for n in (17,16,15,14):
    g=3*n-35;ci=0
    for a in combinations_with_replacement(range(3),4):
        b=g-1-sum(a)
        if not 0<=b<=n-9:continue
        good=[0]+[2*j+1+t for j,c in enumerate(a) for t in range(c)]+list(range(9,9+b))
        expected.append(dict(n=n,kind='hom',case_index=ci,pair_counts=list(a),outside=b,
                             goodbits=sum(1<<j for j in good),blocks=[6,24,96,384],nonhomogeneous_only=False))
        ci+=1
    assert ci=={17:2,16:6,15:11,14:12}[n]
h14_hom=[c for c in expected if c['n']==14]
expected=[c for c in expected if c['n']!=14]
ci=0
for tp in product(range(5),range(5),range(3),range(2),range(2)):
    if tp[0]+tp[1]+2*tp[2]+3*tp[3]+4*tp[4]!=4 or tp[1]==4:continue
    blocks=[];positions=[];at=1
    for size,count in enumerate(tp,1):
        if count:positions.append(at)
        for _ in range(count):blocks.append(((1<<size)-1)<<at);at+=size
    positions.append(at)
    for bad in positions:
        expected.append(dict(n=15,kind='nonhom',case_index=ci,type=list(tp),bad=bad,
                             goodbits=((1<<15)-1)^(1<<bad),blocks=blocks,nonhomogeneous_only=True))
        ci+=1
assert ci==31
expected.extend(h14_hom)
ci=0
for tp in product(range(5),range(5),range(3),range(2),range(2)):
    if tp[0]+tp[1]+2*tp[2]+3*tp[3]+4*tp[4]!=4 or tp[1]==4:continue
    blocks=[];at=1
    for size,count in enumerate(tp,1):
        for _ in range(count):blocks.append(((1<<size)-1)<<at);at+=size
    allocations=[list(combinations_with_replacement(range(size+1),count)) for size,count in enumerate(tp,1)]
    for assigned in product(*allocations):
        outside=9-sum(map(sum,assigned))
        if not 0<=outside<=14-at:continue
        bits=1;position=1
        for size,group in enumerate(assigned,1):
            for amount in group:
                bits|=((1<<amount)-1)<<position;position+=size
        for offset in range(outside):bits|=1<<(at+offset)
        expected.append(dict(n=14,kind='nonhom',case_index=ci,goodbits=bits,blocks=blocks,
                             nonhomogeneous_only=True,type=list(tp),block_good_counts=list(map(list,assigned)),outside=outside))
        ci+=1
assert ci==127 and len(T['cases'])==len(expected)==189
for submitted,wanted in zip(T['cases'],expected):
    label=f"n{wanted['n']}_{wanted['kind']}_{wanted['case_index']}"
    wanted.update(file=label+'.txt',unresolved=0)
    assert submitted==wanted
    tokens=[wanted['n'],56,wanted['goodbits'],int(wanted['nonhomogeneous_only']),len(wanted['blocks']),*wanted['blocks']]
    assert (C/'third_cases'/wanted['file']).read_text()==' '.join(map(str,tokens))+'\n'
assert {p.name for p in (C/'third_cases').iterdir()}=={x['file'] for x in expected}
if '--structure-only' in sys.argv:
    print('PASS A: all 189 canonical cases and exact specification');sys.exit(0)

P=json.loads((C/'caps.json').read_text())
assert P['schema']=='c44-round9-caps-v1' and P['status']=='candidate, unrefereed'
assert P['horizon']==96 and P['base_counts']=={'1':1,'2':4,'3':10,'4':22}
assert P['third_weight_artifact']=='third_weight.json'
previous=Q(80880411492166173705437336107,39614081257132168796771975168)
assert Q(P['previous_bound'])==previous and P['improvement_bar']=='1/10000'
caps={1:Q(1,2),2:Q(1),3:Q(5,4),4:Q(11,8)}
audits=[]
assert [row['d'] for row in P['rows']]==list(range(5,97))
for row in P['rows']:
    d=row['d'];k=d-1;M=1<<k;c=caps[k];n=row['R']+1
    assert row['first_excluded']==n and Q(row['previous'])==c
    b=max([Q(1,2)]+[Q(1,4)+Q(1,1<<(t+1))+caps[t]/2 for t in range(1,d-1)])
    assert Q(row['b'])==b
    def ceiling(x):
        z=2*k*x;h=z.numerator//z.denominator
        if x.denominator>1 and z.denominator==1:h-=1
        if (d,x)==(5,Q(3,2)):h=min(h,10)
        if (d,x)==(6,Q(3,2)):h=min(h,12)
        if (d,x)==(6,Q(7,4)):h=min(h,13)
        return h
    def controls(x):
        top=ceiling(x)
        hs=range(top+1) if d<=14 else {top,min(top,int(Q(4*k,3)*x))}
        values=[]
        for h in hs:
            ordinary=(1<<d)*c+h+1-2*c*x;bound=ordinary
            if x>1 and 3*h>4*k*x:
                q=Q(2,M);r=Q(x-1,M)
                direct=h+(1<<d)*(c*(1-q-r)+(b-Q(1,4))*q)
                formula=(1<<d)*c+h-2*c*x+4*(b-(c+Q(1,2))/2)
                assert direct==formula and r>0
                bound=min(bound,direct)
            values.append((bound,h,bound<ordinary))
        return max(values)
    maximum_weight=Q(d*M,n)
    points={2-Q(1,1<<j) for j in range(k)}
    points.add(Q(2))
    for a in range(4*k,int(2*k*maximum_weight)+2):
        index=(a*M+4*k-1)//(4*k)
        for z in (index,index+1):points.add(Q(2*z,M))
    for a in range(int(Q(4*k,3)*maximum_weight)+2):
        index=(3*a*M+8*k-1)//(8*k)
        for z in (index,index+1):
            if z>=M:points.add(Q(2*z,M))
    allowed_small={2-Q(1,1<<j) for j in range(k)}
    points=sorted(x for x in points if 1<=x<=maximum_weight and (x>=2 or x in allowed_small))
    assert len(points)==row['representatives']
    worst=max(controls(x)[0] for x in points)
    assert worst<n
    given=row['worst'];x=Q(given['normalized_weight'])
    assert x in points and controls(x)[0]==worst==Q(given['budget'])
    w=row['feasible'];x=Q(w['normalized_weight']);value,h,used=controls(x)
    assert 1<=x and x*(n-1)<=d*M and (x*M/2).denominator==1
    assert x>=2 or x in allowed_small
    assert value>=n-1 and Q(w['budget'])==value and (w['h'],w['retained'])==(h,used)
    caps[d]=Q(n-1,1<<d)
    assert caps[d]>=c and caps[d]-c<=Q(d*k,1<<d) and n-1>=3*M-2
    audits.append(dict(d=d,R=n-1,slack=str(n-worst)))
assert P['caps']=={str(d):str(c) for d,c in caps.items()}
tail=Q(9508,1<<96);bound=caps[96]+tail
assert P['tail']==str(tail) and P['bound']==str(bound)
assert bound<Q(P['strict_claim']) and previous-bound>Q(1,10000)
assert caps[5]==Q(50,32) and caps[6]==Q(107,64)
receipt={'status':'PASS','implementation':'A rational next-count exclusion and canonical orbit coverage',
         'bound':str(bound),'improvement':str(previous-bound),'case_count':189,'rows':audits}
out=R.parent/'receipts' if R.name=='frozen' else R/'receipts';out.mkdir(exist_ok=True)
(out/'packet_a.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='rows'}),flush=True)
