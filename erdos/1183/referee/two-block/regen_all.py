"""Referee: regenerate the all-splits DIMACS from the definition (PROOF.md section 5).

Splits (a,b), a>=b, a+b=23, b=0..11 (b=0 is the all-rank case).
Per split: grid variables for cells (i,j), 0<=i<=a, 0<=j<=b, var = base + j*(a+1) + i
(true = colour 1), then 4 selectors for window 0 and 4 for window 1.
Window shape: b<=2 -> shorten A by two (u=a-2, v=b), offsets along A;
              b>=3 -> shorten B by two (u=a, v=b-2), offsets along B.
Selector k of a window forces the window's cells to the rank embedding of word k.
Usage: regen_all.py OUT.cnf
"""
import sys

WORDS = ["0010011100101100011011", "0011001011100010110011",
         "1100110100011101001100", "1101100011010011100100"]


def build():
    clauses = []
    splits = [(23 - b, b) for b in range(12)]
    nxt = 13
    clauses.append(list(range(1, 13)))
    for s, (a, b) in enumerate(splits, start=1):
        base = nxt
        nxt += (a + 1) * (b + 1)
        var = lambda i, j: base + j * (a + 1) + i
        if b <= 2:
            u, v = a - 2, b
            offs = [(0, 0), (1, 0)]
        else:
            u, v = a, b - 2
            offs = [(0, 0), (0, 1)]
        sels = []
        for _ in offs:
            sels.append(list(range(nxt, nxt + 4)))
            nxt += 4
        for (di, dj), sl in zip(offs, sels):
            clauses.append([-s] + sl)
            for k, w in enumerate(WORDS):
                cells = sorted((var(i + di, j + dj), w[i + j])
                               for j in range(v + 1) for i in range(u + 1))
                for x, c in cells:
                    clauses.append([-sl[k], x if c == "1" else -x])
    return nxt - 1, clauses


if __name__ == "__main__":
    nv, cl = build()
    with open(sys.argv[1], "w") as f:
        f.write(f"p cnf {nv} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")
