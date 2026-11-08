import pathlib,json,copy,sys
from verify_ropelength import check
from verify import Reject
P=pathlib.Path(sys.argv[1]);original=json.loads((P/'ROP_BOUND.json').read_text());rows=[]
def test(name,expected,change):
 d=copy.deepcopy(original);change(d)
 try:check(P,d)
 except Reject as e:actual=str(e)
 else:actual='ACCEPTED'
 assert actual==expected,(name,expected,actual)
 rows.append({'corruption':name,'expected':expected,'actual':actual})
test('wrong corollary kind','E_ROP_KIND',lambda d:d.update(kind='sampled_claim'))
test('remove candidate qualification','E_ROP_STATUS',lambda d:d.update(status='proved'))
test('extra schema field','E_ROP_SCHEMA',lambda d:d.update(trust_me=True))
test('wrong construction binding','E_ROP_HASH',lambda d:d.update(artifact_sha256='0'*64))
test('wrong physical coefficient','E_ROP_PHYSICAL_BINDING',lambda d:d.update(physical_coefficient='7'))
test('wrong thickness lower bound','E_ROP_THICKNESS_BINDING',lambda d:d.update(thickness_lower='2'))
test('wrong exact limit','E_ROP_LIMIT',lambda d:d.update(exact_limit_upper='7'))
test('wrong exact additive','E_ROP_ADDITIVE',lambda d:d.update(exact_additive_upper='1'))
test('understated final upper bound','E_ROP_CLAIM',lambda d:d.update(claimed_upper='7'))
test('claim above frozen bar','E_ROP_BAR',lambda d:d.update(claimed_upper='73/10'))
test('wrong finite ropelength ratio','E_ROP_FINITE',lambda d:d.update(finite_ratio_upper='1'))
test('wrong target bar','E_ROP_BAR',lambda d:d.update(bar='7'))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_ROPELENGTH_REJECTIONS_PASS','controls':rows},indent=2))
