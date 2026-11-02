"""Independent exact verification of the stated construction-family ceiling.
This is not a universal R_d upper bound. No search imports.
"""
import json,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=json.loads((root/'compositions.json').read_text())
assert packet['model']=='disjoint cubic-catalogue compositions'
lines=(root/'inputs/round7/inputs/gap1/sources/F10T6.txt').read_text().splitlines()
assert len(lines)==761
spectra=[]
for line in lines:
 assert len(line)==1024 and set(line)<={'0','1'}
 a=[-1 if (int(v)+(x.bit_count()%2))%2 else 1 for x,v in enumerate(line)]
 for width in (1,2,4,8,16,32,64,128,256,512):
  for first in range(0,1024,2*width):
   for j in range(width):
    u,v=a[first+j],a[first+j+width];a[first+j],a[first+j+width]=u+v,u-v
 masks=[s for s in range(1,1024) if a[s]];assert all(s.bit_count()<=3 for s in masks)
 used=0
 for s in masks:used|=s
 variables=[j for j in range(10) if used>>j&1]
 spectra.append((masks,variables))
summary=[]
for data in packet['degrees']:
 d=data['degree'];total=0;global_max=0
 assert len(data['rows'])==761
 for index,(masks,variables) in enumerate(spectra):
  row=data['rows'][index];assert row['line']==index+1
  local={j:max(s.bit_count() for s in masks if s>>j&1) for j in variables}
  maximum=-1;count=0
  if max([0]+[s.bit_count() for s in masks])<=d:
   order=list(reversed(variables));remaining=[d-s.bit_count() for s in masks]
   touches={j:[z for z,s in enumerate(masks) if s>>j&1] for j in order}
   def visit(at,value):
    global maximum,count
    if at==len(order):
     count+=1;maximum=max(maximum,value);return
    j=order[at];top=min([d-local[j]]+[remaining[z] for z in touches[j]])
    for extra in range(top,-1,-1):
     for z in touches[j]:remaining[z]-=extra
     visit(at+1,value+3*(1<<extra)-2)
     for z in touches[j]:remaining[z]+=extra
   visit(0,0)
  assert maximum==row['max'] and count==row['feasible'],(d,index,maximum,row)
  if maximum>=0:
   w=row['weights'];assert len(w)==10
   assert all((1<=w[j]<=d if j in variables else w[j]==0) for j in range(10))
   assert all(sum(w[j] for j in variables if s>>j&1)<=d for s in masks)
   assert sum(3*(1<<(w[j]-1))-2 for j in variables)==maximum
  total+=count;global_max=max(global_max,maximum)
 assert global_max==data['maximum']==3*(1<<(d-1))-2
 assert total==data['feasible']
 summary.append({'degree':d,'maximum':global_max,'allocations':total})
 assert d!=5 or global_max<47
receipts=root.parent/'receipts';receipts.mkdir(exist_ok=True)
(receipts/'compositions_a.json').write_text(json.dumps({'status':'PASS','scope':'only disjoint compositions of cubic catalogue with Xi seeds','rows':summary},indent=2)+'\n')
print(json.dumps(summary),flush=True)
