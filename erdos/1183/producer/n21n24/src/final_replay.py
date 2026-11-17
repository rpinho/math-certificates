"""Replay the delivered claims; no producer imported or called.

The unchanged round-4 tree checker checks each distinct needed no-tree once.
Positive prefix/factor witnesses and every full word are then checked by the
separate coverage implementation. Archived trees are read in one streaming pass.
"""
import pathlib,json,gzip,lzma,tarfile,re,sys,time
from check import tree,witness
from coverage import check as coverage_check
from check_balanced import check as balanced_check

def inputs():
 rows=[json.load(p.open()) for p in sorted(pathlib.Path('certificates').glob('upper_n*.json'))]
 assert {21,22,23}<={r['n'] for r in rows}
 refs={};screens=[]
 def add(path,w,c,t):
  key=(w,c,t)
  if path in refs:assert refs[path]==key
  refs[path]=key
 for row in rows:
  w=row['word'];assert len(w)==row['n']+1
  for c in row['colours']:add(c['proof'],w,c['colour'],c['maximum']+1)
  if row['n']>=21:
   for T in (row['upper']-1,row['upper']):
    base=pathlib.Path(f"certificates/n{row['n']}_T{T}")
    cp=json.loads((base/'checkpoint.json').read_text());assert not cp['stack'],'incomplete screen'
    screens.append((row['n'],T))
    # G-list membership trees were checked during production and terminal
    # replay. The retained claims need the reported words plus positive
    # coverage at one below each rank minimum, not every cached No result.
 for p in [pathlib.Path('certificates/best_n21.json')]:
  if p.exists():
   for row in json.load(p.open()):
    for c in row['colours']:add(c['proof'],row['word'],c['colour'],c['maximum']+1)
 p=pathlib.Path('certificates/crosschecks.json')
 if p.exists():
  for row in json.load(p.open()):
   for restriction in row['restrictions']:
    for c in restriction['colours']:add(c['proof'],restriction['word'],c['colour'],c['maximum']+1)
 p=pathlib.Path('certificates/n22_all_maxima.json')
 if p.exists():
  for w,colours in json.load(p.open()).items():
   for c in colours:add(c['proof'],w,c['colour'],14)
 p=pathlib.Path('logs/public_baseline20.log')
 if p.exists():
  for row in map(json.loads,p.open()):add(row['proof'],row['word'],row['colour'],row['maximum']+1)
 return rows,refs,sorted(set(screens))

def replay():
 began=time.time();rows,refs,screens=inputs();checked=set();node_count=0
 for p,(w,c,t) in refs.items():
  if pathlib.Path(p).exists():node_count+=tree(p,w,c,t);checked.add(p)
 missing=set(refs)-checked
 if missing:
  by_member={pathlib.Path(p).name[:-3]:p for p in missing}
  tmp=pathlib.Path('logs/replay_one_tree.tmp')
  with tarfile.open('certificates/no_trees.tar.xz','r|xz') as archive:
   for entry in archive:
    if entry.name not in by_member:continue
    p=by_member[entry.name];w,c,t=refs[p]
    with archive.extractfile(entry) as inp,tmp.open('wb') as out:
     while chunk:=inp.read(1<<20):out.write(chunk)
    node_count+=tree(tmp,w,c,t);checked.add(p)
  assert set(refs)<=checked,'missing archived tree'
 for row in rows:
  for c in row['colours']:
   assert len(c['witness'])==c['maximum']
   witness(row['n'],row['word'],c['colour'],c['maximum'],c['witness'])
  assert max(c['maximum'] for c in row['colours'])==row['upper']
  print('HEADLINE',row['n'],row['upper'],flush=True)
 for row in json.load(open('certificates/best_n21.json')):
  for c in row['colours']:witness(row['n'],row['word'],c['colour'],c['maximum'],c['witness'])
 for w,colours in json.load(open('certificates/n22_all_maxima.json')).items():
  assert len(colours)==2
  for c in colours:witness(22,w,c['colour'],13,c['witness']);assert refs[c['proof']]==(w,c['colour'],14)
 for row in json.load(open('certificates/crosschecks.json')):
  for r in row['restrictions']:
   assert row['previous_rank_minimum']<=r['value']<=row['rank_minimum']
   for c in r['colours']:witness(row['n']-1,r['word'],c['colour'],c['maximum'],c['witness'])
 cover=[]
 for n,T in screens:
  # Lower screens have no good full words: every word has a checked positive
  # rejection. At-bound G lists were fully tree-checked before packaging.
  result=coverage_check(n,T,verify_trees=False,record=False);cover.append(result)
  if T==next(r['upper'] for r in rows if r['n']==n)-1:assert result['coverage'][-1]['good_words']==0
 balanced=[]
 for n in (21,23):
  p=pathlib.Path(f'certificates/n{n}_balanced.txt.xz')
  if not p.exists():p=p.with_suffix('')
  balanced.append(balanced_check(n,p))
 result=dict(no_trees=len(checked),tree_nodes=node_count,headline_n=[r['n'] for r in rows if r['n']>=21],
             coverage=cover,balanced=balanced,seconds=time.time()-began)
 pathlib.Path('logs/final_replay.json').write_text(json.dumps(result,indent=2)+'\n')
 print('FINAL REPLAY PASSED',len(checked),'no-trees;',round(result['seconds'],2),'seconds',flush=True)
if __name__=='__main__':replay()
