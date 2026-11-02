"""Independent frozen-artifact wrapper. Needs only python-flint and a C++17 compiler.
No generator, optimizer, search graph or search partition is read.
"""
import base64,gzip,hashlib,json,os,struct,subprocess,sys,tempfile,time
from pathlib import Path
from fractions import Fraction
from flint import arb,ctx
ctx.prec=256
artifact=Path(sys.argv[1]).resolve();began=time.time()
d=json.loads(gzip.open(artifact,'rt').read())
assert d['schema']=='c91-dual-zero-frontier-v1' and d['K']==4
assert 2<=d['L']<=21 and 1<=d['W']<=6 and 0<=d['B']<=10
assert 'candidate' in d['status'] and 'unrefereed' in d['status']
def pair(x):
    assert isinstance(x,list) and len(x)==2 and all(type(z) is int and z>0 for z in x)
    assert max(x)<2**64
    return Fraction(*x)
x,t=pair(d['x']),pair(d['t']);z=[pair(p) for p in d['z']];a=pair(d['bound'])
assert x>1 and 0<t<1 and len(z)==4
A=lambda q:arb(q.numerator)/q.denominator
delta=2*A(x).log()+A(a)*A(t).log();assert delta>0
threshold=-2*A(x).log()/A(t).log()
patterns=d['forbidden_patterns']
if 'potential' in d:
    potential=d['potential'];assert potential['encoding']=='ieee754-binary32-le;base64' and 'vector' not in d
    raw=base64.b64decode(potential['data'],validate=True);assert len(raw)==4*d['quotient_states']
    pieces=[]
    for (bits,) in struct.iter_unpack('<I',raw):
        sign=bits>>31;exponent=(bits>>23)&255;mantissa=bits&((1<<23)-1)
        assert sign==0 and 0<exponent<255
        pieces.append(((1<<23)|mantissa,exponent-150))
    common=min(e for m,e in pieces)
    v=[m<<(e-common) for m,e in pieces]
    print('exact_dyadic_potential_common_exponent',common,flush=True)
else:v=d['vector']
assert len(v)==d['quotient_states'] and all(type(k) is int and 0<k<2**64 for k in v)
assert all(isinstance(p,list) and len(p)==2 and all(type(k) is int for k in p) for p in patterns)
assert len({tuple(p) for p in patterns})==len(patterns)
print('artifact_sha256',hashlib.sha256(artifact.read_bytes()).hexdigest(),flush=True)
print('Arb_exponent',delta,'Arb_threshold',threshold,flush=True)
source=Path(__file__).with_name('verify_dual_zero.cpp')
print('checker_cpp_sha256',hashlib.sha256(source.read_bytes()).hexdigest(),flush=True)
print('checker_python_sha256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),flush=True)
with tempfile.TemporaryDirectory(prefix='verification-',dir=artifact.parent) as tmp:
    tmp=Path(tmp);binary=tmp/'checked-input.bin';exe=tmp/'independent-checker'
    with binary.open('wb') as f:
        f.write(b'C91DZ001')
        for k in ('L','W','B','K','original_states','base_states','product_states','quotient_states'):
            assert type(d[k]) is int and (0<=d[k]<2**32 if k=='B' else 0<d[k]<2**32)
            f.write(struct.pack('<I',d[k]))
        f.write(struct.pack('<I',len(patterns)))
        for p in [d['x'],d['t'],*d['z']]:f.write(struct.pack('<QQ',*p))
        for length,word in patterns:
            assert 1<=length<=d['L'] and 0<=word<8**length
            f.write(struct.pack('<IQ',length,word))
        for k in v:f.write(struct.pack('<Q',k))
    subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True)
    subprocess.run([str(exe),str(binary)],check=True)
print('INDEPENDENT_EXACT_ARB_PASS','bound',str(a),'seconds',time.time()-began,flush=True)
