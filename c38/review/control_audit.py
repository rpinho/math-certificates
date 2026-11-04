"""Reproduce the literal and final-source controls from retained data only."""
import hashlib
import json
import pathlib
from fractions import Fraction as Q

root=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def finite(r):return Q(int(r['finite_numerator']),1<<r['finite_denominator_exponent'])
pod=root/'results/pod'
b=Q(51081913,1<<27)
span1=read(pod/'final_source_b1.json')
assert finite(span1)==b+2*sum((b**n for n in range(2,span1['width']+1)),Q(0))
old=read(pod/'b1.json')
for key in ['finite_numerator','finite_denominator_exponent','tail_numerator','tail_denominator_exponent']:
    assert old[key]==span1[key]
assert read(pod/'final_source_count10.json')['bridge_counts']==read(pod/'count10.json')['bridge_counts']
literal=read(root/'results/LITERAL_RECTANGLE.json')
assert literal['N']==25
value=sum((a*b**n for n,h,_,a in literal['rows'] if 3<=h<=5),Q(0))
checks=[]
for name in ['rectangle_control.json','rectangle_control_fast.json','rectangle_control_final.json']:
    r=read(pod/name)
    assert [r[k] for k in ['W','minspan','maxspan','cap']]==[4,3,5,3]
    assert Q(int(r['num_lo']),1<<r['scale'])<=value<=Q(int(r['num_hi']),1<<r['scale'])
    checks.append(name)
producer=read(root.parent/'c38/frozen/rectangle_point/component_control/replay.json')
assert [producer[k] for k in ['W','span_min','span_max','crossing_cap']]==[4,3,5,3]
assert Q(int(producer['num_lo']),1<<96)<=value<=Q(int(producer['num_hi']),1<<96)
record={'status':'PASS','literal_prefixes':literal['prefixes'],'exact_rectangle_value':str(value),
        'rectangle_controls':checks,'producer_control_encloses_literal_value':True,
        'span1_closed_form':True,'final_span10_coefficients_match':True,
        'current_source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                                 for name in ['independent_tm.cpp','independent_rectangle.cpp']}}
(root/'results/CONTROL_AUDIT.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS: literal rectangle, span-1 closed form, final-source controls')
