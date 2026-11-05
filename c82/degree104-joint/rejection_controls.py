"""Required corrupted-certificate rejection controls, using the same verifier."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from numerics import register,write_json

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',required=True);p.add_argument('--verifier',required=True);a=p.parse_args()
    register('rejection_controls');cert=json.loads(Path(a.certificate).read_text());source=Path(a.verifier).read_text();results=[]
    for case in ['changed_bytes','zero_multiplicity','shared_factor']:
        obj=json.loads(json.dumps(cert))
        if case=='changed_bytes':obj['denominator'][0]['coeffs'][-1]+=1
        if case=='zero_multiplicity':obj['denominator'][0]['multiplicity']=0
        if case=='shared_factor':obj['numerator'][0]['coeffs']=obj['denominator'][0]['coeffs'];obj['numerator'][0]['q_rational']='1'
        path='evidence/corrupt-'+case+'.json';write_json(path,obj)
        script=a.verifier
        if case!='changed_bytes':
            sha=hashlib.sha256(Path(path).read_bytes()).hexdigest()
            lines=source.splitlines(True)
            changed=''.join("EXPECTED = '"+sha+"'\n" if line.startswith('EXPECTED = ') else line for line in lines)
            script='evidence/control-'+case+'-verifier.py';Path(script).write_text(changed)
        with open('evidence/control-'+case+'.log','w') as log:
            worker=subprocess.Popen([sys.executable,script,'--certificate',path,'--target','0.2524','--out','evidence/control-'+case+'-result.json'],stdout=log,stderr=subprocess.STDOUT)
            with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'kind':'expected_rejection','pid':worker.pid,'case':case})+'\n')
            code=worker.wait()
        results.append({'case':case,'exit_code':code,'rejected':code!=0,'repinned':case!='changed_bytes'})
    write_json('evidence/rejection-controls.json',results);print(json.dumps(results),flush=True)
    assert all(r['rejected'] for r in results)
