"""Actual exact-code corruptions of the degree-power input."""
import argparse,pathlib,json,tempfile,shutil,hashlib
from verify_power_secant import check,Rejection
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args();original=pathlib.Path(a.artifact).resolve();check(original);seed=json.loads((original/'input/seed.json').read_text());parent=(original/seed['parent_relative']).resolve();scratch=original.parent.parent/'tmp_controls';scratch.mkdir(exist_ok=True);records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def edit_seed(r,fn):p=r/'input/seed.json';d=json.loads(p.read_text());fn(d);dump(p,d)
def test(name,expected,edit,rehash=False):
 with tempfile.TemporaryDirectory(prefix='power_secant_',dir=scratch) as td:
  r=pathlib.Path(td)/'artifact';shutil.copytree(original,r)
  for q in r.rglob('*'):
   if q.is_file():q.chmod(0o644)
  edit(r)
  if rehash:
   p=r/'input/MANIFEST.json';m=json.loads(p.read_text());m['sha256']['seed.json']=sha(r/'input/seed.json');dump(p,m)
  try:check(r,parent)
  except Rejection as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+expected,(name,expected,actual)
  records.append({'corruption':name,'expected':'REJECT:'+expected,'actual':actual,'pass':True,'seed_hash_rebound':rehash})
test('change verifier byte','INPUT_SHA256',lambda r:(r/'input/verify_power_secant.py').write_text((r/'input/verify_power_secant.py').read_text()+'\n'))
test('change seed byte','INPUT_SHA256',lambda r:(r/'input/seed.json').write_text((r/'input/seed.json').read_text()+'\n'))
test('change proof byte','INPUT_SHA256',lambda r:(r/'input/PROOF_POWER_SECANT.md').write_text((r/'input/PROOF_POWER_SECANT.md').read_text()+'\n'))
test('wrong parent binding','PARENT_BINDING',lambda r:edit_seed(r,lambda d:d.update(parent_manifest_sha256='0'*64)),True)
test('wrong parent controls binding','PARENT_CONTROLS_SHA256',lambda r:edit_seed(r,lambda d:d.update(parent_controls_sha256='0'*64)),True)
test('change base point','BASE_POINT',lambda r:edit_seed(r,lambda d:d.update(M=d['M']-1)),True)
test('inflate first17lower','BASE_VALUES',lambda r:edit_seed(r,lambda d:d.update(L17='1')),True)
test('inflate last lower','BASE_VALUES',lambda r:edit_seed(r,lambda d:d.update(L18='1')),True)
test('understate upper','BASE_VALUES',lambda r:edit_seed(r,lambda d:d.update(U='0')),True)
test('inflate extra lower','BASE_VALUES',lambda r:edit_seed(r,lambda d:d.update(e='1')),True)
test('understate last degree','DEGREES',lambda r:edit_seed(r,lambda d:d.update(degree18=1295)),True)
test('understate extra degree','DEGREES',lambda r:edit_seed(r,lambda d:d.update(degree_extra=689)),True)
test('zero step','STEP',lambda r:edit_seed(r,lambda d:d.update(k=0)),True)
test('nonpositive new fugacity','STEP',lambda r:edit_seed(r,lambda d:d.update(k=d['M'],new_M=0)),True)
test('inconsistent new point','NEW_POINT',lambda r:edit_seed(r,lambda d:d.update(new_M=d['new_M']-1)),True)
test('next grid point fails exact powers','BELOW_ONE',lambda r:edit_seed(r,lambda d:d.update(k=d['k']+1,new_M=d['new_M']-1)),True)
test('wrong claimed lower value','CLAIMED_VALUE',lambda r:edit_seed(r,lambda d:d.update(S='1')),True)
test('wrong reciprocal','CLAIMED_MU',lambda r:edit_seed(r,lambda d:d.update(mu='3')),True)
test('remove candidate label','STATUS',lambda r:edit_seed(r,lambda d:d.update(candidate_unrefereed=False)),True)
test('misrepresent coefficients','FAMILY_SCOPE',lambda r:edit_seed(r,lambda d:d.update(family='expanded coefficient vector')),True)
def future(r):
 p=r/'input/MANIFEST.json';d=json.loads(p.read_text());d['frozen_utc']='2100-01-01T00:00:00+00:00';dump(p,d)
test('future freeze','FREEZE_TIME',future)
test('malformed seed with hash rebound','SEED_JSON',lambda r:(r/'input/seed.json').write_text('{'),True)
pathlib.Path(a.receipt).write_text(json.dumps({'status':'PASS','input_manifest_sha256':sha(original/'input/MANIFEST.json'),'controls':records},indent=2)+'\n');print('PASS',len(records),'actual exact-code degree-power controls')
