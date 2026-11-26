"""Independently check the entire exact dyadic cover and 160-bit Arb bounds."""

import argparse
import gzip
from itertools import product
import json
from math import factorial, prod
from pathlib import Path
import subprocess
import sys

from flint import arb, ctx

ctx.prec = 160
MASS = 10_000 * 2**20
MAX_PART = 4_001 * 2**20
MIN_GAP = 1_500 * 2**20
SCALE = 10**12
LIMIT = -10**9
LABELS = ("naive_ab", "case1", "case2")
ROOT = [[0, MAX_PART] for _ in range(5)]
BLUE = tuple((i, j) for i in range(5) for j in range(5) if (j-i) % 5 not in (1, 4))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def clip(bounds, region):
    intervals = [list(pair) for pair in bounds]
    if region == "A":
        inequalities = ((0, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0))
    else:
        inequalities = tuple((i, j, 0) for i in (0, 2) for j in (1, 3, 4)) + ((3, 4, 0),)
        if region == "C":
            inequalities += ((0, 3, MIN_GAP), (2, 3, MIN_GAP))
    for _ in range(3):
        for i, j, difference in inequalities:
            intervals[i][0] = max(intervals[i][0], intervals[j][0] + difference)
            intervals[j][1] = min(intervals[j][1], intervals[i][1] - difference)
        for i, interval in enumerate(intervals):
            other = [item for j, item in enumerate(intervals) if j != i]
            interval[0] = max(interval[0], MASS - sum(item[1] for item in other))
            interval[1] = min(interval[1], MASS - sum(item[0] for item in other))
        if any(low > high for low, high in intervals):
            return None
        if sum(low for low, _ in intervals) > MASS or sum(high for _, high in intervals) < MASS:
            return None
    if region == "B" and min(intervals[0][0], intervals[2][0]) - intervals[3][1] > MIN_GAP:
        return None
    return intervals


def hull(bounds, label):
    if label != "naive_ab":
        return clip(bounds, "C")
    parts = [region for letter in ("A", "B") if (region := clip(bounds, letter)) is not None]
    if parts:
        return [[min(part[i][0] for part in parts), max(part[i][1] for part in parts)] for i in range(5)]
    return None


def profile_vertices(bounds):
    points = set()
    for free in range(5):
        endpoints = [pair if i != free else (0,) for i, pair in enumerate(bounds)]
        for point in product(*endpoints):
            rest = MASS - sum(point)
            if bounds[free][0] <= rest <= bounds[free][1]:
                points.add(point[:free] + (rest,) + point[free+1:])
    return points


def entropy_term(x):
    if x.is_zero():
        return arb(0)
    return x*x.log()


def check_profile(bounds, encoded_tilt, encoded_upper):
    require(isinstance(encoded_upper, int), "noninteger profile bound")
    require(len(encoded_tilt) == 5 and all(type(v) is int and v > 0 for v in encoded_tilt), "invalid tilt")
    tilt = [arb(value)/SCALE for value in encoded_tilt]
    partition = sum(tilt[i]*tilt[j] for i, j in BLUE)
    constant = 5*partition.log()
    max_value = arb(-1000)
    terms = {}
    points = profile_vertices(bounds)
    require(points, "unclassified empty profile slice")
    for point in points:
        rate = constant
        for i, v in enumerate(point):
            key = i, v
            if key not in terms:
                a = arb(v)/MASS
                terms[key] = 9*entropy_term(a) - 10*a*tilt[i].log()
            rate += terms[key]
        require(rate <= arb(encoded_upper)/SCALE, "profile vertex exceeds bound")
        max_value = max_value.max(rate.upper())
    return max_value, tilt, partition


def prove_upper_tail(threshold, probability, rate):
    complement = 1-threshold
    require(threshold > probability, "upper cutoff on wrong side of reference mass")
    divergence = entropy_term(threshold) + entropy_term(complement)
    divergence -= threshold*probability.log() + complement*(1-probability).log()
    require(rate-5*divergence <= arb(LIMIT)/SCALE, "edge-divergence tail does not close")
    return rate-5*divergence


def check_occupancy(label, bound, tilt, part, payload, rate):
    a0 = arb(bound[0][0])/MASS
    require(a0 > 0, "zero lower part-0 bound")
    if label == "case1":
        cap = min(bound[0][1], bound[3][1])
        require(isinstance(payload, list) and len(payload) == 1
                and type(payload[0]) is int and 0 < payload[0] <= cap,
                "invalid Case I upper cutoff")
        high, = payload
        edge = arb(high)/MASS
        x = arb(1) if high >= bound[0][0] else edge/a0
        near = rate + a0*(1-(1-x)**10).log()
        tail = near if high == cap else prove_upper_tail(2*edge, 2*tilt[0]*tilt[3]/part, rate)
    else:
        require(len(payload) == 3 and all(type(x) is int for x in payload), "invalid Case II parameters")
        h02, h24, tangent = payload
        require(0 <= h02 <= MAX_PART and 0 <= h24 < bound[2][0] and 0 < tangent < SCALE,
                "Case II cutoff outside domain")
        tail = arb(-1000)
        for i, j, high in ((0, 2, h02), (2, 4, h24)):
            if high < min(bound[i][1], bound[j][1]):
                result = prove_upper_tail(2*arb(high)/MASS, 2*tilt[i]*tilt[j]/part, rate)
                tail = tail.max(result.upper())
        remaining = bound[2][0]-h24
        p = arb(1) if h02 >= remaining else arb(h02)/remaining
        u = arb(tangent)/SCALE
        f = 1-(1-u)**10
        beta = 10*(1-u)**9/f
        constant = f.log()-beta*u
        require(constant < 0 and beta > 0, "invalid occupancy tangent")
        near = rate + a0*constant + (90*arb(h24)/MASS)*(1+p*((beta/10).exp()-1)).log()

    require(near <= arb(LIMIT)/SCALE, "occupancy upper bound does not close")
    return tail.upper().max(near.upper())


def verify_file(path):
    with gzip.open(path, "rt", encoding="utf-8") as src:
        cert = json.load(src)
    root_lo_hi = [[0]*5, [MAX_PART]*5]
    case = cert["case"]
    require(case in LABELS, "unexpected case")
    expected_format = 2 if case == "case1" else 1
    require(cert["format"] == expected_format and cert["root"] == root_lo_hi and cert["grid"] == MASS
            and cert["tilt_scale"] == SCALE and cert["claim"] == LIMIT, "unexpected root or metadata")
    records = iter(cert["records"])
    counts = dict(split=0, empty=0, naive=0, occupancy=0)
    max_bound = arb(-1000)

    def walk(bounds):
        nonlocal max_bound
        record = next(records, None)
        require(isinstance(record, list) and record, "missing child or malformed node")
        opcode, *values = record
        clipped = hull(bounds, case)
        if opcode == "X":
            require(not values and clipped is None, "unproved empty box")
            counts["empty"] += 1
            return
        require(clipped is not None, "empty box must be marked explicitly")
        if opcode == "S":
            require(len(values) == 2 and all(type(x) is int for x in values), "malformed split")
            axis, cut = values
            widths = [b-a for a, b in clipped]
            require(axis == widths.index(max(widths)) and cut == sum(clipped[axis])//2,
                    "altered split coordinate or boundary")
            low, high = bounds[axis]
            require(low < cut < high, "split outside parent")
            left, right = bounds.copy(), bounds.copy()
            left[axis], right[axis] = [low, cut], [cut, high]
            counts["split"] += 1
            walk(left)
            walk(right)
            return
        require(opcode in ("N", "C"), "unknown leaf")
        require(len(values) == (3 if opcode == "N" else 4), "malformed leaf")
        encoded_tilt, upper, *rest, claim = values
        require(type(claim) is int and claim == LIMIT, "inflated or altered leaf claim")
        maximum, tilt, part = check_profile(clipped, encoded_tilt, upper)
        if opcode == "N":
            require(upper <= LIMIT, "naive claim too weak")
            counts["naive"] += 1
        else:
            require(case != "naive_ab", "occupancy used for naive region")
            maximum = check_occupancy(case, clipped, tilt, part, rest[0], arb(upper)/SCALE)
            counts["occupancy"] += 1
        max_bound = max_bound.max(maximum.upper())

    walk(ROOT)
    end = object()
    require(next(records, end) is end, "trailing children")
    leaves = counts["empty"] + counts["naive"] + counts["occupancy"]
    require(leaves == counts["split"]+1, "invalid binary tree totals")
    print(f"{case} coverage=100% leaves={leaves} uncovered=0 trailing=0 "
          f"upper={max_bound.str(32)} counts={counts}", flush=True)
    return case


def red_witness():
    scale = 10**8
    row_masses = [40_000_000, 13_884, 40_000_000, 18_711_729, 1_274_387]
    off_diagonal = [16_804_449, 12_730, 1_206_998, 10_352_983, 1_134]
    diag = row_masses.copy()
    require(sum(row_masses) == scale and max(row_masses) <= 2*scale//5, "witness is outside its cap")
    for i, size in enumerate(off_diagonal):
        j = (i+2)%5
        diag[i] -= size
        diag[j] -= size
    require(min(diag + off_diagonal) >= 0, "nonfeasible primal witness")
    value = 9*sum(entropy_term(arb(v)/scale) for v in row_masses)
    value -= 5*sum(entropy_term(arb(v)/scale) for v in diag)
    value -= 10*sum(entropy_term(arb(v)/scale) for v in off_diagonal)
    require(value > arb(33)/10_000, "the red primal witness is not positive enough")
    print("bare degree-10 primal witness >", value.lower().str(32), flush=True)


def check_reference_rates(entry):
    """Recompute candidate values from decimal tilts and raw row counts."""
    sizes = [arb(str(x)) for x in entry["profile"]]
    close = arb("1e-9")

    def check_q(found, expected):
        for i, row in enumerate(found):
            require(abs(sum(row)-sizes[i]) < close, "reference row mass error")
            for j, cell in enumerate(row):
                require(abs(cell-found[j][i]) < close, "reference symmetry error")
                require(abs(cell-arb(str(expected[i][j]))) < close, "reference edge count error")

    q = [[arb(str(x)) for x in row] for row in entry["naive_q"]]
    check_q(q, entry["naive_q"])
    for i, row in enumerate(q):
        for j, cell in enumerate(row):
            require(cell >= 0 and ((i,j) in BLUE or cell.is_zero()), "invalid naive edge support")
    primal = 9*sum(map(entropy_term,sizes))-5*sum(entropy_term(x) for row in q for x in row)
    t = [q[i][i].sqrt() for i in range(5)]
    dual = 9*sum(map(entropy_term,sizes)) - 10*sum(a*b.log() for a,b in zip(sizes,t))
    dual += 5*sum(t[i]*t[j] for i,j in BLUE).log()
    require(abs(primal-dual) < close and abs(primal-arb(str(entry["naive"]))) < close,
            "naive reference fails raw primal-dual check")

    for case in (1,2):
        source = entry[f"case_{case}"]
        if source.get("infeasible"):
            require(case == 1 and 10*sizes[3] < sizes[0], "unjustified infeasible reference label")
            continue
        q = [[arb(0) for _ in range(5)] for _ in range(5)]
        row_entropy = arb(0)
        r = []
        for i in range(5):
            dest = [j for j in range(5) if (i,j) in BLUE]
            categories = dest + ([2] if case == 2 and i == 0 else [])
            log_stub = [arb(str(source["log_weights"][i][j])) for j in categories]
            log_hot = arb(str(source["log_hot"][i]))
            total, weighted_log, weighted_hot = arb(0),arb(0),arb(0)
            directed = [arb(0) for _ in range(5)]
            for composition in product(range(11), repeat=len(categories)-1):
                counts = (*composition,10-sum(composition))
                if counts[-1] < 0:
                    continue
                hot = 0
                if i == 0:
                    if case == 1 and (not counts[dest.index(2)] or not counts[dest.index(3)]):
                        continue
                    if case == 2:
                        if not counts[-1]:
                            continue
                        hot = counts[-1]
                if i == 2:
                    if not counts[dest.index(0)]:
                        continue
                    if case == 2 and counts[dest.index(4)]:
                        hot = counts[dest.index(0)]
                tilt = sum(x*y for x,y in zip(counts,log_stub)) + hot*log_hot
                mass = (factorial(10)//prod(factorial(k) for k in counts))*tilt.exp()
                total += mass
                weighted_log += mass*tilt
                weighted_hot += mass*hot
                for j,k in zip(categories,counts):
                    directed[j] += mass*k
            q[i] = [sizes[i]*value/(10*total) for value in directed]
            row_entropy += sizes[i]*(total.log()-weighted_log/total)
            r.append(sizes[i]*weighted_hot/(10*total))
        check_q(q, source["q"])
        rate = 5*sum(entropy_term(x) for row in q for x in row)-sum(map(entropy_term,sizes))+row_entropy
        if case == 2:
            require(abs(r[0]-r[2]) < close and abs(r[0]-arb(str(source["r"]))) < close,
                    "reference hot-stub mismatch")
            rate += 10*(entropy_term(r[0])+entropy_term(q[0][2]-r[0])-entropy_term(q[0][2]))
        require(abs(rate-arb(str(source["rate"]))) < close, "reference rate disagrees with direct row evaluation")


def reference_checks(path):
    """Check that reference labels match raw profiles, and the frozen controls."""
    entries = json.loads(Path(path).read_text())
    for entry in entries.values():
        check_reference_rates(entry)
    original = entries["mirrored_unnormalized"]
    reflected = entries["mirrored_normalized"]
    require([original["profile"][i] for i in (2,1,0,4,3)] == reflected["profile"],
            "reference orientations do not reflect")
    require(original["profile"][3] < original["profile"][4] and
            reflected["profile"][3] > reflected["profile"][4], "reference orientation is mislabeled")
    require(entries["a2_larger"]["profile"][2] > entries["a2_larger"]["profile"][0],
            "asymmetric reference label disagrees with raw profile")
    rate = original["case_2"]["rate"]
    require(abs(rate + .0004) < .0001 and reflected["case_2"]["rate"] < -.02,
            "mirror control outside the recorded tolerance")
    for key, target, cap in (("naive_cap_0.4", .0033635, .4), ("naive_cap_0.4001", .0040314, .4001)):
        row = entries[key]
        a = row["profile"]
        require(abs(sum(a)-1) < 1e-12 and max(a) == cap, "reference profile outside labeled cap")
        require(abs(row["naive"]-target) < 1e-6, "bare reference rate outside tolerance")
    print("reference labels and raw primal-dual values checked", flush=True)
    print(f"Case II mirror: unnormalized={rate:.12f}; normalized={reflected['case_2']['rate']:.12f}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--coverage", action="store_true", help="verify complete coverage (always enabled)")
    parser.add_argument("--finite", action="store_true", help="run the explicit finite-n check after all three certificates")
    parser.add_argument("--red-witness", action="store_true")
    parser.add_argument("--reference", type=Path)
    args = parser.parse_args()
    if args.red_witness:
        red_witness()
    if args.reference:
        reference_checks(args.reference)
    paths = args.files
    if not (paths or args.red_witness or args.reference) or args.finite and not paths:
        paths = [Path(f"cert_{label}.json.gz") for label in LABELS]
    seen = [verify_file(p) for p in paths]
    if args.finite:
        require(sorted(seen) == sorted(LABELS), "finite bound requires all three cases")
        subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("finite.py"))], check=True)


if __name__ == "__main__":
    try:
        main()
    except (ArithmeticError, KeyError, OSError, TypeError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"verification failed: {error}")
