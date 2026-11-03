"""Exact B: Xi leaf-path identity for parity maps; outer truth enumeration
and disjoint homogeneous composition for shared selectors. No search/A imports.
"""
from fractions import Fraction
import collections,json,os,pathlib,subprocess,sys,tempfile
R=pathlib.Path(sys.argv[1]).resolve();binary=pathlib.Path(sys.argv[2]).resolve()
P=json.loads((R/'certificates/lower_results.json').read_text())
assert P['schema']=='c44-lower-results-v1' and P['status']=='candidate, unrefereed'
# Every leaf path and choice of one selector at each ancestor gives a
# Fourier mask. Right-branch/t choices change the coefficient sign.
from functools import lru_cache
@lru_cache(None)
def source_for(degree):
    assert degree in (5,6)
    lengths=[0,1]
    for d in range(2,degree+1):lengths.append(2*lengths[-1]+2)
    depth=degree-1;result={}
    for path in range(1<<depth):
        for choices in range(1<<depth):
            mask=0;sign=1;position=0
            for level in range(depth):
                right=(path>>level)&1;which=(choices>>level)&1
                mask|=1<<(position+which)
                if right and which:sign=-sign
                position+=2+right*lengths[depth-level]
            mask|=1<<position
            assert mask not in result;result[mask]=sign
    assert len(result)==4**depth and all(s.bit_count()==degree for s in result)
    return lengths[degree],1<<depth,result
out=R.parent/'receipts' if R.name=='frozen' else R/'receipts';out.mkdir(exist_ok=True)
ledger={'pid':os.getpid(),'method':'B leaf paths and outer truth tables','children':[],'seeds':[]}
record=out/'lower_b.json'
def save():record.write_text(json.dumps(ledger,indent=2)+'\n')
for entry in P['entries']:
    data=entry['result']
    if entry['family']=='parity':
        source_n,source_den,source=source_for(data.get('seed_degree',5))
        columns=list(map(int,data['columns']));assert all(0<c<(1<<source_n) for c in columns)
        expected=collections.defaultdict(int)
        for mask,coefficient in source.items():
            image=sum(1<<j for j,c in enumerate(columns) if (mask&c).bit_count()%2)
            expected[image]+=coefficient
        expected={s:Fraction(c,source_den) for s,c in expected.items() if c}
        actual={int(s):Fraction(int(c),int(data['denominator'])) for s,c in data['terms'] if c}
        assert len(actual)==len(data['terms']) and actual==expected
        used=0
        for s in actual:used|=s
        n=used.bit_count();d=max(s.bit_count() for s in actual)
        assert (n,d)==(data['relevant_variables'],data['degree']) and d<=5
    else:
        assert entry['family']=='shared-selector'
        weights=data['weights'];terms=data['outer_terms'];n=data['best_count']
        with tempfile.NamedTemporaryFile(mode='w',prefix='outer_',suffix='.txt',dir=out,delete=True) as file:
            file.write(f'{len(weights)} 8 {len(terms)} {n}\n')
            file.write(' '.join(map(str,weights))+'\n')
            for s,c in terms:file.write(f'{s} {c}\n')
            file.flush()
            child=subprocess.Popen([str(binary),file.name],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            row={'label':entry['label'],'pid':child.pid};ledger['children'].append(row);save()
            try:stdout,stderr=child.communicate(timeout=120)
            finally:
                if child.poll() is None:child.kill();child.wait()
            row['code']=child.returncode;assert child.returncode==0,stderr
            actual,d=map(int,stdout.split());assert actual==n
    ledger['seeds'].append({'label':entry['label'],'n':n,'degree':d,'lift':str(Fraction(n+2,1<<d))});save()
best=max(Fraction(x['lift']) for x in ledger['seeds'])
assert str(best)==P['best_lift'] and best==Fraction(3,2)
ledger.update(status='PASS',best_lift=str(best));save()
print('PASS lower B',len(ledger['seeds']),'seeds, best lift',best,flush=True)
