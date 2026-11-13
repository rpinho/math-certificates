"""Reuse our round-9 implementation and warm data; foreign Python is excluded."""
from pathlib import Path
import json,shutil,time,os
src=Path('../c82r9')
for d in ['evidence','logs','rounds','prior_sources','certificates']:Path(d).mkdir(exist_ok=True)
for name in ['numerics.py','joint_lp.py','cvp_search.py','add_columns.py','numerator_search.py','lll_numerators.py','merge_numerators.py','rejection_controls.py','supervise.py','checkpoint.py','run_cg.py','source_inventory.py','verify_public.py','verify_best.py','verify_v5.py','public_reads.py','compact_history.py','cleanup.py','plot_curve.py','PROOF.md','NUMERICS.md','THIRD_PARTY_NOTICE.md','run_local.sh','union-input.json']:
    shutil.copyfile(src/name,name)
for p in (src/'prior_sources').iterdir():
    assert p.suffix!='.py'
    if p.is_file():shutil.copyfile(p,Path('prior_sources')/p.name)
for name in ['PRIOR_ART.md','REPORT.md','SEARCH_SUMMARY.json','COMPUTE.json','FACTOR_PROVENANCE.json','CERTIFICATE_ENCODING.md','RESULT.json']:
    shutil.copyfile(src/name,Path('evidence')/('round9-'+name))
shutil.copyfile(src/'certificate.json','prior_sources/round9-certificate.json')
shutil.copyfile(src/'rounds/finished.json','evidence/round9-finished.json')
f=json.loads((src/'rounds/finished.json').read_text())
shutil.copyfile(src/f['state'],'rounds/warm.json')
shutil.copyfile(src/f['dual'],'rounds/warm-dual.npz')
shutil.copyfile(src/f['state'],'prior_sources/round9-master.json')
shutil.copyfile(src/'prior_sources/union-factor-bank.json','prior_sources/round9-bank.json')
shutil.copyfile(src/'certificate.json','certificate.json')
Path('evidence/start.json').write_text(json.dumps({'start_epoch':Path('BAR.json').stat().st_mtime,'start_iso':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'maximum_hours':10})+'\n')
Path('evidence/pids.jsonl').write_text(json.dumps({'pid':os.getpid(),'kind':'bootstrap'})+'\n')
Path('CERTIFICATE_ENCODING.md').write_text('# Equal-fraction encodings\n\nFor reduced q_rational numerators of 15 or 16 digits, store numerator and denominator doubled; exact Fraction arithmetic is unchanged. Inherited encodings: evidence/round9-CERTIFICATE_ENCODING.md.\n')
Path('REPORT.md').write_text('Shipped: inherited candidate, unrefereed C82 < 0.2519744488; the frozen 0.2519744487 bar has not yet been met.\n\nWarm continuation starting; inherited certificate will be replayed locally before search.\n')
Path('BASELINES.json').write_text(json.dumps({'applicable':False,'reason':'Deterministic mathematical upper-bound construction, no predictive score. Baseline: exact local replay of round 9 certificate.'},indent=2)+'\n')
os.chmod('run_local.sh',0o755)
with open('STATUS.md','a') as out:out.write('\nCopied and reused our round-9 joint LP, numerical helpers, LLL numerator pricing, CVP denominator search, full-bank pricing, mergers, controller, checkpoint code, separately written verifier, controls and source inventory. Warm final LP/dual and full rounds 8–9 coefficient bank retained. Four numerator workers and two CVP workers alternate; sequential solve/verification.\n')
