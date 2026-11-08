"""Each corruption must produce its exact expected semantic rejection."""
import json,pathlib,copy
from verify_diagram import check,Reject
P=pathlib.Path(__file__).resolve().parent
original=json.loads((P/'diagrams.json').read_text())
assert len(check(original))==3
tests=[]
def case(name,expected,mutate):
    d=copy.deepcopy(original);mutate(d)
    try:check(d)
    except Reject as e:
        actual=str(e)
        if actual!=expected:raise AssertionError((name,expected,actual))
    else:raise AssertionError((name,'CORRUPTION_ACCEPTED'))
    tests.append({'corruption':name,'expected':expected,'actual':actual,'pass':True})
def flip_one(d):
    c=d['cases'][0];c['word']=c['word']*c['repeat'];c['repeat']=1;c['word'][0]*=-1
case('reverse exactly one crossing','E_NOT_ALTERNATING',flip_one)
case('fake crossing count','E_CROSSING_COUNT',lambda d:d['cases'][0].__setitem__('crossings',5))
case('nugatory one-crossing closure','E_NUGATORY',lambda d:d['cases'].__setitem__(0,{'m':2,'word':[1],'repeat':1,'crossings':1}))
case('generator outside lanes','E_GENERATOR_RANGE',lambda d:d['cases'][0]['word'].__setitem__(0,4))
case('boolean masquerading as integer','E_INTEGER',lambda d:d['cases'][0].__setitem__('repeat',True))
case('empty collection','E_EMPTY_CASES',lambda d:d.__setitem__('cases',[]))
case('unsupported packet kind','E_PACKET_KIND',lambda d:d.__setitem__('kind','geometric_thickness_certificate'))
print(json.dumps({'verdict':'ALL_EXACT_EXPECTED_REJECTIONS_PASS','controls':tests},indent=2))
