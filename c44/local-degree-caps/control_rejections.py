"""Certificate/specification corruption controls for both independent verifiers."""
import copy,hashlib,json,os,tempfile
from pathlib import Path
from verify_caps import verify as caps
from verify_bound import verify as row
from verify_column import verify as column
R=Path(__file__).resolve().parent
def rejected(fn,arg):
    try:fn(arg)
    except (AssertionError,ValueError,KeyError):return True
    raise RuntimeError('corruption was accepted')
def main():
    print('PID',os.getpid(),flush=True);out=[]
    cert=json.loads((R/'cap_certificate.json').read_text());spec=json.loads((R/'candidate.json').read_text())
    for label,field,value in [('R_too_small','R',179),('bad_M','M',31),('false_lower_cap','lower_cap','2'),('false_minimum_budget','minimum_potential','5/2'),('arbitrary_cap','cap','2')]:
        c=copy.deepcopy(cert);c['certificates'][2][field]=value
        assert rejected(caps,c);out.append({'control':label,'checker':'caps','rejected':True})
    for label,field,value in [('wrong_schema','schema','x'),('arbitrary_caps','caps',{'3':'1'}),('cap_hash','cap_sha256','0'*64),('spectral_hash','spectral_sha256','0'*64),('false_claim','claim','3.9')]:
        c=copy.deepcopy(spec);c[field]=value
        for name,fn in [('row',row),('column',column)]:
            assert rejected(fn,c);out.append({'control':label,'checker':name,'rejected':True})
    # A false mathematical cap with refreshed hashes must still fail.
    bad=copy.deepcopy(cert);bad['certificates'][2]['R']=179;bad['certificates'][2]['cap']='179/64'
    raw=(json.dumps(bad,indent=2)+'\n').encode()
    with tempfile.NamedTemporaryFile(dir=R,prefix='temporary_corrupt_',suffix='.json',delete=False) as f:
        f.write(raw);p=Path(f.name)
    try:
        c=copy.deepcopy(spec);c['cap_source']=p.name;c['cap_sha256']=hashlib.sha256(raw).hexdigest()
        for name,fn in [('row',row),('column',column)]:
            assert rejected(fn,c);out.append({'control':'false_math_refreshed_hash','checker':name,'rejected':True})
    finally:p.unlink() # Only the temporary file created above.
    (R/'sources/rejection_controls.json').write_text(json.dumps({'status':'PASS','controls':out},indent=2)+'\n')
    print('PASS',len(out),'rejection controls',flush=True)
if __name__=='__main__':main()
