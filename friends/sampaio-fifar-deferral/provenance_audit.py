"""Read-only audit of freeze records, hashes, chronology and input restrictions."""
from pathlib import Path
import hashlib,json,datetime,ast
R=Path('/workspace/ref_sampaio_YB01');B=Path('/workspace/board_sampaio')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(p):return datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
families=['fit2025','fit2024','fit_conditional'];results=[]
for family in families:
    root=B/family;p=root/'FROZEN_SELECTION.json';record=json.loads(p.read_text());rows=[]
    freeze=datetime.datetime.fromisoformat(record['utc'])
    for name,digest in record['manifest'].items():
        s=root/name;assert sha(s)==digest,(family,name)
        d=json.loads(s.read_text());models=[]
        if 'winners' in d:names=set(d['winners'].values())
        else:
            names={d['winner']}
            scores=d['scores'];assert min(scores,key=lambda r:r['selection_weighted_logloss'])['name']==d['winner']
        for n in names:
            m=s.parent/(n+'.pkl');assert m.stat().st_mtime<=freeze.timestamp(),str(m)
            models.append(dict(file=str(m.relative_to(B)),sha256=sha(m),mtime=stamp(m)))
        rows.append(dict(file=name,sha256=sha(s),mtime=stamp(s),models=models))
    code=record.get('fit_script_sha256');path=B/({'fit2025':'fit2025.py','fit2024':'fit2024.py','fit_conditional':'fit_conditional.py'}[family])
    if code:assert sha(path)==code,(family,'code changed')
    results.append(dict(family=family,freeze_utc=record['utc'],freeze_sha256=sha(p),selections=len(rows),rows=rows))
gate=json.loads((B/'evidence/BOTH_HOLDOUTS_FROZEN.json').read_text())
for name,digest in gate.items():assert sha(B/name)==digest
important=['evidence/EVALUATION_LOCK2025.json','evidence/EVALUATION_LOCK2024.json','evidence/assignments2025.npz','evidence/VERIFICATION2025.json','evidence/VERIFICATION2024.json']
timeline=[dict(file=x,mtime=stamp(B/x),sha256=sha(B/x)) for x in important]
assert max(datetime.datetime.fromisoformat(x['freeze_utc']) for x in results).timestamp() < (B/'evidence/assignments2025.npz').stat().st_mtime
code_audit=[]
for name in ['fit2025.py','fit2024.py','fit_conditional.py','predictors.py','predict2025.py','predict2024.py','run_frozen_pipeline.py']:
    p=B/name;s=p.read_text();tree=ast.parse(s)
    imported=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):imported.extend(x.name for x in n.names)
        if isinstance(n,ast.ImportFrom):imported.append(n.module)
    selected=[(i,line) for i,line in enumerate(s.splitlines(),1) if any(k in line for k in ['read_parquet','month','fraud_bool','prob_of_error','expert_parameters','VERIFICATION','FROZEN','pickle.load'])]
    code_audit.append(dict(file=name,sha256=sha(p),imports=imported,relevant_lines=selected))
out=dict(families=results,timeline=timeline,code_audit=code_audit,limitation='All freeze records and filesystem timestamps are self-authored and mutable. They are consistent with the claimed order, but provide no external proof of absence of earlier test use. Frozen manifests did not hash all fitted weights. Independent training/validation reconstruction is additional evidence.')
(R/'PROVENANCE_RESULT.json').write_text(json.dumps(out,indent=2))
print(json.dumps(dict(families=[{k:x[k] for k in ['family','freeze_utc','selections']} for x in results],timeline=timeline,limitation=out['limitation']),indent=2))
