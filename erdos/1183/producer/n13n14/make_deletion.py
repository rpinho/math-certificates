"""Remove the unique closure implication violated by a constructed family."""
import argparse,pathlib,json
p=argparse.ArgumentParser();p.add_argument('base');p.add_argument('witness');p.add_argument('out');a=p.parse_args()
m=json.loads(pathlib.Path(a.base+'.json').read_text());w=json.loads(pathlib.Path(a.witness).read_text());ids={s:i+1 for i,s in enumerate(m['members'])};x,y,z=w['missing_implication'];cl=[-ids[x],-ids[y]]+([ids[z]] if z in ids else [])
removed=[]
with open(a.base) as src,open(a.out,'w') as out:
 h=src.readline().split();out.write(f'p cnf {h[2]} {int(h[3])-1}\n')
 for i,line in enumerate(src,1):
  if list(map(int,line.split()[:-1]))==cl:
   removed.append(i);continue
  out.write(line)
assert len(removed)==1,removed
assert removed[0]<=m['closure_clauses']
meta=dict(m,clauses=m['clauses']-1,deleted_clause=cl,deleted_original_clause_index=removed[0],original=a.base)
pathlib.Path(a.out+'.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'result':'ONE CLOSURE CLAUSE DELETED','line_index':removed[0],'clause':cl,'witness':w}))
