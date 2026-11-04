import pathlib,json,copy,sys
from verify_contact import check
from verify import Reject
P=pathlib.Path(sys.argv[1]);original=json.loads((P/'CONTACT.json').read_text());rows=[]
def test(name,expected,change):
 d=copy.deepcopy(original);change(d)
 try:check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 assert actual==expected,(name,expected,actual)
 rows.append({'corruption':name,'expected':expected,'actual':actual})
test('wrong contact construction binding','E_CONTACT_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('invalid strand','E_CONTACT_INDEX',lambda d:d.update(indices=[4,1]))
test('phase outside finite body','E_CONTACT_PHASE',lambda d:d.update(phases=['1','-2']))
test('coincident selected points','E_CONTACT_DEGENERATE',lambda d:d.update(indices=[0,0],phases=['-1','-1']))
test('understated radius upper bound','E_CONTACT_UPPER',lambda d:d.update(radius_upper='1'))
test('valid margin falsely labelled a counterexample','E_CONTACT_FALSE_MARGIN',lambda d:d.update(false_margin_scale='19999/20000'))
test('boolean tangent index','E_CONTACT_TANGENT',lambda d:d.update(tangent_index=True))
test('different lower reach binding','E_CONTACT_LOWER_BINDING',lambda d:d.update(radius_lower='2'))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_CONTACT_REJECTIONS_PASS','controls':rows},indent=2))
