"""Referee's own outward-rounded verifier for the three Erdos #1182 certificate trees.

Written from the referee's derivation (REFEREE.md section c), not from producer code.
Certificate files are read as data only: split coordinates/points, per-leaf tilts and cutoffs.
Every bound is recomputed here in Arb ball arithmetic; the producer's stored values are only compared.

Usage: python -I arbverify.py CERT.json [--corrupt MODE] [--json OUT]
"""
import sys, json, argparse
from fractions import Fraction
from flint import arb, ctx

ctx.prec = 160
D_DEG = 10
BLUE = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0, 2), (0, 3), (1, 3), (1, 4), (2, 4)]
# blue (A_ij = 1) iff (j - i) mod 5 in {0, 2, 3}
for i, j in BLUE:
    assert (j - i) % 5 in (0, 2, 3)
assert len({frozenset(p) for p in BLUE}) == 10

class Reject(Exception):
    pass


def tighten(lo, hi, G, cons):
    """cons: list of (i, j, c) meaning a_i >= a_j + c (integers on grid). Sound interval propagation."""
    lo = list(lo); hi = list(hi)
    for _ in range(200):
        old = (tuple(lo), tuple(hi))
        for i, j, c in cons:
            lo[i] = max(lo[i], lo[j] + c)
            hi[j] = min(hi[j], hi[i] - c)
        sl, sh = sum(lo), sum(hi)
        for i in range(5):
            lo[i] = max(lo[i], G - (sh - hi[i]))
            hi[i] = min(hi[i], G - (sl - lo[i]))
        if any(lo[i] > hi[i] for i in range(5)):
            return None
        if (tuple(lo), tuple(hi)) == old:
            break
    return lo, hi


def vertices(lo, hi, G):
    """All points of box ∩ {sum = G} with >= 4 coordinates at an endpoint (superset of the vertex set)."""
    out = set()
    for free in range(5):
        others = [k for k in range(5) if k != free]
        for mask in range(16):
            p = [0] * 5
            s = 0
            for b, k in enumerate(others):
                p[k] = hi[k] if (mask >> b) & 1 else lo[k]
                s += p[k]
            p[free] = G - s
            if lo[free] <= p[free] <= hi[free]:
                out.add(tuple(p))
    return sorted(out)


def xlogx(x):
    if x == 0:
        return arb(0)
    return x * x.log()


class Ctx:
    def __init__(self, G, tscale):
        self.G = G
        self.Garb = arb(G)
        self.tscale = arb(tscale)

    def a(self, k):
        return arb(k) / self.Garb

    def tilt(self, T):
        if any(x <= 0 for x in T):
            raise Reject("nonpositive tilt")
        t = [arb(x) / self.tscale for x in T]
        Z = arb(0)
        for i, j in BLUE:
            Z += t[i] * t[j] * (1 if i == j else 2)
        B = {}
        for i, j in BLUE:
            if i != j:
                B[(i, j)] = t[i] * t[j] / Z  # one ordered entry; unordered cell mass is 2B
        return t, Z, B

    def U(self, p, t, Z):
        # U_t(a) = 9 sum a log a - 10 sum a log t + 5 log Z
        s = arb(0)
        for i in range(5):
            ai = self.a(p[i])
            s += 9 * xlogx(ai)
            if p[i]:
                s -= 10 * ai * t[i].log()
        return s + 5 * Z.log()


def binKL(x, b):
    # D(x||b) = x log(x/b) + (1-x) log((1-x)/(1-b)), 0<b<1, 0<=x<=1
    return xlogx(x) - x * b.log() + xlogx(1 - x) - (1 - x) * (1 - b).log()


def f_occ(x):
    return 1 - (1 - x) ** D_DEG


def region_parts(case, lo, hi, G, delta):
    """Return list of tightened (lo,hi) boxes whose union contains (region ∩ box)."""
    if case == "naive_ab":
        A = [(0, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)]
        Bord = [(0, 1, 0), (0, 3, 0), (0, 4, 0), (2, 1, 0), (2, 3, 0), (2, 4, 0), (3, 4, 0)]
        # B: min(a0,a2) - a3 <= delta, i.e. B0: a3 + delta >= a0  or  B2: a3 + delta >= a2
        parts = [A, Bord + [(3, 0, -delta)], Bord + [(3, 2, -delta)]]
    else:
        C = [(0, 1, 0), (0, 4, 0), (2, 1, 0), (2, 4, 0), (3, 4, 0), (0, 3, delta), (2, 3, delta)]
        parts = [C]
    out = []
    for cons in parts:
        r = tighten(lo, hi, G, cons)
        if r is not None and vertices(r[0], r[1], G):
            out.append(r)
    return out


def check_leaf(rec, boxes, cx, case, claim):
    kind = rec[0]
    T = rec[1]
    t, Z, B = cx.tilt(T)
    G = cx.G
    allv = []
    for lo, hi in boxes:
        allv += vertices(lo, hi, G)
    Uup = None
    for p in allv:
        uu = up(cx.U(p, t, Z))
        Uup = uu if Uup is None else _amax(Uup, uu)
    info = {"U": float(Uup)}
    if kind == "N":
        bound = Uup
    elif kind == "C" and case == "case1":
        q = Fraction(rec[3][0], G)
        qa = arb(rec[3][0]) / cx.Garb
        a0min = min(p[0] for p in allv)
        a0max = max(p[0] for p in allv)
        a3max = max(p[3] for p in allv)
        if a0min <= 0:
            raise Reject("a0min <= 0")
        x = min(Fraction(1), q / Fraction(a0min, G))
        near = Uup + cx.a(a0min) * f_occ(arb(x.numerator) / x.denominator).log()
        bound = near
        info["near"] = float(near.upper())
        if rec[3][0] < min(a0max, a3max):  # far cell Q03 > q nonempty
            b = 2 * B[(0, 3)]
            if not (2 * qa > b):
                raise Reject("case1 cutoff not above 2*B03 (tail on wrong side)")
            far = Uup - 5 * binKL(2 * qa, b)
            info["far03"] = float(far.upper())
            bound = _amax(near, far)
        info["q_minus_B03"] = float((qa - B[(0, 3)]).mid())
    elif kind == "C" and case == "case2":
        h02i, h24i, ui = rec[3]
        h02 = arb(h02i) / cx.Garb
        h24 = arb(h24i) / cx.Garb
        u = arb(ui) / cx.tscale
        if not (0 < ui < 10**12):
            raise Reject("u not in (0,1)")
        a0min = min(p[0] for p in allv)
        a2min = min(p[2] for p in allv)
        if not h24i < a2min:
            raise Reject("h24 >= a2min")
        fu = f_occ(u)
        beta = D_DEG * (1 - u) ** (D_DEG - 1) / fu
        gamma = fu.log() - beta * u
        if not gamma < 0:
            raise Reject("gamma not certified negative")
        pmax = min(Fraction(1), Fraction(h02i, a2min - h24i))
        pm = arb(pmax.numerator) / pmax.denominator
        near = Uup + cx.a(a0min) * gamma + 90 * h24 * (1 + pm * ((beta / D_DEG).exp() - 1)).log()
        info["near"] = float(near.upper())
        bound = near
        # far cells
        # sound upper bounds on Q02 <= min(a0,a2) and Q24 <= min(a2,a4) over the polytope
        mx02 = min(max(p[0] for p in allv), max(p[2] for p in allv))
        mx24 = min(max(p[2] for p in allv), max(p[4] for p in allv))
        if h02i < mx02:
            b = 2 * B[(0, 2)]
            if not (2 * h02 > b):
                raise Reject("case2 h02 not above 2*B02")
            far = Uup - 5 * binKL(2 * h02, b)
            info["far02"] = float(far.upper())
            bound = _amax(bound, far)
        if h24i < mx24:
            b = 2 * B[(2, 4)]
            if not (2 * h24 > b):
                raise Reject("case2 h24 not above 2*B24")
            far = Uup - 5 * binKL(2 * h24, b)
            info["far24"] = float(far.upper())
            bound = _amax(bound, far)
    else:
        raise Reject("unknown leaf kind %r for case %s" % (kind, case))
    bu = up(bound)
    # certification: exact upper endpoint of the ball <= claim (claim = -1/1000 as a ball; require below its lower end)
    if not (bu <= arb(claim.lower())):
        raise Reject("leaf bound %.15g > claim; lo=%s hi=%s rec=%s" % (float(bu), lo_hi_ctx[0], lo_hi_ctx[1], rec))
    info["bound"] = float(bu)
    return info


def up(x):
    return arb(x.upper())


def _amax(x, y):
    xu = up(x); yu = up(y)
    return xu if xu >= yu else yu


lo_hi_ctx = [None, None]


def run(cert, corrupt=None):
    G = cert["grid"]
    cx = Ctx(G, cert["tilt_scale"])
    claim = arb(cert["claim"]) / cx.tscale
    assert cert["claim"] == -10**9 and cert["tilt_scale"] == 10**12  # claim = -1/1000 exactly
    case = cert["case"]
    # exact root: [0, 4001/10000] in every coordinate
    assert Fraction(cert["root"][1][0], G) == Fraction(4001, 10000), cert["root"]
    assert cert["root"][0] == [0] * 5 and len(set(cert["root"][1])) == 1
    delta = Fraction(3, 20) * G
    assert delta.denominator == 1
    delta = int(delta)
    recs = cert["records"]
    if corrupt:
        recs = corrupt(recs)
    pos = [0]
    stats = {"leaves": 0, "N": 0, "C": 0, "X": 0, "split": 0, "maxbound": None, "maxN_stored": None,
             "max_abs_U_vs_stored": 0.0, "worst": None}

    def rec_fn(lo, hi, depth):
        if pos[0] >= len(recs):
            raise Reject("missing record (tree truncated)")
        r = recs[pos[0]]; pos[0] += 1
        if r[0] == "S":
            _, i, m = r
            if not (lo[i] < m < hi[i]):
                raise Reject("split point not interior")
            stats["split"] += 1
            h1 = list(hi); h1[i] = m
            l2 = list(lo); l2[i] = m
            rec_fn(lo, h1, depth + 1)
            rec_fn(l2, hi, depth + 1)
            return
        stats["leaves"] += 1
        boxes = region_parts(case, lo, hi, G, delta)
        if r[0] == "X":
            if boxes:
                raise Reject("X leaf but region∩box nonempty under referee tightening: %s %s" % (lo, hi))
            stats["X"] += 1
            return
        if not boxes:
            stats["empty_by_referee"] = stats.get("empty_by_referee", 0) + 1
            stats[r[0]] += 1
            return
        lo_hi_ctx[0], lo_hi_ctx[1] = lo, hi
        info = check_leaf(r, boxes, cx, case, claim)
        stats[r[0]] += 1
        if stats["maxbound"] is None or info["bound"] > stats["maxbound"]:
            stats["maxbound"] = info["bound"]; stats["worst"] = {"lo": lo, "hi": hi, "rec": r, **info}
        if r[0] == "N":
            st = r[2] / 1e12
            stats["max_abs_U_vs_stored"] = max(stats["max_abs_U_vs_stored"], abs(info["U"] - st))
            if stats["maxN_stored"] is None or st > stats["maxN_stored"]:
                stats["maxN_stored"] = st
        else:
            stats.setdefault("C_U_vs_stored", 0.0)
            stats["C_U_vs_stored"] = max(stats["C_U_vs_stored"], abs(info["U"] - r[2] / 1e12))

    rec_fn(list(cert["root"][0]), list(cert["root"][1]), 0)
    if pos[0] != len(recs):
        raise Reject("trailing records: %d unused" % (len(recs) - pos[0]))
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--json")
    a = ap.parse_args()
    cert = json.load(open(a.cert))
    try:
        st = run(cert)
        st["verdict"] = "ACCEPT"
    except Reject as e:
        st = {"verdict": "REJECT", "reason": str(e)}
    print(json.dumps(st, indent=1, default=str))
    if a.json:
        json.dump(st, open(a.json, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
