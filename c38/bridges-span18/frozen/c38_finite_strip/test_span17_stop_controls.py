"""Exact expected rejections on the actual two-point span17 stop artifact."""
import pathlib,tempfile,shutil,json,hashlib,argparse
from verify_span17_stop import check,Reject
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');p.add_argument('--binary');p.add_argument('--scratch');a=p.parse_args();original=pathlib.Path(a.artifact).resolve();check(original)
ancestor=next((p for p in original.parents if p.name=='frozen'),None);scratch=pathlib.Path(a.scratch) if a.scratch else (ancestor.parent/'tmp_controls' if ancestor else original.parent/'c38_tmp_controls');scratch.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def rebind(root):
 mp=root/'input/INPUT_MANIFEST.json';m=load(mp)
 for folder in ['replay','replay_public']:
  rp=root/folder/'RECEIPTS.json';rr=load(rp)
  for rec in rr['spans']:
   smp=root/'input'/rec['span_manifest_path'];sm=load(smp);sm['production_sha256']=sha(root/'input'/sm['production_path']);dump(smp,sm);rec['span_manifest_sha256']=sha(smp);rec['input_sha256']=sm['production_sha256'];rec['output_sha256']=sha(root/folder/('span_%d.json'%rec['l']))
  dump(rp,rr)
 for rel in m['sha256']:m['sha256'][rel]=sha(root/'input'/rel)
 dump(mp,m)
 for folder in ['replay','replay_public']:
  p=root/folder/'RECEIPTS.json';rr=load(p);rr['input_manifest_sha256']=sha(mp);dump(p,rr)
def jsonchange(root,file,fun):
 p=root/file;d=load(p);fun(d);dump(p,d)
results=[]
def test(name,expected,edit,rehash=False,full=False):
 with tempfile.TemporaryDirectory(prefix='span17_stop_corruption_',dir=str(scratch)) as td:
  root=pathlib.Path(td)/'artifact';shutil.copytree(original,root)
  for p in root.rglob('*'):
   if p.is_file():p.chmod(0o644)
  edit(root)
  if rehash:rebind(root)
  try:check(root,full,a.binary,pathlib.Path(td)/'fresh' if full else None)
  except Reject as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+expected,(name,expected,actual)
  results.append({'corruption':name,'expected':'REJECT:'+expected,'actual':actual,'pass':True,'rebound_hashes':rehash,'fresh_native_replay':full})
test('producer frozen byte changed','FROZEN_INPUT_SHA256',lambda r:(r/'input/production/span_17.json').write_text((r/'input/production/span_17.json').read_text()+'\n'))
test('auxiliary point changed','FUGACITY',lambda r:jsonchange(r,'replay_public/RECEIPTS.json',lambda d:d.update(M=51081913)))
test('auxiliary span removed','COVERAGE',lambda r:jsonchange(r,'replay_public/RECEIPTS.json',lambda d:d['spans'].pop()))
test('auxiliary replay marked partial','REPLAY_INCOMPLETE',lambda r:jsonchange(r,'replay_public/RECEIPTS.json',lambda d:d['spans'][0].update(status='PARTIAL')))
test('auxiliary replay byte changed','RECEIPT_SHA256',lambda r:(r/'replay_public/span_1.json').write_text((r/'replay_public/span_1.json').read_text()+'\n'))
test('auxiliary finite count changed with hashes rebound','FINITE_NUMERATOR_MISMATCH',lambda r:jsonchange(r,'replay_public/span_1.json',lambda d:d.update(num_lo=str(int(d['num_lo'])+1))),True)
test('negative auxiliary tail with hashes rebound','BRACKET',lambda r:jsonchange(r,'replay_public/span_1.json',lambda d:d.update(num_tail='-1')),True)
test('incomplete native auxiliary verdict','NATIVE_REPLAY_INCOMPLETE',lambda r:jsonchange(r,'replay_public/span_1.json',lambda d:d.update(status='PARTIAL')),True)
test('stage count changed with hashes rebound','STAGE_SIZES',lambda r:jsonchange(r,'replay_public/span_1.json',lambda d:d['stage_sizes'].__setitem__(0,d['stage_sizes'][0]+1)),True)
test('input frozen after replay with hashes rebound','FREEZE_REPLAY_ORDER',lambda r:jsonchange(r,'input/span_manifests/span_1.json',lambda d:d.update(frozen_utc='2100-01-01T00:00:00+00:00')),True)
if a.binary:test('auxiliary tail changed with fresh native replay','FULL_REPLAY_MISMATCH',lambda r:jsonchange(r,'replay_public/span_1.json',lambda d:d.update(num_tail='0')),True,True)
pathlib.Path(a.receipt).write_text(json.dumps({'status':'PASS','input_manifest_sha256':sha(original/'input/INPUT_MANIFEST.json'),'controls':results},indent=2)+'\n');print('PASS',len(results),'actual span17 stop controls')
