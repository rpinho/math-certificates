"""Referee: exact colour maxima (own solver, upper_check.exact_rank_max) for
 - the 1,198 row words in rows.json (rank words on the 21-cube): REPORT claims all <= 13,
   with 12/12: 4, 12/13: 118, 13/12: 118, 13/13: 958;
 - the 28 windows of V.json: REPORT claims each is a rank restriction of a 23-letter word
   (22-cube) with exact maxima 13/13.
Usage: rows_exact.py DATA_DIR  (4 worker processes)
"""
import json
import sys
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, ".")
from upper_check import exact_rank_max  # noqa: E402


def both(w):
    out = []
    for c in "01":
        e, big = exact_rank_max(w, c, cap=14)
        out.append(">=14" if big else e)
    return w, tuple(out)


def main(dd):
    rj = json.load(open(f"{dd}/rows.json"))
    words = rj["words"]
    V = json.load(open(f"{dd}/V.json"))
    win = []
    for a, b in V:
        x, y = words[a], words[b]
        ok = x[1:] == y[:-1]
        win.append(x + y[-1] if ok else None)
    print("windows that are rank restrictions:", sum(w is not None for w in win), "of", len(win))
    with Pool(4) as p:
        res = p.map(both, words, chunksize=8)
        wres = p.map(both, [w for w in win if w])
    print("rows (21-cube) exact maxima distribution:", sorted(Counter(r for _, r in res).items(), key=str))
    print("rows with 12/12:", [w for w, r in res if r == (12, 12)])
    print("windows (22-cube) exact maxima:", Counter(r for _, r in wres))


if __name__ == "__main__":
    main(sys.argv[1])
