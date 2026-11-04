"""Frozen exact verifier, separately written (same agent), adapted from round 5.
Only this source, adjacent C++/include sources and the frozen artifact are read.
No numerical graph, optimizer output or generated partition is read.
"""
import gzip, hashlib, json, os, resource, signal, struct, subprocess, sys, tempfile, time
from fractions import Fraction
from pathlib import Path
from flint import arb, ctx

# A deliberate checkpoint stop must unwind temporary files and reap the child.
def harness_stop(signum, frame):
    raise SystemExit(128+signum)
signal.signal(signal.SIGTERM, harness_stop)

def reject(code, message):
    print(message, file=sys.stderr, flush=True)
    raise SystemExit(code)

ctx.prec = 256
started = time.time()
artifact = Path(sys.argv[1]).resolve()
d = json.load(gzip.open(artifact, 'rt'))
if not (d['schema'] == 'c91-direct-orbit-higher-order-v1' and d['K'] == 8):
    reject(41, 'VERIFY_REJECT schema')
for name in ('L','W','B','S','T','K','original_states','base_states','product_states','quotient_states','lifted_product_states'):
    assert type(d[name]) is int
assert 2 <= d['L'] <= 21 and 1 <= d['W'] <= 6 and 0 <= d['B'] <= 10
assert 0 <= d['S'] <= 3 and 1 <= d['T'] <= 3
assert d['cap_mode'] in ('absolute', 'completion', 'per-lag')
if d['cap_mode'] == 'per-lag':
    assert isinstance(d['lag_cost_caps'], list) and len(d['lag_cost_caps']) == d['W']
    assert all(type(b) is int and -r <= b <= 10 for r,b in enumerate(d['lag_cost_caps'],1))
for name in ('original_states','base_states','product_states','quotient_states'):
    assert 0 < d[name] < 2**32
assert d['orbit'] == 'global-bit-complement;latest-X-bit-zero'
assert d['lifted_product_states'] == 2*d['product_states']-1 < 500000000
assert 'candidate' in d['status'] and 'unrefereed' in d['status']

print('VERIFY_CHECKPOINT schema PASS', flush=True)

def pair(value):
    assert isinstance(value,list) and len(value)==2
    assert all(type(k) is int and 0<k<2**64 for k in value)
    return Fraction(*value)

x,t,a = (pair(d[k]) for k in ('x','t','bound'))
z = [pair(p) for p in d['z']]
assert x>1 and 0<t<1 and len(z)==8 and a>=Fraction(529,2000)
ball = lambda q: arb(q.numerator)/q.denominator
exponent = 2*ball(x).log()+ball(a)*ball(t).log()
if not exponent>0:
    reject(42, 'VERIFY_REJECT exponent')
print('VERIFY_CHECKPOINT exponent PASS', flush=True)
threshold = -2*ball(x).log()/ball(t).log()
recipe = d['potential']
assert set(recipe)=={'encoding','precision','initial','steps'}
assert recipe['encoding']=='integer-lazy-power-ceil-weights-v1'
assert all(type(recipe[k]) is int for k in ('precision','initial','steps'))
assert 16<=recipe['precision']<=48
if not 0<recipe['initial']<=2**60:
    reject(44, 'VERIFY_REJECT initial potential (requires 0 < initial <= 2^60)')
assert 0<=recipe['steps']<=4096
print('VERIFY_CHECKPOINT integer power recipe PASS', flush=True)
patterns = d['forbidden_patterns']
assert isinstance(patterns,list)
assert all(isinstance(p,list) and len(p)==2 and all(type(k) is int for k in p) for p in patterns)
assert all(1<=n<=d['L'] and 0<=w<8**n for n,w in patterns)
bank = {tuple(p) for p in patterns}
assert len(bank)==len(patterns)
phi = (1,0,3,2,5,4,7,6)
for n,w in patterns:
    flipped = sum(phi[(w>>(3*k))&7]<<(3*k) for k in range(n))
    assert (n,flipped) in bank
print('artifact_sha256',hashlib.sha256(artifact.read_bytes()).hexdigest(),flush=True)
print('Arb_exponent',exponent,'Arb_threshold',threshold,flush=True)
print('exact_potential_recipe',recipe,flush=True)
source = Path(__file__).with_name('verify_orbit8.cpp')
for filename in ('verify_orbit8.py','verify_orbit8.cpp','orbit_tracker8.inc','base_complement.inc'):
    path = source.with_name(filename)
    print('checker_source_sha256',filename,hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
with tempfile.TemporaryDirectory(prefix='verification-',dir=artifact.parent) as folder:
    folder = Path(folder)
    binary,executable = folder/'frozen-input.bin',folder/'exact-verifier'
    with binary.open('wb') as stream:
        stream.write(b'C91PO008')
        for name in ('L','W','B','K','original_states','base_states','product_states','quotient_states'):
            stream.write(struct.pack('<I',d[name]))
        mode = {'absolute':0,'completion':1,'per-lag':2}[d['cap_mode']]
        stream.write(struct.pack('<IIII',d['S'],d['T'],mode,len(patterns)))
        if mode==2:
            for b in d['lag_cost_caps']:stream.write(struct.pack('<i',b))
        for value in (d['x'],d['t'],*d['z']):stream.write(struct.pack('<QQ',*value))
        for n,w in patterns:stream.write(struct.pack('<IQ',n,w))
        stream.write(struct.pack('<IIQ',recipe['precision'],recipe['steps'],recipe['initial']))
    # Apple Clang uses the installed libomp; GNU g++ uses -fopenmp.
    omp_flags = (['-Xpreprocessor','-fopenmp','-I/opt/homebrew/opt/libomp/include',
                  '-L/opt/homebrew/opt/libomp/lib','-lomp']
                 if sys.platform == 'darwin' else ['-fopenmp'])
    subprocess.run(['g++','-O3','-std=c++17',*omp_flags,str(source),'-o',str(executable)],check=True)
    # Apply in this single-threaded parent, never in preexec_fn. OS refusal
    # is visible and cannot itself satisfy a rejection control.
    previous_limit = None
    try:
        soft,hard = resource.getrlimit(resource.RLIMIT_AS)
        limit = 100000000000
        if hard != resource.RLIM_INFINITY: limit = min(limit,hard)
        if soft != resource.RLIM_INFINITY: limit = min(limit,soft)
        resource.setrlimit(resource.RLIMIT_AS,(limit,hard))
        previous_limit = (soft,hard)
        print('RESOURCE_LIMIT RLIMIT_AS APPLIED',limit,flush=True)
    except (AttributeError,OSError,ValueError) as error:
        print('RESOURCE_LIMIT RLIMIT_AS SKIPPED',type(error).__name__,str(error),flush=True)
    try:
        checked = subprocess.run([str(executable),str(binary)])
    finally:
        if previous_limit is not None:
            resource.setrlimit(resource.RLIMIT_AS,previous_limit)
    if checked.returncode:
        if checked.returncode < 0:
            print('VERIFY_EXECUTION_ERROR checker signal',-checked.returncode,flush=True)
        raise SystemExit(checked.returncode if checked.returncode>0 else 70)
print('SEPARATELY_WRITTEN_SAME_AGENT_EXACT_ARB_PASS','bound',str(a),'seconds',time.time()-started,flush=True)
