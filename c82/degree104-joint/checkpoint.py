"""Retain only improved, exactly compared interval-certified packets."""
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
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
    r=json.loads(Path(replay).read_text());lo=endpoint(r['bound']['lower']);hi=endpoint(r['bound']['upper'])
    assert r['artificial_integrand_offset']=='0'
    assert r['certificate_sha256']==hashlib.sha256(Path(certificate).read_bytes()).hexdigest()
    if Path('RESULT.json').exists() and hi>=Fraction(json.loads(Path('RESULT.json').read_text())['exact_upper']):return False
    for src,dst in [(certificate,'certificate.json'),(verifier,'verify_best.py'),(replay,'evidence/best-replay.json')]:
        if Path(src).resolve()!=Path(dst).resolve():shutil.copyfile(src,dst)
    bar=Fraction('0.2519758216');ours=Fraction('0.2519923410');public=Fraction('0.2519889614')
    data={'candidate_unrefereed':True,'interval_lower':decimal_out(lo,False),'interval_upper':decimal_out(hi),'exact_lower':str(lo),'exact_upper':str(hi),'target':str(bar),'below_frozen_bar':hi<bar,'ours_comparator':str(ours),'gap_to_ours_at_least':decimal_out(ours-hi,False),'public_comparator':str(public),'gap_to_pr280_v5_at_least':decimal_out(public-hi,False),'certificate_sha256':r['certificate_sha256'],'replay_source':replay,'verification':'separately written (same agent), stdlib + python-flint only'}
    data['gap_to_round8_printed_at_least']=decimal_out(Fraction('0.2519758217')-hi,False)
    data['gap_to_round8_endpoint_at_least']=decimal_out(Fraction('0.2519758216376568674750')-hi,False)
    data['stated_decimal']=decimal_out(hi,True,10)
    data['stated_rational']=str(Fraction(data['stated_decimal']))
    data['exact_endpoint_below_stated_rational']=hi<Fraction(data['stated_decimal'])
    write_json('RESULT.json',data)
    archive='certificates/best_'+decimal_out(hi)+'.json'
    shutil.copyfile('certificate.json',archive)
    write_json(archive.removesuffix('.json')+'-replay.json',r)
    with open('evidence/improvement-curve.jsonl','a') as f:
        import time
        f.write(json.dumps({'epoch':time.time(),'upper':decimal_out(hi),'exact_upper':str(hi),'certificate':archive,'replay_source':replay})+'\n')
    sources=[(label,json.loads(Path(file).read_text())) for label,file in [('ours from round 7','prior_sources/round7-certificate.json'),('ours from round 6','prior_sources/round6-certificate.json'),('ours from round 5 or earlier','prior_sources/round5-certificate.json'),('#280 v5','prior_sources/pr280-v5-certificate.json'),('#280 v4','prior_sources/pr280-v4-certificate.json'),('#280 v3','prior_sources/pr280-v3-certificate.json'),('earlier bank','prior_sources/factor-bank.json'),('initial coefficient union (including v5)','union-input.json')]]
    sources+=[('ours from round 8','prior_sources/round8-certificate.json'),('full round-8 union bank','prior_sources/round8-bank.json')]
    sources=[(label,json.loads(Path(obj).read_text()) if isinstance(obj,str) else obj) for label,obj in sources]
    cert=json.loads(Path(certificate).read_text());provenance={}
    for kind in ['denominator','numerator']:
        provenance[kind]=[]
        for row in cert[kind]:
            matches=[{'origin':label,'name':other['name']} for label,source in sources for other in source[kind] if row['coeffs']==other['coeffs']]
            provenance[kind].append({**row,'origin':matches[0]['origin'] if matches else 'new here','all_full_coefficient_matches':matches})
    write_json('FACTOR_PROVENANCE.json',provenance)
    headline=f'Shipped: candidate, unrefereed C82 < {decimal_out(hi)}; frozen target '+('met.' if hi<bar else 'not yet met.')
    Path('REPORT.md').write_text(headline+'\n\nCertified enclosure: ['+decimal_out(lo,False)+', '+decimal_out(hi)+']. Exact endpoint and gaps are in RESULT.json. Separately written (same agent) interval verifier, stdlib + python-flint only. Factor provenance: FACTOR_PROVENANCE.json. Search continues; no novelty judgment is made.\n')
    with open('STATUS.md','a') as f:f.write('\nCertified checkpoint: '+headline+' Source '+certificate+'\n')
    print(json.dumps(data),flush=True)
    return True
if __name__=='__main__':
    import sys
    checkpoint(*sys.argv[1:])
