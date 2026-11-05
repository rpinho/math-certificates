"""Save a usable certified mathematical result after each accepted master solve."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
from numerics import write_json

def endpoint(rec):
    return Fraction(int(rec['mantissa']))*Fraction(2)**rec['exponent']

def decimal_out(q, upper=True, places=22):
    with localcontext() as c:
        c.prec=100
        c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str((Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal(10)**-places))

def checkpoint(certificate, verifier, replay):
    result=json.loads(Path(replay).read_text())
    lo=endpoint(result['bound']['lower']);hi=endpoint(result['bound']['upper'])
    assert result['artificial_integrand_offset']=='0'
    assert result['certificate_sha256']==hashlib.sha256(Path(certificate).read_bytes()).hexdigest()
    bar=Fraction('0.2520500000');public=Fraction('0.2520591386')
    old=Path('RESULT.json')
    if old.exists() and hi>=Fraction(json.loads(old.read_text())['exact_upper']):return False
    for source,target in [(certificate,'certificate.json'),(verifier,'verify_best.py'),(replay,'evidence/best-replay.json')]:
        if Path(source).resolve()!=Path(target).resolve():shutil.copyfile(source,target)
    cert=json.loads(Path(certificate).read_text())
    comparisons={'candidate_unrefereed':True,'interval_lower':decimal_out(lo,False),'interval_upper':decimal_out(hi),
        'exact_lower':str(lo),'exact_upper':str(hi),'target':str(bar),'below_frozen_bar':hi<bar,
        'public_comparator':str(public),'certified_gap_to_public_at_least':decimal_out(public-hi,False),
        'certificate_sha256':result['certificate_sha256'],'replay_source':str(replay),
        'verification':'separately written (same agent lineage), stdlib + python-flint only'}
    write_json('RESULT.json',comparisons)
    sources=[('ours from round 5 or earlier',json.loads(Path('prior_sources/round5-certificate.json').read_text())),
        ("#280 v3 (V. Patankar)",json.loads(Path('prior_sources/pr280-v3-certificate.json').read_text())),
        ("#280's earlier public numerator bank",json.loads(Path('prior_sources/factor-bank.json').read_text()))]
    provenance={}
    for kind in ['denominator','numerator']:
        records=[]
        for r in cert[kind]:
            matches=[]
            for origin,data in sources:
                matches.extend({'origin':origin,'name':other['name']} for other in data[kind] if r['coeffs']==other['coeffs'])
            primary='new here' if not matches else matches[0]['origin']
            records.append({**r,'origin':primary,'all_full_coefficient_matches':matches})
        provenance[kind]=records
    write_json('FACTOR_PROVENANCE.json',provenance)
    headline=f"Shipped: candidate, unrefereed C82 < {comparisons['interval_upper']}, certified by a separately written (same agent lineage) interval verifier; frozen target {'met' if hi<bar else 'not yet met'}."
    report=[headline,'',f"Certified B lies in [{comparisons['interval_lower']}, {comparisons['interval_upper']}]. The gain over 0.2520591386 is at least {comparisons['certified_gap_to_public_at_least']}. Exact Fraction comparison of the dyadic upper endpoint with 5041/20000: {hi<bar}. RESULT.json retains the exact fractions.",'',
        'The public #280 v3 certificate of V. Patankar was first replayed locally: B lies in [0.2520591385259548 +/- 1.94e-17]. This is a public-data reproduction, credited to Patankar. The optimized result uses the Doche construction, Patankar weighted-CVP method and Pinho joint LP/residue pricing; Grinsztajn and Épi contributed earlier factor libraries. No novelty judgment is made.','',
        f"Current certificate: {len(cert['denominator'])} degree-104 denominators, {len(cert['numerator'])} numerator factors, D={result['audit']['D']}. Each factor's full coefficients, exact weight, and full coefficient provenance comparisons are in FACTOR_PROVENANCE.json. Search/grid objectives are heuristic; only the frozen interval replay supports the bound above.",'',
        'Our own ../c82r5 scripts were copied and reused. The verifier imports only stdlib and python-flint and shares no search helper. No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. Its only initial change was the certificate hash pin. This verifies the finite arithmetic construction under the inherited Doche reduction; it is not a formal proof of the reduction or arithmetic backend.','',
        'Reproduce in this job directory:','', '```sh',
        'export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1',
        'export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1',
        'nice -n 10 python3 verify_best.py --certificate certificate.json --target 0.2520500000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json',
        '```','',
        'PRIOR_ART.md records the scoped public source checks. STATUS.md records the ongoing search and stopping reason; the final compute accounting, corruption controls and Python blob comparison will be appended when search ends.']
    Path('REPORT.md').write_text('\n'.join(report)+'\n')
    with open('STATUS.md','a') as f:f.write('\nCertified checkpoint: '+headline+' Source: '+str(certificate)+'\n')
    print(json.dumps(comparisons),flush=True)
    return True
