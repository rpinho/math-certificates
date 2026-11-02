"""Bind certificate/receipt/coverage, audit exact coverage and reject corruptions.
The endpoint auditor is copied unchanged from the independently written review.
"""
import argparse,copy,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from review_coverage_audit import audit
p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('receipt');p.add_argument('--reference');p.add_argument('--output',required=True);a=p.parse_args()
r=json.loads(Path(a.receipt).read_text());coverpath=Path(a.receipt+'.cover.json');cover=json.loads(coverpath.read_text())
assert r['status']=='PASS'
assert hashlib.sha256(Path(a.certificate).read_bytes()).hexdigest()==r['sha256']
assert hashlib.sha256(coverpath.read_bytes()).hexdigest()==r['coverage_sha256']
result=dict(original=audit(a.certificate,cover),controls=[])
variants={
 'deleted-leaf':lambda c:c.pop(len(c)//2),
 'shifted-endpoint':lambda c:c[0].__setitem__(1,str(F(c[0][1])+F(1,10**30))),
 'wrong-parent':lambda c:c[0].__setitem__(0,c[0][0]+1),
 'nonpositive-lower':lambda c:c[0].__setitem__(3,'-1e-30')}
for name,mut in variants.items():
 c=copy.deepcopy(cover);mut(c)
 try:audit(a.certificate,c)
 except AssertionError as e:result['controls'].append(dict(name=name,rejected=True,reason=str(e)))
 else:raise AssertionError('corrupted coverage accepted: '+name)
if a.reference:
 old=json.loads(Path(a.reference+'.cover.json').read_text());ref=json.loads(Path(a.reference).read_text())
 assert ref['sha256']==r['sha256'] and ref['bound']==r['bound'] and ref['tests']==r['tests']
 key=lambda row:(row[0],F(row[1]),F(row[2]))
 assert sorted(old,key=key)==sorted(cover,key=key),'parallel and sequential leaves differ'
 result['identical_to_sequential_coverage']=True
result.update(certificate_sha256=r['sha256'],coverage_sha256=r['coverage_sha256'],auditor_sha256=hashlib.sha256(Path('review_coverage_audit.py').read_bytes()).hexdigest(),valid=True)
Path(a.output).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
