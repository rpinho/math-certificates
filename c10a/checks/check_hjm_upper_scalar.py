"""Check two printed upper-bound consequences, not HJM's full upper pipeline."""
from fractions import Fraction as F
import json
from pathlib import Path
from flint import arb, ctx

ctx.prec = 256
value = (64*(-arb(512)).exp()*arb(32)**681
         / (345*arb.pi()*(343*arb.fac_ui(681)).sqrt()))
assert value < arb(3)/10**18
mantissa, exponent = map(int, value.upper().man_exp())
upper = F(mantissa)*F(2)**exponent
margin = (F('0.5618773799453352')-F('0.000003878150168295')
          -F('0.000034097111321496')-F('0.000007875733380418'))
assert margin > F(1000000, 1779893)
result = {
    'status': 'PASS_ONE_UPPER_SCALAR_AND_PRINTED_RATIONAL_ASSEMBLY_ONLY',
    'precision_bits': 256,
    'scalar_expression': '64*exp(-512)*32^681/(345*pi*sqrt(343*681!))',
    'scalar_upper': str(upper), 'scalar_upper_decimal': float(upper),
    'printed_rounding_margin': str(margin),
    'printed_margin_slack': str(margin-F(1000000, 1779893)),
    'full_upper_replayed': False,
}
Path('hjm-upper-scalar.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
