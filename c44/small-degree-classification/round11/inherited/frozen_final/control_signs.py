"""Complete finite sign and range controls, independent of scalar checks."""
import itertools,json
k=3;valid=0;face_valid=0
for table in itertools.product((-1,1),repeat=8):
 affine_faces=True
 for fixed in range(k):
  others=[j for j in range(k) if j!=fixed]
  for bit in (0,1):
   corners=[(bit<<fixed)|sum(((v>>at)&1)<<j for at,j in enumerate(others)) for v in range(4)]
   affine_faces &= table[corners[0]]*table[corners[1]]*table[corners[2]]*table[corners[3]]==1
 affine_global=any(all(table[v]==constant*((-1)**((v&mask).bit_count())) for v in range(8)) for mask in range(8) for constant in (-1,1))
 assert affine_global==affine_faces
 face_valid+=affine_faces
 ternary=True
 for point in range(64):
  numerator=0
  for v,coefficient in enumerate(table):
   mask=sum(1<<(2*j+((v>>j)&1)) for j in range(k))
   numerator+=coefficient*(-1 if (mask&point).bit_count()%2 else 1)
  ternary &= numerator in (-8,0,8)
 assert ternary==affine_global
 valid+=ternary
assert valid==face_valid==16
# A pair product has values -1,0,1. Independent components realize every
# combination. Only one component and zero constant has ternary range.
for components in range(1,5):
 allowed=[]
 for constant in range(-64,65):
  if all(constant+64*sum(values) in (-64,0,64) for values in itertools.product((-1,0,1),repeat=components)):
   allowed.append(constant)
 assert allowed==([0] if components==1 else [])
print(json.dumps(dict(status='PASS',sign_tables=256,ternary=valid,face_affine=face_valid,component_counts=4,constant_grid=129)))
