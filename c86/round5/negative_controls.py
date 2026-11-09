"""Adversarial frozen-certificate controls for release replay."""
import copy,hashlib,json,subprocess,sys
from fractions import Fraction as F
from pathlib import Path
src=Path(sys.argv[1]);tag=sys.argv[2];c=json.loads(src.read_bytes())
Path('controls').mkdir(exist_ok=True)
variants={}
c1=copy.deepcopy(c);c1['bound']=str(F(c1['bound'])-F(1,10**8));variants['wrong-bound']=c1
c2=copy.deepcopy(c);c2['b']=[str(F(w)*F(1001,1000)) for w in c2['b']];variants['raised-weights']=c2
results=[]
for name,v in variants.items():
 path=Path('controls')/(tag+'-'+name+'.json');path.write_text(json.dumps(v));log=Path('logs')/(tag+'-control-'+name+'.log')
 cmd=[sys.executable,'-u','independent_verify.py',str(path),'--witness','5']
 with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 row=dict(name=name,file=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),exit_code=r.returncode,log=str(log),rejected=r.returncode!=0)
 if name=='raised-weights':
  import independent_verify as V
  value=V.point_gap(V.load_certificate(path),F(5));assert value<0
  row['certified_negative_witness']=dict(x='5',enclosure=str(value),upper=str(value.upper()))
 results.append(row)
 assert r.returncode!=0,('corruption accepted',name)
 # Distinguish intended failures from incidental errors.
 text=log.read_text()
 assert ('bound equality' in text or "assert bound == trace/mass" in text) if name=='wrong-bound' else 'nonpositive potential witness' in text
# Replay the same corruptions through the other unchanged checker as well.
for name,v in variants.items():
 path=Path('controls')/(tag+'-'+name+'.json');log=Path('logs')/(tag+'-control-'+name+'-first.log')
 cmd=[sys.executable,'-u','verify_linear.py',str(path),'--beat','1.81','--output','controls/'+tag+'-'+name+'-first.json']
 with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode!=0,('first checker accepted corruption',name)
 text=log.read_text()
 assert ('trace/mass==rat' in text) if name=='wrong-bound' else ('E5' in text or 'negative point' in text or 'negative' in text or 'depth' in text),text[-1500:]
 results.append(dict(name=name,verifier='first',file=str(path),exit_code=r.returncode,log=str(log),rejected=True))
Path(tag+'-negative-controls.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),results=results),indent=2))
print(json.dumps(results,indent=2))
