from pathlib import Path
import json,hashlib,subprocess
root=Path('/workspace/ref_hugo_HB01')
audit=json.load(open(root/'audit.json'));cover=json.load(open(root/'covers.json'));dfs=json.load(open(root/'dfs.json'));extra=json.load(open(root/'extra_audit.json'));controls=json.load(open(root/'controls.json'))
assert len(cover)==len(dfs)==len(extra['rows'])==15
assert all(r['returncode']==0 for r in cover.values())
vals=[json.loads(r['stdout']) for r in cover.values()]
complete={k:json.loads(r['stdout']) for k,r in dfs.items() if r.get('returncode')==0}
capped=[k for k,r in dfs.items() if 'status' in r]
claimed=json.load(open(root/'evidence/HB01/FROZEN_CLAIM_COHORT_RUN6.json'))['rows']
for k,v in complete.items():assert v['optimum']==claimed[k]['exact_optimum']
primals_new={k:c['exact_optimum'] for k,c in claimed.items() if c['exact_optimum']>max(c['historical_BKS_B7'],c['best_paper_neural_B1_B7'])}
summary=dict(status='FIFTEEN SCOPED OPTIMA VERIFIED',cover_cases=len(cover),cover_labels=sum(v['labels'] for v in vals),cover_successor_checks=sum(v['arcs'] for v in vals),complete_elementary_cases=list(complete),elementary_caps=capped,complete_elementary_prefixes=sum(v['prefixes'] for v in complete.values()),greedy_optima=[k for k,r in extra['rows'].items() if r['greedy']['score']==r['exact']],greedy_above_paper_neural=[k for k,r in extra['rows'].items() if r['greedy']['score']>claimed[k]['best_paper_neural_B1_B7']],greedy_seconds=sum(r['greedy']['seconds'] for r in extra['rows'].values()),raw_float_edge_discrepancies=sum(len(r['float64_edge_differences']) for r in audit['cases'].values()),rewards_above_all_paper_BKS_neural=primals_new,other_rewards_previously_in_paper=15-len(primals_new),all33_bound_to_official_single_day_set=len(extra['official_single_day_cases'])==33,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'referee.cpp',root/'audit.py',root/'controls.py',root/'run_covers.py',root/'run_dfs.py',root/'greedy.cpp',root/'extra_audit.py']})
(root/'SUMMARY.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
