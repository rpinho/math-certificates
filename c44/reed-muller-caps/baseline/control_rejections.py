"""Corruption checks against both exact implementations, on copied inputs.
Temporary files are session-created and removed by TemporaryDirectory.
"""
import copy,hashlib,json,tempfile
from pathlib import Path
from verify_exact import verify as independent
from verify_rows import verify as rows
R=Path(__file__).resolve().parent
spec=json.loads((R/'candidate.json').read_text());caps=json.loads((R/spec['cap_source']).read_text())
tests=[]
with tempfile.TemporaryDirectory(prefix='rejection_',dir=R) as dirname:
    tmp=Path(dirname)
    def cap_mutation(name,change):
        p=copy.deepcopy(caps);s=copy.deepcopy(spec);change(p,s)
        b=(json.dumps(p,indent=2)+'\n').encode();path=tmp/(name+'.json');path.write_bytes(b)
        s['cap_source']=str(path.relative_to(R));s['cap_sha256']=hashlib.sha256(b).hexdigest()
        return s
    def reject(name,s):
        result={}
        for label,fn in [('independent',independent),('rows',rows)]:
            try:fn(s)
            except (AssertionError,ValueError,KeyError,IndexError):result[label]='REJECTED'
            else:raise AssertionError('accepted corruption '+name+' '+label)
        tests.append({'name':name,**result})
    for name,fn in [
       ('false_quartic_23',lambda p,s:p['certificates'][0].update(R=23,cap='23/16')),
       ('false_sextic_95',lambda p,s:p['certificates'][2].update(R=95,cap='95/64')),
       ('wrong_minimum_budget',lambda p,s:p['certificates'][0].update(minimum_potential='3/2')),
       ('understated_controls',lambda p,s:p['certificates'][0].update(controls=5)),
       ('unsupported_gap',lambda p,s:p['certificates'][0].update(nonminimum_influence='1/4')),
       ('wrong_input_cap',lambda p,s:p['certificates'][1].update(lower_cap='11/8')),
       ('missing_degree',lambda p,s:p['certificates'].pop()),
       ('duplicate_degree',lambda p,s:p['certificates'][1].update(degree=4)),
       ('forged_nonminimum_floor',lambda p,s:p['certificates'][2].update(nonminimum_R=127)),
       ('forged_minimum_floor',lambda p,s:p['certificates'][0].update(minimum_R=23))]:
        reject(name,cap_mutation(name,fn))
    for name,key,value in [
       ('caps_changed','caps',dict(spec['caps'],**{'8':'681/256'})),
       ('wrong_R3','external_R3',9),('wrong_block_theorem','external_bs_theorem','B<=d*d-1'),
       ('wrong_horizon','horizon',95),('stronger_decimal','claim','3.16'),
       ('weaker_decimal','claim','4'),('wrong_spectral_hash','spectral_sha256','0'*64),
       ('wrong_epi_hash','epi_sha256','0'*64),('wrong_cap_hash','cap_sha256','0'*64)]:
        s=copy.deepcopy(spec);s[key]=value;reject(name,s)
out={'status':'PASS','controls':tests,'count':len(tests)}
(R/'control_rejections.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','rejections':len(tests)}))
