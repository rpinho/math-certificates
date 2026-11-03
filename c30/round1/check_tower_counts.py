"""Compare the exact strip tower to the harvested exhaustive enumeration."""
import argparse
import json
from pathlib import Path
from audit_strip_encoding import tower

p=argparse.ArgumentParser();p.add_argument('enumeration');args=p.parse_args()
rows=[json.loads(s) for s in Path(args.enumeration).read_text().splitlines() if s.strip()]
enc=tower(max(r['n'] for r in rows))
result=[]
for row in rows:
    n=row['n']
    for name,arr in enc.items():
        predicted={str(u):c for (u,v),c in arr[n].items() if v==0 and c}
        assert predicted==row['series'][name], (n,name,predicted,row['series'][name])
    assert row['roundtrips']==row['dominoes']
    result.append({'n':n,'status':'PASS','all_avoiders':row['avoiders'],'domino_encodings':row['roundtrips'],'all_five_series_match':True})
Path('artifacts/tower_counts_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
