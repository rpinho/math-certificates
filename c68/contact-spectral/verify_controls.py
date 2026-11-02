"""Rejection controls for both independent C68 interval implementations."""
import copy
import json
import os
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
base=json.loads(Path('certificate-contact-044667.json').read_text())
mutations={}
def add(name,edit):
    d=copy.deepcopy(base);edit(d);mutations[name]=d
add('negative_weight',lambda d:d['weights'].__setitem__(1,'-1/100'))
add('wrong_mass',lambda d:d['weights'].__setitem__(0,str(Q(d['weights'][0])+Q(1,100))))
add('wrong_inner_endpoint',lambda d:d['nodes'].__setitem__(0,'1/5'))
add('reversed_nodes',lambda d:d['nodes'].__setitem__(slice(1,3),d['nodes'][1:3][::-1]))
add('wrong_fourier_constant',lambda d:d.__setitem__('kappa','1/8'))
add('unsupported_zeta',lambda d:d.__setitem__('zeta','1/10'))
add('unjustified_first_tail',lambda d:d.__setitem__('first_tail_k',2))
add('unjustified_second_tail',lambda d:d.__setitem__('second_tail_b','999000001/1000000000'))
def shift(d,source,destination):
    d['weights'][source]=str(Q(d['weights'][source])-Q(1,10))
    d['weights'][destination]=str(Q(d['weights'][destination])+Q(1,10))
add('ordinary_moment_failure',lambda d:shift(d,1,0))
add('weighted_moment_failure',lambda d:shift(d,0,1))
results=[];started=time.monotonic()
for name,d in mutations.items():
    path=Path('.control-'+name+'.json');path.write_text(json.dumps(d))
    try:
        for checker in ('verify_exact.py','verify_interval.py'):
            p=subprocess.run([sys.executable,checker,str(path)],capture_output=True,text=True)
            assert p.returncode!=0,(name,checker,'bad certificate was accepted')
            last=(p.stderr or p.stdout).strip().splitlines()[-1]
            if name=='ordinary_moment_failure':assert "'A'" in last or 'ordinary moment' in last,last
            if name=='weighted_moment_failure':assert "'B'" in last or 'weighted moment' in last,last
            results.append(dict(name=name,checker=checker,status='REJECTED',diagnostic=last))
    finally:
        path.unlink()  # This session's temporary control file only.
# Check the independently validated scalar covering cannot omit a cell.
cover=json.loads(Path('spectral-cover.json').read_text());cover['cells']=cover['cells'][1:]
path=Path('.control-cover-gap.json');path.write_text(json.dumps(cover))
try:
    for checker in ('verify_spectral.py','verify_spectral_interval.py'):
        p=subprocess.run([sys.executable,checker,'--cover',str(path),'--output','unused-control-output.json'],capture_output=True,text=True)
        assert p.returncode!=0,(checker,'accepted cover gap')
        results.append(dict(name='scalar_cover_gap',checker=checker,status='REJECTED',diagnostic=p.stderr.strip().splitlines()[-1]))
finally:
    path.unlink()
cover=json.loads(Path('contact-cover.json').read_text());cover['tree']['mid']='0'
path=Path('.control-contact-tree.json');path.write_text(json.dumps(cover))
try:
    for checker in ('verify_contact.py','verify_contact_interval.py'):
        p=subprocess.run([sys.executable,checker,'--cover',str(path),'--output','unused-control-output.json'],capture_output=True,text=True)
        assert p.returncode!=0,(checker,'accepted invalid contact split')
        results.append(dict(name='contact_cover_invalid_split',checker=checker,status='REJECTED',diagnostic=p.stderr.strip().splitlines()[-1]))
finally:
    path.unlink()
out=dict(status='PASS',controls=len(results),results=results,seconds=time.monotonic()-started)
Path('verification-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
