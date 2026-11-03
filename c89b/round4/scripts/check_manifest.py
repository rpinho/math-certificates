"""Check the portable proof manifest using only the Python standard library."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'MANIFEST.json').read_text())
for row in manifest['files']:
 p=pathlib.PurePosixPath(row['file']);assert not p.is_absolute() and '..' not in p.parts
 data=(root/p).read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],str(p)
print('PASS',len(manifest['files']),'manifest files')
