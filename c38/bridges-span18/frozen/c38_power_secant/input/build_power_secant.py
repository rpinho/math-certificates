"""Integer repeated-squaring producer for exact degree powers."""
import pathlib,json,hashlib,datetime,shutil,sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(200000)
r=pathlib.Path(__file__).resolve().parent;base=r/'frozen/c38_disjoint_extension';b=json.loads((base/'input/seed.json').read_text());s=json.loads((base/b['secant_relative']/'input/seed.json').read_text());assert json.loads((base/'REJECTION_CONTROLS.json').read_text())['status']=='PASS'
M=b['M'];L17,L18,U,e=map(Q,[s['L17'],s['L18'],s['U'],b['extra_lower']])
def power(n,p):
 out=1
 while p:
  if p&1:out*=n
  n*=n;p//=2
 return out
def value(k):
 num=M-k
 return L17-Q(k,314)*(U-L17)+Q(power(num,1296),power(M,1296))*L18+Q(power(num,690),power(M,690))*e
lo=0;hi=M-1;assert value(lo)>=1 and value(hi)<1
while hi-lo>1:
 mid=(lo+hi)//2
 if value(mid)>=1:lo=mid
 else:hi=mid
k=lo;S=value(k);mu=Q(1<<27,M-k);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
artifact=r/'frozen/c38_power_secant';fr=artifact/'input';fr.mkdir(parents=True,exist_ok=False)
d={'schema':'c38-power-seed-v1','candidate_unrefereed':True,'family':'unchanged exact disjoint parent finite family; expanded full coefficient vector unmaterialized','parent_relative':'../c38_disjoint_extension','parent_manifest_sha256':sha(base/'input/MANIFEST.json'),'parent_controls_sha256':sha(base/'REJECTION_CONTROLS.json'),'M':M,'k':k,'new_M':M-k,'L17':str(L17),'L18':str(L18),'U':str(U),'e':str(e),'degree18':1296,'degree_extra':690,'S':str(S),'mu':str(mu)}
(fr/'seed.json').write_text(json.dumps(d,indent=2)+'\n')
for n in ['build_power_secant.py','verify_power_secant.py','test_power_controls.py','PROOF_POWER_SECANT.md']:shutil.copy2(r/n,fr/n)
m={'schema':'c38-power-input-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in fr.iterdir()}}
(fr/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for p in fr.iterdir():p.chmod(0o444)
print(mu,float(mu),k,float(S),sha(fr/'MANIFEST.json'))
