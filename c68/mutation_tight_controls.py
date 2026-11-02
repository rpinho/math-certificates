"""Adversarial controls for the final polynomial-envelope proof checkers."""
import json,subprocess,sys,time,hashlib
from pathlib import Path
from fractions import Fraction as F
root=Path(__file__).resolve().parent;cert=root/'certificate-tight.json';out=root/'mutations-tight';out.mkdir(exist_ok=True);controls=[]
d=json.loads(cert.read_text());d['weights'][0]=str(F(d['weights'][0])+F(1,10000));d['weights'][2]=str(F(d['weights'][2])-F(1,10000));controls.append(('mass-preserving-bad-moments',d,["('A', 2","('A', 2"]))
d=json.loads(cert.read_text());d['second_tail_k']=1;controls.append(('false-infinite-tail',d,['second tail','second tail']))
d=json.loads(cert.read_text());d['lower_envelope']['coefficients_delta'][0]=str(F(d['lower_envelope']['coefficients_delta'][0])+F(1,10000));controls.append(('false-polynomial-lower-bound',d,['Bernstein','Mobius positivity']))
results=[]
for name,d,reasons in controls:
 p=out/(name+'.json');p.write_text(json.dumps(d,indent=2)+'\n')
 for checker,reason in zip(['verify_envelope_arb.py','verify_envelope_rational.py'],reasons):
  start=time.monotonic();proc=subprocess.Popen([sys.executable,str(root/checker),str(p)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);so,se=proc.communicate(timeout=300);(out/(name+'-'+checker+'.log')).write_text(so+se);ok=proc.returncode!=0 and reason in se
  row={'control':name,'checker':checker,'pid':proc.pid,'rejected':ok,'returncode':proc.returncode,'expected_diagnostic':reason,'seconds':time.monotonic()-start};results.append(row);print(json.dumps(row),flush=True);assert ok,(row,so,se)
for checker in ['verify_envelope_arb.py','verify_envelope_rational.py']:
 p=subprocess.run([sys.executable,'-O',str(root/checker),str(cert)],capture_output=True,text=True);assert p.returncode!=0 and 'Refusing -O' in p.stdout+p.stderr;results.append({'control':'optimized-Python-disabled-assertions','checker':checker,'rejected':True})
(root/'mutation-tight-results.json').write_text(json.dumps({'status':'PASS','certificate_sha256':hashlib.sha256(cert.read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
