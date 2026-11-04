"""Exact rational enclosure on the frozen artifact; separately written (same agent)."""
from fractions import Fraction
import gzip, hashlib, json, pathlib, sys

sys.set_int_max_str_digits(20000)
artifact = pathlib.Path(sys.argv[1])
d = json.load(gzip.open(artifact, 'rt'))
x, t, a = (Fraction(*d[k]) for k in ('x', 't', 'bound'))
assert x > 1 and 0 < t < 1 and a >= Fraction(529, 2000)
terms = 120
def enclose_log(q):
    u = (q-1)/(q+1)
    power, square, total = u, u*u, Fraction(0)
    for k in range(terms):
        total += 2*power/(2*k+1)
        power *= square
    # Bound the absolute tail of 2 sum u^(2k+1)/(2k+1).
    error = 2*abs(power)/((2*terms+1)*(1-square))
    return total-error, total+error
lx, ux = enclose_log(x)
lt, ut = enclose_log(t)
low, high = 2*lx+a*lt, 2*ux+a*ut
assert low > 0
receipt = dict(status='passed', terms=terms, bound=str(a),
               gain_over_round5=str(a-Fraction(264263, 1000000)),
               artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
               exact_exponent_lower=[str(low.numerator), str(low.denominator)],
               exact_exponent_upper=[str(high.numerator), str(high.denominator)])
output = pathlib.Path(sys.argv[2])
output.write_text(json.dumps(receipt, indent=2)+'\n')
print('EXACT_RATIONAL_EXPONENT_PASS', 'bound', str(a), 'lower_approx', float(low), flush=True)
