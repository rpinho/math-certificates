"""Exact expected semantic rejection controls on frozen inputs; same agent."""
import copy,json,pathlib,sys,contextlib,io,gzip,hashlib
from verify import Checker,Reject,check_bundle
P=pathlib.Path(sys.argv[1]);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);C=Checker(D);C.scalar();C.topology()
covers={p.name[:-8]:json.loads(gzip.decompress(p.read_bytes())) for p in (P/'covers').glob('*.json.gz')}
rows=[]
def run(name,expected,fn):
 try:
  with contextlib.redirect_stderr(io.StringIO()):fn()
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 if actual!=expected:raise AssertionError((name,expected,actual))
 rows.append({'corruption':name,'expected':expected,'actual':actual})
def artifact(name,expected,path,value):
 def f():
  d=copy.deepcopy(D);obj=d
  for key in path[:-1]:obj=obj[key]
  obj[path[-1]]=value;c=Checker(d);c.scalar();c.topology()
 run(name,expected,f)
def cover(name,expected,key,mutate):
 def f():
  d=copy.deepcopy(covers[key]);mutate(d);C.cover(d,raw)
 run(name,expected,f)
artifact('remove candidate qualification','E_STATUS',['status'],'proved')
artifact('wrong target bar','E_BAR',['claim','bar'],'721/100')
artifact('claim larger than target','E_CLAIM_BAR',['claim','coefficient'],'73/10')
artifact('length coefficient too small','E_LENGTH_COEFFICIENT',['claim','coefficient'],'7')
artifact('nonpositive N','E_N',['parameters','N'],0)
artifact('boolean N','E_N',['parameters','N'],True)
artifact('wrong crossing slope','E_CROSSING_FORMULA',['claim','crossings_slope'],1)
artifact('wrong crossing intercept','E_CROSSING_FORMULA',['claim','crossings_intercept'],0)
artifact('insufficient additive allowance','E_ADDITIVE_LENGTH',['claim','additive'],'100')
artifact('unit cap radius','E_PARAMETER_RANGE',['parameters','cap_radius'],'1')
artifact('zero inner satellite','E_PARAMETER_RANGE',['parameters','inner_radius'],'0')
artifact('scale below admitted domain','E_PARAMETER_RANGE',['parameters','scale'],'1/2')
artifact('unsafe enlarged outer satellite','E_CORE_TUBE',['parameters','outer_radius'],'2')
artifact('truncated phase domain','E_DOMAINS',['certificate_domains','body_phase'],['0','6'])
cover('changed construction digest','E_ARTIFACT_HASH','body_outer_0_0',lambda d:d.update(artifact_sha256='0'*64))
cover('duplicate binary leaf','E_DUPLICATE_OR_PREFIX','interface_0_1',lambda d:d['leaves'].append(d['leaves'][0]))
cover('missing binary leaf','E_COVER_GAP','interface_0_1',lambda d:d['leaves'].pop())
cover('nonbinary leaf address','E_PATH','interface_0_1',lambda d:d['leaves'][0].__setitem__(0,'2'))
cover('false short arc across different strands','E_SHORT_ARC_LEAF','interface_0_1',lambda d:d.update(leaves=[['','short_arc']]))
cover('false whole interface distance enclosure','E_DISTANCE_LEAF','interface_0_1',lambda d:d.update(leaves=[['','mean']]))
cover('false whole body distance enclosure','E_DISTANCE_LEAF','body_outer_0_0',lambda d:d.update(leaves=[['','mean']]))
cover('false whole curvature enclosure','E_CURVATURE_LEAF','curvature_inner_0_0',lambda d:d.update(leaves=[['','curvature']]))
cover('invalid strand index','E_COVER_INDEX','interface_0_1',lambda d:d.update(j=4))
cover('invented proof reason','E_LEAF_REASON','interface_0_1',lambda d:d['leaves'][0].__setitem__(1,'trust_me'))
run('omitted full interface certificate','E_MISSING_COVER',lambda:check_bundle(raw,[v for k,v in covers.items() if k!='interface_3_3']))
run('repeated full certificate','E_DUPLICATE_COVER',lambda:check_bundle(raw,[covers['interface_0_0'],covers['interface_0_0']]))
def bad_geometry():
 d=copy.deepcopy(D);d['parameters']['outer_radius']='4828403/2500000';changed=(json.dumps(d,indent=2)+'\n').encode();c=Checker(d);c.scalar();c.topology()
 cover=copy.deepcopy(covers['body_cross_0_0']);cover['artifact_sha256']=hashlib.sha256(changed).hexdigest();c.cover(cover,changed)
run('decreased outer radius with certificate rebound to changed bytes','E_DISTANCE_LEAF',bad_geometry)
if 'closure' in D:
 artifact('wrong closure mode','E_CLOSURE_MODE',['closure','upper'],'nested_semicircles')
 artifact('insufficient upper vertical clearance','E_UPPER_CLEARANCE',['closure','vertical_clearance'],'1')
 artifact('wrong component count','E_COMPONENT_COUNT',['claim','components'],2)
artifact('wrong exact core-period count','E_PERIODS',['parameters','core_periods'],4)
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_REJECTIONS_PASS','controls':rows},indent=2))
