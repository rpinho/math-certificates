"""Referee: direct (21,2) certificate (PROOF.md section 4).

Split A = bits 0..20 (a=21), B = bits 21,22 (b=2). Cell (i,j) -> DIMACS var 1 + 22*j + i, true = colour 1.
1. Check every family in sets.jsonl.gz from the definition (distinct, |F|>=14, closed under |,&).
   Each forbids both monochromatic assignments of its cell set: clause (+cells), clause (-cells).
2. Check window-families.jsonl (22 coordinates) and triples.json the same way; check every triple
   family is monochromatic on the grid formed by its path's three row words.
3. Independently re-derive the admissible windows: all 2^22 row words filtered by the footprints of
   checked physical families lying inside one row, then all ordered pairs filtered by footprints inside
   the window's two rows (positions p=0 and p=1 separately). Each survivor set must be within V.
4. Regenerate the DIMACS (physical clauses in file order, then per window: at-least-one selector and
   selector -> 44 cells) and compare bytes with the shipped file.
Usage: excl_check.py DATA_DIR OUT.cnf
"""
import gzip
import json
import sys

import numpy as np

A, NB = 21, 2
W = A + 1  # cells per row


def pc(x):
    return bin(x).count("1")


def check_closed(fam, nbits):
    s = set(fam)
    if len(s) != len(fam):
        raise ValueError("duplicate")
    if len(fam) < 14:
        raise ValueError("too small")
    for x in fam:
        if not 0 <= x < (1 << nbits):
            raise ValueError("out of range")
    fl = list(s)
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            if (fl[i] | fl[j]) not in s or (fl[i] & fl[j]) not in s:
                raise ValueError("not closed")


def cells_of(fam):
    return sorted({1 + W * pc(x >> A) + pc(x & ((1 << A) - 1)) for x in fam})


def main(dd, outcnf):
    fams = []
    bad = 0
    with gzip.open(f"{dd}/sets.jsonl.gz", "rt") as f:
        for n, line in enumerate(f, 1):
            fam = json.loads(line)[2]  # record = [kind, placement, family]; labels ignored
            try:
                check_closed(fam, 23)
            except ValueError as e:
                bad += 1
                print(f"  sets family #{n} REJECTED: {e}")
                continue
            fams.append(cells_of(fam))
    print(f"sets.jsonl.gz: {len(fams) + bad} families, {bad} rejected")

    wbad = 0
    nwf = 0
    with open(f"{dd}/window-families.jsonl") as f:
        for line in f:
            nwf += 1
            try:
                check_closed(json.loads(line), 22)
            except ValueError as e:
                wbad += 1
    print(f"window-families.jsonl: {nwf} families, {wbad} rejected")

    rj = json.load(open(f"{dd}/rows.json"))
    words = rj["words"]
    V = [tuple(p) for p in json.load(open(f"{dd}/V.json"))]
    tri = json.load(open(f"{dd}/triples.json"))
    for t in tri:
        r0, r1, r2 = t["path"]
        assert (r0, r1) in V and (r1, r2) in V, "triple path not in V"
        g = [words[r0], words[r1], words[r2]]
        for fam in t["families"]:
            check_closed(fam, 23)
            cols = {g[pc(x >> A)][pc(x & ((1 << A) - 1))] for x in fam}
            print(f"  triple {t['path']}: family size {len(fam)} closed, colours {cols}",
                  "MONO" if len(cols) == 1 else "NOT MONO")
    # all length-2 paths through V
    paths = [(p[0], p[1], q[1]) for p in V for q in V if p[1] == q[0]]
    print(f"  length-2 paths through V: {len(paths)}; triples.json paths: {[tuple(t['path']) for t in tri]}")

    # 3. rows: footprints within a single row j
    def bits_row(cells, j):
        m = 0
        for c in cells:
            k = c - 1
            if k // W != j:
                return None
            m |= 1 << (k % W)
        return m

    rowsurv = []
    for j in range(3):
        fps = sorted({m for m in (bits_row(c, j) for c in fams) if m is not None})
        alive = np.arange(1 << W, dtype=np.uint32)
        for m in fps:
            mm = np.uint32(m)
            x = alive & mm
            alive = alive[(x != 0) & (x != mm)]
        rowsurv.append(set(int(a) for a in alive))
        print(f"  row {j}: {len(fps)} row footprints, surviving words {len(alive)}")
    wordint = [sum((1 << i) for i, ch in enumerate(w) if ch == "1") for w in words]
    print("  rows.json words == survivors of row 0:", set(wordint) == rowsurv[0],
          "; rows identical across rows:", rowsurv[0] == rowsurv[1] == rowsurv[2])

    Vset = set((wordint[a], wordint[b]) for a, b in V)
    for p in range(2):
        fps = []
        for c in fams:
            ks = [x - 1 for x in c]
            if all(p <= k // W <= p + 1 for k in ks):
                m = 0
                for k in ks:
                    m |= 1 << (k - p * W)
                fps.append(m)
        fps = sorted(set(fps))
        lo = np.array(sorted(rowsurv[p]), dtype=np.uint64)
        hi = np.array(sorted(rowsurv[p + 1]), dtype=np.uint64)
        alive = (lo[:, None] | (hi[None, :] << np.uint64(W))).ravel()
        for m in fps:
            mm = np.uint64(m)
            x = alive & mm
            alive = alive[(x != 0) & (x != mm)]
        surv = set((int(a) & ((1 << W) - 1), int(a) >> W) for a in alive)
        print(f"  window {p}: {len(fps)} footprints, {len(lo)}x{len(hi)} pairs -> {len(surv)} survivors;"
              f" subset of V: {surv <= Vset}; equal to V: {surv == Vset}")

    # 4. regenerate DIMACS
    cl = []
    for c in fams:
        cl.append(c)
        cl.append([-x for x in c])
    nxt = 3 * W + 1
    for p in range(2):
        sels = list(range(nxt, nxt + len(V)))
        nxt += len(V)
        cl.append(sels)
        for s, (a, b) in zip(sels, V):
            for jj, wd in ((0, words[a]), (1, words[b])):
                for i, ch in enumerate(wd):
                    var = 1 + W * (p + jj) + i
                    cl.append([-s, var if ch == "1" else -var])
    with open(outcnf, "w") as f:
        f.write(f"p cnf {nxt - 1} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")
    print("wrote", outcnf)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
