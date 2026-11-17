"""Standard lex-leaders for member-bit vectors under all ground-coordinate swaps."""
import argparse,itertools,json,pathlib
p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('out');a=p.parse_args()
m=json.loads(pathlib.Path(a.base+'.json').read_text());Y={s:i+1 for i,s in enumerate(m['members'])}
clauses=[];nv=m['variables']
for u,v in itertools.combinations(range(m['n']),2):
    prev=None
    for s in m['members']:
        t=s^((1<<u)|(1<<v)) if ((s>>u)&1)!=((s>>v)&1) else s
        if s>=t:continue
        x,y=Y[s],Y[t];nv+=1;q=nv;prefix=[-prev] if prev else []
        clauses.extend([prefix+[-x,y],prefix+[-x,-y,q],prefix+[x,y,q]])
        prev=q
with open(a.out,'w') as out,open(a.base) as base:
    next(base);out.write(f'p cnf {nv} {m["clauses"]+len(clauses)}\n')
    for l in base:out.write(l)
    for cl in clauses:out.write(' '.join(map(str,cl))+' 0\n')
meta=dict(m,base_cnf=a.base,base_variables=m['variables'],base_clauses=m['clauses'],variables=nv,clauses=m['clauses']+len(clauses),symmetry='member vector lex <= its image under each of all ground-coordinate transpositions',lex_clauses=len(clauses))
pathlib.Path(a.out+'.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({k:v for k,v in meta.items() if k!='members'}))
