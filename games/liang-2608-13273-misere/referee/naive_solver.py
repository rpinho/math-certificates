import sys, itertools
sys.path.insert(0, '.')
from referee_solver import Game, parse_code
from functools import lru_cache
# naive independent recursion on unsorted tuples, for cross-check
def naive(code, misere=True):
    d = parse_code(code)
    @lru_cache(None)
    def o(h):
        opts = []
        for i, n in enumerate(h):
            rest = h[:i] + h[i+1:]
            for s, dg in enumerate(d):
                r = n - s
                if r < 0 or dg == 0: continue
                if s > 0 and dg & 1 and r == 0: opts.append(rest)
                if s > 0 and dg & 2 and r > 0: opts.append(rest + (r,))
                if dg & 4:
                    for a in range(1, r):
                        opts.append(rest + (a, r - a))
        if not opts: return 'N' if misere else 'P'
        return 'N' if any(o(tuple(sorted(x))) == 'P' for x in opts) else 'P'
    return lambda h: o(tuple(sorted(h)))
