"""Compare p.28 printed single-heap misere outcome rows (2608.13273v2) with referee_solver."""
import sys, re
sys.path.insert(0, '.')
from referee_solver import Game
txt = open('inputs/sources/2608.13273v2.txt', encoding='utf-8').read().splitlines()
start = next(i for i, l in enumerate(txt) if l.strip() == 'Outcomes')
rows = []
i = start + 2
while i < len(txt) and not txt[i].startswith('The above results'):
    name, seq, per = txt[i].strip(), txt[i+1].split(), txt[i+2].strip()
    rows.append((name, [c for c in seq if c in 'PN'], per)); i += 3
def expand(name):
    # shorthand from [25] as quoted in sec 3.5.2: dot d = d,d+1; ddot d = d,d+2; bar d = d..d+3
    out = ['']
    j = 0
    while j < len(name):
        c = name[j]; mark = name[j+1] if j + 1 < len(name) else ''
        if c.isdigit() and mark in '̇̈̄' and False: pass
        j += 1
        if c == '˙': out = [o[:-1] + str(int(o[-1]) + k) for o in out for k in (0, 1)]; continue
        if c == '¨': out = [o[:-1] + str(int(o[-1]) + k) for o in out for k in (0, 2)]; continue
        if c == '¯': out = [o[:-1] + str(int(o[-1]) + k) for o in out for k in (0, 1, 2, 3)]; continue
        out = [o + c for o in out]
    return out
codes = {}
for name, seq, per in rows:
    # marks precede the digit they modify in the text extraction (e.g. '0.32˙6' = 0.32 dot-6)
    n2 = re.sub('([˙¨¯])(\\d)', lambda m: m.group(2) + m.group(1), name)
    codes[name] = expand(n2)
allrows = {}
for name, seq, per in rows:
    L = len(seq)
    for c in codes[name]:
        g = Game(c)
        true = [g.outcome((n,)) for n in range(1, L + 1)]
        allrows[c] = true
        mism = [n for n in range(1, L + 1) if true[n-1] != seq[n-1]]
        print(f"{name:10s} {c:6s} printed-period {per:8s} mismatches at sizes {mism[:12]}{' ...' if len(mism)>12 else ''} ({len(mism)}/{L})")
# does any printed row match a different game's true row exactly?
print('cross-match (printed row of X equals true row of Y):')
for name, seq, per in rows:
    hits = [c for c, t in allrows.items() if t == seq]
    print(' ', name, '->', hits)
