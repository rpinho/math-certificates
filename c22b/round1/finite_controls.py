import pathlib,json,copy,sys
from verify_finite import check
from verify import Reject
P=pathlib.Path(sys.argv[1]);original=json.loads((P/'finite_witness.json').read_text());rows=[]
def test(name,expected,mutate):
 d=copy.deepcopy(original);mutate(d)
 try:check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 if actual!=expected:raise AssertionError((name,expected,actual))
 rows.append({'corruption':name,'expected':expected,'actual':actual})
test('wrong artifact binding','E_FINITE_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('zero repetition count','E_FINITE_N',lambda d:d.update(n=0))
test('wrong finite crossing count','E_FINITE_CROSSINGS',lambda d:d.update(crossings=4644))
test('understated body coefficient','E_FINITE_COEFFICIENT',lambda d:d.update(coefficient_upper='7'))
test('understated cap length','E_FINITE_CAPS',lambda d:d.update(cap_length_upper='100'))
test('wrong target bar','E_FINITE_BAR',lambda d:d.update(bar='7'))
test('wrong exact length','E_FINITE_LENGTH',lambda d:d.update(length_upper_exact='1'))
test('wrong exact ratio','E_FINITE_RATIO',lambda d:d.update(ratio_upper_exact='1'))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_FINITE_REJECTIONS_PASS','controls':rows},indent=2))
