"""Run every exact expected corruption in one process on frozen inputs."""
import pathlib,json,sys,runpy,io,contextlib,copy
import verify_manifest,verify_all,verify
P=pathlib.Path(sys.argv[1]).resolve();groups=[]
for script,expected in [('controls.py',31),('projection_controls.py',15),('length_controls.py',8),('diagram_controls.py',7),('margin_controls.py',6),('finite_controls.py',8),('split_controls.py',8),('ropelength_controls.py',12),('contact_controls.py',8)]:
 old=sys.argv;sys.argv=[str(P/script),str(P)];out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):runpy.run_path(str(P/script),run_name='__main__')
 finally:sys.argv=old
 data=json.loads(out.getvalue());rows=data['controls'];assert len(rows)==expected,(script,len(rows),expected)
 groups.append({'script':script,'controls':rows})
rows=verify_manifest.controls(P)
try:verify_manifest.check(P,{'covers/MANIFEST.json':b'not exempt'})
except verify_manifest.Reject as e:
 actual=str(e);assert actual=='E_FILE_SET',actual
else:raise AssertionError('NESTED_EXTRA_ACCEPTED')
rows.append({'corruption':'nested extra file with reserved basename','expected':'E_FILE_SET','actual':actual});groups.append({'script':'verify_manifest.py','controls':rows})
D=json.loads((P/'CONSTRUCTION.json').read_text());packet=json.loads((P/'diagrams.json').read_text());packet['cases'][0]['repeat']+=2;packet['cases'][0]['crossings']+=2
try:verify_all.diagram_binding(D,packet)
except verify.Reject as e:
 actual=str(e);assert actual=='E_DIAGRAM_BINDING',actual
else:raise AssertionError('WRONG_DIAGRAM_BINDING_ACCEPTED')
groups.append({'script':'verify_all.py','controls':[{'corruption':'valid diagram of the wrong finite knot','expected':'E_DIAGRAM_BINDING','actual':actual}]})
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_CORRUPTION_REJECTIONS_PASS','total_controls':sum(len(g['controls']) for g in groups),'groups':groups},indent=2))
