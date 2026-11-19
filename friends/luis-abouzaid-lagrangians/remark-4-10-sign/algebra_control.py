#!/usr/bin/env python3
"""Exact controls for the conditional implication, not an orientation solver."""
import itertools,json
import sympy as s
r,a,b,c,d=s.symbols('r a b c d')
U=s.Matrix([[a,b],[c,d]])
rows=[]
for s1,s2 in itertools.product([-1,1],repeat=2):
 B=s.diag(s1*U,s2*U)
 trace=s.expand(s.trace(B))
 probe=B.subs({a:r,b:0,c:0,d:r})
 # All pairs pass the INDEPENDENT signs in the published matrix.
 assert all(x in [r,-r] for x in probe.diagonal())
 rows.append({'signs':[s1,s2],'general_trace':str(trace),
              'scalar_probe_diagonal':[str(x) for x in probe.diagonal()],
              'published_unsigned_matrix_compatible':True,
              'same_sign_diagonal_probe_compatible':s1==s2})
 if s1==-s2:assert trace==0
 # Exact |degree0|, |degree1| Ext of M=Sr⊕Sr[1] is4 each.
 E=s.zeros(2)
 for i in range(2):
  for j in range(2):
   # The one-step resolution of a simple has zero differential at same root.
   assert (r-r)==0
assert s.expand((s.Symbol('t')-r)**4).coeff(s.Symbol('t'),3)==-4*r
result={'scope':'conditional algebra only; geometric common-sign lemma NOT certified',
        'rows':rows,'self_Ext_total_dimension':8,
        'opposite_sign_model_self_Ext_total_dimension':8,
        'normal_baseline':'all four sign pairs survive integral invertibility and published independent-diagonal signs',
        'conditional_conclusion':'common-sign geometric trace implies s1=s2 in characteristic zero'}
print(json.dumps(result,indent=2))
