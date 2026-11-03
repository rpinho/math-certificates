"""Exact gate-partition verifier A: inverse Walsh and full sparse expansion."""
import collections,json,math,pathlib,sys
from fractions import Fraction as Q
packet=json.loads(pathlib.Path(sys.argv[1]).read_text());n=packet['controls'];d=packet['target_degree'];size=1<<n
assert packet['status'] in ('OPTIMAL','FEASIBLE')
coverage=[0]*size;gates=[];used=0
for row in packet['gates']:
 den=row['denominator'];p={int(s):int(c) for s,c in row['terms']}
 assert len(p)==len(row['terms']) and all(c and 0<=s<size for s,c in p.items())
 assert max(s.bit_count() for s in p)==row['degree']
 union=0
 for s in p:union|=s
 assert union==row['used'];used|=union
 values=[p.get(s,0) for s in range(size)]
 for level in range(n):
  width=1<<level
  for at in range(0,size,2*width):
   for j in range(width):
    u,v=values[at+j],values[at+j+width];values[at+j]=u+v;values[at+j+width]=u-v
 assert all(v in (-den,0,den) for v in values)
 assert sum(v!=0 for v in values)==row['support_count']
 for x,v in enumerate(values):coverage[x]+=bool(v)
 assert row['payload_degree']==d-row['degree']>=1
 gates.append((p,den,row['payload_degree']))
assert set(coverage)=={1}
def xi(r):
 if r==1:return 1,1,{1:1}
 count,den,p=xi(r-1);out={}
 for s,c in p.items():
  out[(s<<2)|1]=c;out[(s<<2)|2]=c
  out[(s<<(count+2))|1]=c;out[(s<<(count+2))|2]=-c
 return 2*count+2,2*den,out
poly=collections.defaultdict(Q);offset=n
for gate,den,r in gates:
 count,bden,inner=xi(r)
 for s,c in gate.items():
  for t,z in inner.items():poly[s|(t<<offset)]+=Q(c*z,den*bden)
 offset+=count
poly={s:c for s,c in poly.items() if c};den=math.lcm(*(c.denominator for c in poly.values()));p={s:int(c*den) for s,c in poly.items()}
square=collections.defaultdict(int)
for s,c in p.items():
 for t,z in p.items():square[s^t]+=c*z
assert {s:c for s,c in square.items() if c}=={0:den*den}
allused=0
for s in p:allused|=s
count=allused.bit_count();degree=max(s.bit_count() for s in p)
assert count==packet['count'] and degree==d
assert used.bit_count()==packet['relevant_controls']
assert Q(packet['asymptotic_lift'])==Q(count+2,1<<d)
result=dict(status='PASS',verifier='A exact gate tables, full expansion and Boolean square',count=count,degree=degree,lift=str(Q(count+2,1<<d)),terms=len(p))
pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
