"""Independent exact aggregation of freshly replayed HJM lower results.

Does not independently reimplement the analytic or finite-tree verifiers.
Requires their fresh outputs and checks every endpoint against readable inputs.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run this verifier without -O; assertions are required')

SOURCE = Path('sources/hjm_repo/RealGrothendieck-main')
RESULT = Path('hjm-lower-results')


def load(path):
    return json.loads(path.read_text())


def main():
    definitions = load(SOURCE/'data/lower_rows.json')
    report = load(RESULT/'VERIFICATION_REPORT.json')
    arithmetic = load(RESULT/'arithmetic.json')
    controls = load(RESULT/'negative_controls.json')
    assert controls['status'] == 'ALL_NEGATIVE_CONTROLS_REJECTED'
    assert controls['rejected_count'] == report['negative_controls_rejected'] == 32
    assert report['KG_theorem_accepted'] is True
    assert report['all_35_universal_fibres_regenerated'] is True
    assert report['all_non_fibre_arithmetic_regenerated'] is True
    assert len(definitions['rows']) == len(report['rows']) == len(arithmetic['rows']) == 35
    target = F(1000, 1773)-F(1, 10**9)
    assert F(report['norm_bound']) == target == F(definitions['scalar_bound'])
    previous = F()
    assembled, allowance_gaps, report_hashes = [], [], {}
    counts = {k: 0 for k in ['rectangles', 'empty_rectangles', 'flow_rectangles',
                            'branch_rectangles', 'integer_flows', 'binary_nodes', 'binary_leaves']}
    for i, (row, nonfibre, printed) in enumerate(zip(definitions['rows'], arithmetic['rows'], report['rows'])):
        left, right = map(F, row['interval'])
        assert row['index'] == nonfibre['index'] == printed['index'] == i
        assert left == previous and left < right <= 1
        assert list(map(F, nonfibre['interval'])) == [left, right]
        previous = right
        path = RESULT/'fibres'/f'row{i}.json'
        fibre = load(path)
        assert fibre['row'] == i and fibre['status'] == 'UNIVERSAL_FIBRE_REPLAY_PASSED'
        assert fibre['analytic_regenerated'] is True and fibre['precision_bits'] == 384
        assert fibre['certificate_sha256'] == sha256((SOURCE/'lower/certificates'/f'row{i}.json').read_bytes()).hexdigest()
        assert fibre['input_sha256'] == sha256((SOURCE/'lower/inputs'/f'row{i}.bin').read_bytes()).hexdigest()
        assert fibre['finite_scale'] == 2**44 and type(fibre['finite_upper_integer']) is int
        errors = sum((F(fibre[k]) for k in ['interpolation_and_tail_error',
                                          'fixed_point_input_error', 'graph_quantization_error']), F())
        assert errors == F(fibre['total_error']) and errors >= 0
        bound = F(fibre['finite_upper_integer'], 2**44) + errors
        assert bound == F(fibre['certified_fibre_upper']) == F(printed['certified_fibre_upper'])
        allowance = F(row['C'])
        assert bound <= allowance == F(fibre['allowed']) == F(printed['allowed'])
        assert nonfibre['psd_checks_in_row'] == 52
        assert F(nonfibre['minimum_LDL_pivot_lower']) > 0
        assert [cap['N'] for cap in nonfibre['caps']] == [7, 9]
        for cap in nonfibre['caps']:
            assert cap['all_finite_omitted_coefficients_positive'] is True
            assert F(cap['finite_omitted_min_lower']) > 0
            assert F(cap['tail_cone_margin_lower']) > 0
        rest = F(nonfibre['non_fibre_cost_upper'])
        assert rest == F(printed['non_fibre_upper'])
        assert allowance+rest <= target  # Manuscript's printed endpoint condition.
        assembled.append(bound+rest)
        allowance_gaps.append(target-(allowance+rest))
        for k in counts:
            counts[k] += fibre['statistics'].get(k, 0)
        report_hashes[str(path)] = sha256(path.read_bytes()).hexdigest()
    assert previous == 1
    maximum = max(assembled)
    assert maximum == F(report['maximum_assembled_norm_upper']) < target
    assert report['matrix_PD_checks'] == arithmetic['matrix_PD_checks'] == 1820
    assert report['statistics'] == counts
    assert F(report['certified_KG_lower']) == 1/target > F(1773, 1000)
    result = {'status': 'PASS_FRESH_LOWER_EXACT_ASSEMBLY',
              'scope': 'Independent rational aggregation; numerical premises from authors fresh lower replay',
              'rows': 35, 'matrix_checks': 1820, 'statistics': counts,
              'norm_target': str(target), 'maximum_payoff_upper': str(maximum),
              'maximum_payoff_decimal': float(maximum),
              'strict_norm_slack': str(target-maximum),
              'strict_norm_slack_decimal': float(target-maximum),
              'minimum_printed_endpoint_slack': str(min(allowance_gaps)),
              'KG_lower': str(1/target), 'KG_lower_decimal': float(1/target),
              'negative_controls_report_sha256': sha256((RESULT/'negative_controls.json').read_bytes()).hexdigest(),
              'negative_controls': controls, 'fresh_fibre_hashes': report_hashes}
    Path('hjm-independent-final.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['negative_controls', 'fresh_fibre_hashes']}, indent=2))


if __name__ == '__main__':
    main()
