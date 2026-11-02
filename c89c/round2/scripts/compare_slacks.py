import re,json
from pathlib import Path
from fractions import Fraction
pairs={'c6_9.cert':['csdp_lift9_exact.log','csdp_lift9_independent.log'],'c6_8.cert.gz':['csdp_exact.log','csdp_legacy.log'],'c5_8.cert.gz':['k5_column_exact.log','k5_column_legacy.log']};out={}
for name,logs in pairs.items():
 vals=[]
 for log in logs:
  text=Path('receipts',log).read_text();assert 'PASS' in text
  m=re.search(r'MIN_SLACK (\d+) / (\d+) at (\d+)',text) or re.search(r'Smallest slack numerator (\d+), denominator (\d+), graph index (\d+)',text)
  assert m;vals.append((Fraction(int(m[1]),int(m[2])),int(m[3])))
 assert vals[0]==vals[1] and vals[0][0]>0
 out[name]={'minimum_slack':str(vals[0][0]),'graph_index':vals[0][1],'agree':True,'logs':logs}
Path('receipts/exact_slacks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
