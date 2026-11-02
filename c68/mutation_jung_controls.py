"""Adversarial controls for both independent geometric-model checkers."""
import json,subprocess,tempfile,time,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
base=Path(__file__).resolve().parent;source=base/'certificate-jung.json';original=json.loads(source.read_text());results=[]
for mode in ['mass-preserving-bad-moments','unsafe-linear-envelope','false-infinite-tail','wrong-analytic-model']:
 d=json.loads(json.dumps(original))
 if mode=='mass-preserving-bad-moments':
  d['weights'][0]=str(F(d['weights'][0])+F(1,1000));d['weights'][1]=str(F(d['weights'][1])-F(1,1000));diagnostic='first moment'
 elif mode=='unsafe-linear-envelope':d['linear_slope']=str(F(d['linear_slope'])*2);diagnostic='linear envelope'
 elif mode=='false-infinite-tail':d['second_tail_k']=100;diagnostic='second infinite tail'
 else:d['analytic_model']='wrong';diagnostic='AssertionError'
 with tempfile.TemporaryDirectory(dir=base,prefix='mutation-jung-') as tmp:
  p=Path(tmp)/'certificate.json';p.write_text(json.dumps(d))
  for checker in ['verify_jung_arb.py','verify_jung_rational.py']:
   start=time.monotonic();res=subprocess.run(['nice','-n','10',sys.executable,str(base/checker),str(p)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   assert res.returncode!=0 and diagnostic in res.stdout,(mode,checker,res.stdout)
   results.append({'control':mode,'checker':checker,'rejected':True,'expected_diagnostic':diagnostic,'seconds':time.monotonic()-start});print(results[-1],flush=True)
for checker in ['verify_jung_arb.py','verify_jung_rational.py']:
 r=subprocess.run([sys.executable,'-O',str(base/checker),str(source)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);assert r.returncode!=0 and 'Refusing' in r.stdout;results.append({'control':'optimized-Python-disabled-assertions','checker':checker,'rejected':True})
out={'status':'PASS','certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'results':results};(base/'mutation-jung-results.json').write_text(json.dumps(out,indent=2)+'\n')
