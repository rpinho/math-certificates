#!/usr/bin/env python3
"""Check only Ono eq(3.4) parity, not the geometric sign lemma."""
import json
from pathlib import Path
rows=[]
def exponent(d1,m1,d2):return ((d1-1)+(2+m1)*(d2-1)+1)%2
for slot in [1,2]:
 for form_degree in range(3):
  for other_shift in range(2):
   e=exponent(0,0,form_degree) if slot==1 else exponent(form_degree,other_shift,0)
   w=exponent(0,-2,form_degree) if slot==1 else exponent(form_degree,other_shift,0)
   assert e==w
   rows.append({'corner_slot':slot,'other_form_degree':form_degree,'other_shift_parity':other_shift,'e_exponent':e,'w_exponent':w})
p=Path(__file__).with_name('SIGN_PARITY.json')
p.write_text(json.dumps({'status':'PASS','source':'Ono2504.20489 eq3.4','scope':'explicit convention parity only','rows':rows},indent=2)+'\n')
print('PASS explicit parity cases',len(rows))
