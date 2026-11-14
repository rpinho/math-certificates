"""Parse only allowed data files; no producer or third-party code imports."""
import hashlib
import json
import lzma
from pathlib import Path

raw = lzma.decompress(Path('sources/baseline.txt.xz').read_bytes())
lines = [s for s in raw.decode('ascii').splitlines() if s and not s.startswith('#')]
assert lines[0] == 'sunflower3 v1'
tag, n, p, q, m = lines[1].split()
n, p, q, m = map(int, (n, p, q, m))
assert tag == 'block' and (n, p, q, m) == (28, 0, 1, 252292)
assert len(lines) == m + 2
masks = []
for line in lines[2:]:
    pts = [] if line == '-' else list(map(int, line.split()))
    assert pts == sorted(set(pts)) and all(0 <= x < n for x in pts)
    masks.append(sum(1 << x for x in pts))
Path('baseline.masks').write_text('\n'.join(map(str, masks)) + '\n')
meta = {'sha256_decompressed': hashlib.sha256(raw).hexdigest(), 'n': n,
        'ports': [p, q], 'members': m}
Path('logs/baseline_input.json').write_text(json.dumps(meta, indent=2)+'\n')
print(json.dumps(meta))
