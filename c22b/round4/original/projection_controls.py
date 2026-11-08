"""Exact expected rejection controls for the frozen physical braid certificate."""
import pathlib,json,gzip,copy,sys,contextlib,io
from verify_projection import check
from verify import Reject
P=pathlib.Path(sys.argv[1]);original=json.loads(gzip.decompress((P/'projection.json.gz').read_bytes()));rows=[]
def test(name,expected,mutate):
 d=copy.deepcopy(original);mutate(d)
 try:
  with contextlib.redirect_stderr(io.StringIO()):check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 if actual!=expected:raise AssertionError((name,expected,actual))
 rows.append({'corruption':name,'expected':expected,'actual':actual})
def first_root(d):
 return next(row for row in d['covers']['m'] if row[1]=='root')
test('wrong projection packet kind','E_PROJECTION_KIND',lambda d:d.update(kind='sampled_braid'))
test('remove candidate status','E_PROJECTION_STATUS',lambda d:d.update(status='proved'))
test('wrong construction binding','E_PROJECTION_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('change projection vector','E_PROJECTION_VECTOR',lambda d:d.update(projection=[1,0]))
test('degenerate inverse bracket','E_INVERSE_BRACKET',lambda d:d['inverse_brackets']['0'][0].__setitem__(1,d['inverse_brackets']['0'][0][0]))
test('inverse lower endpoint above root','E_INVERSE_LOWER',lambda d:d['inverse_brackets']['0'].__setitem__(0,['1','2']))
test('inverse upper endpoint below root','E_INVERSE_UPPER',lambda d:d['inverse_brackets']['0'].__setitem__(0,['-2','-1']))
test('missing required inverse witness','E_MISSING_INVERSE',lambda d:d['inverse_brackets'].pop('0'))
test('duplicate projection leaf','E_PROJECTION_DUPLICATE',lambda d:d['covers']['m'].append(d['covers']['m'][0]))
test('missing projection leaf','E_PROJECTION_COVER_GAP',lambda d:d['covers']['m'].pop())
def false_empty(d):
 row=first_root(d);row[:]=[row[0],'empty']
test('hide a proven crossing as empty','E_FALSE_EMPTY',false_empty)
def false_whole_root(d):
 bracket=first_root(d)[2];d['covers']['m']=[['','root',bracket]]
test('unjustified global root uniqueness','E_ROOT_DERIVATIVE',false_whole_root)
test('root interval outside leaf','E_ROOT_OUTSIDE_LEAF',lambda d:first_root(d).__setitem__(2,['-1','2']))
test('zero-width root interval','E_ROOT_INTERVAL',lambda d:first_root(d)[2].__setitem__(1,first_root(d)[2][0]))
test('stored crossing sign corrupted','E_WORD_MISMATCH',lambda d:d['word'].__setitem__(0,-d['word'][0]))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_PROJECTION_REJECTIONS_PASS','controls':rows},indent=2))
