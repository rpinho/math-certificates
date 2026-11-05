"""Checkpoint each improved exact certificate using our own verifier output."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import hashlib,json,shutil
from pathlib import Path
from numerics import write_json

def endpoint(r):return Fraction(int(r['mantissa']))*Fraction(2)**r['exponent']
def decimal_out(q,upper=True,places=22):
    with localcontext() as c:
        c.prec=100;c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str((Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal(10)**-places))
def checkpoint(certificate,verifier,replay):
    result=json.loads(Path(replay).read_text());lo=endpoint(result['bound']['lower']);hi=endpoint(result['bound']['upper'])
    assert result['artificial_integrand_offset']=='0'
    assert result['certificate_sha256']==hashlib.sha256(Path(certificate).read_bytes()).hexdigest()
    bar=Fraction('0.2519900000');ours=Fraction('0.2519964890');public=Fraction('0.2520079724')
    if Path('RESULT.json').exists() and hi>=Fraction(json.loads(Path('RESULT.json').read_text())['exact_upper']):return False
    for src,dst in [(certificate,'certificate.json'),(verifier,'verify_best.py'),(replay,'evidence/best-replay.json')]:
        if Path(src).resolve()!=Path(dst).resolve():shutil.copyfile(src,dst)
    comparisons={'candidate_unrefereed':True,'interval_lower':decimal_out(lo,False),'interval_upper':decimal_out(hi),'exact_lower':str(lo),'exact_upper':str(hi),'target':str(bar),'below_frozen_bar':hi<bar,'ours_comparator':str(ours),'gap_to_ours_at_least':decimal_out(ours-hi,False),'public_comparator':str(public),'gap_to_pr280_v4_at_least':decimal_out(public-hi,False),'certificate_sha256':result['certificate_sha256'],'replay_source':str(replay),'verification':'separately written (same agent lineage), stdlib + python-flint only'}
    write_json('RESULT.json',comparisons)
    cert=json.loads(Path(certificate).read_text());sources=[]
    for origin,file in [('ours from round 6','round6-certificate.json'),('#280 v4','pr280-v4-certificate.json'),('#280 v3','pr280-v3-certificate.json'),('ours from round 5 or earlier','round5-certificate.json'),("#280 bank",'factor-bank.json')]:
        sources.append((origin,json.loads((Path('prior_sources')/file).read_text())))
    sources.append(('ours from round 6 earlier search states',json.loads(Path('union-input.json').read_text())))
    provenance={}
    for kind in ['denominator','numerator']:
        records=[]
        for r in cert[kind]:
            matches=[{'origin':origin,'name':other['name']} for origin,data in sources for other in data[kind] if r['coeffs']==other['coeffs']]
            records.append({**r,'origin':matches[0]['origin'] if matches else 'new here','all_full_coefficient_matches':matches})
        provenance[kind]=records
    write_json('FACTOR_PROVENANCE.json',provenance)
    headline=f'Shipped: candidate, unrefereed C82 < {decimal_out(hi)}; frozen target '+('met.' if hi<bar else 'not yet met.')
    Path('REPORT.md').write_text(headline+'\n\nCertified enclosure: ['+decimal_out(lo,False)+', '+decimal_out(hi)+']. Exact endpoint and comparator gaps are in RESULT.json. Separately written (same agent lineage) interval verifier, stdlib + python-flint only. Full coefficient provenance is in FACTOR_PROVENANCE.json. Search continues; no novelty judgment is made.\n')
    with open('STATUS.md','a') as f:f.write('\nCertified checkpoint: '+headline+' Source '+str(certificate)+'\n')
    print(json.dumps(comparisons),flush=True)
    return True
