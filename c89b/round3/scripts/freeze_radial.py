"""Freeze the simple radial construction as a full ordinary rational graphon."""
import gzip,json,pathlib,sys
d,L,D,P,Q=map(int,sys.argv[1:6]);dest=pathlib.Path(sys.argv[6]);assert d%2==0 and 2<=d<=6 and 2<=L<=8 and D>0 and 0<=P<=D and 0<=Q<=D
vertices=[(a,x) for a in range(L) for x in range(1<<d)];R=[]
for a,x in vertices:
 row=[]
 for b,y in vertices:
  w=(x^y).bit_count();dist=min(w,d+1-w)
  row.append((P if dist==1 else D if dist==2 else 0) if a==b else (D if dist==0 else Q if dist==3 else 0))
 R.append(row)
z=dict(schema='rational-step-graphon-v1',edge_probability_denominator=D,block_weights=[1]*len(R),red_probability_numerators=R,radial_parameters=dict(dimension=d,layers=L,p_numerator=P,q_numerator=Q),status='candidate and unrefereed; accepted only with exact receipts')
raw=json.dumps(z,separators=(',',':')).encode();dest.write_bytes(gzip.compress(raw,mtime=0) if dest.suffix=='.gz' else raw)
print('FROZEN',dest,len(R),'parts',flush=True)
