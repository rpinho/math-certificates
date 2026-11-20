"""Referee: independent replay of the exterior-count face induction (PROOF.md section 5).

Inputs (data only): ../data/faces.jsonl.gz  lines [u, v, z, [family, ...]], family = list of
23-bit masks. Every family is checked from the definition here:
  * members distinct, size >= 14, pairwise closed under | and &;
  * every member is a local set (mask < 2^d, d=u+v; bits 0..u-1 = A, u..d-1 = B) or an
    exterior prefix [k] = {0..k-1}, d < k <= 23, coloured 0 iff k-d <= z;
  * the exterior members all have one colour c (or there are none).
A checked family forbids, in context z, every table on which its local cells are all colour c.

Enumeration (mine): S(u,v,z) = tables T on the (u+1)x(v+1) grid surviving in context z.
  (0,0): both colours, every z in [0,23].
  (u,0): from left window (cells 0..u-1, context z+[T(u)=0]) and right window
         (cells 1..u, context z+[T(0)=0]) of shape (u-1,0).
  (u,v), v>=1: from lower (rows 0..v-1, context z+[T(u,v)=0]) and upper
         (rows 1..v, context z+[T(0,0)=0]) windows of shape (u,v-1).
Then every joined table is rejected iff some checked family of (u,v,z) is monochromatic on it.
Bit index of cell (i,j) is j*(u+1)+i, bit = colour.
"""
import gzip
import json
import sys
from collections import defaultdict

N = 23
TARGET = 14
WORDS = ["0010011100101100011011", "0011001011100010110011",
         "1100110100011101001100", "1101100011010011100100"]


def popcount(x):
    return bin(x).count("1")


def check_family(fam, u, v, z):
    """Return (cellmask, colours) or raise. colours = set of colours c it can forbid."""
    d = u + v
    if len(fam) < TARGET:
        raise ValueError("family too small")
    s = set(fam)
    if len(s) != len(fam):
        raise ValueError("duplicate member")
    for x in fam:
        if not (0 <= x < (1 << N)):
            raise ValueError("member out of range")
    fl = list(s)
    for i in range(len(fl)):
        a = fl[i]
        for j in range(i + 1, len(fl)):
            b = fl[j]
            if (a | b) not in s or (a & b) not in s:
                raise ValueError("not closed")
    cellmask = 0
    ext_cols = set()
    for x in fam:
        if x < (1 << d):
            i = popcount(x & ((1 << u) - 1))
            j = popcount(x >> u)
            cellmask |= 1 << (j * (u + 1) + i)
        else:
            k = popcount(x)
            if x != (1 << k) - 1 or k <= d:
                raise ValueError("member neither local nor exterior prefix")
            ext_cols.add(0 if k - d <= z else 1)
    if len(ext_cols) > 1:
        raise ValueError("exterior members of both colours (family can never be monochromatic)")
    cols = ext_cols if ext_cols else {0, 1}
    return cellmask, cols


def load_witnesses(path, drop=None):
    W = defaultdict(list)  # (u,v,z) -> list of (cellmask, colours)
    nfam = 0
    bad = 0
    with gzip.open(path, "rt") as f:
        for line in f:
            u, v, z, fams = json.loads(line)
            for fam in fams:
                nfam += 1
                if drop is not None and drop == nfam:
                    fam = fam[:-1]
                try:
                    W[(u, v, z)].append(check_family(fam, u, v, z))
                except ValueError as e:
                    bad += 1
                    print(f"  REJECTED family #{nfam} at {(u, v, z)}: {e}")
    return W, nfam, bad


def forbidden(T, ncell, wl):
    full = (1 << ncell) - 1
    for m, cols in wl:
        if 1 in cols and T & m == m:
            return True
        if 0 in cols and T & m == 0:
            return True
    return False


def join(child, W, Rp, t, u, v, Wit, stats):
    """child: dict z -> set of child tables (Rp-1 rows of width W). Returns dict z -> set."""
    nc = (Rp - 1) * W
    ov = (Rp - 2) * W
    ovmask = (1 << ov) - 1
    topbit = nc - 1
    out = {}
    for z in range(t + 1):
        surv = set()
        wl = Wit.get((u, v, z), [])
        for L0 in (0, 1):
            for Ut in (0, 1):
                Ls = [L for L in child.get(z + 1 - Ut, ()) if L & 1 == L0]
                Us = [U for U in child.get(z + 1 - L0, ()) if (U >> topbit) & 1 == Ut]
                idx = defaultdict(list)
                for U in Us:
                    idx[U & ovmask].append(U)
                for L in Ls:
                    for U in idx.get(L >> W, ()):
                        T = L | (U << W)
                        stats["joined"] += 1
                        if not forbidden(T, Rp * W, wl):
                            surv.add(T)
        if surv:
            out[z] = surv
    return out


def rank_table(w, u, v):
    T = 0
    for j in range(v + 1):
        for i in range(u + 1):
            if w[i + j] == "1":
                T |= 1 << (j * (u + 1) + i)
    return T


def main(path, drop=None):
    Wit, nfam, bad = load_witnesses(path, drop)
    print(f"families read {nfam}, rejected by checker {bad}, cases {len(Wit)}")
    stats = defaultdict(int)
    S = {}
    # base
    base = {}
    for z in range(N + 1):
        surv = {T for T in (0, 1) if not forbidden(T, 1, Wit.get((0, 0, z), []))}
        if surv:
            base[z] = surv
    S[(0, 0)] = base
    nsurv = sum(len(s) for s in base.values())
    for u in range(1, 22):
        S[(u, 0)] = join(S[(u - 1, 0)], 1, u + 1, N - u, u, 0, Wit, stats)
        nsurv += sum(len(s) for s in S[(u, 0)].values())
    for u in range(12, 21):
        for v in range(1, 22 - u):
            S[(u, v)] = join(S[(u, v - 1)], u + 1, v + 1, N - u - v, u, v, Wit, stats)
            nsurv += sum(len(s) for s in S[(u, v)].values())
    print(f"joined table/context pairs {stats['joined']}, survivors over all levels {nsurv}")
    ok = True
    for u in range(12, 22):
        v = 21 - u
        res = S[(u, v)]
        rk = {rank_table(w, u, v): w for w in WORDS}
        desc = {z: sorted(rk.get(T, "NONRANK") for T in s) for z, s in res.items()}
        print(f"shape ({u},{v}): survivors by context {desc}")
        if set(res) != {1} or res[1] != set(rk):
            ok = False
    # sizes per shape
    for key in sorted(S):
        print("  ", key, {z: len(s) for z, s in S[key].items()})
    # overlap comparisons
    mind = 99
    for w in WORDS:
        for w2 in WORDS:
            dd = sum(x != y for x, y in zip(w[1:], w2[:21]))
            mind = min(mind, dd)
            print(f"  suffix21({w}) vs prefix21({w2}): {dd} differing positions")
    print("minimum difference", mind)
    print("FACE CLAIM", "CONFIRMED" if ok and mind >= 1 else "NOT CONFIRMED")
    return ok


if __name__ == "__main__":
    drop = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(sys.argv[1], drop)
