"""Publication arithmetic only; no mathematical certificate replay.
Derive the old radius rendering and radius difference from the two certificates.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
P=Path(__file__).resolve().parent
current=Q(json.loads((P/'certificates/certificate-0447.json').read_text())['c'])
old=Q(json.loads((P/'../signed-contact/certificate-44685.json').read_text())['c'])
gain=current-old
assert old==Q(44685,100000) and gain==Q(3,20000)
print(json.dumps({'old_radius':str(old),'old_decimal':'0.44685','gain':str(gain)}))
