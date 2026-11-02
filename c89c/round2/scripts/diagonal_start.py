"""Keep the verified primal start and use a positive diagonal dual start."""
from pathlib import Path
source=Path('artifacts/ordered8balanced_color.warm');dest=Path('artifacts/ordered8diag_color.warm')
with source.open() as src,dest.open('w') as out:
 out.write(next(src))
 for line in src:
  v=line.split()
  if v[0]=='1' and v[2]!=v[3]:continue
  out.write(line)
print('diagonal dual start written',flush=True)
