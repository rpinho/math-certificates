"""Actual exact-code corruptions of the disjoint-family extension input."""
import argparse,pathlib,json,tempfile,shutil,hashlib
from verify_disjoint_extension import check,Rejection
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args();original=pathlib.Path(a.artifact).resolve();check(original)
seed=json.loads((original/'input/seed.json').read_text());locations={n:(original/seed[n+'_relative']).resolve() for n in ['secant','point22','point23']};scratch=original.parent.parent/'tmp_controls';scratch.mkdir(exist_ok=True);records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def edit_seed(r,fn):p=r/'input/seed.json';d=json.loads(p.read_text());fn(d);dump(p,d)
def test(name,expected,edit,rehash=False):
 with tempfile.TemporaryDirectory(prefix='disjoint_',dir=scratch) as td:
  r=pathlib.Path(td)/'artifact';shutil.copytree(original,r)
  for q in r.rglob('*'):
   if q.is_file():q.chmod(0o644)
  edit(r)
  if rehash:
   p=r/'input/MANIFEST.json';m=json.loads(p.read_text());m['sha256']['seed.json']=sha(r/'input/seed.json');dump(p,m)
  try:check(r,locations)
  except Rejection as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+expected,(name,expected,actual)
  records.append({'corruption':name,'expected':'REJECT:'+expected,'actual':actual,'pass':True,'seed_hash_rebound':rehash})
test('change verifier byte','INPUT_SHA256',lambda r:(r/'input/verify_disjoint_extension.py').write_text((r/'input/verify_disjoint_extension.py').read_text()+'\n'))
test('change scalar checker byte','INPUT_SHA256',lambda r:(r/'input/verify_rectangle_point_packet.py').write_text((r/'input/verify_rectangle_point_packet.py').read_text()+'\n'))
test('change seed byte','INPUT_SHA256',lambda r:(r/'input/seed.json').write_text((r/'input/seed.json').read_text()+'\n'))
test('wrong secant binding','SECANT_BINDING',lambda r:edit_seed(r,lambda d:d.update(secant_manifest_sha256='0'*64)),True)
test('wrong secant seed binding','SECANT_SEED_SHA256',lambda r:edit_seed(r,lambda d:d.update(secant_seed_sha256='0'*64)),True)
test('wrong width22 input binding','POINT_INPUT_SHA256',lambda r:edit_seed(r,lambda d:d.update(point22_manifest_sha256='0'*64)),True)
test('wrong width23 input binding','POINT_INPUT_SHA256',lambda r:edit_seed(r,lambda d:d.update(point23_manifest_sha256='0'*64)),True)
test('wrong width22 controls binding','POINT_CONTROLS_SHA256',lambda r:edit_seed(r,lambda d:d.update(point22_controls_sha256='0'*64)),True)
test('wrong width23 controls binding','POINT_CONTROLS_SHA256',lambda r:edit_seed(r,lambda d:d.update(point23_controls_sha256='0'*64)),True)
test('change base point','BASE_POINT',lambda r:edit_seed(r,lambda d:d.update(M=d['M']-1)),True)
test('inflate width22 lower','POINT_VALUES',lambda r:edit_seed(r,lambda d:d.update(lower22='1')),True)
test('understate width23 upper','POINT_VALUES',lambda r:edit_seed(r,lambda d:d.update(upper23='0')),True)
test('inflate extra lower','EXTRA_LOWER',lambda r:edit_seed(r,lambda d:d.update(extra_lower='1')),True)
test('include overlapping span18','EXTRA_FAMILY',lambda r:edit_seed(r,lambda d:d.update(extra_span_min=18)),True)
test('change extra range','EXTRA_FAMILY',lambda r:edit_seed(r,lambda d:d.update(extra_range=23)),True)
test('change crossing cap','EXTRA_FAMILY',lambda r:edit_seed(r,lambda d:d.update(extra_crossing_cap=7)),True)
test('understate extra degree','EXTRA_DEGREE',lambda r:edit_seed(r,lambda d:d.update(extra_degree=689)),True)
test('zero step','STEP',lambda r:edit_seed(r,lambda d:d.update(k=0)),True)
test('inconsistent new point','NEW_POINT',lambda r:edit_seed(r,lambda d:d.update(new_M=d['new_M']-1)),True)
test('negative multiplier','NEGATIVE_MULTIPLIER',lambda r:edit_seed(r,lambda d:d.update(k=40000,new_M=d['M']-40000)),True)
test('next grid point fails exact bound','BELOW_ONE',lambda r:edit_seed(r,lambda d:d.update(k=d['k']+1,new_M=d['new_M']-1)),True)
test('wrong claimed value','CLAIMED_VALUE',lambda r:edit_seed(r,lambda d:d.update(S='1')),True)
test('wrong reciprocal','CLAIMED_MU',lambda r:edit_seed(r,lambda d:d.update(mu='3')),True)
test('remove candidate status','STATUS',lambda r:edit_seed(r,lambda d:d.update(candidate_unrefereed=False)),True)
test('misrepresent coefficient expansion','FAMILY_SCOPE',lambda r:edit_seed(r,lambda d:d.update(family='full expanded vector')),True)
def future(r):
 p=r/'input/MANIFEST.json';d=json.loads(p.read_text());d['frozen_utc']='2100-01-01T00:00:00+00:00';dump(p,d)
test('future freeze','FREEZE_TIME',future)
test('malformed seed with hash rebound','SEED_JSON',lambda r:(r/'input/seed.json').write_text('{'),True)
pathlib.Path(a.receipt).write_text(json.dumps({'status':'PASS','input_manifest_sha256':sha(original/'input/MANIFEST.json'),'controls':records},indent=2)+'\n');print('PASS',len(records),'actual exact-code disjoint controls')
