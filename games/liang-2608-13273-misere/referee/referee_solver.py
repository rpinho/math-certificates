#!/usr/bin/env python3
"""Clean-room exact outcome solver for octal games (impartial or partizan),
written from DEFINITIONS.md only (Liang arXiv:2608.13273v2 sec. 2.1, 3.2).

Code d0.d1d2d3...: digit d_s (s >= 1) is a sum of bits
  1: remove a whole heap of exactly s tokens
  2: remove s tokens, leaving a nonempty remainder
  4: remove s tokens, split the remainder into two nonempty heaps
d0 may be 0 or 4 (4 = split a heap into two nonempty heaps, removing nothing).

Outcome (Def. 2.1 / 2.2): a terminal position is P under normal play and N
under misere play; otherwise N iff some option is P.

Partizan codes "Lcode:Rcode" use the paper's labelled reduction (sec. 3.2):
the label says whose rules apply and flips after every move.

Usage:
  referee_solver.py CODE POS [POS ...]   e.g. 0.157 28,7,4,4 25,4,4,4
  referee_solver.py --normal CODE POS
  referee_solver.py --row CODE N         single-heap outcomes 1..N
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def parse_code(code):
    head, _, tail = code.partition(".")
    d0 = int(head)
    if d0 not in (0, 4):
        raise ValueError("d0 must be 0 or 4: %r" % code)
    digits = [d0] + [int(c, 8) for c in tail]
    for d in digits:
        if not 0 <= d <= 7:
            raise ValueError(code)
    return tuple(digits)


def heap_options(digits, n):
    """All results of one move on a single heap of size n, as tuples of heap sizes."""
    out = set()
    for s, d in enumerate(digits):
        if d == 0 or s > n:
            continue
        r = n - s
        if s == 0:  # d0 = 4: pure split
            if d & 4:
                for a in range(1, r // 2 + 1):
                    out.add((r - a, a))
            continue
        if d & 1 and r == 0:
            out.add(())
        if d & 2 and r > 0:
            out.add((r,))
        if d & 4 and r >= 2:
            for a in range(1, r // 2 + 1):
                out.add((r - a, a))
    return tuple(out)


class Game:
    """One octal code (impartial) or a pair (partizan). Memoised per instance."""

    def __init__(self, code, misere=True):
        self.code = code
        self.misere = misere
        if ":" in code:
            l, r = code.split(":")
            self.rules = (parse_code(l), parse_code(r))
        else:
            d = parse_code(code)
            self.rules = (d, d)
        self.partizan = self.rules[0] != self.rules[1]
        self._hopt = [{}, {}]
        self.memo = {}

    def hopt(self, side, n):
        c = self._hopt[side]
        if n not in c:
            c[n] = heap_options(self.rules[side], n)
        return c[n]

    def canon(self, heaps, side):
        # empty heaps never move; order is irrelevant (sec. 3.2)
        h = tuple(sorted((x for x in heaps if x > 0), reverse=True))
        return (side if self.partizan else 0, h)

    def options(self, key):
        side, h = key
        nxt = 1 - side if self.partizan else 0
        seen = set()
        for i, n in enumerate(h):
            if i and h[i - 1] == n:
                continue
            rest = h[:i] + h[i + 1:]
            for res in self.hopt(side, n):
                k = self.canon(rest + res, nxt)
                if k not in seen:
                    seen.add(k)
                    yield k

    def outcome_key(self, key):
        memo = self.memo
        if key in memo:
            return memo[key]
        # iterative DFS to avoid deep Python recursion cost
        # frame: [key, option iterator, saw_any_option, pending child]
        stack = [[key, self.options(key), False, None]]
        while stack:
            fr = stack[-1]
            k, it, any_opt, pend = fr
            if k in memo:
                stack.pop()
                continue
            if pend is not None:
                fr[3] = None
                if memo[pend] == "P":
                    memo[k] = "N"
                    stack.pop()
                    continue
            res = None
            descended = False
            for o in it:
                any_opt = True
                v = memo.get(o)
                if v is None:
                    fr[2] = True
                    fr[3] = o
                    stack.append([o, self.options(o), False, None])
                    descended = True
                    break
                if v == "P":
                    res = "N"
                    break
            if descended:
                continue
            if res is None:
                if not any_opt:  # terminal
                    res = "N" if self.misere else "P"
                else:
                    res = "P"
                memo[k] = res
                stack.pop()
                continue
            if res is not None:
                memo[k] = res
                stack.pop()
        return memo[key]

    def outcome(self, heaps, side=0):
        return self.outcome_key(self.canon(tuple(heaps), side))


def parse_pos(s):
    s = s.strip().strip("()")
    return tuple(int(x) for x in s.split(",") if x.strip()) if s else ()


def main(argv):
    misere = True
    if argv and argv[0] == "--normal":
        misere = False
        argv = argv[1:]
    if argv and argv[0] == "--row":
        g = Game(argv[1], misere)
        print(" ".join(g.outcome((n,)) for n in range(1, int(argv[2]) + 1)))
        return
    g = Game(argv[0], misere)
    for p in argv[1:]:
        print(p, g.outcome(parse_pos(p)))


if __name__ == "__main__":
    main(sys.argv[1:])
