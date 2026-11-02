"""Fresh integer optimization at fixed influence, plus low-degree full-grid check.
No search, generator, or other verifier code imported.
"""
from fractions import Fraction
import pathlib,json,sys,math
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if root.is_file():root=root.parent

def optimize(d,r,mode,full=False):
 # lambda is represented as s/M. All objectives are evaluated as integers.
 M=1<<(d-1);K=d-1;lower=3*M-2;top=(d*M*M)//lower
 def allowed(s):
  if s>=2*M:return True
  return any(s==2*M-(M>>j) for j in range(K))
 if full:
  energies=[s for s in range(M,top+1,2) if allowed(s)]
 else:
  energies=[2*M-(M>>j) for j in range(K)]
  # Enumerate the original floor cells. If a left endpoint is demoted by
  # the equality lemma the next grid value may recover the old control cost.
  for cell in range(4*K,(2*K*top)//M+1):
   first=2*((cell*M+4*K-1)//(4*K))
   energies += [first,first+2]
 best=-1;arg=None
 for s in set(energies):
  if s>top or not allowed(s):continue
  h=(2*K*s)//M
  if mode in ('refined','quartic','quintic','classified') and s%M and (2*K*s)%M==0:h-=1
  if mode=='second_equality' and 2*s==3*M:h-=1
  if mode in ('quartic','quintic','classified') and d==5 and 2*s==3*M:h=min(h,10)
  if mode=='quintic' and d==6 and 2*s==3*M:h=min(h,13)
  if mode=='classified' and d==6 and 2*s==3*M:h=min(h,12)
  # Previous W = r/M. Budget = 2r+h - (2r-M)*s/M².
  budget=((2*r+h)*M*M-(2*r-M)*s)//(M*M)
  influence=(d*M*M)//s
  value=min(budget,influence)
  if value>best:best=value;arg=(s,h)
 return best,arg

computed={}
for mode in ['combined','second_equality','refined','quartic','quintic','classified']:
 counts={1:1,2:4,3:10,4:22};rows=[]
 for degree in range(5,97):
  value,arg=optimize(degree,counts[degree-1],mode)
  if degree<=13:assert optimize(degree,counts[degree-1],mode,True)[0]==value
  counts[degree]=value;rows.append([degree,value,arg])
 bound=Fraction(counts[96]+9508,1<<96)
 computed[mode]={'counts':counts,'rows':rows,'bound':str(bound)}
# Artifact read only after all independent calculations.
C=json.loads((root/'certificate.json').read_text())
assert C['schema']=='c44-round7-v1' and C['horizon']==96 and C['status']=='candidate, unrefereed'
assert C['base_counts']=={'1':1,'2':4,'3':10,'4':22}
for mode,result in computed.items():
 assert result['bound']==C['modes'][mode]['bound']
 assert all(Fraction(C['modes'][mode]['caps'][str(d)])==Fraction(r,1<<d) for d,r in result['counts'].items())
 assert Fraction(result['bound'])<Fraction(C['claims'][mode])
assert computed['quartic']['counts'][5]==51
outdir=root.parent/'receipts' if root.name=='frozen' else root/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'scalar_b.json').write_text(json.dumps({'status':'PASS','implementation':'B: fixed-influence integer maximum, full grid through degree 13','modes':computed},indent=2)+'\n')
print(json.dumps({m:{'bound':x['bound'],'first_counts':list(x['counts'].items())[:12]} for m,x in computed.items()},indent=2),flush=True)
