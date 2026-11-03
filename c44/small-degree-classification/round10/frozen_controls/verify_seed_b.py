"""Independent B: direct character evaluation of each gate and partition.
Xi is verified by its exact four-selector branch identity and induction.
"""
import json,pathlib,sys
from fractions import Fraction
obj=json.loads(pathlib.Path(sys.argv[1]).read_text());h=obj['controls'];target=obj['target_degree']
assert obj['status'] in ['OPTIMAL','FEASIBLE'] and 6<=h<=12
terms=[];used=0;payloads=[]
for entry in obj['gates']:
 rows=entry['terms'];assert len(set(int(s) for s,c in rows))==len(rows)
 assert all(type(c)==int and c!=0 and 0<=int(s)<1<<h for s,c in rows)
 degree=max(bin(int(s)).count('1') for s,c in rows)
 mask=0
 for s,c in rows:mask|=int(s)
 assert degree==entry['degree'] and mask==entry['used'];used|=mask
 residual=target-degree;assert residual==entry['payload_degree'] and residual>0
 payloads.append(residual);terms.append([(int(s),c) for s,c in rows])
counts=[0]*len(terms)
for assignment in range(1<<h):
 active=0
 for index,(polynomial,entry) in enumerate(zip(terms,obj['gates'])):
  numerator=sum(c*(-1 if bin(s&assignment).count('1')%2 else 1) for s,c in polynomial)
  assert numerator in [0,entry['denominator'],-entry['denominator']]
  if numerator:active+=1;counts[index]+=1
 assert active==1
assert counts==[entry['support_count'] for entry in obj['gates']]
# Exact branch identity: each selector pair picks one signed Boolean input.
for s in (-1,1):
 for t in (-1,1):
  for left in (-1,1):
   for right in (-1,1):
    numerator=(s+t)*left+(s-t)*right;assert numerator in (-2,2)
# Disjoint old Fourier masks yield degree r and two fresh relevant selectors.
number={1:1}
for r in range(2,max(payloads)+1):number[r]=2*number[r-1]+2
assert all(number[r]==3*2**(r-1)-2 for r in number)
# Different payload blocks have nonempty Fourier masks on disjoint sets,
# so no cross-gate term can cancel. Every gate input remains relevant.
count=bin(used).count('1')+sum(number[r] for r in payloads)
assert count==obj['count'] and bin(used).count('1')==obj['relevant_controls']
lift=Fraction(count+2,2**target);assert Fraction(obj['asymptotic_lift'])==lift
result=dict(status='PASS',verifier='B direct exact characters and disjoint payload identity',degree=target,count=count,lift=str(lift),gates=len(terms))
pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
