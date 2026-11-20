"""Three rejection controls on the shipped packet using the actual verifier."""
import json,subprocess,sys
from pathlib import Path
from result import read,sha,put
from numerics import register

def main():
    register('controls');results=[]
    cert=sys.argv[1] if len(sys.argv)>1 else 'certificate.json'
    for case,expected in [('changed_bytes','SHA256 differs'),('zero_multiplicity','q>0'),('shared_factor','p.gcd(r).degree() == 0')]:
        obj=read(cert)
        if case=='zero_multiplicity':obj['denominator'][0]['multiplicity']=0
        elif case=='shared_factor':obj['numerator'][0].update(coeffs=obj['denominator'][0]['coeffs'],q_rational='1')
        path='evidence/control-input.json';put(path,obj)
        if case=='changed_bytes':
            with open(path,'a') as f:f.write('\n')
        pin=sha(cert) if case=='changed_bytes' else sha(path)
        p=subprocess.Popen([sys.executable,'verify.py','--sha',pin,'--certificate',path,'--out','evidence/control-result.json'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        with open('evidence/pids.jsonl','a') as f:print(json.dumps(dict(pid=p.pid,kind=case)),file=f)
        output=p.communicate()[0];Path('logs/control-'+case+'.log').write_text(output)
        assert p.returncode!=0 and expected in output
        results.append(dict(case=case,rejected=True,exit_code=p.returncode,pin=pin,reason=expected))
    result=dict(certificate_sha256=sha(cert),cases=results)
    put('evidence/rejections-'+sha(cert)[:16]+'.json',result)
    if sha(cert)==sha('certificate.json'):put('evidence/rejection-controls.json',result)
if __name__=='__main__':main()
