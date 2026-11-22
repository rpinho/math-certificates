"""Check the user-supplied input directory against the pinned sha256 values (see README).
usage: python -I check_inputs.py INPUTS_DIR     (INPUTS_DIR contains unktok/ and wetch/)
Exit code 0 only if every pinned file is present and matches."""
import hashlib, json, os, sys
root = sys.argv[1]
WETCH = {'central-certificate.json': 'ccc9f53815b1a7c56d49caecfa549427748feb8133c5d591f716210df37967fd',
         'outer-certificate.json': 'c8019383dbcf7eb5892c27be2d918e0095e11cabe9b2f3d5b0e8184a1a16d93b'}
bad = 0
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''): h.update(blk)
    return h.hexdigest()
for n, want in WETCH.items():
    p = os.path.join(root, 'wetch', n)
    ok = os.path.exists(p) and sha(p) == want; bad += not ok
    print('wetch/' + n, 'OK' if ok else 'BAD')
man = json.load(open(os.path.join(root, 'unktok', 'proof', 'MANIFEST.json')))['files']
data = sorted(k for k in os.listdir(os.path.join(root, 'unktok', 'proof', 'data')) if k.endswith('.json'))
for n in data:
    want = man['data/' + n]['sha256']
    ok = sha(os.path.join(root, 'unktok', 'proof', 'data', n)) == want; bad += not ok
    print('unktok/proof/data/' + n, 'OK' if ok else 'BAD')
need = {'selected-exact-kernel.json', 'exact-periodic-offsets.json', 'target.json', 'barrier-functional.json', 'selected-paid-rows.json'}
miss = need - set(data); bad += len(miss)
if miss: print('MISSING', sorted(miss))
print('check_inputs:', 'PASS' if bad == 0 else 'FAIL')
sys.exit(1 if bad else 0)
