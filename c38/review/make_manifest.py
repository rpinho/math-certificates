"""Hash the final small referee sources, documents, and retained evidence."""
import datetime
import hashlib
import json
import pathlib

root=pathlib.Path(__file__).resolve().parent
output=root/'results'/'MANIFEST.json'
files=[]
for p in sorted(root.rglob('*')):
    if not p.is_file() or p==output or '__pycache__' in p.parts:continue
    if p.suffix not in {'.md','.py','.cpp','.json','.jsonl','.log','.txt','.html','.csv'}:continue
    content=p.read_bytes()
    files.append({'path':str(p.relative_to(root)),'bytes':len(content),
                  'sha256':hashlib.sha256(content).hexdigest()})
size=sum(r['bytes'] for r in files)
assert size<50_000_000
assert (root/'REFEREE.md').read_text().splitlines()[-1] in {
    'VERDICT: HOLDS','VERDICT: HOLDS WITH CAVEATS','VERDICT: FAILS'}
output.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                             'total_bytes':size,'files':files},indent=2)+'\n')
print(f'{len(files)} files, {size} bytes; manifest excludes itself')
