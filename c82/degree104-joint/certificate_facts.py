"""Recompute release certificate facts and exact comparison gaps; no search helpers."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
from pathlib import Path
import hashlib
import json
from flint import fmpz_poly

P=Path(__file__).resolve().parent

def endpoint(x):
    return Fraction(int(x['mantissa']))*Fraction(2)**x['exponent']

def outward(q, upper=False):
    with localcontext() as c:
        c.prec=100
        c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str((Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal('1e-22')))

def main():
    raw=(P/'certificate.json').read_bytes()
    cert=json.loads(raw)
    receipt=json.loads((P/'receipts/release-verifier.json').read_text())
    sha=hashlib.sha256(raw).hexdigest()
    assert receipt['status']=='PASS' and receipt['certificate_sha256']==sha
    assert receipt['source_sha256']==hashlib.sha256((P/'verify_best.py').read_bytes()).hexdigest()
    den=cert['denominator'];num=[x for x in cert['numerator'] if Fraction(x['q_rational'])>0]
    D=sum((len(x['coeffs'])-1)*x['multiplicity'] for x in den)
    a=sum((len(x['coeffs'])-1)*Fraction(x['q_rational']) for x in num)
    assert all(type(x['multiplicity']) is int and x['multiplicity']>0 and x['coeffs'][0]==1 for x in den)
    assert a<D and all(Fraction(x['q_rational'])>=0 for x in cert['numerator'])
    pairs=0
    for n in num:
        for d in den:
            assert fmpz_poly(n['coeffs'][::-1]).gcd(fmpz_poly(d['coeffs'][::-1])).degree()==0
            pairs+=1
    roots=2*sum(len(x['coeffs'])-1 for x in den+num)
    expected={'D':D,'degree_A':str(a),'coprimality_pairs':pairs,'composed_roots':roots,'denominator_factors':len(den),'numerator_factors':len(num)}
    assert receipt['audit']==expected
    lo=endpoint(receipt['bound']['lower']);hi=endpoint(receipt['bound']['upper']);target=Fraction('0.2519744488')
    assert hi<target and receipt['target']=='0.2519744488'
    facts={'certificate_sha256':sha,'D':D,'a':str(a),'slack':str(D-a),'active_gcd_pairs':pairs,'composed_roots':roots,
           'denominator_factors':len(den),'numerator_factors':len(num),'denominator_degrees':sorted({len(x['coeffs'])-1 for x in den}),
           'non_monic_numerators':{x['name']:x['coeffs'][0] for x in num if x['coeffs'][0]!=1},
           'exact_lower':str(lo),'exact_upper':str(hi),'interval_lower':outward(lo),'interval_upper':outward(hi,True),
           'release_target':'0.2519744488','exact_margin_lower':str(target-hi),
           'gap_to_280_v3_at_least':outward(Fraction('0.2520591386')-hi),
           'gap_to_previous_330_at_least':outward(Fraction('0.2519923410')-hi),
           'gap_to_280_v4_at_least':outward(Fraction('0.2520079724')-hi),
           'exact_gap_to_280_v3':str(Fraction('0.2520591386')-hi),'exact_gap_to_previous_330':str(Fraction('0.2519923410')-hi),'exact_gap_to_280_v4':str(Fraction('0.2520079724')-hi),
           'source':'Computed from certificate.json and receipts/release-verifier.json by certificate_facts.py; coefficient order descending. Composed-root count agrees with certified root isolation in verify_best.py.',
           'encoding_note':'Producer release bytes retained unchanged; see CERTIFICATE_ENCODING.md for equal-fraction representations.'}
    for label, value in {'280_v5':'0.2519889614', 'round8_printed':'0.2519758217',
                         'round8_endpoint':'0.2519758216376568674750'}.items():
        facts['gap_to_'+label+'_at_least']=outward(Fraction(value)-hi)
        facts['exact_gap_to_'+label]=str(Fraction(value)-hi)
    for version in ['v3','v4','v5']:
        public_raw=(P/f'prior_sources/pr280-{version}-certificate.json').read_bytes()
        public=json.loads(public_raw)
        facts[f'pr280_{version}_certificate_sha256']=hashlib.sha256(public_raw).hexdigest()
        facts[f'pr280_{version}_factor_overlap']={k:[{'packet_name':x['name'],'public_name':y['name']} for x in cert[k] for y in public[k] if x['coeffs']==y['coeffs']] for k in ['denominator','numerator']}
    (P/'receipts/certificate-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2))

if __name__=='__main__':main()
