"""Verify frozen input/code hashes and agreement of independent implementations."""
import datetime,hashlib,json
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent
manifest=json.loads((R/'MANIFEST.json').read_text())
for name,sha in manifest['sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
def read(name):return json.loads((R/name).read_text())
a=read('verification_rows.json');b=read('verification_independent_H96.json');c=read('verification_independent_H72.json')
for r in (a,b,c):assert r['status']=='PASS' and F(r['bound'])<F('3.1674542553') and F(r['gain'])==F(417,512)
assert a['bound']==b['bound'] and a['finite']==b['finite'] and a['tail']==b['tail']
assert a['B']==b['B'] and a['B'][:73]==c['B']
assert [a['finite_degrees'][str(d)] for d in range(1,97)]==b['finite_degrees']
assert F(a['bound'])<=F(c['bound'])
assert a['B'][8]==33
for name in ['control_gap.json','control_witnesses.json','control_rejections.json','verification_structure_cases.json']:
    assert read(name)['status']=='PASS'
assert read('control_rejections.json')['count']==19
ledger=read('PROCESS_LEDGER.json')
assert ledger['nice']>=10 and ledger['concurrent_workers']==1
assert all(v=='1' for v in ledger['threads'].values())
assert all(r['returncode']==0 for r in ledger['steps'] if r['label']!='receipt')
assert max(r['cumulative_max_child_RSS_KiB'] for r in ledger['steps'] if r['label']!='receipt')<40*1024**2
out={'status':'PASS candidate, unrefereed','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'bound96':a['bound'],'bound72':c['bound'],'gain':'417/512','B8':33,
 'static_files_checked':len(manifest['sha256']),
 'manifest_sha256':hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest(),
 'receipt_hashes':{name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in
    ['verification_rows.json','verification_independent_H96.json','verification_independent_H72.json',
     'control_gap.json','control_witnesses.json','control_rejections.json','verification_structure_cases.json']}}
(R/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
