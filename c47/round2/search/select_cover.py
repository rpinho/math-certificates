"""Our exact greedy witness pruning helper, reused from c47r2."""
import bisect
def select_cover(rectangles):
 # Exact greedy cover on each x slab, with a prefix-maximum tree over active
 # interval starts. Candidate pruning only; verify_exact.py checks the result.
 import heapq
 if not rectangles:return []
 ys=sorted({r[2] for r in rectangles});yi={y:i for i,y in enumerate(ys)}
 size=1
 while size<len(ys):size*=2
 tree=[(-1,-1)]*(2*size);heaps=[[] for _ in ys];counts=[0]*len(ys);present=[False]*len(ys)
 live=[False]*len(rectangles);active_y=[];used=set();events={}
 for i,(x0,x1,y0,y1) in enumerate(rectangles):events.setdefault(x0,[]).append((1,i));events.setdefault(x1,[]).append((-1,i))
 def update(j,value):
  j+=size;tree[j]=value;j//=2
  while j:tree[j]=max(tree[2*j],tree[2*j+1]);j//=2
 def prefix(pos):
  l=size;r=size+bisect.bisect_right(ys,pos);answer=(-1,-1)
  while l<r:
   if l&1:answer=max(answer,tree[l]);l+=1
   if r&1:r-=1;answer=max(answer,tree[r])
   l//=2;r//=2
  return answer
 for x,changes in sorted(events.items()):
  touched=set()
  for sign,i in changes:
   j=yi[rectangles[i][2]];touched.add(j)
   if sign==1:live[i]=True;counts[j]+=1;heapq.heappush(heaps[j],(-rectangles[i][3],i))
   else:live[i]=False;counts[j]-=1
  for j in touched:
   h=heaps[j]
   while h and not live[h[0][1]]:heapq.heappop(h)
   has=counts[j]>0
   if has and not present[j]:bisect.insort(active_y,j)
   elif present[j] and not has:active_y.pop(bisect.bisect_left(active_y,j))
   present[j]=has;update(j,(-h[0][0],h[0][1]) if h else (-1,-1))
  if not active_y:continue
  pos=ys[active_y[0]]
  while True:
   end,i=prefix(pos)
   if end>pos:used.add(i);pos=end
   else:
    j=bisect.bisect_left(active_y,bisect.bisect_right(ys,pos))
    if j==len(active_y):break
    pos=ys[active_y[j]]
 return sorted(used)
