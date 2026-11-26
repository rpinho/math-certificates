"""Independent proof check for the bidegree upper bound in Erdős problem 1182."""
import gzip
import hashlib
import json
import os
import resource
import signal
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import product

from flint import arb, ctx

ctx.prec = 192
ctx.threads = 1
N0 = 450000
GRID = 10485760000
SCALE = 10**12
CAP = GRID * 4001 // 10000
GAP = GRID * 3 // 20
TARGET = F(-3, 2000)
ALOW = F(1, 10)
AHIGH = ALOW + F(19, 10 * N0)
DMIN, DMAX = 10 - AHIGH, 10 - ALOW
CASES = ("naive_ab", "case1", "case2")
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs", "certificates")
BLUE = [(i, j) for i in range(5) for j in range(i + 1, 5) if (j - i) in (2, 3)]


class Failure(ValueError):
    pass


def check(condition, message):
    if not condition:
        raise Failure(message)


def real(q):
    return arb(q.numerator) / q.denominator


def maximum(values):
    # Comparing rounded balls directly can discard an overlapping upper endpoint.
    endpoints = []
    for v in values:
        check(v.is_finite(), "nonfinite rate candidate")
        endpoints.append(v.upper())
    return max(endpoints)


def integer(v):
    return type(v) is int


def bad_number(token):
    raise Failure(f"noninteger JSON token {token}")


def validate_header(d, case):
    spec = dict(format=3, model="bidegree_9_10", c_num=99, c_den=20, n0=N0,
                case=case, root=[[0] * 5, [CAP] * 5], grid=GRID, tilt_scale=SCALE,
                claim=int(TARGET * SCALE))
    for key, expected in spec.items():
        check(type(d[key]) is type(expected) and d[key] == expected, f"header {key}")


def load_certificates():
    with open(os.path.join(FOLDER, "SHA256SUMS"), encoding="ascii") as f:
        manifest = [line.split() for line in f if line.strip()]
    filenames = ["cert_" + c + ".json.gz" for c in CASES]
    check(len(manifest) == 3 and {p for _, p in manifest} ==
          {"certificates/" + name for name in filenames}, "manifest membership")
    hashes = {p: h for h, p in manifest}
    docs = {}
    for case, name in zip(CASES, filenames):
        with open(os.path.join(FOLDER, name), "rb") as f:
            raw = f.read()
        digest = hashlib.sha256(raw).hexdigest()
        check(digest == hashes["certificates/" + name], f"SHA-256 {name}")
        print(f"{case} sha256 {digest}")
        doc = json.loads(gzip.decompress(raw), parse_float=bad_number, parse_constant=bad_number)
        validate_header(doc, case)
        docs[case] = doc
    return docs


def walk(records):
    stack = [((0,) * 5, (CAP,) * 5)]
    for index, rec in enumerate(records):
        check(bool(stack), "trailing tree record")
        lo, hi = stack.pop()
        if rec[0] != "S":
            yield index, rec, lo, hi
            continue
        check(len(rec) == 3, "split shape")
        _, axis, cut = rec
        check(integer(axis) and 0 <= axis < 5 and integer(cut)
              and lo[axis] < cut < hi[axis], "split outside parent")
        lower_hi, upper_lo = list(hi), list(lo)
        lower_hi[axis] = upper_lo[axis] = cut
        stack.extend([(tuple(upper_lo), hi), (lo, tuple(lower_hi))])
    check(not stack, "missing tree record")


# Each triple means a[i] >= a[j] + gap, in units of 1/GRID.
A = [(0, 1, 0)] + [(1, j, 0) for j in (2, 3, 4)]
TOP = [(i, j, 0) for i in (0, 2) for j in (1, 3, 4)] + [(3, 4, 0)]
B0, B2 = (TOP + [(3, i, -GAP)] for i in (0, 2))
C = TOP + [(0, 3, GAP), (2, 3, GAP)]


def contract(lo, hi, inequalities):
    l, h = list(lo), list(hi)
    while True:
        old = (tuple(l), tuple(h))
        for i, j, gap in inequalities:
            l[i] = max(l[i], l[j] + gap)
            h[j] = min(h[j], h[i] - gap)
        low_sum, high_sum = sum(l), sum(h)
        if low_sum > GRID or high_sum < GRID or any(x > y for x, y in zip(l, h)):
            return None
        for i in range(5):
            l[i] = max(l[i], GRID - high_sum + h[i])
        # Use the updated lower endpoints for the complementary upper bounds.
        low_sum = sum(l)
        for i in range(5):
            h[i] = min(h[i], GRID - low_sum + l[i])
        if old == (tuple(l), tuple(h)):
            return old


def vertices(lo, hi):
    points = set()
    for free in range(5):
        others = [i for i in range(5) if i != free]
        for ends in product(*[(lo[i], hi[i]) for i in others]):
            rest = GRID - sum(ends)
            if lo[free] <= rest <= hi[free]:
                points.add(ends[:free] + (rest,) + ends[free:])
    return sorted(points)


def tangent(u):
    check(0 < u < 1, "tangent outside (0,1)")
    p = real(u)
    q = 1 - p
    hit = 1 - q**10
    slope = 10 * q**9 / hit
    return slope, hit.log() - slope * p


def rho(a):
    return real(F(1, 9) if a <= AHIGH else a / (10 * a - AHIGH))


def dual(points, weights, eta, s03, s02, linear):
    t = [real(F(i, SCALE)) for i in weights]
    z = sum(x*x for x in t)
    for i, j in BLUE:
        s = {(0, 3): s03, (0, 2): s02}.get((i, j), 1)
        z += 2 * t[i] * t[j] * s
    alpha = real(ALOW).union(real(AHIGH))
    degree = 10 - alpha
    base = alpha * alpha.log() + (1-alpha)*(1-alpha).log() + degree*z.log()/2 - eta*alpha
    columns = []
    for i, ti in enumerate(t):
        dt = degree*ti
        kfactor = dt * (eta-1).exp()
        column = {}
        for coordinate in {v[i] for v in points}:
            if coordinate == 0:
                column[0] = arb(0)
                continue
            a = real(F(coordinate, GRID))
            k = kfactor / a
            radical = ((8+k)**2 + 36).sqrt()
            y = 18 / (8+k+radical)
            xi = 2*k / (10+k+radical)
            column[coordinate] = a * (9*a.log() + 10*((9+y)/dt).log()
                                      - y.log() + xi + linear[i])
        columns.append(column)
    return base + maximum(sum(col[x] for col, x in zip(columns, v)) for v in points)


def divergence(x, b):
    def term(p, q):
        return real(p)*(real(p/q)).log() if p else arb(0)
    return term(x, b) + term(1-x, 1-b)


def kl_distance(left, right, mass):
    nearest = min(max(mass, left), right)
    return divergence(2*nearest, 2*mass) if nearest != mass else arb(0)


def hot(d, p, q, w):
    extra = (w-1)*p
    return (1+extra)**d - (1-q+extra)**d + (1-q)**d - (1-p)**d


def case_two(base, weights, pars, low, high, tally):
    cut0, cut4, ref = pars
    u = F(ref, SCALE)
    slope, intercept = tangent(u)
    w = (slope*rho(low[0])).exp()
    z = sum(t*t for t in weights) + 2*sum(weights[i]*weights[j] for i, j in BLUE)
    min_row = max(9*low[2], 10*low[2]-AHIGH)
    max_row = [min(10*a, 9*a+1-ALOW) for a in high]
    bounds, axes = [], []
    for j, raw in ((0, cut0), (4, cut4)):
        cut = F(raw, GRID)
        check(0 < cut < F(1, 2), "binary cutoff domain")
        b = F(weights[2]*weights[j], z)
        if cut < min(max_row[2], max_row[j])/DMIN:
            check(cut > b, "tail cutoff below reference")
            bounds.append(base - real(DMIN/2)*divergence(2*cut, 2*b))
            tally[f"KL tail 2-{j}"] += 1
        else:
            tally[f"empty tail 2-{j}"] += 1
        cells = []
        for k in range(8):
            left, right = k*cut/8, (k+1)*cut/8
            cells.append((real(min(1, DMAX*right/min_row)), kl_distance(left, right, b)))
        axes.append(cells)
    offset = base + real(low[0])*intercept
    for p, dp in axes[0]:
        for q, dq in axes[1]:
            m = hot(10, p, q, w)
            check(m > 0, "hot polynomial log domain")
            tally["KL cells"] += 1
            logm = m.log()
            # Arb endpoints only; both products are valid candidates.
            gain = maximum([real(low[2])*logm, real(high[2])*logm])
            bounds.append(offset + gain - real(DMIN/2)*dp.max(dq))
    return maximum(bounds)


def evaluate(rec, case, lo, hi, tally):
    tag = rec[0]
    boxes = [b for r in ((A, B0, B2) if case == "naive_ab" else (C,))
             if (b := contract(lo, hi, r)) is not None]
    if tag == "X":
        check(len(rec) == 1 and not boxes, "feasible box labelled empty")
        return None
    check(tag == "N" or (case, tag) in (("case1", "C1"), ("case2", "C2")), "leaf type")
    check(len(rec) == (6 if tag == "C2" else 5), "leaf arity")
    check(integer(rec[-1]) and rec[-1] == TARGET*SCALE, "leaf pass line")
    weights, eta_code = rec[1:3]
    check(len(weights) == 5 and all(integer(v) and v > 0 for v in weights), "tilt domain")
    check(integer(eta_code), "multiplier")
    eta = real(F(eta_code, SCALE))
    if tag != "N":
        params = rec[-2]
        check(len(params) == 3 and all(map(integer, params)), "occupancy parameter shape")
    values = []
    for l, h in boxes:
        points = vertices(l, h)
        check(bool(points), "empty sliced box")
        low, high = [[F(x, GRID) for x in side] for side in (l, h)]
        linear = [arb(0)]*5
        s03 = s02 = arb(1)
        if tag == "C1":
            (b1, g1), (b2, g2), (b3, g3) = [tangent(F(u, SCALE)) for u in params]
            s03 = (rho(low[0])*b1).exp()
            s02 = (rho(low[0])*b2 + rho(low[2])*b3).exp()
            linear[0], linear[2] = g1+g2, g3
        tally["slice vertices"] += len(points)
        value = dual(points, weights, eta, s03, s02, linear)
        if tag == "C2":
            value = case_two(value, weights, params, low, high, tally)
        values.append(value)
    return maximum(values) if values else None


def verify_one(rec, case, lo, hi, tally=None):
    value = evaluate(rec, case, lo, hi, Counter() if tally is None else tally)
    check(value is None or (value.is_finite() and value < real(TARGET)),
          f"rate misses cutoff {value}")
    return value


def finite_bound(n):
    poly = 30 * 3**9 * (n+1)**8 * (10*n+1)**11 * (200*n)**19
    logb = arb(poly).log() + real(TARGET*n)
    b = arb(poly) * real(TARGET*n).exp()
    ratio = arb(1).exp() * (real(F(50, 49))**9 / 2**7).sqrt()
    disconnected = ratio / (1-ratio)
    total = b + disconnected
    derivative = real(F(38, n) + TARGET)
    check(ratio < 1 and total < real(F(3574, 10000)), "finite probability exceeds budget")
    check(logb < -41 and b < real(F(2, 10**18)) and derivative < 0, "finite threshold")
    return dict(logB=logb, B=b, rho=ratio, disconnected=disconnected,
                total=total, derivative_upper=derivative)


def degree_checks():
    def counts(n):
        n9 = 2*((n+19)//20)
        n10 = n-n9
        stubs = 9*n9+10*n10
        return n9, n10, stubs
    for r in range(40):
        n = N0+r
        a, b, stubs = counts(n)
        check((a % 2, stubs % 2) == (0, 0) and min(a, b) >= 0, "degree parity")
        check(stubs//2 == 99*n//20 and 0 <= 10*a-n <= 19, "edge count or alpha")
        check(counts(n+40) == (a+4, b+36, stubs+396), "residue increment")
        check((99*(n+40))//20 == stubs//2 + 198, "floor increment")
    check(F(2, 5)+F(3, 5*N0) < F(CAP, GRID) and F(3*N0, 20) > 38
          and DMIN > F(49, 5), "global side conditions")


def factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result


def pairing_check():
    colors = (0, 0, 1, 2, 2, 2, 3, 4)
    pairs = [(i, j) for i in range(5) for j in range(i, 5)]
    observed = Counter()

    def enumerate_pairs(stubs, edges):
        if not stubs:
            observed[tuple(edges.count(p) for p in pairs)] += 1
            return
        for k in range(1, len(stubs)):
            edge = tuple(sorted((colors[stubs[0]], colors[stubs[k]])))
            enumerate_pairs(stubs[1:k]+stubs[k+1:], edges+[edge])
    enumerate_pairs(tuple(range(len(colors))), [])
    den = factorial(8)//(2**4 * factorial(4))
    check(sum(observed.values()) == den == 105, "perfect matching enumeration")
    row_product = 1
    for i in range(5):
        row_product *= factorial(colors.count(i))
    for profile, count in observed.items():
        divisor = 1
        for (i, j), multiplicity in zip(pairs, profile):
            divisor *= factorial(multiplicity)
            if i == j:
                divisor *= 2**multiplicity
        check(F(row_product, divisor*den) == F(count, 105), "pairing law")
    return len(observed)


def blue(i, j):
    return (i-j) % 5 in (0, 2, 3)


def simplification_check():
    from itertools import permutations
    edges = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 3), (3, 3)]
    simple = {(min(i, j), max(i, j)) for i, j in edges if i != j}
    host = (0, 0, 1, 1, 2, 3, 4)
    maps = {p for p in product(range(5), repeat=4)
            if all(p.count(i) <= host.count(i) for i in range(5))
            and all(blue(p[i], p[j]) for i, j in edges)}
    lifted = {tuple(host[i] for i in placement) for placement in permutations(range(7), 4)
              if all(blue(host[placement[i]], host[placement[j]]) for i, j in simple)}
    check(maps == lifted and len(maps) > 0, "loop/parallel map equivalence")
    return len(maps)


def swap_check():
    # Five stationary roles, pivot, promoted neighbour, donor.
    old, new = (0, 1, 2, 3, 4, 0, 2, 0), (0, 1, 2, 3, 4, 3, 0, 2)
    forbidden = {(2, 5), (5, 7), (4, 6), (3, 7)}
    count = 0
    for i in range(8):
        for j in range(i, 8):
            if blue(old[i], old[j]) and (i, j) not in forbidden:
                check(blue(new[i], new[j]), "swap creates red edge")
                count += 1
    for d in (9, 10):
        for r in range(1, d+1):
            check(20-1-(d-r) >= r-1, "donor shortage")
    return count


def cutoff_test(reversed_sign=False):
    # A row on 38 vertices: assign one destination-3 stub to each hit vertex
    # and one destination-2 stub to every vertex. Leftover stubs may stay local.
    for hits in (18, 19, 20, 38):
        viable = hits <= 38-19 if reversed_sign else hits >= 38-19
        check(viable == (38-hits <= 19), "Case I cutoff direction")


def hot_check():
    count = 0
    for d in (9, 10):
        for p, q in [(F(1, 3), F(1, 4)), (F(2, 5), F(3, 5)),
                     (F(0), F(1)), (F(1, 2), F(0))]:
            for w in (F(1), F(3, 2)):
                exact = F(0)
                for n0 in range(1, d+1):
                    for n4 in range(d-n0+1):
                        rest = d-n0-n4
                        ways = factorial(d)//(factorial(n0)*factorial(n4)*factorial(rest))
                        exact += ways * p**n0 * q**n4 * (1-p-q)**rest * (w**n0 if n4 else 1)
                check(exact == hot(d, p, q, w), "hot-stub polynomial")
                if d == 9:
                    check(exact <= hot(10, p, q, w), "degree coupling")
                count += 1
    return count


WITNESS_A = tuple(F(x, 10**8) for x in (40000000, 13884, 40000000, 18711729, 1274387))


def positive_witness():
    # Independently selected rational edge masses. The diagonal fixes row sums.
    a = WITNESS_A
    weights = (168044485492, 103529834892, 127303331, 11342490, 12069980801)
    matrix = [[F(0)]*5 for _ in a]
    for (i, j), v in zip(BLUE, weights):
        matrix[i][j] = matrix[j][i] = F(v, 10**12)
    for i in range(5):
        matrix[i][i] = a[i]-sum(matrix[i])
    check(sum(a) == 1 and max(a) == F(2, 5), "witness simplex")
    check(min(a[0], a[2])-max(a[3], a[4]) >= F(3, 20),
          "witness gap")
    for i, row in enumerate(matrix):
        check(min(row) >= 0 and sum(row) == a[i], "witness row")
        check(all(x == matrix[j][i] and (blue(i, j) or x == 0)
                  for j, x in enumerate(row)), "witness colors")
    def entropy_term(x):
        return real(x)*real(x).log() if x else arb(0)
    rows = sum(map(entropy_term, a))
    pairs = sum(entropy_term(x) for row in matrix for x in row)
    rates = [(real(d)-1)*rows-real(d/2)*pairs for d in (F(10), DMAX)]
    check(rates[0] > real(F(33635, 10**7)) and rates[1] > real(F(14, 1000)),
          "bare positive witness")
    return rates


def corruptions(docs, examples):
    count = 0
    def reject(label, reason, action):
        nonlocal count
        try:
            action()
        except Failure as err:
            check(reason in str(err), f"unexpected failure for {label}: {err}")
        else:
            raise Failure(f"accepted corruption: {label}")
        print(f"rejected {label}")
        count += 1

    doc = docs["case1"]
    for key, val in (("n0", N0-1), ("root", [[1]*5, [CAP]*5]), ("c_num", 100)):
        reject(f"changed {key}", f"header {key}", lambda: validate_header({**doc, key: val}, "case1"))
    records = doc["records"]
    reject("dropped last leaf", "missing tree", lambda: list(walk(records[:-1])))
    reject("appended duplicate leaf", "trailing tree", lambda: list(walk(records+[records[-1]])))
    reject("split at parent boundary", "split outside", lambda: list(walk([["S", 0, CAP]]+records[1:])))
    def corrupt_leaf(case, make, reason, name):
        _, rec, lo, hi = examples[case]
        reject(name, reason, lambda: verify_one(make(rec), case, lo, hi))
    corrupt_leaf("case1", lambda r: r[:-1]+[0], "leaf pass line", "raised leaf rate claim")
    corrupt_leaf("case1", lambda r: ["X"], "feasible box", "nonempty box relabelled empty")
    corrupt_leaf("case1", lambda r: ["N", r[1], r[2], 0, r[-1]], "rate misses",
                 "removed Case I occupancy at positive witness")
    corrupt_leaf("case1", lambda r: r[:3]+[[SCALE//2]*3, r[-1]], "rate misses",
                 "three interior Case I tangents changed")
    corrupt_leaf("case2", lambda r: r[:4]+[[1, *r[4][1:]], r[-1]], "tail cutoff below",
                 "Case II tail starts below its reference mass")
    corrupt_leaf("case2", lambda r: r[:4]+[[*r[4][:2], SCALE//100], r[-1]], "rate misses",
                 "interior Case II tangent changed")
    reject("reversed Case I cutoff", "cutoff direction", lambda: cutoff_test(True))
    reject("finite sum started at 400000", "finite probability", lambda: finite_bound(400000))
    return count


def peak_rss():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rss if sys.platform == "darwin" else rss*1024


def main():
    signal.alarm(600)
    docs = load_certificates()
    degree_checks()
    cutoff_test()
    print(f"40 residues; {pairing_check()} matching profiles in 105 pairings;"
          f" {simplification_check()} maps lift; {swap_check()} permitted swap role pairs;"
          f" {hot_check()} exact hot moments")
    print("unrestricted rates", *(v.str(22) for v in positive_witness()))
    for name, value in finite_bound(N0).items():
        print(name, value.str(28))
    examples, total = {}, 0
    for case, expected in zip(CASES, (1093, 2596, 7322)):
        tally, kinds = Counter(), Counter()
        worst, worst_index = None, None
        for index, rec, lo, hi in walk(docs[case]["records"]):
            if index % 128 == 0:
                check(peak_rss() < 1800000000, "RSS budget")
            try:
                rate = verify_one(rec, case, lo, hi, tally)
            except Failure as err:
                raise Failure(f"{case} record {index}: {err}") from err
            kinds[rec[0]] += 1
            if rate is not None:
                point = rate.upper()
                if worst is None or point > worst:
                    worst, worst_index = point, index
            if case != "naive_ab" and all(l <= a*GRID <= h for a, l, h in zip(WITNESS_A, lo, hi)):
                check(rec[0] in ("C1", "C2"), "bare-positive witness lacks occupancy")
                examples[case] = (index, rec, lo, hi)
        check(sum(kinds.values()) == expected, f"{case} leaf count")
        total += expected
        print(f"{case} leaves {dict(kinds)}, max upper {worst.str(30)},"
              f" record {worst_index}, {dict(tally)}", flush=True)
    check(total == 11011, "total leaves")
    controls = corruptions(docs, examples)
    peak_bytes = peak_rss()
    check(peak_bytes <= 2000000000, "peak RSS limit")
    print(f"VERDICT: HOLDS; {total} leaves; {controls} rejected mutations; peak RSS {peak_bytes} bytes")
    signal.alarm(0)


if __name__ == "__main__":
    main()
