"""Read-only integrity check of the frozen review packet."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
expected=set(m['files'])|{'MANIFEST.json','SHA256SUMS'}
assert actual==expected, {'unexpected':sorted(actual-expected),'missing':sorted(expected-actual)}
for rel,entry in m['files'].items():
    p=root/rel
    assert p.is_file(),rel
    data=p.read_bytes()
    assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],rel
print('PASS: '+str(len(m['files']))+' frozen files match their SHA-256 hashes.')
