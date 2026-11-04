"""Independent periodic-body reproduction of pinned Li/Claude baseline.
No prior-entry program is read, run, or imported. This is not a review of
that entry's finite closing caps. Formulas are from its paper, Section 3.
"""
from independent_geometry import A, PI, F, cover
import json

a=A('1.934062');i=A('0.075486');b=A('0.322723')
va=(a*a+b*b).sqrt();vi=(i*i+b*b).sqrt()
# |delta| >= 7 is vertically clear; inner |delta| <= 7 is short.
assert 7*b>2 and 7*vi<PI
# Self pairs below 3/2 are short; this deliberately covers a larger
# remaining interval than is needed for a minimum doubly critical chord.
assert A('3/2')*va<PI
def outer(d):return 2*a*a*(1-d.cos())+b*b*d*d,(2*a*a*d.sin()+2*b*b*d,)
def unlike(d):return a*a+i*i+2*a*i*d.cos()+b*b*d*d,(-2*a*i*d.sin()+2*b*b*d,)
res=dict(coefficient=str(PI*(va+vi)),curvature_radii=[str((a*a+b*b)/a),str((i*i+b*b)/i)],
    covers=[cover('baseline_outer_self',outer,[(F(3,2),7)],A(4)),
            cover('baseline_unlike',unlike,[(-7,7)],A(4))],
    scope='Periodic double helix only; prior finite closure not replayed or verified')
assert (a*a+b*b)/a>1 and (i*i+b*b)/i>1
with open('baseline_results.json','w') as f:json.dump(res,f,indent=2)
print(json.dumps(res))
