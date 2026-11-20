import gzip, json, os, subprocess, sys
PY = sys.executable; C = 'corrupt'
raw = json.load(gzip.open('../data/t-10-6-4.gz'))
fam = raw[1][0]; i = fam.index(31); raw[1][0] = fam[:i] + fam[i+1:]       # 31 = 1|30 -> closure broken
json.dump(raw, gzip.open(C + '/data/t-10-6-4.gz', 'wt'))
r = subprocess.run([PY, '-I', 'induct.py', C + '/data', C + '/out'], capture_output=True, text=True).stdout.strip()
line = 'drop set 31 (=1|30) from family t-10-6-4[z=1][0]: %s' % r
open(C + '/controls.log', 'a').write(line + '\n'); print(line)
