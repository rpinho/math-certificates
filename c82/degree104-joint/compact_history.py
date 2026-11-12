"""Keep the requested <50 MB packet by compressing completed search history."""
import gzip,json,re,subprocess
from pathlib import Path
from numerics import register
register('compact_completed_history')
p=json.loads(Path('rounds/progress.json').read_text());limit=p['history'][-1]['round']
keep_state=Path(p['state']);keep_json={keep_state}
if Path('RESULT.json').exists():
    best=Path(json.loads(Path('RESULT.json').read_text())['replay_source']);keep_json.add(best)
    if best.name.endswith('-replay.json'):keep_json.add(best.with_name(best.name.replace('-replay.json','-certificate.json')))
keep_dual={Path(p['dual']),Path('rounds/warm-dual.npz')}
compressed=[];retired=[]
for path in sorted(Path('rounds').glob('*.json')):
    digits=re.findall(r'\d+',path.stem);k=int(digits[0]) if digits else 0
    if k>limit or path in keep_json:continue
    data=json.loads(path.read_text())
    state=isinstance(data,dict) and isinstance(data.get('mu'),list) and isinstance(data.get('w'),list)
    archived_record=path.name.endswith(('-certificate.json','-replay.json','-lp.json','-added.json'))
    if not (state or archived_record or '-search-' in path.name or path.name.endswith('-screen.json')):continue
    with gzip.open(str(path)+'.gz','wb') as out:out.write(path.read_bytes())
    compressed.append(path)
for path in sorted([*Path('logs').glob('*.log'),*Path('rounds').glob('*-verify.log')]):
    if path.name=='cg.log' or path.stat().st_size<8192:continue
    digits=re.findall(r'\d+',path.stem);k=int(digits[0]) if digits else 0
    if k>limit:continue
    with gzip.open(str(path)+'.gz','wb') as out:out.write(path.read_bytes())
    compressed.append(path)
for path in sorted(Path('rounds').glob('*-dual.npz')):
    digits=re.findall(r'\d+',path.stem);k=int(digits[0]) if digits else 0
    if k<=limit and path not in keep_dual:retired.append(path)
if compressed or retired:
    subprocess.run(['/usr/bin/trash',*[str(p.resolve()) for p in compressed+retired]],check=True)
    with open('STATUS.md','a') as f:f.write(f'\nRetained <50 MB: gzip-compressed {len(compressed)} completed historical JSON/log files and moved {len(retired)} old regenerable dual caches to macOS Trash. The live master/dual, complete coefficient bank, standalone best certificate/replay and every Python/verifier remain uncompressed; older round certificate/replay metadata may also be gzip-compressed. Compressed originals were also moved to Trash.\n')
print(json.dumps({'compressed_history_files':len(compressed),'retired_dual_caches':len(retired)}))
