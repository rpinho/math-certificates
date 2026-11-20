"""Prepare the exact incumbent and raw coefficient union from the two sources."""
import json, math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from flint import fmpz_poly, nmod_poly
from numerics import write_json,register

def read(path): return json.loads(Path(path).read_text())
def degree(row): return len(row['coeffs'])-1
def total(cert): return sum(degree(r)*r['multiplicity'] for r in cert['denominator'])

def main():
    register('prepare')
    incumbent=read('inputs/v6.json')
    ours=read('inputs/round11.json')
    bank=read('inputs/bank.json')
    state=read('inputs/restricted-archive-num-111-0.json')
    old={tuple(r['coeffs']) for r in bank['numerator']}
    extra=incumbent['numerator'][-16:]
    hist=lambda rows: dict(sorted(Counter(map(degree,rows)).items()))
    write_json('evidence/degrees.json',dict(our_bank=hist(bank['numerator']),v6_new=hist(extra),v6_new_names=[r['name'] for r in extra],v6_new_also_in_bank=[r['name'] for r in extra if tuple(r['coeffs']) in old]))
    for kind in ['denominator','numerator']:
        master={tuple(r['coeffs']):r for r in state[kind]}
        master.update({tuple(r['coeffs']):dict(name=r['name'],coeffs=r['coeffs']) for r in incumbent[kind] if tuple(r['coeffs']) not in master})
        if kind=='denominator': master.update({tuple(r['coeffs']):r for r in bank[kind] if tuple(r['coeffs']) not in master})
        state[kind]=list(master.values())
        whole={tuple(r['coeffs']):r for r in bank[kind]}
        whole.update({k:r for k,r in master.items() if k not in whole})
        bank[kind]=list(whole.values())
    D=total(incumbent)
    common=math.lcm(total(ours),D,*(degree(r) for r in bank['denominator']))
    for c in (incumbent,ours):
        scale=common//total(c)
        assert total(c)*scale==common
        for kind,key in [('denominator','multiplicity'),('numerator','q_rational')]:
            for r in c[kind]:assert Fraction(r[key])*scale/common==Fraction(r[key])/total(c)
    for kind,key,field in [('denominator','multiplicity','mu'),('numerator','q_rational','w')]:
        weights={tuple(r['coeffs']):Fraction(r[key])/D for r in incumbent[kind]}
        state[field]=[float(weights.get(tuple(r['coeffs']),0)) for r in state[kind]]
    # All denominators are monic, so any common monic integer divisor
    # survives reduction modulo a prime. Use exact Z[X] for ambiguous residues.
    primes=[65521,65519]
    den=[fmpz_poly(r['coeffs'][::-1]) for r in bank['denominator']]
    products=[]
    for prime in primes:
        prod=nmod_poly([1],prime)
        for r in bank['denominator']:
            assert r['coeffs'][0]==1
            prod*=nmod_poly(r['coeffs'][::-1],prime)
        products.append(prod)
    exceptions={k:[r['name'] for r in v if r['coeffs'][-1]==0 or sum(r['coeffs'])==0] for k,v in bank.items()}
    assert set(exceptions['numerator'])=={'P1','P2'} and not exceptions['denominator']
    fallbacks=0
    for row in bank['numerator']:
        c=row['coeffs'][::-1]
        if any(prod.gcd(nmod_poly(c,p)).degree()==0 for p,prod in zip(primes,products)):continue
        f=fmpz_poly(c);assert all(f.gcd(g).degree()==0 for g in den);fallbacks+=1
    write_json('evidence/structure.json',dict(common_D=str(common),v6_D=D,r11_D=total(ours),endpoint_factors=exceptions,nonzero_resultant_pairs=len(den)*len(bank['numerator']),exact_fallback_rows=fallbacks))
    state['common_D']=common
    write_json('inputs/union-master.json',state,compact=True)
    write_json('inputs/full-bank.json',bank,compact=True)

if __name__=='__main__': main()
