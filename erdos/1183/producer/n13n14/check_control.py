"""Separately written (same agent): one closure deletion and a full SAT model."""
import argparse,json,pathlib,itertools
p=argparse.ArgumentParser();p.add_argument('original');p.add_argument('deleted');p.add_argument('--model');p.add_argument('--witness');a=p.parse_args()
m=json.loads(pathlib.Path(a.original+'.json').read_text());d=json.loads(pathlib.Path(a.deleted+'.json').read_text());drop=d['deleted_original_clause_index'];assert 1<=drop<=m['closure_clauses']
assert d['clauses']==m['clauses']-1 and d['variables']==m['variables']
if a.model:
 values={abs(int(z)):int(z)>0 for l in pathlib.Path(a.model).read_text().splitlines() if l.startswith('v ') for z in l.split()[1:] if int(z)}
else:
 w=json.loads(pathlib.Path(a.witness).read_text());family=set(w['family']);allowed=m['members'];target=m['target'];N=len(allowed)
 values={i+1:s in family for i,s in enumerate(allowed)};v=N
 count=0
 for i,s in enumerate(allowed,1):
  count+=s in family
  for j in range(1,min(i,target)+1):v+=1;values[v]=count>=j
 for x,y in itertools.combinations(range(m['n']),2):
  equal=True
  for s in allowed:
   t=s^((1<<x)|(1<<y)) if ((s>>x)^(s>>y))&1 else s
   if s>=t:continue
   equal &= ((s in family)==(t in family));v+=1;values[v]=equal
 assert v==m['variables']
 pathlib.Path(a.deleted+'.witness_model').write_text('s SATISFIABLE\n'+'\n'.join('v '+' '.join(str(i if values[i] else -i) for i in range(start,min(start+100,v+1)))+' 0' for start in range(1,v+1,100))+'\n')
assert set(range(1,m['variables']+1))<=set(values)
def satisfied(cl):return any(values[abs(v)]==(v>0) for v in cl)
checked=0
with open(a.original) as orig,open(a.deleted) as deleted:
 oh=orig.readline().split();dh=deleted.readline().split();assert int(oh[3])-1==int(dh[3]) and oh[2]==dh[2]
 for i,l in enumerate(orig,1):
  cl=list(map(int,l.split()[:-1]))
  if i==drop:
   assert cl==d['deleted_clause'] and not satisfied(cl)
  else:
   assert deleted.readline()==l and satisfied(cl),('remaining clause not satisfied',i);checked+=1
 assert not deleted.read().strip()
# Original set operations confirm exactly one missing closure requirement.
n=m['n'];family={frozenset(j+1 for j in range(n) if s//2**j%2) for i,s in enumerate(m['members'],1) if values[i]}
assert len(family)>=m['target']
violations=[(sorted(s),sorted(t),sorted(z)) for s,t in itertools.combinations(family,2) for z in [s|t,s&t] if z not in family]
assert len(violations)==1
print(json.dumps({'result':'ONE CLOSURE DELETION MAKES SAT; EVERY REMAINING CLAUSE SATISFIED','clauses_checked':checked,'deleted_original_clause':drop,'deleted_clause':d['deleted_clause'],'selected_members':len(family),'closure_violations':violations,'model':a.model or a.deleted+'.witness_model'}))
