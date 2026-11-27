import sys, itertools
sys.path.insert(0, '.')
exec(open('controls_rows.py').read().split("allrows = {}")[0])
import referee_solver as rs
orig = rs.heap_options
def make(perm):
    # perm maps paper bit -> meaning: meaning 1 whole, 2 leave, 4 split
    def ho(digits, n):
        nd = []
        for d in digits:
            e = 0
            for b, m in zip((1, 2, 4), perm):
                if d & b: e |= m
            nd.append(e)
        return orig(tuple(nd), n)
    return ho
for perm in itertools.permutations((1, 2, 4)):
    rs.heap_options = make(perm)
    for mis in (True, False):
        for st in (0, 1):
            tot = 0; exact = 0
            for name, seq, per in rows:
                c = codes[name][0]
                g = rs.Game(c, mis)
                t = [g.outcome((n,)) for n in range(st, st + len(seq))]
                m = sum(a != b for a, b in zip(seq, t)); tot += m; exact += (m == 0)
            print(perm, 'misere' if mis else 'normal', 'start', st, 'total mismatches', tot, 'exact rows', exact)
