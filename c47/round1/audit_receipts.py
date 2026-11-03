"""Cross-check frozen inputs, independent exact receipts and finite parameters."""
import hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text())
v=load('logs/half59-exact.json'); c=load('certificates/half59.json'); m=load('certificates/half59-measure.json'); p=load('certificates/parent-117-measure.json'); e=load('logs/half-extraction.json'); f=load('logs/half59-finite.json'); u=load('certificates/half59-measure.check2.json')
assert len(m['pts'])==59 and m['pts']==[p['pts'][i] for i in e['selected_indices_zero_based']]
assert F(m['Py'])*2==F(p['Py']) and m['Px']==p['Px'] and m['lam']==p['lam']
assert all(0<=F(a[1])<F(m['Py']) for a in m['pts'])
assert c['measure']==m and c['measure_sha256']==hashlib.sha256((root/'certificates/half59-measure.json').read_bytes()).hexdigest()
assert v['artifact_sha256']==hashlib.sha256((root/'certificates/half59.json').read_bytes()).hexdigest()
assert v['verifier_sha256']==hashlib.sha256((root/'verify_exact.py').read_bytes()).hexdigest()=='f01475b149795e25821fc5c434ee2d535b941967897c758dbdc1391e8ae3edfe'
q=F(v['ratio']);assert q==F(int(u['ratio_num']),int(u['ratio_den']))==F(v['area'])/F(v['mass'])
assert math.floor(q*100000)==170311 and math.floor(q*10000)==17031
assert len(c['witnesses'])==559 and u['rectangles']==33356
controls=load('logs/rejection-controls-half59.json');assert len(controls)==7 and all(a['returncode']==1 and a['output']['result']=='FAIL' for a in controls)
h,N,eps=f['boundary_cells'],f['block_side_cells'],F(f['smear_radius'])
R=max(F(w['radius']) for w in c['witnesses']);s=F(v['min_strict_mass_slack']);lam=F(m['lam'])
assert h*min(F(m['Px']),F(m['Py']))>R and eps>0
assert all(4*lam*((F(w['radius'])+eps)**2-F(w['radius'])**2)<s for w in c['witnesses'])
assert F(f['finite_ratio_lower_bound'])==q*F((N-2*h)**2,N*N)>F(170311,100000)
assert F(f['finite_function_L1_norm'])==N*N*F(v['mass']) and f['finite_atom_count']==N*N*59
b=load('sources/tomar-v5/lowerbound/c2lower_1p70272.check2.json');assert F(int(b['ratio_num']),int(b['ratio_den']))==F('482167717377842991882283179477574801392641890014291050323/283174368139841919615520431313000857449005056000000000000')
for left,right in [('sources/hf-fresh.py','sources/tomar-v5/lowerbound/search/hf.py'),('sources/check_exact2-fresh.py','sources/tomar-v5/lowerbound/check_exact2.py')]:assert (root/left).read_bytes()==(root/right).read_bytes()
result=dict(result='PASS',fixed_measure_no_retuning=True,source_hashes_match=True,upstream_fraction_agrees=True,corruptions_rejected=7,finite_witness_smear_margins_checked=559,claim='170311/100000',artifact_sha256=v['artifact_sha256'],status='candidate, unrefereed')
(root/'logs/receipt-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
