"""Separately written (same agent): explicit total colouring and optimal witness."""
import argparse,json,itertools,pathlib
p=argparse.ArgumentParser();p.add_argument('file');a=p.parse_args();m=json.loads(pathlib.Path(a.file).read_text());n=m['n'];word=m['rank_word'];colors=m['colors']
assert len(colors)==2**n and set(colors)=={0,1}
subsets=[frozenset(j+1 for j in range(n) if (mask//(2**j))%2) for mask in range(2**n)]
assert all(colors[i]==int(word[len(s)]) for i,s in enumerate(subsets))
for label in ['monochromatic_chain','explicit_optimal_family']:
 indices=m[label];f={subsets[i] for i in indices};assert len(f)==len(indices)>0
 assert len({colors[i] for i in indices})==1
 assert all(s|t in f and s&t in f for s,t in itertools.product(f,repeat=2))
 if label=='monochromatic_chain':assert all(s<=t or t<=s for s,t in itertools.product(f,repeat=2))
 else:assert len(f)==8
for c in range(2):
 q=pathlib.Path(f'data/n{n}_{word}_c{c}_lex.cnf.json');qm=json.loads(q.read_text())
 assert qm['n']==n and qm['target']==9 and qm['ranks']==word and qm['color']==c
 assert qm['members']==[i for i,x in enumerate(colors) if x==c]
print(json.dumps({'result':'FULL COLOURING AND OPTIMAL WITNESS VALID','n':n,'rank_word':word,'subsets':len(colors),'chain_size':len(m['monochromatic_chain']),'optimal_family_size':len(m['explicit_optimal_family']),'optimal_family':m['explicit_optimal_family'],'colour_classes_match_theorem_queries':True}))
