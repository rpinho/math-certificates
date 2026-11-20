"""Recompute release certificate facts and exact comparison gaps; no search helpers."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
from pathlib import Path
import hashlib
import json
from flint import fmpz_poly

P=Path(__file__).resolve().parent
TARGET='0.2519694759'

def endpoint(x):
    return Fraction(int(x['mantissa']))*Fraction(2)**x['exponent']

def outward(q, upper=False):
    with localcontext() as c:
        c.prec=100
        c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return format((Decimal(q.numerator)/Decimal(q.denominator)).quantize(Decimal('1e-22')),'f')

def main():
    raw=(P/'certificate.json').read_bytes()
    cert=json.loads(raw)
    receipt=json.loads((P/'receipts/release-verifier.json').read_text())
    sha=hashlib.sha256(raw).hexdigest()
    assert receipt['status']=='PASS' and receipt['certificate_sha256']==sha
    assert receipt['source_sha256']==hashlib.sha256((P/'verify.py').read_bytes()).hexdigest()
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
    lo=endpoint(receipt['bound']['lower']);hi=endpoint(receipt['bound']['upper']);target=Fraction(TARGET)
    assert hi<target and receipt['target']==TARGET
    from math import gcd
    reduced=all(gcd(int(x['q_rational'].split('/')[0]),int(x['q_rational'].split('/')[1] if '/' in x['q_rational'] else 1))==1 for x in cert['numerator'])
    facts={'certificate_sha256':sha,'q_rational_all_in_lowest_terms':reduced,'D':D,'a':str(a),'slack':str(D-a),'active_gcd_pairs':pairs,'composed_roots':roots,
           'denominator_factors':len(den),'numerator_factors':len(num),'denominator_degrees':sorted({len(x['coeffs'])-1 for x in den}),
           'non_monic_numerators':{x['name']:x['coeffs'][0] for x in num if x['coeffs'][0]!=1},
           'exact_lower':str(lo),'exact_upper':str(hi),'interval_lower':outward(lo),'interval_upper':outward(hi,True),
           'release_target':TARGET,'exact_margin_lower':str(target-hi),
           'source':'Computed from certificate.json and receipts/release-verifier.json by certificate_facts.py; coefficient order descending. Composed-root count agrees with certified root isolation in verify.py.',
           'encoding_note':'Producer release bytes retained unchanged; see CERTIFICATE_ENCODING.md for equal-fraction representations.'}
    comparators={'280_v6':'0.2519694883','round11_printed':'0.2519695579','330_round10':'0.2519696460','round9_printed':'0.2519744488',
                 '330_a12':'0.2519923410','280_v5':'0.2519889614','280_v4':'0.2520079724','280_v3':'0.2520591386'}
    for label,value in comparators.items():
        facts['comparator_'+label]=value
        facts['gap_to_'+label+'_at_least']=outward(Fraction(value)-hi)
        facts['exact_gap_to_'+label]=str(Fraction(value)-hi)
    # earlier replays of the public #280 v6 certificate and of our unpublished round 11 (producer step 0, evidence/)
    for label,name in (('pr280_v6','v6'),('round11','round11')):
        r=json.loads((P/f'evidence/{name}.json').read_text())
        assert r['status']=='PASS'
        l=endpoint(r['bound']['lower']);u=endpoint(r['bound']['upper'])
        facts[label+'_replay']={'certificate_sha256':r['certificate_sha256'],'target':r['target'],'interval_lower':outward(l),'interval_upper':outward(u,True),'source':f'evidence/{name}.json'}
    # split of the gain over the exact #280 v6 replay: full-bank union (rounds/union-0-replay.json), then later pricing
    un=json.loads((P/'rounds/union-0-replay.json').read_text())
    assert un['status']=='PASS'
    v6hi=endpoint(json.loads((P/'evidence/v6.json').read_text())['bound']['upper'])
    unhi=endpoint(un['bound']['upper'])
    facts['union_replay']={'certificate_sha256':un['certificate_sha256'],'interval_upper':outward(unhi,True),'source':'rounds/union-0-replay.json'}
    facts['gain_union_over_pr280_v6_replay_at_least']=outward(v6hi-unhi)
    facts['gain_after_union_at_least']=outward(unhi-hi)
    facts['gain_total_over_pr280_v6_replay_at_least']=outward(v6hi-hi)
    # exact full-coefficient overlaps with the public #280 certificates
    sources={'v3':'prior_sources/pr280-v3-certificate.json','v4':'prior_sources/pr280-v4-certificate.json','v5':'prior_sources/pr280-v5-certificate.json','v6':'inputs/v6.json'}
    for version,rel in sources.items():
        public_raw=(P/rel).read_bytes()
        public=json.loads(public_raw)
        facts[f'pr280_{version}_certificate_sha256']=hashlib.sha256(public_raw).hexdigest()
        facts[f'pr280_{version}_factor_overlap']={k:[{'packet_name':x['name'],'public_name':y['name']} for x in cert[k] for y in public[k] if x['coeffs']==y['coeffs']] for k in ['denominator','numerator']}
    # credit classes from FACTOR_PROVENANCE.json, whose coefficients must equal the certificate's
    prov=json.loads((P/'FACTOR_PROVENANCE.json').read_text())
    for k in ['denominator','numerator']:
        assert [(x['name'],x['coeffs']) for x in prov[k]]==[(x['name'],x['coeffs']) for x in cert[k] if k=='denominator' or Fraction(x['q_rational'])>0]
    v6_num={o['packet_name'] for o in facts['pr280_v6_factor_overlap']['numerator']}
    only_v6=[x['name'] for x in prov['numerator'] if set(x['exact_matches'])=={'#280 v6'}]
    none=[x['name'] for x in prov['numerator']+prov['denominator'] if not x['exact_matches']]
    assert v6_num=={x['name'] for x in prov['numerator'] if x['also_in_v6']}
    facts['credit_classes']={'numerators_found_only_in_pr280_v6':only_v6,'numerators_also_in_pr280_v6':len(v6_num),
        'factors_with_no_earlier_match':none,'denominators_also_in_pr280_v6':len(facts['pr280_v6_factor_overlap']['denominator'])}
    (P/'receipts/certificate-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2))

if __name__=='__main__':main()
