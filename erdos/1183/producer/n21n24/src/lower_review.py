import itertools,json,pathlib
from check import witness
words=['111','10101','1001001','110011001','101101001','1101001101','1011001101','1001101001']
factors=[[[0,1],[0,1]],[[0,2],[0,2]],[[0,3],[0,3]],[[0,1,4],[0,4]],[[0,2,5],[0,3]],[[0,3],[0,3],[0,3]],[[0,3],[0,3],[0,3]],[[0,3],[0,3],[0,3]]]
for w,fs in zip(words,factors):
 fam=[0];shift=0
 for ranks in fs:
  masks=[((1<<r)-1)<<shift for r in ranks];fam=[a|b for a in fam for b in masks];shift+=max(ranks)
 assert shift==len(w)-1
 witness(shift,w,1,w.count('1')+1,fam)
forbidden=set()
for w in words:
 inv=''.join(str(1-int(c)) for c in w);forbidden.update([w,w[::-1],inv,inv[::-1]])
covered=0
for b in itertools.product('01',repeat=12):
 w=''.join(b);assert any(v in w for v in forbidden),w;covered+=1
rows=[]
for n in range(21,25):
 q,r=divmod(n+1,20)
 rows.append(dict(n=n,chain=(n+2)//2,flower=(n+2+(n+1)//12)//2,omega=(n+3)//2 if n%2 else None,twenty=(n+2+2*q+(r>=12))//2))
pathlib.Path('logs/lower_bounds.json').write_text(json.dumps(dict(gadgets=8,twelve_words=covered,bounds=rows),indent=2)+'\n');print(rows)
