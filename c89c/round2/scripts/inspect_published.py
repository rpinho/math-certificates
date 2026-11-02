import json
from pathlib import Path
x=json.load(open('sources/published_c5.json'))
print('keys',[(k,type(v).__name__,len(v) if hasattr(v,'__len__') else v) for k,v in x.items()])
for k,v in x.items():
 if k not in ('admissible_graphs',): print(k,str(v)[:800])
