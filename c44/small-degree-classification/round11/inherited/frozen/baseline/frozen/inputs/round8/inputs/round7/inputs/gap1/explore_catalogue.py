"""Read the published Rasoolzadeh catalogue; exact integer Walsh arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json, hashlib
R=Path(__file__).resolve().parent
raw=(R/'sources/F10T6.txt').read_bytes()
rows=[]
for index,line in enumerate(raw.decode().splitlines()):
    line=line.strip()
    if not line:continue
    assert len(line)==1024 and set(line)<=set('01')
    a=[(-1 if int(v)^(x.bit_count()&1) else 1) for x,v in enumerate(line)]
    h=1
    while h<1024:
        for base in range(0,1024,2*h):
            for j in range(base,base+h):a[j],a[j+h]=a[j]+a[j+h],a[j]-a[j+h]
        h*=2
    assert sum(c*c for c in a)==1024**2
    terms={s:c for s,c in enumerate(a) if c}
    assert max(s.bit_count() for s in terms)<=3
    local=[max([s.bit_count() for s in terms if s>>i&1],default=0) for i in range(10)]
    D=sum((Q(1,2**d) for d in local if d),Q(0))
    e3=sum(c*c for s,c in terms.items() if s.bit_count()==3)
    assert D<=1+Q(e3,4*1024**2)
    if D==1+Q(e3,4*1024**2):
        signature=(D,Q(e3,1024**2),sum(bool(d) for d in local),tuple(sorted(d for d in local if d)))
        assert signature in [(Q(1),Q(0),4,(2,)*4),(Q(9,8),Q(1,2),9,(3,)*9),(Q(5,4),Q(1),10,(3,)*10)]
    rows.append({'line':index+1,'R':sum(bool(d) for d in local),'D':str(D),
                 'homogeneous3':e3==1024**2,'E3':str(Q(e3,1024**2)),
                 'local_degrees':local})
result={'source_sha256':hashlib.sha256(raw).hexdigest(),'classes':len(rows),
        'R_histogram':dict(sorted(Counter(r['R'] for r in rows).items())),
        'nonhomogeneous_max_D':str(max(Q(r['D']) for r in rows if not r['homogeneous3'])),
        'weight_maximizers':[r for r in rows if Q(r['D'])==Q(5,4)],'rows':rows}
assert len(rows)==761
assert [r['line'] for r in rows if Q(r['D'])==1+Q(r['E3'])/4]==[700,716,757]
(R/'catalogue_analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
