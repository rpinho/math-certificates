"""Direct evaluation of every clause under a complete solver assignment."""
import argparse,pathlib
p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('model');a=p.parse_args()
text=pathlib.Path(a.model).read_text();assert 's SATISFIABLE' in text
values={abs(int(x)):int(x)>0 for l in text.splitlines() if l.startswith('v ') for x in l[2:].split() if int(x)}
with open(a.cnf) as f:
    _,_,nv,nc=f.readline().split();assert all(i in values for i in range(1,int(nv)+1));count=0
    for l in f:
        if not l.strip() or l.startswith('c'):continue
        lits=list(map(int,l.split()[:-1]));assert any(values[abs(v)]==(v>0) for v in lits);count+=1
    assert count==int(nc)
print(f'VALID COMPLETE SAT MODEL: {nv} variables, {nc} clauses checked')
