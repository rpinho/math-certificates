"""Exact comparisons of printed bounds; standard library only."""
from fractions import Fraction as F
import json
q=F('1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000')
a=F('1.7040280575')
assert a-F('1.7032090736')==F('0.0008189839')
assert a-F('1.70311')==F('0.0009180575')
print(json.dumps({'printed_margin_over_public':str(a-F('1.7032090736')),'printed_margin_over_round1':str(a-F('1.70311')),'periodic_margin_over_public':str(q-F('1.7032090736')),'periodic_margin_over_round1':str(q-F('1.70311'))},indent=2))
