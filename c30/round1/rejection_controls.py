"""Mutate certificate fields and require rejection by the frozen-artifact verifier."""
import copy
import json
from pathlib import Path
import tempfile
from verify_baseline import verify

base=json.loads(Path('artifacts/baseline_certificate.json').read_text())
rows=[]
cases=[('target_inflation','lambda','521/50'),('wrong_profile','profile',{'0':'1','2':'1','3':'1'}),('bad_tangent','q0','20'),('bad_density','alpha','3/5'),('bad_z','z','1/100'),('changed_bar','bar_sha256','0'*64),('negative_lambda','lambda','-1')]
with tempfile.TemporaryDirectory(dir='artifacts',prefix='controls-') as td:
    for name,key,value in cases:
        c=copy.deepcopy(base)
        c[key]=value
        p=Path(td)/(name+'.json')
        p.write_text(json.dumps(c))
        try:
            verify(p)
        except (AssertionError,ValueError,ZeroDivisionError) as e:
            rows.append({'case':name,'rejected':True,'reason':str(e)})
        else:
            raise RuntimeError('corrupted certificate accepted: '+name)
Path('artifacts/rejection_controls.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
