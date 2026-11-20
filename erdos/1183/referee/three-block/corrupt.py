import gzip, json, os, shutil, subprocess, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lrat import check
PY = sys.executable
C = 'corrupt'; out = []
def lines(p): return open(p).read().splitlines()
# 1. flip one clause literal (a selector->cell implication used by the proof) in split23 and face roots
for name in ('split23/9-7-7', 'split23/11-11-1', 'face/7-7-7', 'face/11-10-0'):
    L = lines('../data/%s.cnf' % name); k = 2 if name.startswith('split') else 4
    t = L[k].split(); t[-2] = str(-int(t[-2])); L[k] = ' '.join(t)
    p = '%s/%s.cnf' % (C, name.replace('/', '_')); open(p, 'w').write('\n'.join(L) + '\n')
    own = check(p, '../data/%s.lrat' % name)
    dt = subprocess.run(['ext/lrat-check', p, '../data/%s.lrat' % name], capture_output=True, text=True).stdout
    out.append('flip literal %s clause %d: own=%s | drat-trim verified=%s' % (name, k, own, 'c VERIFIED' in dt))
# regeneration comparison detects the flipped split23 clause
exec(open('roots.py').read().split('s23 = ')[0])
out.append('flip literal split23/9-7-7: regenerated clause multiset equal = %s' % (split23(9, 7, 7) == cnf('%s/split23_9-7-7.cnf' % C)))
# 2. alter one LRAT hint
for name in ('split23/9-7-7', 'face/7-7-7', 'split22/10-7-5'):
    L = lines('../data/%s.lrat' % name)
    t = L[0].split(); z = t.index('0', 1); t[z + 1] = str(int(t[z + 1]) + 1); L[0] = ' '.join(t)
    p = '%s/%s.lrat' % (C, name.replace('/', '_')); open(p, 'w').write('\n'.join(L) + '\n')
    own = check('../data/%s.cnf' % name, p)
    dt = subprocess.run(['ext/lrat-check', '../data/%s.cnf' % name, p], capture_output=True, text=True).stdout
    out.append('alter hint %s: own=%s | drat-trim verified=%s' % (name, own, 'c VERIFIED' in dt))
# 3. drop one set from witness families: induction data copy with one used family damaged
os.makedirs(C + '/data', exist_ok=True)
for f in os.listdir('../data'):
    if f.endswith('.gz'): shutil.copy('../data/' + f, C + '/data/' + f)
raw = json.load(gzip.open('../data/t-10-6-4.gz'))
fam = raw[1][0]; dropped = fam[4]; raw[1][0] = fam[:4] + fam[5:]
json.dump(raw, gzip.open(C + '/data/t-10-6-4.gz', 'wt'))
r = subprocess.run([PY, '-I', 'induct.py', C + '/data', C + '/out'], capture_output=True, text=True).stdout.strip()
out.append('drop set %d from family t-10-6-4[z=1][0]: %s' % (dropped, r))
# split22 family with one set dropped -> rejected by the family check
raw = json.load(gzip.open('../data/split22/10-7-5.families.gz')); f0 = raw[0]
S = set(f0[:3] + f0[4:])
out.append('drop set from split22/10-7-5 family 0: closed=%s size=%d (need closed and 13)' % (all((a|b) in S and (a&b) in S for a in S for b in S), len(S)))
open(C + '/controls.log', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
