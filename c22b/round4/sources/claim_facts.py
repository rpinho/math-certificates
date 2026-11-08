"""Exact rational consequences of the published length inequality; no geometry claim."""
import json
from fractions import Fraction as F
from pathlib import Path
packet=Path(__file__).resolve().parents[1]
bound=json.loads((packet/'candidate_high/BOUND.json').read_text())
construction=json.loads((packet/'candidate_high/CONSTRUCTION.json').read_text())
comparator=json.loads((packet/'sources/pr342.json').read_text())
c=F(bound['upper_bound'])
old=F('7.087662112')
assert '7.087662112' in comparator['body']
assert c==F(442972439,62500000)
finite=F(c*1324+150,1327)
assert finite==F(148967627309,20734375000)
assert finite<F('7.184572832')
for prefix in ['7.184572831782969','7.18457283178296910324']:
 unit=F(1,10**len(prefix.split('.')[1]))
 assert F(prefix)<=finite<F(prefix)+unit
assert old-c==F('0.000103088')
print(json.dumps({'family_coefficient':str(c),'finite_n1':str(finite),'finite_n1_upper':'7.184572832','gap_to_pr342':str(old-c),'qualification':'Consequences conditional on the separately established geometric length/thickness theorem.'},indent=2))
