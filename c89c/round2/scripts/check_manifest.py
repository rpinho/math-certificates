"""Check every file in a frozen proof-bundle manifest."""
import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
manifest=json.loads((root/'ARTIFACT_MANIFEST.json').read_text())
for name,record in manifest['files'].items():
 data=(root/name).read_bytes();assert len(data)==record['bytes'],name;assert hashlib.sha256(data).hexdigest()==record['sha256'],name
print('PASS',len(manifest['files']),'manifest files')
