"""Keep each improvement after exact comparison of the verifier's dyadic endpoints."""
import hashlib,json,shutil,time
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction
from pathlib import Path
from worker import START

def read(path): return json.loads(Path(path).read_text())
def put(path, value):
    dest=Path(path);temp=dest.with_suffix('.tmp')
    temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(dest)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def endpoint(r):return int(r['mantissa'])*Fraction(2)**r['exponent']
def decimal(q,places=22,upper=True):
    with localcontext() as c:
        c.prec=120;c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return format((Decimal(q.numerator)/q.denominator).quantize(Decimal(1).scaleb(-places)),'f')
def status(line):
    with open('STATUS.md','a') as f:print('\n'+time.strftime('%Y-%m-%d %H:%M:%S %Z')+' '+line,file=f)
def save(cert,replay,label):
    r=read(replay)
    assert r['certificate_sha256']==sha(cert) and r['artificial_integrand_offset']=='0'
    lo,hi=[endpoint(r['bound'][k]) for k in ['lower','upper']]
    if Path('RESULT.json').exists() and hi>=Fraction(read('RESULT.json')['exact_upper']):return False
    stated=decimal(hi,10);assert hi<Fraction(stated)
    archive='certificates/best_'+decimal(hi)+'.json'
    shutil.copyfile(cert,archive);shutil.copyfile(replay,archive[:-5]+'-replay.json')
    shutil.copyfile(cert,'certificate.json')
    data=dict(label=label,candidate_unrefereed=True,interval=[decimal(lo,upper=False),decimal(hi)],exact_lower=str(lo),exact_upper=str(hi),stated=stated,archive=archive,sha256=sha(cert),replay=replay,below_printed_bar=hi<Fraction('0.2519694883'),elapsed_hours=(time.time()-START)/3600)
    put('RESULT.json',data)
    with open('IMPROVEMENT_CURVE.jsonl','a') as f: print(json.dumps(data),file=f)
    Path('REPORT.md').write_text(f'Shipped: candidate, unrefereed C82 < {stated} ({label}).\n\nUpper endpoint rounded outward to 22 places: '+decimal(hi)+'. Exact endpoint and packet path in RESULT.json. Search in progress.\n')
    status(f'Certified {label} upper endpoint {decimal(hi)}. Saved {archive}.')
    return True
