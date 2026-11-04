"""Corrupt the actual sealed point packet; require each exact rejection code."""
import argparse,copy,hashlib,json,pathlib,shutil,tempfile,os
from verify_packet import check,Rejection
p=argparse.ArgumentParser();p.add_argument('packet');p.add_argument('receipt');p.add_argument('--binary');p.add_argument('--finite-binary');p.add_argument('--scratch');a=p.parse_args()
original=pathlib.Path(a.packet).resolve();base=original.parent
# The valid actual packet must first pass unchanged.
check(original)
frozen_ancestor=next((p for p in base.parents if p.name=='frozen'),None)
scratch=pathlib.Path(a.scratch).resolve() if a.scratch else ((frozen_ancestor.parent/'tmp_controls') if frozen_ancestor else base.parent/'c38_tmp_controls');scratch.mkdir(parents=True,exist_ok=True)
results=[]
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rebind(root,d):
 # Deliberately rebind all hashes in the temporary copy for semantic controls.
 for e in d['spans']:
  for role in ['production','separate']:e[role]['sha256']=sha(root/e[role]['path'])
 ip=root/d['frozen_input_manifest']['path'];im=load(ip)
 rp=root/d['frozen_replay_receipts']['path'];rr=load(rp);rr['spans']=rr['spans'][:len(d['spans'])]
 for e,r in zip(d['spans'],rr['spans']):
  sp=ip.parent/r['span_manifest_path'];sm=load(sp);sm['production_sha256']=e['production']['sha256'];dump(sp,sm)
  r['span_manifest_sha256']=sha(sp);r['input_sha256']=e['production']['sha256'];r['output_sha256']=e['separate']['sha256']
 for rel in im['sha256']:im['sha256'][rel]=sha(ip.parent/rel)
 dump(ip,im);d['frozen_input_manifest']['sha256']=sha(ip);rr['input_manifest_sha256']=sha(ip)
 dump(rp,rr);d['frozen_replay_receipts']['sha256']=sha(rp)
def mutate_data(root,d,role,fun,l=0):
 path=root/d['spans'][l][role]['path'];data=load(path);fun(data);dump(path,data)
def test(name,expected,edit,rehash=False,full=False):
 with tempfile.TemporaryDirectory(prefix='point_corruption_',dir=str(scratch)) as td:
  root=pathlib.Path(td)/'packet';shutil.copytree(base,root)
  for q in root.rglob('*'):
   if q.is_file():q.chmod(0o644)
  d=load(root/original.name);edit(root,d)
  if rehash:rebind(root,d)
  dump(root/original.name,d)
  try:
   check(root/original.name,full=full,binary=a.binary,work=pathlib.Path(td)/'fresh_replay' if full else None,finite_binary=a.finite_binary)
  except Rejection as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+expected,(name,expected,actual)
  results.append({'corruption':name,'expected':'REJECT:'+expected,'actual':actual,'pass':True,'all_hashes_rebound':rehash,'fresh_native_replay':full})
def edit_receipt(root,d,fun):
 p=root/d['frozen_replay_receipts']['path'];rr=load(p);fun(rr);dump(p,rr);d['frozen_replay_receipts']['sha256']=sha(p)
def edit_span_manifest(root,d,fun):
 rr=load(root/d['frozen_replay_receipts']['path']);p=(root/d['frozen_input_manifest']['path']).parent/rr['spans'][0]['span_manifest_path'];sm=load(p);fun(sm);dump(p,sm)
if load(original).get('terminal_span_mode')=='FINITE_LAST_SPAN_LOWER_ONLY':
 test('unbound finite last verifier source','FINITE_VERIFIER_SOURCE_UNPINNED',lambda r,d:d['source_sha256'].pop('verify_finite_strip.cpp'))
 test('finite last verifier source byte changed','SOURCE_SHA256',lambda r,d:(r/'verify_finite_strip.cpp').write_text((r/'verify_finite_strip.cpp').read_text()+'\n'))
 test('frozen finite native input source byte changed','FINITE_CORE_INPUT_SHA256',lambda r,d:(r/'input/finite/verify_finite_strip.cpp').write_text((r/'input/finite/verify_finite_strip.cpp').read_text()+'\n'))
 test('terminal mode changed','TERMINAL_MODE',lambda r,d:d.update(terminal_span_mode='FULL_WIDTH_CERTIFIED'))
 test('finite marker falsely claims infinite tail','FINITE_MODE',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(infinite_tail_certified=True),-1),True)
 test('finite marker has nonzero unused tail','FINITE_TAIL_MARKER',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(num_tail='1'),-1),True)
test('target numerator changed','TARGET_CHANGED',lambda r,d:d['target'].update(p=1052))
test('weaker dyadic point','TARGET_TOO_WEAK',lambda r,d:d.update(M=d['M']+1))
test('missing span','SPAN_COVERAGE',lambda r,d:d['spans'].pop())
test('duplicate span','SPAN_ORDER_OR_DUPLICATE',lambda r,d:d['spans'][1].update(l=1))
test('unbound verifier source','VERIFIER_SOURCE_UNPINNED',lambda r,d:d['source_sha256'].pop('verify_strip.cpp'))
test('verifier source byte changed','SOURCE_SHA256',lambda r,d:(r/'verify_strip.cpp').write_text((r/'verify_strip.cpp').read_text()+'\n'))
test('producer frozen byte changed','FROZEN_INPUT_SHA256',lambda r,d:(r/d['spans'][-1]['production']['path']).write_text((r/d['spans'][-1]['production']['path']).read_text()+'\n'))
test('separate replay byte changed','DATA_SHA256',lambda r,d:(r/d['spans'][-1]['separate']['path']).write_text((r/d['spans'][-1]['separate']['path']).read_text()+'\n'))
test('separate replay removed','DATA_MISSING',lambda r,d:(r/d['spans'][-1]['separate']['path']).unlink())
test('partial complete-replay receipt','RECEIPTS_INCOMPLETE',lambda r,d:edit_receipt(r,d,lambda x:x['spans'][0].update(status='PARTIAL')))
test('wrong per-span manifest path','SPAN_MANIFEST_PATH',lambda r,d:edit_receipt(r,d,lambda x:x['spans'][0].update(span_manifest_path='span_manifests/span_999.json')))
test('wrong per-span manifest hash','SPAN_MANIFEST_SHA256',lambda r,d:edit_receipt(r,d,lambda x:x['spans'][0].update(span_manifest_sha256='0'*64)))
test('wrong per-span source core binding','SPAN_CORE_BINDING',lambda r,d:edit_receipt(r,d,lambda x:x['spans'][0].update(core_manifest_sha256='0'*64)))
test('input declared frozen after replay with all hashes rebound','FREEZE_REPLAY_ORDER',lambda r,d:edit_span_manifest(r,d,lambda x:x.update(frozen_utc='2100-01-01T00:00:00+00:00')),True)
def corrupt_manifest_json(root,d):
 p=root/d['frozen_input_manifest']['path'];p.write_text('{');d['frozen_input_manifest']['sha256']=sha(p)
test('malformed frozen input manifest JSON','FROZEN_MANIFEST_JSON',corrupt_manifest_json)
test('malformed separate numerical JSON with hashes rebound','DATA_JSON',lambda r,d:(r/d['spans'][0]['separate']['path']).write_text('{'),True)
test('width metadata changed','WIDTH_METADATA',lambda r,d:d['spans'][0].update(w=d['spans'][0]['w']+1))
test('zero width','WIDTH',lambda r,d:d['spans'][0].update(w=0))
test('partial native verdict','REPLAY_INCOMPLETE',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(status='PARTIAL')),True)
test('wrong arithmetic scale','SCALE',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(S=95)),True)
test('negative tail numerator','NEGATIVE_NUMERATOR',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(num_tail='-1')),True)
def alter_producer(r,d):
 def f(x):
  q=next(e for e in x['x'] if e['Mnum']==d['M']);q['num_lo']=str(int(q['num_lo'])+1)
 mutate_data(r,d,'production',f,-1)
test('exact finite count changed and all hashes rebound','FINITE_NUMERATOR_MISMATCH',alter_producer,True)
test('graph state count changed','GRAPH_COUNT_MISMATCH',lambda r,d:mutate_data(r,d,'production',lambda x:x.update(total_states=x['total_states']+1)),True)
test('stage count sum corrupted','STAGE_COUNT_SUM',lambda r,d:mutate_data(r,d,'separate',lambda x:x['stage_sizes'].__setitem__(0,x['stage_sizes'][0]+1)),True)
test('degree bound reduced','DEGREE_BOUND',lambda r,d:d.update(max_degree=d['max_degree']-1))
test('claimed rational sum changed','CLAIMED_SUM_MISMATCH',lambda r,d:d.update(P_lower='2'))
test('expanded coefficient scope misrepresented','COEFFICIENT_ENCODING',lambda r,d:d.update(coefficient_encoding='expanded integer coefficients verified'))
test('candidate status removed','STATUS_LABEL',lambda r,d:d.update(candidate_unrefereed=False))
if a.binary:
 test('actual tail changed with rebound hashes and fresh native replay','FULL_REPLAY_MISMATCH',lambda r,d:mutate_data(r,d,'separate',lambda x:x.update(num_tail='0')),True,True)
pathlib.Path(a.receipt).write_text(json.dumps({'status':'PASS','packet_sha256':sha(original),'controls':results},indent=2)+'\n');print('PASS',len(results),'actual packet controls with exact rejections')
