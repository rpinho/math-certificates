#!/usr/bin/env python3
"""Check the complete fixed colouring agrees with the two exact upper queries."""
import json,pathlib
p=json.loads(pathlib.Path('certificates/1183_n11_coloring.json').read_text());assert p['n']==11 and p['candidate_value']==7
colors=p['color_by_mask'];assert len(colors)==2048 and set(colors)=={0,1}
for mask,c in enumerate(colors):
 cardinality=len([i for i in range(11) if mask//(2**i)%2]);assert c==p['rank_colors'][cardinality]
for c in [0,1]:
 q=json.loads(pathlib.Path(f'data/1183_n11_c{c}.cnf.json').read_text());assert q['n']==11 and q['target']==8 and q['color']==c and not q['union_only']
 assert q['members']==[s for s in range(2048) if colors[s]==c]
 assert q['ranks']==''.join(map(str,p['rank_colors']))
witness={1,3,5,7,31,63,1023}
assert len(witness)==7 and all(colors[s]==0 for s in witness)
assert all((a|b) in witness and (a&b) in witness for a in witness for b in witness)
print('VALID SEVEN-MEMBER LATTICE: masks 1,3,5,7,31,63,1023, all colour 0')
print('VALID COMPLETE COLOURING: all 2048 subsets; matches both no-eight-set lattice CNFs')
