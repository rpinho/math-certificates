"""Exact sign-array crosscheck; no correction to the printed list is made."""
import json
from pathlib import Path
from flint import fmpz_poly,ctx
ctx.prec=160
A=json.load(open('sources/aguirre-peral07-list.json'))['rows'];old=list(map(tuple,json.load(open('literature-plus09-pool.json'))));out=[]
for r in A:
 if r['row'] not in [39,40,41,42,43]:continue
 q=r['q'];d=len(q)-1;alt=[(-1)**(d-k)*abs(v) for k,v in enumerate(q)];rr=fmpz_poly(q).complex_roots();nonreal=sum(int(m) for z,m in rr if not z.imag.is_zero())
 out.append(dict(row=r['row'],printed_q=q,printed_nonreal_roots=nonreal,alternating_magnitudes=alt,alternating_already_in_previous_union=tuple(alt) in old,note='Magnitude/sign crosscheck only; no inferred correction entered as an author-listed polynomial'))
Path('sources/ap07-sign-crosscheck.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
