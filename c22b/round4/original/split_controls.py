"""Exact expected rejections specific to split-radius caps, same agent."""
import pathlib,json,gzip,copy,sys,contextlib,io
from verify import Checker,Reject,check_bundle
P=pathlib.Path(sys.argv[1]);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);C=Checker(D);C.scalar();C.topology()
covers={p.stem[:-5]:json.loads(gzip.decompress(p.read_bytes())) for p in (P/'covers').glob('*.json.gz')}
rows=[]
def test(name,expected,fn):
 try:
  with contextlib.redirect_stderr(io.StringIO()):fn()
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 assert actual==expected,(name,expected,actual)
 rows.append({'corruption':name,'expected':expected,'actual':actual})
def cap_cover(change):
 d=copy.deepcopy(covers['lower_cap_pair_1_3']);change(d);C.cover(d,raw)
def artifact(change):
 d=copy.deepcopy(D);change(d);Checker(d).scalar()
test('omitted outer-connector/inner-semicircle cover','E_MISSING_COVER',lambda:check_bundle(raw,[d for k,d in covers.items() if k!='lower_cap_pair_1_3']))
test('false whole-square distance proof','E_CAP_PAIR_DISTANCE',lambda:cap_cover(lambda d:d.update(leaves=[['','mean']])) )
test('false short-arc exclusion for different-radius cap pieces','E_CAP_PAIR_METADATA',lambda:cap_cover(lambda d:d.update(leaves=[['','short_arc']])) )
test('wrong semicircle index','E_CAP_PAIR_INDEX',lambda:cap_cover(lambda d:d.update(k=2)))
test('inner connector substituted for outer connector','E_CAP_PAIR_INDEX',lambda:cap_cover(lambda d:d.update(j=0)))
test('unit inner connector radius','E_PARAMETER_RANGE',lambda:artifact(lambda d:d['parameters'].update(inner_cap_radius='1')))
test('inner connector too short for slab reduction','E_CAP_VERTICAL_SEPARATION',lambda:artifact(lambda d:d['parameters'].update(inner_cap_radius='8')))
test('missing inner connector radius','E_PARAMETER_SCHEMA',lambda:artifact(lambda d:d['parameters'].pop('inner_cap_radius')))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_SPLIT_CAP_REJECTIONS_PASS','controls':rows},indent=2))
