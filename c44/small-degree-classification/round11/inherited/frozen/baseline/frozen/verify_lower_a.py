"""Exact lower-seed verifier A: full rational expansion and integer square.
Imports neither search nor any other verifier. It certifies stored seeds,
not coverage of the heuristic search spaces.
"""
from fractions import Fraction as Q
import collections,functools,json,math,pathlib,sys
R=pathlib.Path(sys.argv[1]).resolve()
packet=json.loads((R/'certificates/lower_results.json').read_text())
assert packet['schema']=='c44-lower-results-v1' and packet['status']=='candidate, unrefereed'
def check(polynomial,denominator):
    p={int(s):int(c) for s,c in polynomial if c}
    assert len(p)==len(polynomial)
    square=collections.defaultdict(int)
    for s,a in p.items():
        for t,b in p.items():square[s^t]+=a*b
    assert {s:c for s,c in square.items() if c}=={0:denominator**2}
    used=0
    for s in p:used|=s
    return used.bit_count(),max(s.bit_count() for s in p)
@functools.lru_cache(None)
def seed(d):
    if d==1:return 1,{1:Q(1)}
    n,p=seed(d-1);q={}
    for s,c in p.items():
        q[(s<<2)|1]=c/2;q[(s<<2)|2]=c/2
        q[(s<<(n+2))|1]=c/2;q[(s<<(n+2))|2]=-c/2
    return 2*n+2,q
def integerize(p):
    den=math.lcm(*(c.denominator for c in p.values()))
    return [[s,int(c*den)] for s,c in sorted(p.items()) if c],den
results=[]
for entry in packet['entries']:
    data=entry['result']
    if entry['family']=='parity':
        n,d=check(data['terms'],int(data['denominator']))
        assert n==data['relevant_variables'] and d==data['degree'] and d<=5
        assert len(data['columns'])>=n
    else:
        assert entry['family']=='shared-selector'
        outer={int(s):Q(int(c),8) for s,c in data['outer_terms']}
        assert len(outer)==len(data['outer_terms'])
        weights=data['weights'];variables=len(weights);used=0
        for s in outer:used|=s
        assert used==(1<<variables)-1
        check(data['outer_terms'],8)
        pol={};offsets=[];inners=[];n=0
        for r in weights:
            assert isinstance(r,int) and 1<=r<=5
            size,p=seed(r);offsets.append(n);inners.append(p);n+=size
        for s,c in outer.items():
            terms={0:c}
            for j in range(variables):
                if not s>>j&1:continue
                next_terms={}
                for a,x in terms.items():
                    for b,y in inners[j].items():next_terms[a|(b<<offsets[j])]=x*y
                terms=next_terms
            for a,x in terms.items():pol[a]=pol.get(a,Q(0))+x
        pol={s:c for s,c in pol.items() if c}
        terms,den=integerize(pol);actual,d=check(terms,den)
        assert actual==n==data['best_count'] and d<=5
    lift=Q(n+2,1<<d)
    results.append({'label':entry['label'],'n':n,'degree':d,'lift':str(lift)})
assert len(results)==len(packet['entries']) and results
maximum=max(Q(row['lift']) for row in results)
assert str(maximum)==packet['best_lift']
assert maximum==Q(3,2), 'an improved seed requires an updated proof and packet'
out=R.parent/'receipts' if R.name=='frozen' else R/'receipts';out.mkdir(exist_ok=True)
(out/'lower_a.json').write_text(json.dumps({'status':'PASS','method':'full exact sparse expansion and Boolean square','best_lift':str(maximum),'seeds':results},indent=2)+'\n')
print('PASS lower A',len(results),'seeds, best lift',maximum,flush=True)
