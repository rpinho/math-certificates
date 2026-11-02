"""Administrative file-transfer integrity; no mathematical acceptance decisions."""
import json,hashlib
from pathlib import Path
mraw=Path('MANIFEST.json').read_bytes();assert hashlib.sha256(mraw).hexdigest()==Path('MANIFEST.sha256').read_text().split()[0];m=json.loads(mraw)
for r in m['entries']:
 p=Path(r['path']);raw=p.read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],r['path']
total=sum(r['bytes'] for r in m['entries'])+len(mraw)+len(Path('MANIFEST.sha256').read_bytes());assert total==m['retained_total_bytes']<50_000_000;print('TRANSFER PASS',len(m['entries']),'hashed members;',total,'retained bytes')
