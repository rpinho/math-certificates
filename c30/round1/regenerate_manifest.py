"""Explicit reseal after intentional release edits; never called by reproduction."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
files={}
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root).as_posix()
    if not p.is_file() or rel in {'MANIFEST.json','SHA256SUMS'} or '__pycache__' in p.parts: continue
    data=p.read_bytes(); files[rel]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
m={'job':'math_c30rel_1103','frozen_utc':datetime.now(timezone.utc).isoformat(),'status':'candidate C30 >= 521/50 = 10.42*; conditional on unrefereed Norton v3; L0 whole bound; finite L1-same-agent; no human referee','hash_policy':'All payload files; SHA256SUMS additionally binds MANIFEST.json. Caches excluded and prohibited in the public release.','files':files}
(root/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
lines=[f"{v['sha256']}  {k}" for k,v in files.items()]
lines.append(hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()+'  MANIFEST.json')
(root/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print('Sealed',len(files),'payload files;',sum(v['bytes'] for v in files.values()),'bytes')
