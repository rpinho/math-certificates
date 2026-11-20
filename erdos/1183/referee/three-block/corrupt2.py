import gzip, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lrat import check
PY = sys.executable; C = 'corrupt'; out = []
for name in ('split23/9-7-7', 'split23/11-11-1', 'split22/10-7-5', 'face/7-7-7'):
    L = open('../data/%s.cnf' % name).read().splitlines()
    nc = int(L[0].split()[3])
    tok = open('../data/%s.lrat' % name).readline().split()[1:]; hints = [int(x) for x in tok[tok.index('0')+1:-1]]
    h = [x for x in hints if 0 < x <= nc][0]                      # first original clause the proof uses
    t = L[h].split(); t[0] = str(-int(t[0])); L[h] = ' '.join(t)
    p = '%s/used_%s.cnf' % (C, name.replace('/', '_')); open(p, 'w').write('\n'.join(L) + '\n')
    dt = subprocess.run(['ext/lrat-check', p, '../data/%s.lrat' % name], capture_output=True, text=True).stdout
    out.append('flip first literal of used clause %d in %s: own=%s | drat-trim verified=%s' % (h, name, check(p, '../data/%s.lrat' % name), 'c VERIFIED' in dt))
import sys as _s; _s.exit(print('\n'.join(out)) or open(C + '/controls.log', 'a').write('\n'.join(out) + '\n') and 0)
raw = None
fam = raw[1][0]; i = fam.index(31); raw[1][0] = fam[:i] + fam[i+1:]       # 31 = 1|30 -> closure broken
json.dump(raw, gzip.open(C + '/data/t-10-6-4.gz', 'wt'))
r = subprocess.run([PY, '-I', 'induct.py', C + '/data', C + '/out'], capture_output=True, text=True).stdout.strip()
out.append('drop set 31 (=1|30) from family t-10-6-4[z=1][0]: %s' % r)
open(C + '/controls.log', 'a').write('\n'.join(out) + '\n'); print('\n'.join(out))
