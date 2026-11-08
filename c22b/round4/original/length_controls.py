"""Exact expected rejection controls for the speed identity certificate."""
import pathlib,json,copy,sys
from fractions import Fraction as F
from verify_length_identity import check,Reject
P=pathlib.Path(sys.argv[1]);original=json.loads((P/'length_identity.json').read_text());rows=[]
def test(name,expected,mutate):
 d=copy.deepcopy(original);mutate(d)
 try:check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 if actual!=expected:raise AssertionError((name,expected,actual))
 rows.append({'corruption':name,'expected':expected,'actual':actual})
test('wrong identity kind','E_SPEED_KIND',lambda d:d.update(kind='numerical_speed'))
test('wrong construction binding','E_SPEED_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('wrong quadratic field relation','E_SPEED_RELATION',lambda d:d.update(quadratic_relation='1'))
test('missing signed radius row','E_SPEED_ROWS',lambda d:d['rows'].pop())
test('wrong signed radius','E_SPEED_RADII',lambda d:d['rows'][0].__setitem__('signed_radius','1'))
test('altered exact coefficient','E_SPEED_COEFFICIENT',lambda d:d['rows'][0]['coefficients'][0].__setitem__(0,str(F(d['rows'][0]['coefficients'][0][0])+1)))
test('altered exact mean','E_SPEED_MEAN',lambda d:d['rows'][0]['mean'].__setitem__(0,str(F(d['rows'][0]['mean'][0])+1)))
test('unexpected identity field','E_SPEED_SCHEMA',lambda d:d.update(trust_me=True))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_SPEED_REJECTIONS_PASS','controls':rows},indent=2))
