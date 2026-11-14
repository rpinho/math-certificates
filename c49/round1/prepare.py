"""Rebuild the mathematical construction; no third-party code is used."""
import itertools,json,lzma,hashlib,re,time
from pathlib import Path
edges=list(itertools.combinations(range(5),2))
eindex={f'{a}{b}':i for i,(a,b) in enumerate(edges)}
F=set()
for v in range(5): F.add(sum(1<<i for i,e in enumerate(edges) if v in e))
for aa in itertools.combinations(range(5),2):
    F.add(sum(1<<i for i,(a,b) in enumerate(edges) if (a in aa)!=(b in aa)))
for cc in itertools.combinations(range(10),4):
    deg=[0]*5
    for i in cc:
        for v in edges[i]: deg[v]+=1
    if sorted(deg)!=[1,1,1,2,3]: continue
    reached={0}
    while True:
        more=reached|{v for i in cc for v in edges[i] if set(edges[i])&reached}
        if more==reached: break
        reached=more
    if len(reached)==5:F.add(1023^sum(1<<i for i in cc))
H=set()
for seed in ([0,1,2,3,4,5,6],[0,1,2,3,4,6,7],[0,1,2,6,9]):
    for a in {x*x%11 for x in range(1,11)}:
        for b in range(11):H.add(sum(1<<((a*x+b)%11) for x in seed))
assert len(F)==75 and len(H)==121
h=[sorted(d>>1 for d in H if (d&1)==k) for k in (0,1)]
assert list(map(len,h))==[46,75]
p1,p2=eindex['03'],eindex['04']
kept=[i for i in range(10) if i not in (p1,p2)]
def core(c):return sum(((c>>i)&1)<<j for j,i in enumerate(kept))
proof=Path('sources/koshta_PROOF.md').read_text()
sections=proof.split('```')
def edge_templates(s):
    return [sum(1<<eindex[e] for e in line.split()) for line in re.split(r'[|\n]',s) if line.strip()]
A1=edge_templates(sections[1]);A2=edge_templates(sections[3])
W=[sum(1<<(int(v)-1) for v in t.split()) for t in re.split(r'[|\n]',sections[5]) if t.strip()]
assert len(A1)==len(A2)==15 and len(W)==20
parts=[]
parts.append({core(c)|(u<<8)|(v<<18) for c in F for u in h[1-((c>>p1)&1)] for v in h[1-((c>>p2)&1)]})
parts.append({core(c)|(v<<18) for c in A1 for v in h[1-((c>>p2)&1)]})
parts.append({core(c)|(u<<8) for c in A2 for u in h[1-((c>>p1)&1)]})
parts.append({u<<8 for u in W}|{core(sum(1<<eindex[e] for e in ['12','14','23']))|(1023<<18)})
assert list(map(len,parts))==[250659,806,806,21]
masks=sorted(set.union(*parts))
assert len(masks)==252292
raw=lzma.decompress(Path('sources/two_pendant_extra_1.5678599.txt.xz').read_bytes())
lines=[l for l in raw.decode().splitlines() if not l.startswith('#')]
assert lines[:2]==['sunflower3 v1','block 28 0 1 252292']
public=sorted(sum(1<<int(i) for i in l.split()) if l!='-' else 0 for l in lines[2:])
assert masks==public
cert={'n':28,'ports':[0,1],'masks':masks,'claimed_rate_lower':'1.56785990242458988585','credit':'D. Koshta with Claude; IRSI/Aspect5 transfer construction; joshua17-create F/H; Sylla pendant augmentation'}
Path('certificates/baseline.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
Path('sources/ingredients.json').write_text(json.dumps({'edges':edges,'F':sorted(F),'H':sorted(H),'A1':A1,'A2':A2,'W':W,'kept_edges':kept},indent=2)+'\n')
with open('certificates/baseline.masks','w') as f:
    for m in masks:f.write(str(m)+'\n')
print(json.dumps({'members':len(masks),'parts':list(map(len,parts)),'public_sha256':hashlib.sha256(raw).hexdigest(),'equals_public_certificate':True}))
