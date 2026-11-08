"""Exact Fox-color determinant of the inherited cap/body closure.

Separately written (same agent). Geometric cap identification remains the
unreviewed inherited prose proof. This check uses the actual physical word,
not just the claimed 2x2 action. Lower cap eliminates to colors
[x,y,3y-2x,2y-x]; upper imposes c2=c0, c3=2c0-c1.
After quotienting constant coloring (y=0), the torsion order is the gcd
of the resulting one-column integer relations.
"""
import gzip,json,math,pathlib,sys
from fractions import Fraction as F
from verify import need
P=pathlib.Path(sys.argv[1]);d=json.loads((P/'CONSTRUCTION.json').read_text());packet=json.loads(gzip.decompress((P/'projection.json.gz').read_bytes()));word=packet['word'];turns=F(d['parameters']['N']).numerator
rows=[]
for n in [1,2,3]:
 # y=0 is a legitimate quotient by the constant-color generator.
 colors=[1,0,-2,-1]
 for _ in range(n):
  for g in word:
   j=abs(g)-1;x,y=colors[j:j+2]
   colors[j:j+2]=[2*x-y,x] if g>0 else [y,2*y-x]
 relations=[colors[2]-colors[0], colors[3]-2*colors[0]+colors[1]]
 determinant=math.gcd(*relations)
 need(determinant==4*turns*n+3,'E_PHYSICAL_CLOSURE_DETERMINANT')
 rows.append({'n':n,'relations_after_constant_color_quotient':relations,'determinant':determinant,'expected':4*turns*n+3})
print(json.dumps({'verdict':'PHYSICAL_WORD_CAP_DETERMINANTS_PASS','verifier':'separately written (same agent)','cases':rows,'qualification':'cap identifications use inherited prose; determinant alone does not identify knot type'},indent=2))
