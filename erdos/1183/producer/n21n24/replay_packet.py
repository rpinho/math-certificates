"""Replay packaged certificates in a new output directory, keeping seals intact.

From the packet root:
python3 -B producer/n21n24/replay_packet.py --work-dir ../replay-n21n24 \
    --balanced-n23 ../release_assets/n23_balanced.txt.xz
For the eight headline trees and witnesses alone, use --headline-only instead.
No network, third-party code or search is used.
"""
import argparse,gzip,hashlib,json,pathlib,shutil,subprocess,sys
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--work-dir',required=True,type=pathlib.Path)
p.add_argument('--balanced-n23',type=pathlib.Path)
p.add_argument('--headline-only',action='store_true')
a=p.parse_args();package=pathlib.Path(__file__).resolve().parent;packet=package.parents[1]
work=a.work_dir.resolve();work.mkdir(parents=True,exist_ok=False)
if a.headline_only:
 sys.path.insert(0,str(package/'src'))
 from check import tree,witness
 nodes=0
 for n in range(21,25):
  row=json.loads((packet/f'certificates/n{n}_coloring.json').read_text())
  assert row['n']==n and len(row['word'])==n+1
  for c in row['colours']:
   assert len(c['witness'])==c['maximum']
   witness(n,row['word'],c['colour'],c['maximum'],c['witness'])
   nodes+=tree(packet/c['proof'],row['word'],c['colour'],c['maximum']+1)
  assert max(c['maximum'] for c in row['colours'])==row['upper']
  print('HEADLINE PASS',n,row['word'],[c['maximum'] for c in row['colours']],flush=True)
 result={'headline_trees':8,'headline_witnesses':8,'tree_nodes':nodes}
 (work/'headline.json').write_text(json.dumps(result,indent=2)+'\n')
 print('HEADLINE REPLAY PASSED',json.dumps(result),flush=True)
else:
 assert a.balanced_n23 is not None,'supply the downloaded n23 balanced-witness asset'
 asset=a.balanced_n23.resolve()
 assert hashlib.sha256(asset.read_bytes()).hexdigest()=='29b3aa237c9a2582e37a78113f132773a1d8e2ddbcab85acc1dd1ee6da6a6fba','n23 asset hash'
 shutil.copytree(package/'certificates',work/'certificates')
 (work/'logs').mkdir();(work/'src').mkdir()
 shutil.copy2(asset,work/'certificates/n23_balanced.txt.xz')
 shutil.copy2(package/'logs/public_baseline20.log',work/'logs/public_baseline20.log')
 subprocess.run(['clang++','-O3','-std=c++17',str(package/'src/coverage.cpp'),'-o',str(work/'src/coverage')],check=True)
 subprocess.run([sys.executable,'-B',str(package/'src/final_replay.py')],cwd=work,check=True)
 lists=0
 for original in (package/'certificates').glob('n*_T*/G_*.txt.gz'):
  generated=work/'certificates'/original.relative_to(package/'certificates')
  if generated.exists():
   with gzip.open(original,'rb') as x,gzip.open(generated,'rb') as y:
    assert x.read()==y.read(),('saved word list mismatch',str(original.relative_to(package)))
   lists+=1
 result=json.loads((work/'logs/final_replay.json').read_text())
 assert result['headline_n']==[21,22,23,24] and result['no_trees']==42
 assert [r['balanced_words'] for r in result['balanced']]==[705432,2704156]
 print('SAVED WORD LISTS MATCH',lists,flush=True)
 print('PACKET REPLAY PASSED',result['no_trees'],'retained trees and every new positive witness',flush=True)
