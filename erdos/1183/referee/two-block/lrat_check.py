"""Referee's own LRAT checker (RUP-with-hints only; RAT steps, i.e. negative hints, are rejected).

Usage: lrat_check.py FORMULA.cnf PROOF.lrat
Prints 'VERIFIED UNSAT' and exits 0 only if the proof derives the empty clause,
every addition step is justified by its hints by unit propagation in hint order,
and every referenced clause exists and has not been deleted.
"""
import sys


def read_cnf(path):
    clauses = {}
    nv = nc = None
    cur = []
    with open(path) as f:
        for line in f:
            t = line.split()
            if not t or t[0] == "c":
                continue
            if t[0] == "p":
                assert t[1] == "cnf"
                nv, nc = int(t[2]), int(t[3])
                continue
            for x in map(int, t):
                if x == 0:
                    clauses[len(clauses) + 1] = cur
                    cur = []
                else:
                    assert abs(x) <= nv, "literal out of range"
                    cur.append(x)
    assert not cur and len(clauses) == nc, "clause count mismatch"
    return nv, clauses


def check(cnf, lrat):
    nv, db = read_cnf(cnf)
    last = len(db)
    empty = False
    with open(lrat) as f:
        for ln, line in enumerate(f, 1):
            t = line.split()
            if not t:
                continue
            cid = int(t[0])
            if t[1] == "d":
                ids = list(map(int, t[2:]))
                assert ids[-1] == 0
                for i in ids[:-1]:
                    db.pop(i, None)
                continue
            assert cid > last, f"line {ln}: non-increasing id"
            nums = list(map(int, t[1:]))
            z = nums.index(0)
            lits, hints = nums[:z], nums[z + 1:]
            assert hints and hints[-1] == 0, f"line {ln}: malformed"
            hints = hints[:-1]
            for x in lits:
                assert 0 < abs(x) <= nv
            assign = {}
            for x in lits:
                assign[abs(x)] = -x  # value literal true: store the true literal
            val = {}
            for x in lits:
                val[-x] = True
                val[x] = False
            conflict = False
            for h in hints:
                if h < 0:
                    raise AssertionError(f"line {ln}: RAT hint not supported")
                if h not in db:
                    raise AssertionError(f"line {ln}: hint {h} missing/deleted")
                unassigned = []
                sat = False
                for y in db[h]:
                    v = val.get(y)
                    if v is True:
                        sat = True
                        break
                    if v is None:
                        unassigned.append(y)
                if sat:
                    raise AssertionError(f"line {ln}: hint {h} satisfied (not unit)")
                if not unassigned:
                    conflict = True
                    break
                if len(unassigned) > 1:
                    raise AssertionError(f"line {ln}: hint {h} not unit")
                y = unassigned[0]
                val[y] = True
                val[-y] = False
            if not conflict:
                raise AssertionError(f"line {ln}: hints do not reach a conflict")
            db[cid] = lits
            last = cid
            if not lits:
                empty = True
                break
    return empty


if __name__ == "__main__":
    try:
        ok = check(sys.argv[1], sys.argv[2])
    except AssertionError as e:
        print("REJECTED:", e)
        sys.exit(1)
    if ok:
        print("VERIFIED UNSAT")
        sys.exit(0)
    print("REJECTED: no empty clause")
    sys.exit(1)
