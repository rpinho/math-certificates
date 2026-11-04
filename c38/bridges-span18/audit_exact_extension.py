"""Read-only final consistency audit; mathematical verification stays in the frozen checker."""
import argparse,pathlib,json,hashlib,datetime,importlib.util,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('output');a=p.parse_args();root=pathlib.Path(a.artifact).resolve();fr=root/'input';manifest=fr/'MANIFEST.json';m=json.loads(manifest.read_text())
cases={'c38_secant_rescale':('verify_secant_rescale.py',22),'c38_disjoint_extension':('verify_disjoint_extension.py',27),'c38_power_secant':('verify_power_secant.py',22)}
source,count=cases[root.name];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(fr/source)==m['sha256'][source]
spec=importlib.util.spec_from_file_location('final_exact_extension',fr/source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert datetime.datetime.fromisoformat(m['frozen_utc'])<=datetime.datetime.fromisoformat(started)
result=mod.check(root);stored=json.loads((root/'VERIFIED.json').read_text());assert result==stored
verified=datetime.datetime.now(datetime.timezone.utc).isoformat()
controls=json.loads((root/'REJECTION_CONTROLS.json').read_text());assert controls['status']=='PASS' and len(controls['controls'])==count and controls['input_manifest_sha256']==sha(manifest)
assert all(c['pass'] is True and c['actual']==c['expected'] and c['expected'].startswith('REJECT:') for c in controls['controls'])
fresh_controls=pathlib.Path(a.output).with_suffix('.controls.json').resolve()
test_source={'c38_secant_rescale':'test_secant_controls.py','c38_disjoint_extension':'test_disjoint_controls.py','c38_power_secant':'test_power_controls.py'}[root.name]
assert sha(fr/test_source)==m['sha256'][test_source]
subprocess.run([sys.executable,str(fr/test_source),str(root),str(fresh_controls)],check=True)
assert json.loads(fresh_controls.read_text())==controls
controls_completed=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert datetime.datetime.fromisoformat(started)<=datetime.datetime.fromisoformat(verified)<=datetime.datetime.fromisoformat(controls_completed)
files=[manifest,fr/'seed.json',root/'VERIFIED.json',root/'REJECTION_CONTROLS.json'];pod=[]
if (root/'POD_VERIFIED.json').exists():
 assert json.loads((root/'POD_VERIFIED.json').read_text())==result;files.append(root/'POD_VERIFIED.json');pod.append('copied-pod exact checker receipt matches')
if (root/'POD_REJECTION_CONTROLS.json').exists():
 pc=json.loads((root/'POD_REJECTION_CONTROLS.json').read_text());assert pc==controls;files.append(root/'POD_REJECTION_CONTROLS.json');pod.append('copied-pod actual corruption controls match')
out={'status':'PASS_COMPLETED_EXACT_EXTENSION','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_unrefereed':True,'verifier':'separately written (same agent), frozen source','mu':result['mu'],'input_manifest_sha256':sha(manifest),'actual_exact_rejection_controls':count,'fresh_verification_started_utc':started,'fresh_verification_completed_utc':verified,'fresh_actual_controls_completed_utc':controls_completed,'fresh_controls_sha256':sha(fresh_controls),'freeze_before_verification_before_controls':True,'chronology_evidence':'actual ordered fresh audit calls with embedded UTC times; filesystem mtimes are not used because rsync rounds subsecond timestamps','copied_pod_checks':pod,'sha256':{str(q.relative_to(root)):sha(q) for q in files},'full_expanded_integer_coefficient_vector_materialized':False}
pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['mu'],count)
