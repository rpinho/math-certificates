"""Independent round-6 decoder, exact coefficients/exponent, and graph driver.
Derivation: permitted independent round-5 implementation plus round-6 statement.
All writes are to a disposable TMPDIR directory; no producer code is imported.
"""
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from fractions import Fraction as Q

sys.set_int_max_str_digits(20000)
MASKS = [3, 5, 9, 15, 17, 23, 27, 29]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def log_interval(q, n=120):
    y = (q-1)/(q+1)
    sign = 1 if y >= 0 else -1
    y = abs(y)
    total = sum((2*y**(2*k+1)/Q(2*k+1) for k in range(n)), Q(0))
    tail = 2*y**(2*n+1)/((2*n+1)*(1-y*y))
    return (total, total+tail) if sign == 1 else (-total-tail, -total)

def main():
    need(len(sys.argv) == 2, 'usage: independent.py certificate.json.gz')
    data = Path(sys.argv[1]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    cert = json.loads(gzip.decompress(data))
    need(cert['schema'] == 'c91-direct-orbit-higher-order-v1', 'schema')
    need([cert[k] for k in ('W','B','S','T','K','L')] == [3,2,0,2,8,21], 'frontier/features')
    need(cert['cap_mode'] == 'absolute', 'cap mode')
    need(cert['orbit'] == 'global-bit-complement;latest-X-bit-zero', 'orbit convention')
    need(cert['state_count_kind'] == 'reachable complement orbits', 'state count kind')
    for k in ('original_states','base_states','product_states','quotient_states','lifted_product_states'):
        need(type(cert[k]) is int and 0<cert[k]<2**32, 'invalid count '+k)
    need(cert['lifted_product_states'] == 2*cert['product_states']-1 < 500000000, 'lifted count/cap')
    need(cert['bound'] == [265988,1000000], 'claimed bound')
    need(len(cert['z']) == 8, 'feature weights')
    for pair in [cert['x'],cert['t'],cert['bound']]+cert['z']:
        need(len(pair)==2 and all(type(v) is int and 0<v<2**64 for v in pair), 'positive uint64 rational')
    x,t,a = (Q(*cert[k]) for k in ('x','t','bound'))
    need(x>1 and 0<t<1 and a>=Q(529,2000), 'parameter ranges/bar')
    xl,xu=log_interval(x); tl,tu=log_interval(t)
    lo,hi=2*xl+a*tl,2*xu+a*tu
    need(lo>0, 'rational exponent not positive')
    print('exact rational exponent enclosure positive', flush=True)
    pot=cert['potential']
    need(pot['encoding']=='integer-lazy-power-ceil-weights-v1', 'potential encoding')
    b,M,steps=(pot[k] for k in ('precision','initial','steps'))
    need(type(b) is int and 0<=b<=48, 'precision range')
    need(type(M) is int and 0<M<=2**60, 'initial value range')
    need(type(steps) is int and 0<=steps<=100000, 'iteration count range')
    pn,qn=cert['x']; rn,sn=cert['t']; den=4*qn**2*sn
    for u,v in cert['z']:
        den *= u*u*v*v
    # Mixed radix code is sum (h_j+2)*5**j. Python integers are unbounded.
    factors=[[u**(2+h)*v**(2-h) for h in range(-2,3)] for u,v in cert['z']]
    products=[1]
    for fs in factors:
        products=[p*f for f in fs for p in products]
    with tempfile.TemporaryDirectory(prefix='c91-independent-') as scratch:
        root=Path(scratch); source=Path(__file__).with_suffix('.cpp')
        binary=root/'independent'; inp=root/'input.txt'; result=root/'graph_result.json'
        subprocess.run(['g++','-O3','-std=c++17','-fopenmp',str(source),'-o',str(binary)],check=True)
        with inp.open('w') as f:
            f.write(' '.join(str(cert[k]) for k in ('W','B','S','T','original_states','base_states','product_states','quotient_states'))+'\n')
            f.write(str(len(cert['forbidden_patterns']))+'\n')
            for length,word in cert['forbidden_patterns']:
                need(type(length) is int and type(word) is int and 0<length<=21 and 0<=word<8**length,'word format')
                f.write(f'{length} {word}\n')
            f.write(f'{b} {M} {steps}\n')
            for factor in (pn*pn*sn,pn*pn*rn,2*pn*qn*rn):
                for p in products:
                    numerator=(factor*p)<<b
                    u=(numerator+den-1)//den
                    need(0<u<2**48, 'coefficient range')
                    need((u-1)*den<numerator<=u*den, 'ceiling invariant')
                    f.write(str(u)+'\n')
        print('exact ceilings constructed for all 1171875 formal edge monomials',flush=True)
        del products,cert
        subprocess.run([str(binary),str(inp),str(result)],check=True)
        r=json.loads(result.read_text())
    r.update(verdict='AGREES',claim='265988/1000000',certificate_sha256=digest,
             exponent_exact_lower=str(lo),exponent_exact_upper=str(hi),
             rational_clearing_denominator=str(den),walsh_masks=MASKS,
             potential_precision=b,potential_initial=M,potential_steps=steps)
    print(json.dumps(r,sort_keys=True,indent=2),flush=True)

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('DISAGREES: '+str(exc),flush=True)
        raise
