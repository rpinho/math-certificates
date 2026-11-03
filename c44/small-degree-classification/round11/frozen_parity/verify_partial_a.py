"""Acceptance A metadata/driver, separately written (same agent) base-three case reconstruction."""
import argparse,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('--binary',required=True);p.add_argument('--case',type=int);p.add_argument('--positive',action='store_true');a=p.parse_args()
d=json.loads(pathlib.Path(a.artifact).read_text())
assert d['schema']=='c44-parity-partial-v1' and d['status']=='candidate, unrefereed'
assert (d['degree'],d['controls'],d['norms'],d['minimum_norm'],d['gap'],d['component_variance_numerator'])==(6,21,[120,124],32,16,63)
assert d['homogeneous_seed'] is True and d['even_masks'] is True
cases=[]
for norm,maximum in ((120,3),(124,4)):
 profiles=[]
 for word in range(243):
  x=word;v=[]
  for j in range(5):v.append(x%3);x//=3
  if v!=sorted(v) or sum(v)>maximum:continue
  profiles.append(v)
 for profile in sorted(profiles):
  mask=0
  for i,c in enumerate(profile):
   for j in range(c):mask+=1<<(1+2*i+j)
  for j in range(maximum-sum(profile)):mask+=1<<(11+j)
  cases.append(dict(norm=norm,omitted=mask,seed_pair_counts=profile))
assert len(cases)==15 and d['cases']==cases
assert d['conclusion']==dict(ceiling=20,weights=['15/8','31/16'],R7=227)
if a.positive:subprocess.run([a.binary,'12','64',str((1<<12)-1),'1'],check=True)
else:
 for index in (range(15) if a.case is None else [a.case]):
  c=cases[index];out=subprocess.check_output([a.binary,'21',str(c['norm']),str(((1<<21)-1)^c['omitted']),'0'],text=True);j=json.loads(out);assert j['unsigned_leaves']==0;print(json.dumps(dict(case=index,**j)),flush=True)
