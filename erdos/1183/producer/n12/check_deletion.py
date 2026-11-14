"""Check that exactly the final threshold unit was deleted and check its SAT model."""
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('original');p.add_argument('deleted');p.add_argument('model');a=p.parse_args()
m=json.loads(pathlib.Path(a.original+'.json').read_text())
threshold=m.get('base_variables',m['variables']);position=m.get('base_clauses',m['clauses'])
with open(a.original) as src,open(a.deleted) as dst:
    sh=src.readline().split();dh=dst.readline().split()
    assert sh[:3]==dh[:3] and int(sh[3])==int(dh[3])+1
    for index,line in enumerate(src,1):
        if index==position:assert line==f'{threshold} 0\n'
        else:assert line==dst.readline()
    assert dst.read()==''
text=pathlib.Path(a.model).read_text();assert 's SATISFIABLE' in text
values={abs(int(v)):int(v)>0 for l in text.splitlines() if l.startswith('v ') for v in l[2:].split() if int(v)}
with open(a.deleted) as f:
    next(f)
    for l in f:
        cl=list(map(int,l.split()[:-1]));assert any(values[abs(v)]==(v>0) for v in cl)
print('VALID DELETION CONTROL: exactly the at-least-eight unit removed; SAT assignment satisfies every remaining clause')
