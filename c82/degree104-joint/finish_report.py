"""Report the candidate bound and actual warm-search outcomes."""
import csv,gzip,hashlib,json,re,time
from fractions import Fraction
from pathlib import Path
from checkpoint import decimal_out
from numerics import register,write_json
register('finish_report')
def read(path):
 p=Path(path)
 if not p.exists():p=Path(str(p)+'.gz')
 return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
r=read('RESULT.json');v=read('evidence/final-replay.json');cert=read('certificate.json');prov=read('FACTOR_PROVENANCE.json');finished=read('rounds/finished.json')
if finished['stop']=='wall or batch limit':
 finished['stop']='wall time budget: no new round started after 9.5 hours; final packet time reserved'
 write_json('rounds/finished.json',finished)
hi=Fraction(r['exact_upper']);lo=Fraction(r['exact_lower']);bar=Fraction(read('BAR.json')['bar'])
assert hi<Fraction(r['stated_rational'])
assert hashlib.sha256(Path('certificate.json').read_bytes()).hexdigest()==r['certificate_sha256']==v['certificate_sha256']
assert all(c['rejected'] for c in read('evidence/rejection-controls.json'))
r['final_exact_endpoint_matches_saved_best']=Fraction(v['bound']['upper']['mantissa'])*Fraction(2)**v['bound']['upper']['exponent']==hi
assert r['final_exact_endpoint_matches_saved_best']
r['final_exact_endpoint_below_frozen_bar']=hi<bar;r['final_replay_source']='evidence/final-replay.json';write_json('RESULT.json',r)
# Add full-coefficient matches in the inherited round-8 final LP as well.
master=read('prior_sources/round8-master.json')
for kind in ['denominator','numerator']:
 for row in prov[kind]:
  extra=[{'origin':'round-8 final LP master','name':other['name']} for other in master[kind] if row['coeffs']==other['coeffs']]
  row['all_full_coefficient_matches']=[m for m in row['all_full_coefficient_matches'] if m['origin']!='round-8 final LP master']+extra
write_json('FACTOR_PROVENANCE.json',prov)
start=read('evidence/start.json')['start_epoch'];records=[json.loads(x) for x in Path('evidence/compute.jsonl').read_text().splitlines()]
cpu=sum(x['cpu_seconds'] for x in records);wall=(time.time()-start)/3600;allowance=.01+.01*wall;peaks=[]
for p in Path('.').rglob('*.time'):
 m=re.search(r'(\d+)\s+maximum resident set size',p.read_text())
 if m:peaks.append({'file':str(p),'peak_rss_bytes':int(m.group(1))})
compute={'recorded_cpu_seconds':cpu,'recorded_core_hours':cpu/3600,'estimated_total_core_hours':cpu/3600+allowance,'unmeasured_allowance_core_hours':allowance,'wall_hours':wall,'largest_sampled_aggregate_rss_bytes':max(x.get('sampled_aggregate_peak_bytes',0) for x in records),'worker_peaks':peaks,'accounting':'Sum of disjoint supervised RUSAGE_CHILDREN deltas, including ps sampling. Estimate adds .01 core-hour setup plus .01 per elapsed hour for controller/setup/reporting.','single_threaded_blas_highs_flint':True,'maximum_simultaneous_numerical_workers':4,'allocation':'4 numerator generation/full-bank pricing, 2 CVP denominator; alternating, sequential LP and verification','nice_command':'nice -n 10','aggregate_rss_limit_bytes':3000000000}
write_json('COMPUTE.json',compute)
summary=[]
for p in sorted([*Path('rounds').glob('*search-*.json'),*Path('rounds').glob('*search-*.json.gz')]):
 d=read(p);summary.append({'file':str(p),'settings':d.get('settings'),'elapsed':d.get('elapsed'),'cpu_seconds':d.get('cpu_seconds'),'trials':d.get('trials'),'priced':d.get('priced'),'negative_candidates':len(d.get('negative_candidates',[])),'best_rc':d['best']['rc'] if d.get('best') else None})
write_json('SEARCH_SUMMARY.json',{'searches':summary,'rounds':finished})
curve=[json.loads(x) for x in Path('evidence/improvement-curve.jsonl').read_text().splitlines()]
with open('IMPROVEMENT_CURVE.csv','w') as out:
 w=csv.writer(out);w.writerow(['elapsed_hours','certified_upper','certificate','replay_source'])
 for row in curve:w.writerow([f"{(row['epoch']-start)/3600:.6f}",row['upper'],row['certificate'],row['replay_source']])
lines=[f"Shipped: candidate, unrefereed C82 < {r['stated_decimal']}; "+('the exact certified upper endpoint is below the frozen 0.2519744487 bar.' if hi<bar else 'the frozen bar was not reached; this is the best certified value.'),'',f"Certified enclosure: [{r['interval_lower']}, {r['interval_upper']}]. Exact upper endpoint: {hi}. The endpoint is strictly below the stated rational {r['stated_rational']}, using exact Fraction arithmetic.",'','| Comparator | Certified improvement (at least) |','| --- | ---: |']
for label,q in [('Round 9 printed 0.2519744488','0.2519744488'),('Round 8 printed 0.2519758217','0.2519758217'),('[#330](https://github.com/teorth/optimizationproblems/pull/330) earlier printed 0.2519923410 (requested comparator)','0.2519923410'),('[#280 v5](https://github.com/teorth/optimizationproblems/pull/280) printed 0.2519889614','0.2519889614')]:lines.append(f'| {label} | {decimal_out(Fraction(q)-hi,False)} |')
lines+=['','At the final public refresh, [#330](https://github.com/teorth/optimizationproblems/pull/330) had advanced to 0.2519744488, matching the round-9 baseline. The 0.2519923410 row preserves the requested historical comparator; #280 v5 still states 0.2519889614. This job made no external writes.','',f"The packet contains {len(cert['denominator'])} denominator and {len(cert['numerator'])} numerator factors. D={v['audit']['D']}; deg A={v['audit']['degree_A']}; {v['audit']['coprimality_pairs']} exact gcd pairs; {v['audit']['composed_roots']} composed roots. SHA256: {r['certificate_sha256']}.",'','Verification uses the inherited separately written (same agent) stdlib + python-flint verifier. It checks pinned bytes, integer coefficients, monic denominators, positive multiplicities, nonnegative rational powers, strict degree inequality, all numerator/denominator gcds, exact composition, root isolation and interval integration. Changed bytes, repinned zero multiplicity and repinned shared factor are rejected (evidence/rejection-controls.json). The Doche reduction and arithmetic backend are not formally verified; PROOF.md and NUMERICS.md give the argument and interval formulas. This result is candidate and unrefereed.','']
warm=read('rounds/warm.json');bank=read('prior_sources/round9-bank.json')
lines += ['The controller was interrupted once after a certified replay because a running original reader could not see an immutable bank compressed during execution. The storage change was reverted first, original bytes restored, and round 53 resumed after the certified pass without repeating generation. Numerical search and certificate arithmetic were unchanged. STATUS.md records the exact failure and recovery.', '', f"Our own round-9 scripts and separately written verifier were copied and reused: joint LP, numerical helpers, dual-weighted evaluation-lattice LLL numerator pricing, degree-104 monic CVP denominator search, full-bank pricing, mergers, controller, checkpoint code and rejection controls. Search starts from its final LP and dual, retaining {len(warm['denominator'])} denominator columns, {len(warm['numerator'])} active numerator columns and the complete rounds 8–9 bank of {len(bank['numerator'])} numerator and {len(bank['denominator'])} archive denominator factors. Round-9 certificate replay reproduced the supplied endpoint before search. BAR.json was written first.",'','The inherited standard alternation was retained. Numerator search uses the current dual, followed by joint LP, certification and full-bank repricing after moved solves; CVP then uses the updated dual. Numerator generation and full-bank pricing receive four workers and CVP two, sequentially, following the paying moves in round 9. First generation batches were measured solo under /usr/bin/time -l. BLAS, HiGHS and FLINT use one thread, via nice -n 10. Search settings/seeds/outcomes are retained in SEARCH_SUMMARY.json. Neither pricing nor CVP is claimed optimal.','',f"Stopping reason: {finished['stop']}. Completed {len(finished['history'])} alternating rounds starting at 52. A no-gain round is a complete alternation without a smaller certified endpoint. The 9.5-hour search cutoff reserves time for the final packet inside ten hours."]
recent=finished['history'][-3:];worth=any(Fraction(x.get('certified_gain','0'))>0 for x in recent) and 'no-gain' not in finished['stop']
lines += ['',('Another warm round is worth trying: the latest completed rounds still improved the certified endpoint when the time budget ended.' if worth else 'Another identical warm round is not recommended after three consecutive complete rounds without certified gain. This is not an optimality result.'),'Resume state: '+finished['state']+'; dual: '+finished['dual']+'. Use the full union bank.','', 'The improvement curve contains actual certified checkpoints, without fitting or extrapolation. Every checkpoint is in IMPROVEMENT_CURVE.csv and certificates/.','', '![Certified improvement curve](IMPROVEMENT_CURVE.png)','','| Elapsed hours | Certified upper endpoint |','| ---: | ---: |']
seen=set()
for i,row in enumerate(curve):
 hour=int((row['epoch']-start)/3600)
 if hour not in seen or i==len(curve)-1:lines.append(f"| {(row['epoch']-start)/3600:.3f} | {row['upper']} |");seen.add(hour)
lines += ['',f"Compute: {cpu/3600:.4f} recorded core-hours; {compute['estimated_total_core_hours']:.4f} estimated total with controller/setup allowance; {wall:.3f} wall hours. Largest sampled aggregate RSS {compute['largest_sampled_aggregate_rss_bytes']:,} bytes (3 GB limit). COMPUTE.json gives measured peaks and accounting. evidence/process-cleanup.json records the final ps check.",'','Factor provenance below uses full coefficient equality, not names. FACTOR_PROVENANCE.json includes exact weights and every match to the inherited sources. “Generated in this continuation” means absent from those compared coefficient banks; no novelty judgment is made.','','| Denominator | Degree | Multiplicity | Full coefficient matches |','| --- | ---: | ---: | --- |']
def origins(row):return '; '.join(dict.fromkeys(m['origin'] for m in row['all_full_coefficient_matches'])) or 'generated in this continuation'
for row in prov['denominator']:lines.append(f"| {row['name']} | {len(row['coeffs'])-1} | {row['multiplicity']} | {origins(row)} |")
lines+=['','| Numerator | Degree | Full coefficient matches |','| --- | ---: | --- |']
for row in prov['numerator']:lines.append(f"| {row['name']} | {len(row['coeffs'])-1} | {origins(row)} |")
lines += ['', 'CERTIFICATE_ENCODING.md records equal fractions with both numerator and denominator doubled for each 15- or 16-digit q_rational numerator; exact rational checks remain unchanged.','', 'No vidigoat/optimization-records Python was downloaded, copied, imported or executed. PYTHON_BLOBS.json records the git blob hash of every .py in this directory and compares against every blob in complete metadata-only trees at 197962c, 3a7a84f, 79ce0df and 191064e; none matches and none imports their modules. Their supplied certificate JSON is data only. Credits: Doche, Grinsztajn, Epi, Pinho PR301/#330, Patankar #280 v3/v4/v5, and our rounds 5–9 lineage; THIRD_PARTY_NOTICE.md supplies inherited credits.','', 'PRIOR_ART.md records inherited and refreshed read-only public sources. No novelty judgment is made. Nothing was committed, pushed, posted, uploaded or sent. All outputs are in this job directory. Historical files are compressed as needed; all certified best packets and exact replays remain retained.','', 'Reproduce the best bound:','','```sh',f"./run_local.sh verify_best.py --certificate certificate.json --target {r['stated_decimal']} --precision 256 --tol 1e-13 --out evidence/reproduced-best.json",'```','','REPRODUCE.md gives the warm replay, search, controls and source-inventory commands.']
Path('REPORT.md').write_text('\n'.join(lines)+'\n')
with open('STATUS.md','a') as f:f.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S')+' '+lines[0]+' Stop: '+finished['stop']+f'; {cpu/3600:.4f} recorded core-hours.\n')
print(lines[0])
