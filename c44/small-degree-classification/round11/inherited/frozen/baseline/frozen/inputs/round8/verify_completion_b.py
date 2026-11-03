"""Independent B: integer fixed-influence optimization, full low-degree grid.
No generator/checker A imports. Uses one common integer denominator per row.
"""
import json,pathlib,sys
from fractions import Fraction
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if root.is_file():root=root.parent
P=json.loads((root/'completion_certificate.json').read_text())
assert P['schema']=='c44-round8-completion-v1' and P['status']=='candidate, unrefereed'
assert P['horizon']==96 and P['base_counts']=={'1':1,'2':4,'3':10,'4':22}
assert P['strict_claim']=='2.0417086280' and P['improvement_bar']=='1/1000'
assert P['previous_bound']=='164865563398608188023949601889/79228162514264337593543950336'
outputs={}
for mode in ['simple','sharp']:
 counts={1:1,2:4,3:10,4:22};steps=[]
 for degree in range(5,97):
  k=degree-1;G=1<<(degree-2);square=G*G;old=counts[k]
  # b has denominator 2G: max over the constant branch and every exact
  # lower-degree potential cap plus selector weights.
  B=max([G]+[G//2+(counts[t]+1)*(1<<(degree-t-2)) for t in range(1,degree-1)])
  maximum_z=(2*degree*square)//(6*G-2)
  candidates={2*G-(G>>j) for j in range(degree-1)}
  candidates.add(2*G)
  # Critical indices are generated directly as integer quotients.
  for cut in range(4*k,(2*k*maximum_z)//G+1):
   left=(cut*G+2*k-1)//(2*k)
   candidates.add(left);candidates.add(left+1)
  for cut in range((4*k*maximum_z)//(3*G)+2):
   left=(3*cut*G+4*k-1)//(4*k)
   if left>=2*G:candidates.add(left)
  allowed_small={2*G-(G>>j) for j in range(degree-1)}
  candidates={z for z in candidates if G<=z<=maximum_z and (z>=2*G or z in allowed_small)}
  def at(z):
   h=(2*k*z)//G
   if z%G and (2*k*z)%G==0:h-=1
   if mode=='sharp' and degree==5 and 2*z==3*G:h=min(h,10)
   if mode=='sharp' and degree==6 and 2*z==3*G:h=min(h,12)
   ordinary_last=min(h,(4*k*z)//(3*G))
   scores=[]
   # Budgets increase by exactly one with h in either valid regime.
   for a in {ordinary_last,h}:
    numerator=(2*old+a+1)*square-old*z
    if z>G and 3*a*G>4*k*z:
     correction=(2*B-old-2*G)*G
     if correction<0:numerator+=correction
    scores.append((numerator,a))
   numerator,a=max(scores)
   control=numerator//square;influence=(2*degree*square)//z
   return min(control,influence),numerator,a
  best,z=max((at(z)[0],z) for z in candidates)
  if degree<=16:
   full=set(allowed_small)
   full.update(range(2*G,maximum_z+1))
   full={z for z in full if z<=maximum_z}
   brute=max((at(z)[0],z) for z in full)
   assert brute[0]==best,(degree,best,brute)
   grid_size=len(full)
  else:grid_size=None
  # Read the submitted row only after deriving the integer optimum.
  row=P['modes'][mode]['rows'][degree-5]
  assert row['d']==degree and row['R']==best
  assert Fraction(row['b'])==Fraction(B,2*G)
  assert Fraction(row['previous'])==Fraction(old,2*G)
  assert row['first_excluded']==best+1
  counts[degree]=best
  steps.append({'degree':degree,'R':best,'grid_points':grid_size,'critical_points':len(candidates),'maximizer_grid_index':str(z)})
 caps={str(d):str(Fraction(v,1<<d)) for d,v in counts.items()}
 assert caps==P['modes'][mode]['caps']
 tail=Fraction(9508,1<<96);bound=Fraction(counts[96],1<<96)+tail
 assert str(bound)==P['modes'][mode]['bound'] and str(tail)==P['modes'][mode]['tail']
 assert Fraction(P['previous_bound'])-bound>Fraction(1,1000)
 assert bound<Fraction(P['strict_claim']) and counts[5]==50 and counts[6]==109
 outputs[mode]={'bound':str(bound),'rows':steps}
assert outputs['simple']['bound']==outputs['sharp']['bound']
receipts=root.parent/'receipts';receipts.mkdir(exist_ok=True)
(receipts/'completion_b.json').write_text(json.dumps({'status':'PASS','method':'independent integer maxima with full grid through 16','modes':outputs},indent=2)+'\n')
print(json.dumps({m:{'bound':v['bound'],'R5':v['rows'][0]['R'],'R6':v['rows'][1]['R']} for m,v in outputs.items()},indent=2),flush=True)
