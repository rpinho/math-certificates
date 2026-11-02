"""Finite minimum-support classification controls, not universal proof."""
import itertools,json
from pathlib import Path
R=Path(__file__).resolve().parent
def partitions(a):
    if not a:
        yield [];return
    first,*rest=a
    for p in partitions(rest):
        yield [[first]]+[b[:] for b in p]
        for j in range(len(p)):
            yield [([first]+b if i==j else b[:]) for i,b in enumerate(p)]
rows=[]
for n in range(1,5):
    found={}
    for fixed in range(1<<n):
        rest=[i for i in range(n) if not fixed>>i&1]
        for p in partitions(rest):
            groups=[g for g in p if len(g)>=2]
            h=fixed.bit_count()+sum(map(len,groups))
            k=fixed.bit_count()+sum(len(g)-1 for g in groups)
            assert h==k+len(groups)<=2*k
            for translation in range(1<<n):
                vals=[]
                for x in range(1<<n):
                    y=x^translation
                    if y&fixed or any(len({(y>>i)&1 for i in g})>1 for g in groups):
                        vals.append(0)
                    else:
                        vals.append((-1)**sum((y>>g[0])&1 for g in groups if len(g)%2==0))
                for sign in [1,-1]:
                    code=sum((1+sign*v)*3**j for j,v in enumerate(vals))
                    if code in found:assert found[code]==k
                    found[code]=k
    rows.extend((n,code,k) for code,k in sorted(found.items()))
(R/'structure_templates.txt').write_text(''.join(f'{n} {code} {k}\n' for n,code,k in rows))
print(json.dumps({'status':'GENERATED','templates':{str(n):sum(a==n for a,_,_ in rows) for n in range(1,5)}}))
