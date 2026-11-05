"""Report the certified bound, coefficient provenance, compute and stopping reason."""
from pathlib import Path
from fractions import Fraction
import json,time,os
from checkpoint import decimal_out,endpoint
from numerics import register,write_json
register('finish_report')
r=json.loads(Path('RESULT.json').read_text());replay=json.loads(Path('evidence/best-replay.json').read_text());p=json.loads(Path('FACTOR_PROVENANCE.json').read_text())
finished=json.loads(Path('rounds/finished.json').read_text())
compute=[json.loads(l) for l in Path('evidence/compute.jsonl').read_text().splitlines()]
# The resume wrapper also measures its complete child loop. Use the detailed
# child records once, rather than adding this inclusive aggregate a second time.
compute=[x for x in compute if (x.get('args') or [None])[0]!='run_cg.py']
cpu=sum(x['cpu_seconds'] for x in compute)
pid_records=[json.loads(l) for l in Path('evidence/pids.jsonl').read_text().splitlines()]
old_starts=[x['time'] for x in pid_records if x.get('kind')=='cvp' and x.get('pid') in [96330,96331] and 'time' in x]
resume_start=min(x['time'] for x in pid_records if x.get('kind')=='resume_column_generation')
recovered=sum(x['cpu_seconds'] for x in compute if x.get('kind')=='interrupted_cvp_pair_recovered')
missing_upper=max(0,2*(resume_start-min(old_starts))-recovered)
summary={'tracked_subprocess_cpu_seconds':cpu,'tracked_core_hours':cpu/3600,'interrupted_search_unmeasured_cpu_seconds_upper_bound':missing_upper,'total_core_hours_conservative_upper_bound':(cpu+missing_upper)/3600+0.01,'additional_short_setup_reporting_allowance_core_hours':0.01,'wall_hours':(time.time()-json.loads(Path('evidence/start.json').read_text())['start_epoch'])/3600,'maximum_numerical_workers':2,'maximum_allowed_cores':3,'blas_threads':1,'highs_threads':1,'flint_threads':1,'nice_invocation':10,'effective_nice':os.getpriority(os.PRIO_PROCESS,0),'note':'Detailed child CPU records counted once; wrapper aggregate excluded. Interrupted round-one CPU uses saved process_time lower bounds; conservatively bound missing tails by two cores until resume. Short setup/reporting allowance separate.'}
write_json('COMPUTE.json',summary)
lo=Fraction(r['exact_lower']);hi=Fraction(r['exact_upper'])
scale=10**10;publication=Fraction((hi.numerator*scale)//hi.denominator+1,scale)
if publication==hi:publication+=Fraction(1,scale)
r.update({'publication_bound':f'{float(publication):.10f}','publication_rational':str(publication),'exact_upper_below_publication_bound':hi<publication,'exact_publication_margin':str(publication-hi),'exact_gap_to_ours':str(Fraction('0.2519964890')-hi),'exact_gap_to_pr280_v4':str(Fraction('0.2520079724')-hi),'exact_margin_to_bar':str(Fraction('0.2519900000')-hi)})
write_json('RESULT.json',r)
batches=[]
for path in sorted(Path('rounds').glob('search-*-*.json'),key=lambda x:tuple(map(int,x.stem.split('-')[1:]))):
    x=json.loads(path.read_text());batches.append({'batch':path.stem,'starts':x['trials'],'priced':x['priced'],'negative_candidates':len(x['negative_candidates']),'best_rc':(x['best'] or {}).get('rc'),'cpu_seconds':x['cpu_seconds'],'settings':x['settings']})
write_json('SEARCH_SUMMARY.json',{'batches':batches,'loop':finished})
headline=f"Shipped: candidate, unrefereed C82 < {r['publication_bound']}, certified upper endpoint {r['interval_upper']}; frozen B < 0.2519900000 target "+('met.' if r['below_frozen_bar'] else 'not met.')
lines=[headline,'',f"Certified B ∈ [{r['interval_lower']}, {r['interval_upper']}]. Exact dyadic endpoint < {publication}: {hi<publication}. Exact endpoint < 25199/100000: {r['below_frozen_bar']}. RESULT.json contains the exact Fraction comparisons and margins.",'',f"Gap below our printed round-6 0.2519964890: at least {r['gap_to_ours_at_least']}. Gap below Patankar #280 v4 0.2520079724: at least {r['gap_to_pr280_v4_at_least']}. A positive gap means the certified endpoint is smaller. No novelty judgment is made, as requested.",'',
'This is a candidate, unrefereed Doche construction. The interval verifier was separately written (same agent), uses stdlib + python-flint only, and imports no search helper. It checks exact integer polynomial composition, positive integer denominator multiplicities, nonnegative exact rational numerator powers, strict degree inequality, all active numerator/denominator gcds, certified composed-root isolation and interval integration. The Doche reduction and arithmetic backend are not formalized here. PROOF.md gives the inherited mathematical argument; NUMERICS.md describes the enclosure formulas.','',
f"Final certificate: {replay['audit']['denominator_factors']} denominator factors, {replay['audit']['numerator_factors']} numerators, D={replay['audit']['D']}, deg A={replay['audit']['degree_A']}; {replay['audit']['coprimality_pairs']} gcd pairs and {replay['audit']['composed_roots']} composed roots. Exact q_rational values are unchanged by equal-fraction encoding; CERTIFICATE_ENCODING.md lists the doubled encodings. Certificate SHA256: {r['certificate_sha256']}.",'',
'Before the union solve, both inputs were replayed locally with our separately written verifier. Our round-6 release gives upper endpoint 0.2519964889882011727026; Patankar v4 gives B = 0.25200797232842968… . See evidence/round6-replay.json and evidence/pr280-v4-replay.json. The v4 JSON SHA256 matches c1981f1c4f5e1813f625c54ce952e9b5fa210f2cccbd5ac832d2a41f12ccc72f.','',
'BAR.json was written before step 1. The complete joint master used the union of round-6 final factors, Patankar v4, the round-6 union bank and all coefficient dictionaries/candidate factors found in saved round-6 states. There are 104 initial denominator arrays and 913 numerator arrays. The inherited N=524288 grid, HiGHS simplex and full-grid row generation were used. rounds/union-lp.json records its numerical objective; rounds/union-replay.json certifies its exact frozen weights.','',
'Our own c82r6/c82r5 numerics.py, joint_lp.py, cvp_search.py, add_columns.py, numerator_search.py, run_cg.py, rejection controls, verifier and numerical notes were copied and reused. The core algorithms/defaults were preserved. The initial full-matrix np.column_stack copy hit shared-memory thrashing for over 11 minutes before any LP solve (8 GB footprint); the LP file was reverted, then retried with a single column-contiguous raw-log matrix and scaled active rows, retaining the same factors/grid/LP. STATUS.md and stack samples record the resource failure. Changes: r7 labels, complete union assembly, input-shape handling for historical JSON, degree-104 direct warm-start filtering, exact fraction encoding, updated checkpoint/provenance reporting and stopping on actual LP gain. The initial historical reader failed on a list-valued metadata JSON; the added launcher was reverted before that input correction. STATUS.md records it.','',
'The inherited weighted-CVP method uses degree 104; H=X(X−1)P4 residue restriction; 1024 stratified weighted-evaluation samples; 380-bit evaluation arithmetic; exact integer Gram LLL with delta .99; 16 retained Schnorr–Euchner points; four million nodes; up to eight IRLS steps. Two 240-second single-threaded workers use each new dual. All union degree-104 denominators are direct warm starts; degree-44/60 archive products are also starts. Complete numerator-bank pricing follows each round. Zero numerator columns are removed only from restricted masters, retaining the full bank for pricing. Search objectives and reduced costs are heuristic; only frozen, interval-verified certificates support the stated bound. No CVP optimality claim is made.','',
f"Stopping reason: {finished['stop']}. {len(finished['history'])} rounds. The per-round gains and final master/dual paths are in rounds/finished.json; SEARCH_SUMMARY.json records the batches.",'',
'The first attempt was interrupted during round-one searches (saved elapsed values about 206 and 204 seconds of the requested 240 seconds). Resume attempt 2 consumed their checkpointed candidate, re-solved and certified it, then continued full standard batches from round 2. Completed input replays, union solving and saved searches were not repeated; the original job clock was retained. Recovered interrupted-search CPU times are lower bounds, with the missing tails covered conservatively in COMPUTE.json.','',
('Another identical round is not recommended now: three consecutive rounds had LP gain below 1e-10. This is a plateau for these starts, duals and budgets, not an optimality result.' if finished['stop']=='three no-gain rounds' else 'Another round is worth considering: the wall/batch limit ended the loop before a three-round plateau. Continue from the saved master and dual.'),'',
'Factor provenance follows by full coefficient-array comparison; names are labels only. FACTOR_PROVENANCE.json retains every array, exact weight and all source matches.','',
'| Denominator | Provenance | Degree | Multiplicity |','| --- | --- | ---: | ---: |']
for x in p['denominator']:
    origins = sorted({m['origin'] for m in x['all_full_coefficient_matches']})
    label = x['origin']
    other = [s for s in origins if s != label]
    if other: label += ' (also ' + '; '.join(other) + ')'
    lines.append(f"| {x['name']} | {label} | {len(x['coeffs'])-1} | {x['multiplicity']} |")
lines+=['','Numerator provenance (full coefficient comparison):','']
for x in p['numerator']:
    origins='; '.join(sorted({m['origin'] for m in x['all_full_coefficient_matches']})) or 'new here'
    lines.append(f"- {x['name']}: {origins}; q={x['q_rational']}.")
controls=json.loads(Path('evidence/rejection-controls.json').read_text())
lines+=['',f"Rejection controls: changed bytes, zero multiplicity with repinned hash, and shared numerator/denominator factor with repinned hash all rejected: {all(x['rejected'] for x in controls)}. See evidence/rejection-controls.json and individual logs. The exact endpoint check against the stated rational is in RESULT.json.",'',
'No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. Every .py in this job directory, including generated pinned verifier copies, was hashed with git hash-object and compared against every blob in the complete GitHub trees at 197962c9610f583e9bc56efe37bfb994c1eeb834, 3a7a84fec9c64ae426f06a5f52597c84b3453ba0 and 79ce0dfb211a67ff7e387b58b0d19ff1d6accfba. None equals any blob in those trees; AST import inspection confirms none imports their modules. PYTHON_BLOBS.json lists every file/hash/import. Only JSON data and tree metadata were read from that repository.','',
'Method/factor credit: Doche; Grinsztajn and Epi; R. Pinho PR #301 joint LP, residue restriction and pricing; our earlier search factors; V. Patankar PR #280 weighted CVP, product starts and public coefficient JSON. THIRD_PARTY_NOTICE.md records data/method credit.','',
'PRIOR_ART.md records the scoped source review: live official table, open PRs #280/#330 and the open-PR list; updated-first repository search; seven lab/result repositories; inherited same-day awesome-list searches; Doche publisher page and recent primary arXiv/author sources; focused community searches. Final source refreshes are saved in prior_sources/*-final.*. The live merged table and open-PR values are public comparators, not a worldwide priority judgment.','',
f"Measured/recovered bootstrap and CG CPU: at least {summary['tracked_core_hours']:.4f} core-hours; conservative total upper estimate {summary['total_core_hours_conservative_upper_bound']:.4f} core-hours including unsaved interrupted-search tails and a 0.01 core-hour setup/reporting allowance. Wrapper aggregates are excluded to avoid double counting. Wall time {summary['wall_hours']:.3f} hours. Single-threaded BLAS/HiGHS/FLINT, nice -n 10 (effective nice {summary['effective_nice']}); two parallel CVP workers and no overlapping LP/replay. Mini load was checked. COMPUTE.json records accounting. Process cleanup is recorded in evidence/process-cleanup.json. All writes stayed in the job directory; no commits, pushes, PRs, posts, uploads or messages.",'',
'Reproduce the certificate at the stated rational:','','```sh',f"./run_local.sh verify_best.py --certificate certificate.json --target {r['publication_bound']} --precision 256 --tol 1e-13 --out evidence/reproduced-best.json",'```','',
'REPRODUCE.md gives input replay, union LP, CVP and rejection-control commands. Every numerical solve is checkpointed, with the best certified certificate retained incrementally.']
Path('REPORT.md').write_text('\n'.join(lines)+'\n')
print(headline)
