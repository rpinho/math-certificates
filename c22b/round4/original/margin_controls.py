import pathlib,json,copy,sys,hashlib,contextlib,io
from fractions import Fraction as F
from verify_margin import check
from verify import Reject
P=pathlib.Path(sys.argv[1]);original=json.loads((P/'margin.json').read_text());rows=[]
def test(name,expected,mutate):
 d=copy.deepcopy(original);mutate(d)
 try:
  with contextlib.redirect_stderr(io.StringIO()):check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 if actual!=expected:raise AssertionError((name,expected,actual))
 rows.append({'corruption':name,'expected':expected,'actual':actual})
test('wrong original artifact binding','E_MARGIN_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('expansion instead of shrink','E_MARGIN_FACTOR',lambda d:d.update(scale_down='2'))
test('wrong reciprocal thickness','E_MARGIN_RECIPROCAL',lambda d:d.update(original_thickness_lower='2'))
test('wrong transformed artifact hash','E_MARGIN_TRANSFORM_HASH',lambda d:d.update(scaled_artifact_sha256='0'*64))
test('wrong margin certificate kind','E_MARGIN_KIND',lambda d:d.update(kind='sampled_margin'))
def consistent_false_margin(d):
 rho=F(json.loads((P/'CONTACT.json').read_text())['false_margin_scale'])
 D=json.loads((P/'CONSTRUCTION.json').read_text())
 for key in ['scale','cap_radius','inner_cap_radius']:D['parameters'][key]=str(F(D['parameters'][key])*rho)
 D['closure']['vertical_clearance']=str(F(D['closure']['vertical_clearance'])*rho)
 changed=(json.dumps(D,indent=2)+'\n').encode()
 d.update(scale_down=str(rho),original_thickness_lower=str(1/rho),scaled_artifact_sha256=hashlib.sha256(changed).hexdigest())
test('overstated margin with consistent reciprocal and transformed hash','E_DISTANCE_LEAF',consistent_false_margin)
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_MARGIN_REJECTIONS_PASS','controls':rows},indent=2))
