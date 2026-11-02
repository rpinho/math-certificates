from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import json
P=Path(__file__).resolve().parent
s=json.loads((P/'candidate.json').read_text());caps={int(d):Q(v) for d,v in s['caps'].items()}
a=json.loads((P/'verification_a.json').read_text());b=json.loads((P/'verification_b.json').read_text())
assert a['bound']==b['bound'] and a['finite_columns']==b['finite_columns']
with localcontext() as ctx:
    ctx.prec=75
    dec=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
    bound=Q(a['bound']);finite=caps[96];gain=Q(a['gain_over_round5'])
    out={'status':'candidate, unrefereed','bound':str(bound),'decimal':dec(bound),
      'finite_cap96':str(finite),'finite_decimal':dec(finite),'tail':str(bound-finite),
      'gain':str(gain),'gain_decimal':dec(gain),'gap_to_lower_3_over_2':str(bound-Q(3,2)),
      'gap_decimal':dec(bound-Q(3,2)),
      'relaxation_limit_interval':[dec(finite),dec(bound)],
      'modes':{m:{'decimal':dec(Q(r['bound'])),'bound':r['bound']} for m,r in a['results'].items()},
      'low_degree':[{'d':d,'R':int(caps[d]*2**d),'cap':str(caps[d]),'B':b['B'][d],
         'saturates_at_bs':b['saturation'][d-1],
         'B_slack':b['B'][d]-b['saturation'][d-1]} for d in range(1,21)]}
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
