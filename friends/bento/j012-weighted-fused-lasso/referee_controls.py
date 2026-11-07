"""Construct the skeptic's independent-components control using our solver."""
import json
from pathlib import Path
from referee_primal import solve, encode
from fractions import Fraction as F

baseline=json.loads(Path('inputs.json').read_text())['fig1']
y,w=baseline['y'],baseline['alpha']
sub=solve(y[1:],w[1:])
for p in sub:
    p['a']=[F(y[0])]+p['a']
    p['b']=[F(0)]+p['b']
case=dict(y=y,alpha=w,pieces=encode(sub),
          explanation='Computed after setting edge 1 to zero; tested under original positive weight.')
Path('zero_edge_control.json').write_text(json.dumps(case,indent=2))

