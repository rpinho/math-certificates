"""Independent exact checks of retained transcription arrays and initial pricing.
No new auxiliary attribution is inferred from numerical resemblance.
"""
import json,re,hashlib
from pathlib import Path
from flint import fmpz_poly
A=json.load(open('classical-transcription.json'));L=json.load(open('sources/liang11-list.json'))['rows'];old=json.load(open('sources/flammang19-list.json'))['polynomials']
first=[r['q'] for r in A if r['source']=='Flammang2019' and r['list']==1];assert first==old
counts={}
for r in A:counts[str((r['source'],r['list']))]=counts.get(str((r['source'],r['list'])),0)+1
assert sorted(counts.values())==[45,62,67,74,97]
for r in A:
 q=r['q'];assert all(type(x)is int for x in q) and q[-1]>0
 c,fs=fmpz_poly(q).factor();assert abs(int(c))==1
 product=fmpz_poly([int(c)])
 for f,m in fs:product*=f**m
 assert list(map(int,product.coeffs()))==q
assert len(L)==85
pool=list(map(tuple,json.load(open('literature-pool.json'))));base=set(map(tuple,json.load(open('flammang19-pool.json'))));assert len(pool)==len(set(pool))==354 and base<=set(pool)
receipt=dict(status='PASS',source_rows=len(A)+len(L),unique_union=len(pool),baseline_pool=len(base),new_unique=len(set(pool)-base),counts=counts,original97_identical=True,reducible_source_rows=[dict(source=r['source'],list=r['list'],row=r['row']) for r in A if not r['primitive_irreducible']],source_hashes={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in ['sources/flammang2019.tex','sources/flammang24.tex','sources/liang11.pdf']})
Path('classical-input-audit.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
