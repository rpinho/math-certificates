"""Exact cubic potential/count envelope, Walsh implementation A."""
import json,os,pathlib,sys
import numpy as np
assert os.getpriority(os.PRIO_PROCESS,0)>=10
raw=pathlib.Path(sys.argv[1]).read_text().splitlines();rows=[]
limits=[0]*11;nine=[];ten=[]
parity=np.array([x.bit_count()%2 for x in range(1024)],dtype=np.int64)
for index,line in enumerate(raw,1):
 assert len(line)==1024 and set(line)<=set('01')
 a=1-2*(np.array([int(c) for c in line])^parity)
 width=1
 while width<1024:
  b=a.reshape(-1,2*width);u=b[:,:width].copy();v=b[:,width:].copy();b[:,:width]=u+v;b[:,width:]=u-v;width*=2
 assert int(a@a)==1024**2
 masks=[s for s in range(1024) if a[s]];assert max(map(int.bit_count,masks),default=0)<=3
 local=[max((s.bit_count() for s in masks if s>>j&1),default=0) for j in range(10)]
 count=sum(d>0 for d in local);units=sum(1<<(3-d) for d in local if d)
 for budget in range(count,11):limits[budget]=max(limits[budget],units)
 if count==9:assert a[0]==0 and all(d in (0,3) for d in local);nine.append(index)
 if count==10:assert all(s.bit_count()==3 for s in masks);ten.append(index)
 rows.append((count,units))
assert len(rows)==761 and limits==[0,4,4,6,8,8,8,8,8,9,10]
assert nine==[485,571,633,689,701,716] and ten==[700]
result=dict(status='PASS',classes=761,potential_units_eighths=limits,nine_balanced=nine,ten_homogeneous=ten)
pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
