import json,pathlib,math
from prepare import Field
P=pathlib.Path('results');checks={}
for path in sorted(pathlib.Path('inputs').glob('q*.txt')):
 name=path.stem; r=json.loads((P/f'{name}.json').read_text()); p=json.loads((P/f'{name}.prep.json').read_text());f=Field(r['q'])
 G=[list(map(int,l.split())) for l in path.read_text().splitlines()]; R,piv=f.rref(G);w=r['witness'];assert sum(x!=0 for x in w)==r['distance']
 assert f.encode(R,[w[c] for c in piv])==w
 union=set();expected=0;lb=0
 for b,depth in zip(p['blocks'],r['depths']):
  assert not (union&set(b['new_pivots']));union.update(b['new_pivots'])
  assert f.rref(b['G'])[0]==R
  assert len(b['new_pivots'])==b['rank']
  assert all(b['G'][i][c]==int(i==j) for j,c in enumerate(b['pivots']) for i in range(r['k']))
  expected+=sum(math.comb(r['k'],s)*(r['q']-1)**(s-1) for s in range(1,depth+1))
  lb+=max(0,depth+1-(r['k']-b['rank']))
 assert expected==r['tested_projective_messages_with_repeats'] and lb==r['lower_bound'] and lb>=r['distance'] and r['complete']
 checks[name]={'witness_original_row_space':True,'disjoint_pivots_and_bases':True,'expected_enumeration_count':expected,'proven_lower':lb,'witness_weight':r['distance']}
A=[list(map(int,l.split())) for l in pathlib.Path('inputs/q5_n130_k14_d81.txt').read_text().splitlines()]
B=[list(map(int,l.split())) for l in pathlib.Path('inputs/q5_n130_k16_d77.txt').read_text().splitlines()]
checks['rank_stacked_130_k14_k16']=len(Field(5).rref(A+B)[1])
(P/'result_checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
