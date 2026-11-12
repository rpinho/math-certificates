"""Copy our round-8 implementation and warm data; never fetch foreign Python."""
from pathlib import Path
import json,shutil,time,os
src=Path('../c82r8')
for d in ['evidence','logs','rounds','prior_sources','certificates']:Path(d).mkdir(exist_ok=True)
for name in ['numerics.py','joint_lp.py','cvp_search.py','add_columns.py','numerator_search.py','lll_numerators.py','merge_numerators.py','rejection_controls.py','supervise.py','checkpoint.py','run_cg.py','source_inventory.py','verify_public.py','verify_best.py','verify_v5.py','PROOF.md','NUMERICS.md','THIRD_PARTY_NOTICE.md','run_local.sh','union-input.json']:
    shutil.copyfile(src/name,name)
for p in (src/'prior_sources').iterdir():
    assert p.suffix!='.py'
    if p.is_file():shutil.copyfile(p,Path('prior_sources')/p.name)
for name in ['PRIOR_ART.md','REPORT.md','SEARCH_SUMMARY.json','COMPUTE.json','FACTOR_PROVENANCE.json','CERTIFICATE_ENCODING.md']:
    shutil.copyfile(src/name,Path('evidence')/('round8-'+name))
shutil.copyfile(src/'certificate.json','prior_sources/round8-certificate.json')
shutil.copyfile(src/'rounds/finished.json','evidence/round8-finished.json')
shutil.copyfile(src/'certificate.json','certificate.json')
shutil.copyfile(src/'evidence/final-replay.json','evidence/round8-replay.json')
f=json.loads((src/'rounds/finished.json').read_text())
shutil.copyfile(src/f['state'],'rounds/warm.json')
shutil.copyfile(src/f['dual'],'rounds/warm-dual.npz')
shutil.copyfile(src/'RESULT.json','evidence/round8-RESULT.json')
Path('evidence/start.json').write_text(json.dumps({'start_epoch':Path('BAR.json').stat().st_mtime,'start_iso':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'maximum_hours':10})+'\n')
Path('evidence/pids.jsonl').write_text(json.dumps({'pid':os.getpid(),'kind':'bootstrap'})+'\n')
Path('CERTIFICATE_ENCODING.md').write_text('# Equal-fraction encodings\n\nFor reduced q_rational numerators of 15 or 16 digits, write the numerator and denominator doubled; equality is checked with Fraction. Inherited packet encodings: evidence/round8-CERTIFICATE_ENCODING.md.\n')
Path('REPORT.md').write_text('Shipped: inherited candidate, unrefereed C82 < 0.2519758217; warm continuation is starting and the 0.2519758216 frozen bar is not yet met.\n\nThe inherited certificate will be replayed locally before search.\n')
Path('BASELINES.json').write_text(json.dumps({'applicable':False,'reason':'Deterministic mathematical upper-bound construction, no predictive score. Baseline is round-8 exact certificate replay; public comparison certificate v5 is inherited data.'},indent=2)+'\n')
with open('STATUS.md','a') as out:out.write('\nCopied and reused our round-8 numerical helpers, joint LP, LLL numerator search, CVP search, mergers, controller, separately written verifier, rejection controls and source-inventory method, plus full union bank and final LP state/dual. Inherited public data only; no third-party Python. Four numerator workers and two denominator workers, alternating, with sequential LP/verification.\n')
