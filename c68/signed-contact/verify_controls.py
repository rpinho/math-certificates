"""Negative acceptance controls, on copies of the frozen inputs."""
import copy,json,tempfile,pathlib,contextlib,io
from fractions import Fraction as F
from flint import ctx
from verify_measure import run
from verify_signed_cover import verify
ctx.prec=160
cert=json.loads(pathlib.Path('certificate-44685.json').read_text());cover=json.loads(pathlib.Path('signed-cover.json').read_text())
controls=[]
for label,change in [
 ('unsupported model',lambda d:d.update(model='other')),
 ('unsupported constant',lambda d:d.update(zeta='1/10')),
 ('negative weight',lambda d:d['weights'].__setitem__(1,'-1')),
 ('mass mismatch',lambda d:d['weights'].__setitem__(1,str(F(d['weights'][1])+F(1,1000)))),
 ('mismatched lengths',lambda d:d['nodes'].pop()),
 ('wrong first node',lambda d:d['nodes'].__setitem__(0,'1/8')),
 ('wrong tail coverage',lambda d:d['tail_partition'].__setitem__(0,'1/2')),
 ('invalid tail interval',lambda d:d.update(second_tail_a='9999/10000',second_tail_b='999/1000')),
]:
 d=copy.deepcopy(cert);change(d);controls.append((label,d,run))
for label,change in [
 ('scalar wrong root',lambda d:d['root'].__setitem__(0,'1/1000')),
 ('scalar false S leaf',lambda d:d.update(tree={'kind':'S'})),
 ('scalar false small leaf',lambda d:d.update(tree={'kind':'small'})),
 ('scalar endpoint split',lambda d:d['tree'].update(mid='0')),
]:
 d=copy.deepcopy(cover);change(d);controls.append((label,d,verify))
results=[]
with tempfile.TemporaryDirectory(dir='.') as td:
 for j,(label,d,fn) in enumerate(controls):
  path=pathlib.Path(td)/f'control-{j}.json';path.write_text(json.dumps(d))
  try:fn(path)
  except (AssertionError,ValueError,ArithmeticError) as e:results.append(dict(control=label,status='REJECTED',reason=str(e)[:100]))
  else:raise RuntimeError(('CORRUPTED INPUT ACCEPTED',label))
print(json.dumps(results,indent=2));pathlib.Path('controls-results.json').write_text(json.dumps(results,indent=2)+'\n')
