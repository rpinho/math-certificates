"""Actual component-artifact corruptions for the extension gap verifier."""
import pathlib,tempfile,shutil,json,argparse,hashlib
from verify_extension_gap import check,Reject
a=argparse.ArgumentParser();a.add_argument('stop');a.add_argument('point');a.add_argument('output');p=a.parse_args();stop=pathlib.Path(p.stop).resolve();point=pathlib.Path(p.point).resolve();valid=check(stop,point)
ancestor=next(x for x in point.parents if x.name=='frozen');scratch=ancestor.parent/'tmp_controls';scratch.mkdir(exist_ok=True);results=[]
def change(file,fn):
 d=json.loads(file.read_text());fn(d);file.write_text(json.dumps(d,indent=2)+'\n')
def test(name,expected,edit):
 with tempfile.TemporaryDirectory(prefix='extension_gap_',dir=str(scratch)) as td:
  s=pathlib.Path(td)/'stop';r=pathlib.Path(td)/'point';shutil.copytree(stop,s);shutil.copytree(point,r)
  for root in [s,r]:
   for q in root.rglob('*'):
    if q.is_file():q.chmod(0o644)
  edit(s,r)
  try:check(s,r)
  except Reject as e:actual='REJECT:'+str(e)
  else:actual='ACCEPTED'
  assert actual=='REJECT:'+expected,(name,expected,actual)
  results.append({'corruption':name,'expected':'REJECT:'+expected,'actual':actual,'pass':True})
test('span17 producer byte changed','STOP_FROZEN_INPUT_SHA256',lambda s,r:(s/'input/production/span_17.json').write_text((s/'input/production/span_17.json').read_text()+'\n'))
test('point search byte changed','POINT_INPUT_SHA256',lambda s,r:(r/'input/search.json').write_text((r/'input/search.json').read_text()+'\n'))
test('overlapping span scope','DISJOINT_SPAN_SCOPE',lambda s,r:change(r/'input/MANIFEST.json',lambda d:d['parameters'].update(span_min=17)))
test('span17 standard full replay missing','STOP_FULL_INCOMPLETE',lambda s,r:change(s/'FULL_ACCEPTANCE.json',lambda d:d.update(fresh_full_replay=False)))
test('point controls incomplete','POINT_CONTROLS_INCOMPLETE',lambda s,r:change(r/'REJECTION_CONTROLS.json',lambda d:d.update(status='PARTIAL')))
pathlib.Path(p.output).write_text(json.dumps({'status':'PASS','span17_input_manifest_sha256':valid['span17_input_manifest_sha256'],'point_input_manifest_sha256':valid['point_input_manifest_sha256'],'control_source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'controls':results},indent=2)+'\n');print('PASS',len(results),'actual extension comparison controls')
