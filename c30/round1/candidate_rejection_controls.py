"""Frozen candidate and first-moment rejection controls; no search."""
import copy
import json
from pathlib import Path
import tempfile
from verify_candidate import verify
from verify_mean_two_leaf import verify as verify_mean

c=json.loads(Path('artifacts/candidate_certificate.json').read_text())
m=json.loads(Path('artifacts/mean_two_leaf_certificate.json').read_text())
rows=[]
cases=[('inflate_bound','lambda','1043/100'),('bad_profile','profile',{'0':'1','1':'1','2':'1','3':'1'}),('too_few_two_leaf_strips','two_leaf_cap','1/20'),('invalid_leaf_density','alpha','3/5'),('negative_kappa','kappa','-1'),('bad_saddle','q0','2'),('bad_z','z','1/100'),('wrong_bar','bar_sha256','0'*64),('wrong_mean_hash','mean_certificate_sha256','0'*64)]
with tempfile.TemporaryDirectory(dir='artifacts',prefix='candidate-controls-') as td:
    for name,key,val in cases:
        bad=copy.deepcopy(c);bad[key]=val
        p=Path(td)/(name+'.json');p.write_text(json.dumps(bad))
        try:verify(p)
        except (AssertionError,ValueError,ZeroDivisionError) as e:rows.append({'case':name,'rejected':True,'reason':str(e)})
        else:raise RuntimeError('corrupted candidate accepted: '+name)
for name,key,val in [('wrong_root','root_lower','1/4'),('root_not_isolated','root_lower','39/100'),('bad_mean_threshold','markov_threshold','1/20'),('mean_bar_hash','bar_sha256','0'*64)]:
    bad=copy.deepcopy(m);bad[key]=val
    try:verify_mean(bad)
    except (AssertionError,ValueError,ZeroDivisionError) as e:rows.append({'case':name,'rejected':True,'reason':str(e)})
    else:raise RuntimeError('corrupted mean certificate accepted: '+name)
Path('artifacts/candidate_rejection_controls.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'status':'PASS','corrupted_certificates_rejected':len(rows),'controls':rows},indent=2))
