"""Exact packet verifier B: integer optimization and orbits built by a separately written (same agent) checker.
No search, generator or A imports. verify_third_b.cpp supplies the fresh
conditional tensor enumeration for every case of this specification.
"""
import itertools, json, pathlib, sys
from fractions import Fraction
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
directory=R/'certificates'
S=json.loads((directory/'third_weight.json').read_text())
assert S['schema']=='c44-third-weight-v2' and S['status']=='candidate, unrefereed'
assert S['degree']==5 and Fraction(S['normalized_weight'])==Fraction(7,4)
assert S['denominator']==32 and S['numerator_norm']==56
assert S['minimum_partial_energy']==16 and S['next_partial_energy']==24
assert S['conclusion']=='controls <= 13'
assert S['template_counts']==dict(zip(('13','14','15','16','17'),(359502,752752,1479478,2757118,4910178)))
# Construct degree-cost partitions as nondecreasing lists of block sizes,
# By a separately written (same agent) checker, without A's multiplicity enumeration.
partitions=[]
def parts(cost,minimum,chosen):
    if cost==4:partitions.append(tuple(chosen));return
    for size in range(minimum,6):
        extra=max(1,size-1)
        if cost+extra<=4:parts(cost+extra,size,chosen+[size])
parts(0,1,[])
assert len(partitions)==12
canonical={}
for dimensions in (14,15,16,17):
    count=3*dimensions-35
    combinations=sorted({tuple(sorted(a)) for a in itertools.product((0,1,2),repeat=4) if 0<=count-1-sum(a)<=dimensions-9})
    assert len(combinations)=={14:12,15:11,16:6,17:2}[dimensions]
    for ci,a in enumerate(combinations):
        outside=count-1-sum(a);bits=1
        for p,amount in enumerate(a):
            for side in range(amount):bits|=1<<(2*p+1+side)
        for offset in range(outside):bits|=1<<(9+offset)
        canonical[(dimensions,'hom',ci)]=(bits,False,[6,24,96,384],list(a),outside,None,None)
nonhom=[]
for sizes in partitions:
    if sizes==(2,2,2,2):continue
    groups=[];starts={};at=1
    for size in sizes:
        starts.setdefault(size,at)
        groups.append(sum(1<<j for j in range(at,at+size)));at+=size
    multiplicities=[sizes.count(j) for j in range(1,6)]
    for bad in [starts[j] for j in sorted(starts)]+[at]:
        nonhom.append((multiplicities,bad,groups))
nonhom.sort(key=lambda row:(row[0],row[1]))
assert len(nonhom)==31
for ci,(tp,bad,groups) in enumerate(nonhom):canonical[(15,'nonhom',ci)]=(((1<<15)-1)^(1<<bad),True,groups,None,None,tp,bad)
extra=[]
for sizes in partitions:
    if sizes==(2,2,2,2):continue
    groups=[];at=1
    for size in sizes:
        groups.append(sum(1<<j for j in range(at,at+size)));at+=size
    tp=[sizes.count(j) for j in range(1,6)]
    for amounts in itertools.product(*[range(size+1) for size in sizes]):
        if any(sizes[j]==sizes[j-1] and amounts[j]<amounts[j-1] for j in range(1,len(sizes))):continue
        outside=9-sum(amounts)
        if not 0<=outside<=14-at:continue
        bits=1;position=1
        for size,amount in zip(sizes,amounts):
            for q in range(amount):bits|=1<<(position+q)
            position+=size
        for q in range(outside):bits|=1<<(at+q)
        assigned=[[amount for size,amount in zip(sizes,amounts) if size==m] for m in range(1,6)]
        extra.append((tp,assigned,outside,bits,groups))
extra.sort(key=lambda item:(item[0],item[1]))
assert len(extra)==127
for ci,(tp,assigned,outside,bits,groups) in enumerate(extra):
    canonical[(14,'nonhom',ci)]=(bits,True,groups,None,outside,tp,assigned)
assert len(S['cases'])==len(canonical)==189
seen=set()
for row in S['cases']:
    key=(row['n'],row['kind'],row['case_index']);assert key in canonical and key not in seen;seen.add(key)
    bits,nh,groups,pairs,outside,tp,bad=canonical[key]
    assert (row['goodbits'],row['nonhomogeneous_only'],row['blocks'],row['unresolved'])==(bits,nh,groups,0)
    if nh:
        assert row['type']==tp
        if key[0]==15:assert row['bad']==bad
        else:assert row['block_good_counts']==bad and row['outside']==outside
    else:assert row['pair_counts']==pairs and row['outside']==outside
    filename=f'n{key[0]}_{key[1]}_{key[2]}.txt';assert row['file']==filename
    expected=[key[0],56,bits,int(nh),len(groups),*groups]
    actual=list(map(int,(directory/'third_cases'/filename).read_text().split()))
    assert actual==expected
assert seen==set(canonical)
if '--structure-only' in sys.argv:
    print('PASS B: independent degree-cost partitions and 189 case files');sys.exit(0)

A=json.loads((directory/'caps.json').read_text())
assert A['schema']=='c44-round9-caps-v1' and A['status']=='candidate, unrefereed'
assert A['horizon']==96 and A['base_counts']==dict(zip(('1','2','3','4'),(1,4,10,22)))
assert A['third_weight_artifact']=='third_weight.json' and A['improvement_bar']=='1/10000'
oldbound=Fraction(80880411492166173705437336107,39614081257132168796771975168)
assert Fraction(A['previous_bound'])==oldbound
counts={1:1,2:4,3:10,4:22};audit=[]
for degree in range(5,97):
    k=degree-1;G=1<<(degree-2);G2=G*G;old=counts[k]
    B=max([G]+[G//2+(counts[t]+1)*(1<<(degree-t-2)) for t in range(1,degree-1)])
    upper=(2*degree*G2)//(6*G-2)
    little={2*G-(G>>j) for j in range(k)}
    samples=set(little);samples.add(2*G)
    for cut in range(4*k,(2*k*upper)//G+2):
        first=(cut*G+2*k-1)//(2*k)
        samples.update((first,first+1))
    for cut in range((4*k*upper)//(3*G)+2):
        first=(3*cut*G+4*k-1)//(4*k)
        if first>=2*G:samples.update((first,first+1))
    samples={z for z in samples if G<=z<=upper and (z>=2*G or z in little)}
    def optimize(z):
        high=(2*k*z)//G
        if z%G and (2*k*z)%G==0:high-=1
        if degree==5 and 2*z==3*G:high=min(high,10)
        if degree==6 and 2*z==3*G:high=min(high,12)
        if degree==6 and 4*z==7*G:high=min(high,13)
        low=min(high,(4*k*z)//(3*G));best=-1
        for controls in (low,high):
            integer_budget=(2*old+controls+1)*G2-old*z
            if z>G and 3*controls*G>4*k*z:integer_budget+=min(0,(2*B-old-2*G)*G)
            result=min(integer_budget//G2,(2*degree*G2)//z)
            best=max(best,result)
        return best
    actual=max(optimize(z) for z in samples)
    scanned=None
    if degree<=16:
        every={z for z in little if z<=upper}|set(range(2*G,upper+1))
        assert actual==max(optimize(z) for z in every)
        scanned=len(every)
    row=A['rows'][degree-5]
    assert row['d']==degree and row['R']==actual and row['first_excluded']==actual+1
    assert Fraction(row['previous'])==Fraction(old,2*G) and Fraction(row['b'])==Fraction(B,2*G)
    counts[degree]=actual
    audit.append(dict(degree=degree,R=actual,critical_points=len(samples),full_grid_points=scanned))
caps={str(d):str(Fraction(v,1<<d)) for d,v in counts.items()}
assert A['caps']==caps
tail=Fraction(96*96+3*96+4,1<<96)
bound=Fraction(counts[96],1<<96)+tail
assert str(tail)==A['tail'] and str(bound)==A['bound']
assert bound<Fraction(A['strict_claim']) and oldbound-bound>Fraction(1,10000)
assert counts[5]==50 and counts[6]==107
result={'status':'PASS','implementation':'B independent integer maxima, full grid through 16, degree-cost case coverage',
        'bound':str(bound),'improvement':str(oldbound-bound),'case_count':len(canonical),'rows':audit}
out=R.parent/'receipts' if R.name=='frozen' else R/'receipts';out.mkdir(exist_ok=True)
(out/'packet_b.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
