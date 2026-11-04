"""Actual corruptions of the frozen span-degree extension, exact-code assertions."""
import pathlib,tempfile,shutil,json,hashlib,argparse
from verify_span_degree import check,Rejection
parser=argparse.ArgumentParser();parser.add_argument('artifact');parser.add_argument('receipt');args=parser.parse_args()
original=pathlib.Path(args.artifact).resolve();check(original)
seed=json.loads((original/'input/seed.json').read_text());base=(original/seed['main_relative_path']).resolve()
scratch=original.parent.parent/'tmp_controls';scratch.mkdir(exist_ok=True);results=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def edit_seed(r,fn):
 p=r/'input/seed.json';d=json.loads(p.read_text());fn(d);dump(p,d)
def test(name,code,edit,rehash=False):
 with tempfile.TemporaryDirectory(prefix='span_degree_',dir=scratch) as td:
  r=pathlib.Path(td)/'artifact';shutil.copytree(original,r)
  for q in r.rglob('*'):
   if q.is_file():q.chmod(0o644)
  edit(r)
  if rehash:
   p=r/'input/MANIFEST.json';m=json.loads(p.read_text());m['sha256']['seed.json']=sha(r/'input/seed.json');dump(p,m)
  try:check(r,base)
  except Rejection as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+code,(name,code,actual)
  results.append({'corruption':name,'expected':'REJECT:'+code,'actual':actual,'pass':True,'seed_hash_rebound':rehash})
test('alter verifier byte','INPUT_SHA256',lambda r:(r/'input/verify_span_degree.py').write_text((r/'input/verify_span_degree.py').read_text()+'\n'))
test('alter seed byte','INPUT_SHA256',lambda r:(r/'input/seed.json').write_text((r/'input/seed.json').read_text()+'\n'))
test('drop a span','SPAN_COVERAGE',lambda r:edit_seed(r,lambda d:d['spans'].pop()),True)
test('duplicate span','SPAN_ORDER',lambda r:edit_seed(r,lambda d:d['spans'][1].update(h=1)),True)
test('change width','WIDTH',lambda r:edit_seed(r,lambda d:d['spans'][0].update(w=40)),True)
test('understate degree','DEGREE',lambda r:edit_seed(r,lambda d:d['spans'][0].update(degree=40)),True)
test('inflate per-span lower value','ALPHA',lambda r:edit_seed(r,lambda d:d['spans'][0].update(alpha='1')),True)
test('change weighted sum','WEIGHTED_SUM',lambda r:edit_seed(r,lambda d:d.update(T='1')),True)
test('change base point','BASE_POINT',lambda r:edit_seed(r,lambda d:d.update(M=d['M']-1)),True)
test('zero step','STEP',lambda r:edit_seed(r,lambda d:d.update(k=0)),True)
test('inconsistent new point','NEW_POINT',lambda r:edit_seed(r,lambda d:d.update(new_M=d['new_M']-1)),True)
test('negative multiplier','NEGATIVE_MULTIPLIER',lambda r:edit_seed(r,lambda d:d.update(k=10000,new_M=d['M']-10000)),True)
test('next grid step fails linear bound','BELOW_ONE',lambda r:edit_seed(r,lambda d:d.update(k=d['k']+1,new_M=d['new_M']-1)),True)
test('false lower value','CLAIMED_VALUE',lambda r:edit_seed(r,lambda d:d.update(S='1')),True)
test('false reciprocal','CLAIMED_MU',lambda r:edit_seed(r,lambda d:d.update(mu='3')),True)
test('remove candidate status','STATUS',lambda r:edit_seed(r,lambda d:d.update(candidate_unrefereed=False)),True)
test('misrepresent coefficient family','FAMILY_SCOPE',lambda r:edit_seed(r,lambda d:d.update(family='expanded coefficients')),True)
test('change main binding','BASE_BINDING',lambda r:edit_seed(r,lambda d:d.update(main_packet_sha256='0'*64)),True)
test('change full replay receipt binding','BASE_FULL_SHA256',lambda r:edit_seed(r,lambda d:d.update(main_full_sha256='0'*64)),True)
def future(r):
 p=r/'input/MANIFEST.json';d=json.loads(p.read_text());d['frozen_utc']='2100-01-01T00:00:00+00:00';dump(p,d)
test('future freeze timestamp','FREEZE_TIME',future)
test('malformed seed with hash rebound','SEED_JSON',lambda r:(r/'input/seed.json').write_text('{'),True)
pathlib.Path(args.receipt).write_text(json.dumps({'status':'PASS','input_manifest_sha256':sha(original/'input/MANIFEST.json'),'controls':results},indent=2)+'\n')
print('PASS',len(results),'actual exact-code controls')
