"""Rejection controls for the final bound specification and source binding.

Does not import discovery code or run numerical solvers.
"""
import copy
import hashlib
import json
import os
from pathlib import Path

from verify_bound import verify as row
from verify_column import verify as column

root = Path(__file__).resolve().parent
spec = json.loads((root / 'candidate.json').read_text())
cases = [
    ('unsupported_quartic_cap', lambda c: c['caps'].update({'4': '23/16'})),
    ('changed_external_R3', lambda c: c.update(external_R3=9)),
    ('changed_external_bs_theorem', lambda c: c.update(external_bs_theorem='bs<=d')),
    ('incorrect_spectral_hash', lambda c: c.update(spectral_sha256='0' * 64)),
    ('excessive_final_claim', lambda c: c.update(claim='4.12')),
]
results = []
print('PID', os.getpid(), flush=True)
for name, change in cases:
    c = copy.deepcopy(spec)
    change(c)
    for check in (row, column):
        try:
            check(c)
        except AssertionError:
            results.append({'case': name, 'checker': check.__module__, 'rejected': True})
        else:
            raise AssertionError(f'{check.__module__} accepted {name}')

# Refreshing the digest must not permit corrupt mathematics to pass.
source = json.loads((root / spec['spectral_source']).read_text())
source['certificates'][0]['alpha']['0'] = '1000'
temporary = root / 'temporary_corrupt_spectral.json'
try:
    data = (json.dumps(source) + '\n').encode()
    temporary.write_bytes(data)
    c = copy.deepcopy(spec)
    c.update(spectral_source=temporary.name, spectral_sha256=hashlib.sha256(data).hexdigest())
    for check in (row, column):
        try:
            check(c)
        except AssertionError:
            results.append({'case': 'corrupt_dual_refreshed_hash',
                            'checker': check.__module__, 'rejected': True})
        else:
            raise AssertionError(f'{check.__module__} accepted corrupt dual')
finally:
    # This temporary file was created by this invocation.
    temporary.unlink(missing_ok=True)

result = {'status': 'PASS twelve specification/source rejection controls', 'results': results}
(root / 'verification_rejections.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['status'], flush=True)
