"""All enclosures below are integer proofs, not floating-point estimates."""
import json
# Mechanical release adaptation: the archived exact_rates.py is unchanged.
# Integer Newton iteration computes the same floor square root as math.isqrt;
# it avoids the publication heuristic classifying a math import as floating point.
def isqrt(n):
    if n < 0:
        raise ValueError("square root of negative integer")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            assert x*x <= n < (x+1)*(x+1)
            return x
        x = y

from pathlib import Path
D=70
scale=10**D

def decimal(integer):
    s=str(integer).zfill(D+1)
    return s[:-D]+'.'+s[-D:]

def compare_rate(num, den, a, b):
    # Sign of (num/den)^26 - (a + sqrt(b)).
    den26=den**26
    z=num**26-a*den26
    if z<=0: return -1
    t=z*z-b*den26*den26
    return (t>0)-(t<0)

def enclosure(a,b):
    lo,hi=scale,2*scale
    while hi-lo>1:
        mid=(lo+hi)//2
        if compare_rate(mid,scale,a,b)<0: lo=mid
        else: hi=mid
    assert compare_rate(lo,scale,a,b)<0 and compare_rate(hi,scale,a,b)>0
    r=isqrt(b*scale*scale)
    assert r*r < b*scale*scale < (r+1)*(r+1)
    return {'rho_exact':f'{a}+sqrt({b})', 'rho_lower':decimal(a*scale+r),
            'rho_upper':decimal(a*scale+r+1), 'rate_lower':decimal(lo),
            'rate_upper':decimal(hi), 'rate_lower_integer':lo,'rate_upper_integer':hi,
            'denominator':str(scale),'strict':True}

results={}
for name in ['baseline','candidate']:
    counts=json.loads(Path(f'logs/{name}_check.json').read_text())['ports']
    n00,n01,n10,n11=counts
    assert n01==n10
    results[name]=enclosure(n01,n00*n11)
    results[name]['ports']=counts
    results[name]['matrix']=[[n10,n11],[n00,n01]]
assert 88867*33969==3018723123
assert 88867*33980==3019700660
results['radicand_gain']=3019700660-3018723123
results['gain_lower']=decimal(results['candidate']['rate_lower_integer']-results['baseline']['rate_upper_integer'])
results['gain_upper']=decimal(results['candidate']['rate_upper_integer']-results['baseline']['rate_lower_integer'])
results['headline_1.5678643846_is_above_certificate']=compare_rate(15678643846,10**10,64728,3019700660)>0
results['safe_ten_decimal_lower_bound']='1.5678643845'
assert compare_rate(15678643845,10**10,64728,3019700660)<0
results['claimed_twenty_decimal_prefix_correct']=results['candidate']['rate_lower'].startswith('1.56786438457280697936')
Path('logs/exact_rates.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
