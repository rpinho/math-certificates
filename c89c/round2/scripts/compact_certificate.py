"""Remove exactly zero factor rows and wholly zero root families, losslessly."""
from pathlib import Path
import sys
lines=Path(sys.argv[1]).read_text().splitlines();h=list(map(int,lines[0].split()))
tokens=iter(map(int,' '.join(lines[1:]).split()));blocks=[]
for _ in range(h[3]):
    t,m,typ,d,height=[next(tokens) for _ in range(5)]
    keys=[next(tokens) for _ in range(d)]
    rows=[[next(tokens) for _ in range(d)] for _ in range(height)]
    rows=[row for row in rows if any(row)]
    blocks.append((t,m,typ,d,keys,rows))
assert next(tokens,None) is None
active={(t,m) for t,m,typ,d,keys,rows in blocks if rows}
blocks=[b for b in blocks if b[:2] in active];h[3]=len(blocks)
with open(sys.argv[2],'w') as f:
    print(*h,file=f)
    for t,m,typ,d,keys,rows in blocks:
        if not rows:rows=[[0]*d]
        print(t,m,typ,d,len(rows),file=f);print(*keys,file=f)
        for row in rows:print(*row,file=f)
print('blocks',len(blocks),'families',sorted(active),'factor rows',sum(len(b[-1]) for b in blocks))
