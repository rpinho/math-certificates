"""Independent rational endpoint audit; does not regenerate analytic endpoints.

No imports from either author's code. Fractions are parsed from original JSON.
The separate source replay is necessary to justify these endpoint premises.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ArithmeticError(message)


def atan_bracket(q, pairs=80):
    # Integrate the finite geometric expansion of 1/(1+x^2).
    # An even number of terms is a strict lower bound; next term is upper.
    lo = sum((F(1, (4*j+1)*q**(4*j+1))
              - F(1, (4*j+3)*q**(4*j+3)) for j in range(pairs)), F())
    return lo, lo + F(1, (4*pairs+1)*q**(4*pairs+1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path('sources/peng_source/anc/certificate.json'))
    parser.add_argument('--circle', type=Path,
                        default=Path('sources/peng_source/anc/circle_bounds.json'))
    parser.add_argument('--output', type=Path, default=Path('independent_exact.json'))
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    circle = json.loads(args.circle.read_text())
    physical_path = Path('sources/peng_source/anc/physical.json')
    require(sha256(physical_path.read_bytes()).hexdigest() ==
            '3077b5a8011868ff8a9200590bebb73cb41ad3ba10b09eb37860d5074c3b1653',
            'Paper Appendix C input identity')
    physical = json.loads(physical_path.read_text())
    poly = {int(k): F(v) for k, v in physical['P'].items()}
    require(set(poly) == set(range(1, 82, 2)), 'Preprocessing degrees')
    require(sum(map(abs, poly.values()), F()) == F(999999999999, 10**12),
            'Strict preprocessing norm')
    intervals = [[F(x) for x in row] for row in cert['coefficients']]
    require(len(intervals) == 404 and cert['degree'] == 403, 'Head coverage')
    require(all(len(row) == 2 and row[0] <= row[1] for row in intervals), 'Intervals')
    require(all(row == [F(), F()] for row in intervals[::2]), 'Parity')
    error = F(cert['head_analytic_error_upper'])
    require(0 < error < F(1597802294094, 10**22), 'Head analytic error ceiling')
    head = intervals[1][0] - sum((max(abs(a), abs(b))
                                for a, b in intervals[3::2]), F()) - error
    require(head == F(cert['head_lower']), 'Head checksum')
    require(head > F(88263349, 10**8), 'Paper head threshold')
    if 'fourth_derivative_upper' in circle:
        balls = circle['fourth_derivative_upper']
    else:
        require([row['index'] for row in circle['intervals']] == list(range(2048)),
                'Panel order')
        balls = [row['fourth_derivative_upper'] for row in circle['intervals']]
    require(circle['panels'] == len(balls) == 2048, 'Circle coverage')
    endpoints = []
    for ball in balls:
        require(set(ball) == {'m', 'r', 'e'} and F(ball['r']) >= 0
                and isinstance(ball['e'], int), 'Ball format')
        endpoint = (F(ball['m']) + F(ball['r'])) * F(10)**ball['e']
        require(endpoint > 0, 'Positive derivative majorant')
        endpoints.append(endpoint)
    q4 = sum((x*x for x in endpoints), F())/len(endpoints)
    c4 = F(1006651833, 2048)
    require(q4 == F(cert['Q4_upper']) and q4 <= c4*c4, 'Derivative norm')
    # Cauchy--Schwarz and sum_{odd n>403} n^-8 < 1/(14*403^7).
    tail = F(1, 10000)
    require(c4*c4 < 14*403**7*tail**2, 'Infinite tail')
    require(F(cert['tail_upper']) == tail, 'Tail value')
    gamma = head-tail
    require(gamma == F(cert['gamma_lower']), 'Gamma checksum')
    gamma0 = F(88253349, 10**8)
    require(gamma > gamma0, 'Paper gamma threshold')
    a, b = atan_bracket(5), atan_bracket(239)
    # (5+i)^4 = 476+480i. This identity makes the quotient
    # ((5+i)/(5-i))^4 / ((239+i)/(239-i)) exactly i.
    # The angle 4 atan(1/5)-atan(1/239) lies between 0 and 1 radian,
    # fixing the branch to pi/4 and establishing Machin's identity.
    require(239*476+480 == 239*480-476, 'Gaussian-integer Machin identity')
    require(0 < 4*a[0]-b[1] < 4*a[1]-b[0] < 1, 'Machin branch')
    pi_hi = 16*a[1]-4*b[0]
    decimal_pi_hi = F(3141592653589794, 10**15)
    require(pi_hi < decimal_pi_hi, 'Independent Machin bound')
    bound = F(44496791, 25000000)
    paper_margin = 2*gamma0*bound-decimal_pi_hi
    require(paper_margin == F(17031633, 2500000000000000), 'Paper integer identity')
    require(paper_margin > 0 and 2*gamma*bound-pi_hi > 0, 'Strict final bound')
    result = {
        'status': 'PASS_ENDPOINT_ARITHMETIC_ONLY',
        'scope': 'Exact conditional inference from supplied endpoint enclosures; source replay separate',
        'bound': str(bound), 'bound_decimal': '1.77987164',
        'head_lower': str(head), 'head_decimal': float(head),
        'gamma_lower': str(gamma), 'gamma_decimal': float(gamma),
        'paper_margin': str(paper_margin), 'paper_margin_decimal': float(paper_margin),
        'full_endpoint_margin_decimal': float(2*gamma*bound-pi_hi),
        'norm_ceiling_decimal': float(c4), 'q4_decimal': float(q4),
        'tail_squared_margin': str(14*403**7*tail**2-c4*c4),
        'certificate_sha256': sha256(args.certificate.read_bytes()).hexdigest(),
        'circle_sha256': sha256(args.circle.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_lower')}, indent=2))


if __name__ == '__main__':
    main()
