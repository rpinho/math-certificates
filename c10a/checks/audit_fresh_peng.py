"""Independent identity and coverage audit of a complete fresh Peng replay.

Standard library only; no author imports. This checks provenance/coverage,
not a second implementation of the Fourier integrator. Run before compacting
the regenerable intermediate files. Exact final inequalities are checked
separately by exact_check.py.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run this audit without -O; assertions are required')


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path, default=Path('peng-full'))
    args = parser.parse_args()
    root = Path('.')
    source = root/'sources/peng_source/anc'
    work = args.workdir
    cert = work/'certificates'
    head = cert/'rebuild-20261013'
    pair = cert/'pairs-20261015'
    tail = cert/'tail-rebuild-20261015'
    continued = (work/'execution_continued.json').exists()
    receipt = read(work/('execution_continued.json' if continued else 'execution.json'))
    if continued:
        assert receipt['status'] == 'PASS_COMPLETE_PUBLISHED_NUMERICAL_STAGES'
        assert len(receipt['stages']) == 12
    else:
        assert receipt['mode'] == 'full' and len(receipt['stages']) == 14
    verification = read(work/'verification.json')
    assert verification['status'] == 'PASS' and verification['bound'] == '44496791/25000000'
    inventory = read(source/'inventory.json')['files']
    assert set(inventory) == {p.name for p in source.iterdir() if p.is_file()}-{'inventory.json'}
    for name, row in inventory.items():
        assert digest(source/name) == row['sha256'], name
    dependencies = read(source/'dependencies.json')['files']
    mapping = read(source/'layout.json')
    for name, relative in mapping.items():
        original = (root/'dependency-cache' if name in dependencies else source)/name
        expected = digest(original)
        if name in dependencies:
            assert expected == dependencies[name]['sha256']
        assert digest(work/relative) == expected, relative
        if continued:
            assert receipt['preserved_source_hashes'][relative] == expected
    for name, row in dependencies.items():
        assert digest(root/'dependency-cache'/name) == row['sha256']
        if (tail/'source'/name).exists():
            assert digest(tail/'source'/name) == row['sha256']
    head_ledger, pair_ledger = read(head/'ledger.json'), read(pair/'ledger.json')
    assert set(head_ledger['files']) == {'zero.json', 'analytic-error.json'} | {
        f'nodes/{n:04d}.json' for n in range(1, 769)}
    if continued:
        assert receipt['head_ledger_sha256'] == digest(head/'ledger.json')
    assert pair_ledger['binding']['input_ledger_sha256'] == digest(head/'ledger.json')
    assert pair_ledger['binding']['precision_bits'] == 512
    assert pair_ledger['binding']['degree'] == 403
    for name, expected in head_ledger['files'].items():
        assert digest(head/name) == expected, name
        if name.startswith('nodes/'):
            row = read(head/name)
            assert row['index'] == int(Path(name).stem)
            assert row['binding'] == head_ledger['binding']
            assert len(row['features']) == len(row['profiles']) == 404
    assert set(pair_ledger['files']) == {f'rows/{n:04d}.json' for n in range(1, 769)}
    products, weighted = 0, 0
    for name, expected in pair_ledger['files'].items():
        assert digest(pair/name) == expected, name
        row = read(pair/name)
        n = int(Path(name).stem)
        assert (row['u'], row['v_first'], row['v_last']) == (n, n, 768)
        assert row['binding'] == pair_ledger['binding']
        assert row['pair_count'] == 769-n
        assert row['weighted_count'] == 2*(769-n)-1
        assert len(row['coefficients']) == 404
        products += row['pair_count']
        weighted += row['weighted_count']
    assert (products, weighted) == (295296, 589824)
    progress = read(pair/'progress.json')
    assert progress['status'] == 'complete_pair_component'
    assert progress['complete_rows'] == 768 and progress['pairs_covered'] == products
    pilot = read(tail/'pilot/result.json')
    assert pilot['status'] == 'certified_conditional_energy_component'
    assert pilot['binding']['input_sha256'] == digest(source/'physical.json')
    assert pilot['binding']['precision_bits'] == 256
    assert len(pilot['local_weights']) == 25 and len(pilot['scalar_contributions']) == 80
    for row in pilot['local_weights']:
        path = tail/'pilot/local_weights'/('_'.join(map(str, row['exponents']))+'.json')
        assert digest(path) == row['sha256']
        local = read(path)
        assert local['binding'] == pilot['binding']
        assert local['whole_bin_conditions_checked'] == 14337
        assert local['finite_frequency_count'] == len(local['values']) == 3073
    grid = read(tail/'grid/result-portable.json')
    assert grid['status'] == 'certified_mixed_energy_grid'
    assert grid['binding']['input_sha256'] == digest(source/'physical.json')
    assert grid['binding']['precision_bits'] == 256
    assert grid['binding']['manifest_sha256'] == digest(tail/'source/fourier_circle_manifest.json')
    assert grid['binding']['budget_sha256'] == digest(tail/'source/fourier_circle_error_budget_final.json')
    assert len(grid['rows']) == 126 and len(grid['scalar_contributions']) == 981
    expected_rows = {(F(n, 100), p, q) for n in range(81, 98, 2)
                     for p in range(5) for q in range(5-p) if p+q}
    assert {(F(row['radius']), row['p'], row['q']) for row in grid['rows']} == expected_rows
    scalar_paths = set()
    for row in grid['scalar_contributions']:
        name = row['path']
        assert name not in scalar_paths and not Path(name).is_absolute() and '..' not in Path(name).parts
        scalar_paths.add(name)
        assert digest(tail/'grid'/name) == row['sha256'], name
    for manifest_name in ['fourier_pilot_manifest.json', 'fourier_circle_manifest.json']:
        manifest = read(tail/'source'/manifest_name)
        assert manifest['precision_bits'] == 256
        for name, expected in manifest['files'].items():
            assert digest(tail/'source'/name) == expected, name
    circle = read(tail/'circle.json')
    assert circle['input_sha256'] == digest(source/'physical.json')
    assert circle['energy_result_sha256'] == digest(tail/'grid/result-portable.json')
    assert circle['manifest_sha256'] == digest(tail/'source/fourier_circle_manifest.json')
    assert circle['panels'] == 2048 and len(circle['intervals']) == 2048
    assert [row['index'] for row in circle['intervals']] == list(range(2048))
    expected_pairs = {(p, q) for p in range(5) for q in range(5-p) if p+q}
    assert all(len(row['mixed_bounds']) == 14 and
               {(b['p'], b['q']) for b in row['mixed_bounds']} == expected_pairs
               for row in circle['intervals'])
    final = read(cert/'fresh-final-arithmetic.json')
    assert final['input_hashes'] == {
        'primitive_ledger': digest(head/'ledger.json'),
        'pair_ledger': digest(pair/'ledger.json'), 'circle': digest(tail/'circle.json')}
    for stage in receipt['stages']:
        assert stage['exit_code'] == 0
        assert digest(work/stage['log']) == stage['log_sha256']
    result = dict(status='PASS_FRESH_SOURCE_IDENTITY_AND_COVERAGE',
                  checked_utc=datetime.now(timezone.utc).isoformat(),
                  published_source_files=len(inventory), pinned_dependencies=len(dependencies),
                  primitive_nodes=768, triangular_products=products, ordered_terms=weighted,
                  local_transforms=25, scalar_integrals=981, mixed_energies=126, circle_panels=2048,
                  stages=len(receipt['stages']), receipt_kind='continuation' if continued else 'from-scratch',
                  auditor_sha256=digest(Path(__file__)),
                  certificate_sha256=digest(cert/'fresh-final-arithmetic.json'),
                  circle_sha256=digest(tail/'circle.json'),
                  scope='Independent hashes, bindings and coverage; mathematical integrators remain authors code')
    Path('peng-fresh-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
