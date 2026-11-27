"""For each printed p.28 row, find the closest true single-heap row among all 55 expanded codes,
under misere/normal play and start size 0/1. Diagnostic for the reading of the p.28 table."""
import sys
sys.path.insert(0, '.')
exec(open('controls_rows.py').read().split("allrows = {}")[0])  # reuse parser: rows, codes
from referee_solver import Game
allc = [c for n in codes for c in codes[n]]
tr = {}
for c in allc:
    for mis in (True, False):
        g = Game(c, mis)
        tr[(c, mis)] = [g.outcome((n,)) for n in range(0, 40)]
for name, seq, per in rows:
    best = []
    for (c, mis), t in tr.items():
        for st in (0, 1):
            m = sum(a != b for a, b in zip(seq, t[st:st+len(seq)]))
            best.append((m, c, 'misere' if mis else 'normal', st))
    best.sort()
    own = [b for b in best if b[1] in codes[name] and b[2] == 'misere' and b[3] == 1][0]
    print(f"{name:9s} own(misere,from1)={own[0]:2d}  best={best[:3]}")
