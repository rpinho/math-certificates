"""Exact comparisons of every completed extra referee run, with explicit coverage."""
import json
import pathlib
import sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(500000)
ROOT=pathlib.Path(__file__).resolve().parent
DATA=ROOT/'results/pod'
BASE=ROOT.parent/'c38/frozen'
def read(p):return json.loads(p.read_text())
def claim(h,name):
    folder='c38_finite_strip/replay' if name=='b' else 'span17_all_length_stop/replay_public'
    return read(BASE/folder/f'span_{h}.json')
def endpoints(row):
    if 'finite_numerator' in row:
        low=high=Q(int(row['finite_numerator']),1<<row['finite_denominator_exponent'])
        tail=Q(int(row['tail_numerator']),1<<row['tail_denominator_exponent'])
    else:
        low=Q(int(row['num_lo']),1<<row['scale'])
        high=Q(int(row['num_hi']),1<<row['scale'])
        tail=Q(int(row['num_tail']),1<<row['scale'])
    return low,high,tail
result={'main':[],'isolated_points':[],'rectangles':[]}
for h in range(11,16):
    for name in ['b','c']:
        p=DATA/f'{name}{h}.json' if h<=12 else DATA/f'{name}{h}_interval.json'
        if not p.exists():continue
        own=read(p);lo,hi,tail=endpoints(own)
        claimed=claim(h,name)
        assert own['span']==h and own['width']==claimed['w'] and own['M']==claimed['M']
        clo=Q(int(claimed['num_lo']),1<<96);chi=Q(int(claimed['num_hi']),1<<96)
        assert clo<=lo<=hi<=chi
        assert hi+tail<=chi+Q(int(claimed['num_tail']),1<<96)
        result['isolated_points'].append({'h':h,'point':name,'finite_and_full_upper_pass':True})
for name in ['b','c']:
    lower=[Q(0)];upper=[Q(0)];alpha=[Q(0)];beta=[Q(0)]
    clower=[Q(0)];cupper=[Q(0)];calpha=[Q(0)];cbeta=[Q(0)]
    for h in range(1,16):
        p=DATA/f'{name}{h}.json' if h<=12 else DATA/f'{name}{h}_interval.json'
        if not p.exists():break
        own=read(p);lo,hi,tail=endpoints(own)
        claimed=claim(h,name)
        assert own['span']==h and own['width']==claimed['w'] and own['M']==claimed['M']
        clo=Q(int(claimed['num_lo']),1<<96);chi=Q(int(claimed['num_hi']),1<<96)
        cu=chi+Q(int(claimed['num_tail']),1<<96)
        assert clo<=lo<=hi<=chi, (name,h,'finite mismatch')
        assert hi+tail<=cu,(name,h,'upper not strengthened')
        lower.append(lo);upper.append(hi+tail);clower.append(clo);cupper.append(cu)
        alpha.append(max(Q(0),lo-sum((beta[j]*upper[h-j] for j in range(1,h)),Q(0))))
        beta.append(hi+tail-sum((alpha[j]*lower[h-j] for j in range(1,h)),Q(0)))
        calpha.append(max(Q(0),clo-sum((cbeta[j]*cupper[h-j] for j in range(1,h)),Q(0))))
        cbeta.append(cu-sum((calpha[j]*clower[h-j] for j in range(1,h)),Q(0)))
        assert 0<=calpha[h]<=alpha[h]<=beta[h]<=cbeta[h]
        result['main'].append({'point':name,'h':h,'method':'exact' if h<=12 else 'directed160',
                               'all_checks':True,'finite_midpoint_diagnostic':float((lo+hi)/2),
                               'alpha_diagnostic':float(alpha[h]),'beta_diagnostic':float(beta[h]),
                               'independent_finite_interval_width':str(hi-lo)})
for W,folder in [(22,'w22_h18_30_c5'),(23,'w23_h18_18_c5_parallel')]:
    p=DATA/f'rectangle{W}.json'
    if not p.exists():continue
    own=read(p);claimed=read(BASE/'rectangle_point'/folder/'replay.json')
    assert [own[k] for k in ['W','minspan','maxspan','cap']]==[W,18,30 if W==22 else 18,5]
    lo=Q(int(own['num_lo']),1<<own['scale']);hi=Q(int(own['num_hi']),1<<own['scale'])
    assert Q(int(claimed['num_lo']),1<<96)<=lo<=hi<=Q(int(claimed['num_hi']),1<<96)
    record={'W':W,'all_checks':True,'lo':str(lo),'hi':str(hi),'midpoint_diagnostic':float((lo+hi)/2)}
    if W==22:
        el=sum((Q(int(r['lo']),1<<own['scale']) for r in own['per_span'] if r['h']>=19),Q(0))
        eu=sum((Q(int(r['hi']),1<<own['scale']) for r in own['per_span'] if r['h']>=19),Q(0))
        e=Q(read(ROOT/'results/EXACT_AUDIT.json')['e'])
        assert e<=el<=eu
        record.update({'E_direct_lower':str(el),'E_direct_upper':str(eu),'E_direct_diagnostic':float((el+eu)/2),'claimed_e_below_direct_lower':True})
    result['rectangles'].append(record)
result['completed_main_max']={name:max((r['h'] for r in result['main'] if r['point']==name),default=0) for name in ['b','c']}
result['status']='PASS_FOR_RECORDED_COVERAGE'
(ROOT/'results/EXTENSION_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','completed_main_max']}))
print('rectangles:',[r['W'] for r in result['rectangles']])
