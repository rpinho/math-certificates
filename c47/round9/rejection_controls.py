"""Semantic corruption controls; run the separately written verifier in subprocesses."""
import copy,json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'certificates/tomar-frozen.json');cert=json.loads(p.read_text());claim='482167717377842991882283179477574801392641890014291050323/283174368139841919615520431313000857449005056000000000000'
if len(sys.argv)>2:claim=sys.argv[2]
from fractions import Fraction as F
out=Path('certificates/controls')/p.stem;out.mkdir(exist_ok=True,parents=True)
cases=[]
cases.append(('raised-claim',copy.deepcopy(cert),str(F(claim)+F(1,10**30))))
b=copy.deepcopy(cert);b['measure']['pts'][1][2]=str(F(b['measure']['pts'][1][2])*F(99,100));cases.append(('changed-heavy-mass',b,claim))
b=copy.deepcopy(cert);b['witnesses'][0]['radius']='100';cases.append(('oversized-radius',b,claim))
b=copy.deepcopy(cert);b['witnesses'][0]['rectangle'][0]='0';b['witnesses'][0]['rectangle'][1]=b['measure']['Px'];cases.append(('expanded-rectangle',b,claim))
b=copy.deepcopy(cert);b['measure']['pts'][2][0]=b['measure']['Px'];cases.append(('atom-outside-cell',b,claim))
b=copy.deepcopy(cert);b['measure']['pts'][2][2]='0';cases.append(('zero-mass',b,claim))
b=copy.deepcopy(cert);b['measure']['pts'].append(b['measure']['pts'][2]);cases.append(('duplicate-atom',b,claim))
results=[]
for name,c,q in cases:
 file=out/(name+'.json');file.write_text(json.dumps(c))
 r=subprocess.run([sys.executable,'verify_exact.py',str(file),'--claim',q],capture_output=True,text=True)
 results.append({'control':name,'returncode':r.returncode,'output':json.loads(r.stdout)})
 print(name,r.returncode,results[-1]['output'],flush=True)
Path('logs/rejection-controls-'+p.stem+'.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['returncode']!=0 and r['output']['result']=='FAIL' for r in results)
