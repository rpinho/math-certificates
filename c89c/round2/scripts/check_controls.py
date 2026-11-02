"""Negative controls for the independently written frozen-artifact verifier."""
import subprocess,json
from pathlib import Path
root=Path('artifacts/controls');root.mkdir(exist_ok=True)
cert=Path('artifacts/frozen_rows8.cert').read_text();lines=cert.splitlines();header=lines[0].split();cases={}
def write(name,content):
 p=root/name;p.write_text(content);return str(p)
wrong=header.copy();wrong[4]=str(int(wrong[4])*2)
cases['doubled_bound']=[write('bad_bound.cert',' '.join(wrong)+'\n'+'\n'.join(lines[1:])+'\n'),'sources/graph8.g6']
wrong=header.copy();wrong[2]=str(int(wrong[2])*2)
cases['wrong_factor_denominator']=[write('bad_scale.cert',' '.join(wrong)+'\n'+'\n'.join(lines[1:])+'\n'),'sources/graph8.g6']
wrong=lines.copy();flags=wrong[2].split();flags[1]=flags[0];wrong[2]=' '.join(flags)
cases['duplicate_flag']=[write('duplicate.cert','\n'.join(wrong)+'\n'),'sources/graph8.g6']
graphs=Path('sources/graph8.g6').read_text().splitlines()
cases['duplicate_graph']=['artifacts/frozen_rows8.cert',write('duplicate.g6','\n'.join([graphs[0],graphs[0]])+'\n')]
cases['missing_graph']=['artifacts/frozen_rows8.cert',write('incomplete.g6','\n'.join(graphs[:-1])+'\n')]
results={}
for name,args in cases.items():
 p=subprocess.run(['./verify_frozen',*args],capture_output=True,text=True)
 results[name]={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 print(name,p.returncode,p.stderr.strip(),flush=True);assert p.returncode!=0
Path('receipts/negative_controls.json').write_text(json.dumps(results,indent=2))
print('PASS all five invalid artifacts rejected',flush=True)
