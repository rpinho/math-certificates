"""Audit HJM source identity and exact inputs, allowing two known README defects.

This does not certify the lower numerical inequalities. It never edits source.
The unmodified root command's failure is retained in hjm-data-only.log.
"""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

if not __debug__:
    raise RuntimeError('Run this audit without -O; assertions are required')

sys.dont_write_bytecode = True
ROOT = Path('sources/hjm_repo/RealGrothendieck-main').resolve()
KNOWN_DOCS = {
    'lower/README.md': ('f5cf6d25557d0dd4ea2b8aa1b960d7666d73e59b17ef237a8d672fea78b2a1bf',
                        'a7cd186140490e95fc339961e6b816be386908e26d5571bd1e9dedb976c39040'),
    'upper/README.md': ('01830d531f22de99493975582bdbdc9bc0cd1e62054cedee57b6d8a6b3f89a35',
                        'f63294edf26e07e02b23e9484892375f8b749c7048f0efd0955dc66c67f7609d'),
}


def audited_manifest():
    entries, defects = {}, {}
    for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        p = Path(name)
        assert not p.is_absolute() and '..' not in p.parts and name not in entries
        path = ROOT/p
        assert path.is_file() and not path.is_symlink()
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            assert KNOWN_DOCS.get(name) == (expected, actual), name
            defects[name] = {'expected': expected, 'actual': actual}
        entries[name] = expected
    assert set(defects) == set(KNOWN_DOCS)
    actual_files = {'verify.py', 'data_link.py', 'requirements.txt'}
    for folder in ['data', 'lower', 'upper']:
        actual_files.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file())
    assert actual_files == set(entries)
    return entries


def main():
    entries = audited_manifest()
    spec = importlib.util.spec_from_file_location('hjm_data_link', ROOT/'data_link.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check_manifest = audited_manifest
    structural = module.check_data()
    data = json.loads((ROOT/'data/lower_rows.json').read_text())
    paper_q = ['1', '-0.654509751718', '-0.159925966134', '0.047785078787',
               '0.086465878916', '0.076371662489', '0.072282834573',
               '-0.004420811526', '-0.058106583958', '-0.041412929910', '0.016668224599']
    assert {int(k): F(v) for k, v in data['q'].items()} == {
        2*i+1: F(v) for i, v in enumerate(paper_q)}
    gaps = []
    previous = F()
    for i, row in enumerate(data['rows']):
        left, right = map(F, row['interval'])
        assert row['index'] == i and left == previous and left < right
        previous = right
        for cap in row['angular']:
            weights = list(map(F, cap['weights']))
            gap = weights[0] - sum((max(F(), -x) for x in weights[1:]), F())
            assert gap > 0
            gaps.append(gap)
    assert previous == 1 and len(gaps) == 70
    result = {'status': 'INPUTS_AND_SOURCE_AUDITED_WITH_TWO_DOCUMENTATION_HASH_DEFECTS',
              'numerical_proof_replayed': False, 'manifest_files': len(entries),
              'manifest_sha256': sha256((ROOT/'MANIFEST.sha256').read_bytes()).hexdigest(),
              'documentation_hash_defects': KNOWN_DOCS,
              'authors_structural_check': structural,
              'independent_rotation_checks': len(gaps), 'minimum_rotation_gap': str(min(gaps))}
    Path('hjm-input-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
