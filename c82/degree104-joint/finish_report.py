"""Write the result, factor credits, compute use and stopping reason."""
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import time
from numerics import register, write_json

if __name__=='__main__':
    register('finish_report')
    result=json.loads(Path('RESULT.json').read_text())
    provenance=json.loads(Path('FACTOR_PROVENANCE.json').read_text())
    replay=json.loads(Path('evidence/best-replay.json').read_text())
    compute=[json.loads(s) for s in Path('evidence/compute.jsonl').read_text().splitlines()]
    tracked=sum(x['cpu_seconds'] for x in compute)
    bootstrap=json.loads(Path('rounds/union-lp.json').read_text())['seconds']+json.loads(Path('evidence/public-v3-replay.json').read_text())['seconds']
    summary={'tracked_subprocess_cpu_seconds':tracked,'tracked_subprocess_core_hours':tracked/3600,
        'bootstrap_single_thread_wall_seconds_upper_estimate':bootstrap,
        'estimated_total_core_hours':(tracked+bootstrap)/3600,
        'small_unmeasured_overhead_allowance_core_hours':0.01,
        'wall_hours':(time.time()-json.loads(Path('evidence/start.json').read_text())['start_epoch'])/3600,
        'max_numerical_workers':3,'blas_threads':1,'nice_invocation':10,'effective_nice':20}
    write_json('COMPUTE.json',summary)
    controls=json.loads(Path('evidence/rejection-controls.json').read_text())
    assert all(x['rejected'] for x in controls)
    inventory=json.loads(Path('PYTHON_BLOBS.json').read_text())
    assert inventory['all_python_blobs_distinct_from_every_blob_in_both_trees'] and inventory['none_imports_foreign_modules']
    finished=json.loads(Path('rounds/finished.json').read_text())
    batches=[]
    for path in sorted(Path('rounds').glob('search-*-*.json'),key=lambda p:tuple(map(int,p.stem.split('-')[1:]))):
        x=json.loads(path.read_text())
        batches.append({'batch':path.stem,'starts':x['trials'],'root_priced':x['priced'],'negative':len(x['negative_candidates']),
            'best_rc':(x['best'] or {}).get('rc'),'cpu_seconds':x['cpu_seconds']})
    write_json('SEARCH_SUMMARY.json',{'batches':batches,'loop':finished,'all_rounds':json.loads(Path('rounds/all-rounds.json').read_text())})
    headline=f"Shipped: candidate, unrefereed C82 < {result['interval_upper']}, with a separately written (same agent) interval-verified certificate; frozen B < 0.2520500000 target {'met' if result['below_frozen_bar'] else 'not met'}."
    lines=[headline,'',
        f"Certified enclosure: B ∈ [{result['interval_lower']}, {result['interval_upper']}]. The certified gain over 0.2520591386 is at least {result['certified_gap_to_public_at_least']}. Exact dyadic upper endpoint < 5041/20000: {result['below_frozen_bar']}. RESULT.json saves the exact Fraction comparison; evidence/best-replay.json saves H, J, B, outward endpoints and integration details.",'',
        f"The final public-source refresh found [PR #330](https://github.com/teorth/optimizationproblems/pull/330) now prints 0.2520179248. The final bound is below that live printed comparator by at least {result['certified_gap_to_live_public_at_least']}. A concise candidate claim is C82 < {result['publication_bound']}; RESULT.json checks its exact rational margin. The final replay against 0.2520500000 passed in evidence/final-bar-replay.json.",'',
        'This is a candidate arithmetic construction under the inherited Doche reduction, unrefereed. The verifier was separately written (same agent). It imports stdlib and python-flint only, composes polynomials exactly, isolates all composed roots, checks positive integer denominator multiplicities, nonnegative rational numerator powers, strict degree inequality, every active numerator/denominator gcd, and bounds the integral with interval arithmetic. It shares no helper with the search. The reduction and arithmetic backend were not formalized in this job.','',
        'Before searching, our verifier replayed V. Patankar (@vidigoat) #280 v3: B ∈ [0.2520591385259547806692, 0.2520591385259548085535], H = 0.2520394006582629915263. This public-data reproduction is credited to Patankar; evidence/public-v3-replay.json records it. The requested JSON hash matched 00125f6984ad2646a79d8782ee38f5161bd24c17d4899e4af74ff3e529ba1dbe. Only the expected hash pin was changed in our copied round-5 verifier.','',
        'BAR.json was frozen before the union solve. The standard full union master used 7 degree-104 denominators and all 895 distinct certificate/public-bank numerators on N=524288 points. Grid B = 0.25205913844096395; its frozen certified upper endpoint was 0.2520591385259580091897, slightly worse than the original public replay due to weight freezing. The incumbent was restored to the public certificate before column generation. No meaningful gain came from union reweighting alone.','',
        'Column generation reused our own ../c82r5 numerics.py, joint_lp.py, cvp_search.py, add_columns.py and numerator_search.py. Changes were the r6 label/provenance and complete union bank path. Our own verifier, rejection controls and numerical documentation were also reused. New orchestration saved exact-weight certificates after each improved solve. Standard restricted masters removed zero numerator columns but all 895 public numerators remained available to complete-dual pricing. All union denominators remained warm starts.','',
        'The inherited CVP settings were degree 104, H=X(X−1)P4 residue restriction, 1024 stratified weighted-evaluation samples, 380-bit evaluation arithmetic, exact integer Gram LLL (delta .99), 16 retained Schnorr–Euchner points, four million nodes and up to eight IRLS steps. Two single-threaded 240-second batches ran against each dual. Floating grid objectives and negative prices are heuristic; the interval-replayed frozen certificate alone supports the headline bound. No closest-vector optimality claim is made. After the original-order search stopped with three no-gain rounds (4–6), the continuation prioritized and rotated positive-weight warm starts between workers, keeping all union denominators available and retaining the same algorithms and numerical defaults. Original loop summaries are in rounds/original-finished.json and rounds/original-progress.json.','',
        'SEARCH_SUMMARY.json and the per-round states retain the search settings, prices, actual LP gains and CPU use.']
    lines.extend(['','Full coefficient comparison determines every factor attribution; names are labels only.','',
        'All requested rejection controls passed by rejecting changed bytes, zero multiplicity with a repinned hash, and a shared numerator/denominator factor with a repinned hash. See evidence/rejection-controls.json and individual logs. The final bound also has an exact upper-endpoint comparison with the stated rational in RESULT.json.','',
        f"Final certificate: {replay['audit']['denominator_factors']} monic degree-104 denominator factors, {replay['audit']['numerator_factors']} numerator factors, D={replay['audit']['D']}, deg A={replay['audit']['degree_A']}. FACTOR_PROVENANCE.json records every coefficient array, exact weight, and all full-coefficient matches against #280 v3, our round 5, and the earlier public bank.",'',
        '| Denominator | Coefficient provenance | Integer multiplicity |','| --- | --- | ---: |'])
    for r in provenance['denominator']:lines.append(f"| {r['name']} | {r['origin']} | {r['multiplicity']} |")
    lines.extend(['','Numerator provenance, by full coefficient comparison:',''])
    for r in provenance['numerator']:
        sources='; '.join(sorted({m['origin'] for m in r['all_full_coefficient_matches']})) or 'new here'
        lines.append(f"- {r['name']}: {sources}; q={r['q_rational']}.")
    lines.extend(['',
        'Method/factor credit: Doche (perturbed-polynomial construction); Grinsztajn and Épi (earlier factors); R. Pinho PR #301 (joint LP, residue restriction and prices), our own round-5 factors; V. Patankar PR #280 (public JSON factors and weighted-CVP/product-start method). No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. All third-party retrievals from that repository were JSON data or GitHub tree metadata. No novelty judgment is made, as requested.','',
        'PRIOR_ART.md records the scoped source survey: official raw 82a table, relevant open PR bodies (#242, #280, #301, #330), updated-first repository searches, BakeLab/Épi, both DeepMind repositories, OpenAI math, kisonecat, plasma-ai/erdos, EinsteinArena, primary Doche paper, arXiv:2601.18978v2 and 2609.39505, and focused recent-paper/community queries. The final refreshed official table and open-PR reads remain in prior_sources/*-final.*. This is a scoped public comparison, not a worldwide priority judgment.','',
        f"Compute: measured orchestration child CPU {summary['tracked_subprocess_core_hours']:.4f} core-hours; estimated total {summary['estimated_total_core_hours']:.4f} core-hours using single-threaded bootstrap elapsed time, plus at most about 0.01 core-hours of short setup/control/accounting work. Wall time {summary['wall_hours']:.3f} hours. At most three numerical workers, BLAS/FLINT/HiGHS single-threaded, nice -n 10 (effective nice 20 inherited). Mini load was checked. COMPUTE.json and evidence/pids.jsonl retain the accounting. Final process inspection is in evidence/process-cleanup.json. Artifacts stay below 50 MB. All writes stayed in this job directory; no commits, pushes, PRs, posts, uploads or messages were made.",'',
        'Reproduce final certification:','', '```sh',
        'export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1',
        'export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1',
        'nice -n 10 python3 verify_best.py --certificate certificate.json --target 0.2520500000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json',
        '```','',
        'REPRODUCE.md gives public replay, full-union solve, CVP loop and rejection-control commands. NUMERICS.md gives the inherited verifier enclosure formulas.','',
        'Every local .py git blob was computed with git hash-object and compared with every blob in the complete GitHub trees at vidigoat/optimization-records@197962c9610f583e9bc56efe37bfb994c1eeb834 and @3a7a84fec9c64ae426f06a5f52597c84b3453ba0. None matches any blob in either tree. AST import inspection confirms none imports their modules. PYTHON_BLOBS.json contains all filenames, hashes, and imports.','',
        'The complete per-file git-blob inventory is in PYTHON_BLOBS.json.'])
    lines.extend(['',f"Stopping reason: {finished['stop']}. The final dual/state and per-round gains are in rounds/finished.json.",'',
        ('Another identical round: no, not recommended now. The final three rotated warm-start rounds found no useful columns. This is a scoped search plateau, not an optimality result. A later round with broader denominator starts or a changed proposal distribution may be useful; that follow-up was not tested here.' if finished['stop']=='three no-gain rounds' else 'Another round: yes, the last search batch ended at its round or wall budget rather than a three-round plateau. Continue from the saved final dual and master with the current best certificate retained.')])
    Path('REPORT.md').write_text('\n'.join(lines)+'\n')
    with open('STATUS.md','a') as f:f.write('\n'+headline+'\nFinal stop: '+finished['stop']+'. See REPORT.md.\n')
    print(headline)
