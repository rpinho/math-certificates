"""Deterministic exact and randomized controls for the pairing proof."""

from collections import Counter
from fractions import Fraction
import gzip
from itertools import combinations, product
import json
from math import comb, factorial, floor, prod
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory

from flint import arb
import numpy as np

from finite import CAP, GAP, N0
from reference_table import naive
import verify

BLUE = {(i,j) for i in range(5) for j in range(5) if (j-i) % 5 in (0,2,3)}
EDGES = [(i,(i+2)%5) for i in range(5)]
EDGE_03 = (3,0)
INDEX_03 = EDGES.index(EDGE_03)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def region(v):
    if v[0] >= v[1] >= max(v[2:]):
        return "A"
    if min(v[0],v[2]) < max(v[1],v[3],v[4]) or v[3] < v[4]:
        return None
    if min(v[0],v[2])-v[3] <= GAP*sum(v):
        return "B"
    return "C"


def coverage(rng):
    counts = Counter()
    parities = Counter()
    for trial in range(15_000):
        n = N0+trial if trial < 1000 else rng.randrange(N0,20*N0)
        h,s = divmod(2*n-1,5)
        large = set(rng.sample(range(5),s))
        capacities = [h+(i in large) for i in range(5)]
        kind = trial%3
        while True:
            if kind == 0:
                v = [rng.randrange(cap+1) for cap in capacities[:4]]
            elif kind == 1:
                v = [capacities[0]-rng.randrange(n//35), rng.randrange(n//100),
                     capacities[2]-rng.randrange(n//35), rng.randrange(n//5)]
            else:
                v = [rng.randrange(n//5,n//3) for _ in capacities[:4]]
            v.append(n-sum(v))
            if 0 <= v[-1] <= capacities[-1]:
                break
        require(sum(v)==n and all(0 <= x <= y for x,y in zip(v,capacities)), "bad raw profile")
        require(max(v) <= CAP*n, "integer cap failure")
        found = set()
        for shift,sign in product(range(5),(-1,1)):
            image = [v[(shift+sign*i)%5] for i in range(5)]
            current = region(image)
            if current is None:
                continue
            if current == "C" or current == "B" and min(image[0],image[2])-image[3] == GAP*n:
                require(min(image[0],image[2]) >= image[3]+2 and image[2] >= image[4]+2,
                        "integer gap failure on a C image")
                require(image[3]+1 <= h and image[0]>=2*19, "capacity or exemption failure")
            found.add(current)
        require(found, ("uncovered profile", v))
        for label in found:
            counts[label] += 1
        parities[n%2] += 1
    require(set(counts)=={"A","B","C"} and len(parities)==2, "coverage test lacks one region or parity")
    print("1 coverage: 15000 integer profiles; n parity", dict(parities), "regions", dict(counts),
          "; zero uncovered or integer-gap failures", flush=True)


def polynomial(d, rule):
    result = Counter()
    for x in range(d+1):
        for y in range(d+1-x):
            z = d-x-y
            key = rule(x,y,z)
            if key is not None:
                result[key] += factorial(d)//(factorial(x)*factorial(y)*factorial(z))
    return result


def convolve(left,right):
    out = Counter()
    for x, nx in left.items():
        for y, ny in right.items():
            out[tuple(i+j for i,j in zip(x,y))] += nx*ny
    return out


def exact_case2(d, v0, v2):
    stubs0, stubs2 = d*v0, d*v2
    conditions = Counter()
    actual = Counter()
    direct_n0 = Counter()
    hot_histogram = Counter()
    compare = positives = 0
    mgf_checks = 0
    # First enumerate actual hot subsets of the complete row-0 stub pool.
    row0 = {}
    for r in range(stubs0+1):
        good = sum(len({slot//d for slot in selection}) == v0
                   for selection in combinations(range(stubs0),r))
        row0[r] = Fraction(good,comb(stubs0,r))
    for labels in product("sob",repeat=stubs2):
        x,y = labels.count("o"),labels.count("b")
        if x > stubs0:
            continue
        conditions[x,y] += 1
        blocks = [labels[i:i+d] for i in range(0,stubs2,d)]
        r = sum(block.count("o") for block in blocks if "b" in block)
        hot_histogram[x,y,r] += 1
        if any("o" not in block for block in blocks):
            continue
        direct_n0[x,y,r] += 1
        actual[x,y,r] += row0[r]

    marks = polynomial(d,lambda s,o,b:(o,b,o if b else 0) if o else None)
    hot = Counter({(j,):comb(d,j) for j in range(1,d+1)})
    joint_v2, joint_v0 = Counter({(0,0,0):1}), Counter({(0,):1})
    for _ in range(v2):
        joint_v2 = convolve(joint_v2,marks)
    for _ in range(v0):
        joint_v0 = convolve(joint_v0,hot)
    for (x,y), denominator in conditions.items():
        if stubs2 > y:
            m = min(stubs2-y,(d-1)*y)
            for tilt in (Fraction(5,4),Fraction(2),Fraction(4)):
                raw = sum(hot_histogram[x,y,r]*tilt**r for r in range(x+1))/denominator
                envelope = (1+Fraction(x,stubs2-y)*(tilt-1))**m
                require(raw <= envelope, ("Case II hypergeometric bound mismatch",d,x,y,tilt))
                mgf_checks += 1
        for r in range(x+1):
            num = joint_v2[x,y,r]
            assignment = Fraction(joint_v0[(r,)],comb(stubs0,r))
            p = Fraction(num,denominator)*assignment
            require(num==direct_n0[x,y,r] and p==Fraction(actual[x,y,r],denominator),
                    ("case II exact mismatch",d,x,y,r))
            compare += 1
            positives += p>0
    return compare,positives,mgf_checks


def exact_case1(d):
    nstubs = 2*d
    cases = (0,1)
    counts = Counter()
    actual = {b:Counter() for b in cases}
    positive_cross = Counter()
    tilts = ((Fraction(1), Fraction(2), Fraction(1,2)),
             (Fraction(2,3), Fraction(7,5), Fraction(3)),
             (Fraction(3), Fraction(1,4), Fraction(2,3)))
    for labels in product("scb",repeat=nstubs):
        key = tuple(labels.count(letter) for letter in "scb")
        counts[key] += 1
        if "c" not in labels[:d] or "c" not in labels[d:]:
            continue
        positive_cross[key] += 1
        missing = sum("b" not in block for block in (labels[:d],labels[d:]))
        for b in cases:
            actual[b][key] += missing<=b

    tight = polynomial(d,lambda s,c,t:(s,c,t) if c and t else None)
    loose = polynomial(d,lambda s,c,t:(s,c,t) if c else None)
    compatible = {}
    for key in counts:
        compatible.setdefault(key[1],[]).append(key)
    compare = positives = 0
    for tilt in tilts:
        def monomial(powers):
            return prod(z**power for z,power in zip(tilt,powers))

        tight_value = sum(coeff*monomial(exp) for exp,coeff in tight.items())
        loose_value = sum(coeff*monomial(exp) for exp,coeff in loose.items())
        row_den = {k:monomial(k)*count for k,count in counts.items()}
        for b in cases:
            numerator = comb(2,b)*tight_value**(2-b)*loose_value**b
            for key, denominator in counts.items():
                exact = Fraction(actual[b][key],denominator)
                upper = numerator/row_den[key]
                require(exact <= upper, ("Case I row-0 Chernoff mismatch",d,b,key,tilt))
                for key2 in compatible[key[1]]:
                    row2 = Fraction(positive_cross[key2],counts[key2])
                    row2_upper = loose_value**2/row_den[key2]
                    require(row2 <= row2_upper and exact*row2 <= upper*row2_upper,
                            ("Case I joint Chernoff mismatch",d,b,key,key2,tilt))
                    compare += 1
                    positives += exact*row2>0
    for b in cases:
        for key, denominator in counts.items():
            p = Fraction(key[2],nstubs)
            f = 1-(1-p)**d
            upper = (nstubs+1)*comb(2,b)*f**(2-b)
            require(Fraction(actual[b][key],denominator) <= upper,
                    ("Case I occupancy mismatch",d,b,key))
    require(positives>0, ("vacuous Case I control",d))
    return compare,positives


def pairing(rng, d, v):
    labels = [c for c,size in enumerate(v) for _ in range(size)]
    slots = [[d*u+j for u,col in enumerate(labels) if c==col for j in range(d)] for c in range(5)]
    for row in slots:
        rng.shuffle(row)
    limits = [min(len(slots[0]),len(slots[2]))*2//3, len(slots[1])//2,
              min(len(slots[4]),len(slots[2]))//2, v[0]-2*d, len(slots[1])//2]
    edges = []
    for (i,j), limit in zip(EDGES,limits):
        budget = min(limit,len(slots[i]),len(slots[j]))
        for _ in range(2*rng.randrange(1+budget//2)):
            edges.append((slots[i].pop(),slots[j].pop()))
    for row in slots:
        edges.extend(zip(row[::2],row[1::2]))
    require(sorted(x for edge in edges for x in edge)==list(range(d*sum(v))), "invalid stub pairing")
    return labels,edges


def mutation(rng):
    tested = Counter()
    swaps = Counter()
    mutants = Counter()
    first_negative = None
    choices = ((12,2,12,4,4),(14,2,12,6,4),(12,4,14,6,4),(16,0,16,6,4))
    attempts = rejected = 0
    while sum(tested.values()) < 6000:
        attempts += 1
        require(attempts <= 12000, "configuration control attempt limit")
        d = 2+sum(tested.values())%3
        v = rng.choice(choices)
        labels,slots = pairing(rng,d,v)
        edges = [(u//d,w//d) for u,w in slots]
        h,s = divmod(2*sum(v)-1,5)
        large = set(rng.sample(range(5),s))
        cap = [h+(i in large) for i in range(5)]
        in_c = region(v) == "C" or (region(v) == "B" and min(v[0],v[2])-v[3] == GAP*sum(v))
        require(in_c and all(x<=k for x,k in zip(v,cap)), "mutation profile inconsistent")
        require(all((labels[u],labels[w]) in BLUE for u,w in edges), "invalid starting map")
        neigh = [set() for _ in labels]
        for u,w in edges:
            neigh[u].add(w)
            neigh[w].add(u)
        members = [[i for i,c in enumerate(labels) if c==j] for j in range(5)]
        z0 = {u for u in members[0] if not (set(members[3]) & neigh[u])}
        hot = {u for u in members[2] if set(members[4]) & neigh[u]}
        candidates = [u for u in members[0] if not (neigh[u] & hot)]
        require(len(z0)>=2*d, "planted Z0 threshold failed")
        if not candidates:
            rejected += 1
            continue
        tested[d] += 1
        old_phi = sum(x*x for x in v)

        def change(u, blockers, donors):
            result = labels.copy()
            result[u] = 3
            for w in blockers:
                result[w] = 0
            for w in donors:
                result[w] = 2
            return result

        for u in candidates:
            blockers = sorted(neigh[u] & set(members[2]))
            r = len(blockers)
            donors = sorted(z0-neigh[u]-{u})
            used = max(0,r-1)
            require(len(donors)>=used, "short donor list")
            moved = change(u,blockers,donors[:used])
            sizes = [moved.count(j) for j in range(5)]
            require(all((moved[x],moved[y]) in BLUE for x,y in edges), "correct swap is invalid")
            require(all(x<=k for x,k in zip(sizes,cap)) and sum(x*x for x in sizes)-old_phi<=-2,
                    "correct swap does not improve an admissible map")
            swaps[d] += 1

            adjacent = sorted((z0 & neigh[u])-{u})
            if used and adjacent:
                chosen = [adjacent[0],*donors[:used-1]]
                broken = change(u,blockers,chosen)
                forbidden = [(x,y) for x,y in edges if (broken[x],broken[y]) not in BLUE]
                require(any({x,y}=={u,adjacent[0]} for x,y in forbidden), "mutant did not fail")
                mutants[d] += 1
                if first_negative is None:
                    first_negative = dict(d=d, sizes=v, capacities=cap, stub_pairs=slots, u=u,
                                          blockers=blockers, donors=chosen, red_edge=[u,adjacent[0]])
    require(sum(tested.values())>=5000 and sum(mutants.values())>=1, "insufficient mutation controls")
    print("4 swap mutation: configurations",dict(tested),"valid decreasing swaps",dict(swaps),
          "edge-creating mutant failures",dict(mutants), "unqualified draws", rejected, flush=True)
    print("4 concrete negative mutant (0-indexed vertices and stubs):",json.dumps(first_negative),flush=True)


def ball(x):
    return arb(x.numerator)/x.denominator


def occupancy_rate(a0, edge):
    p = ball(edge)/ball(a0)
    return ball(a0)*(1-(1-p)**10).log()


def primal_rate(a, edges):
    diag = list(a)
    for (i,j), edge in zip(EDGES, edges):
        diag[i] -= edge
        diag[j] -= edge
    require(min([*diag, *edges]) >= 0 and sum(a) == 1, "nonfeasible Case I sample")
    # The five edge masses fill the ten directed off-diagonal cells;
    # the remaining row mass fills the diagonal and all red cells are zero.
    entropy = verify.entropy_term
    return (9*sum(entropy(ball(x)) for x in a)
            - 5*sum(entropy(ball(x)) for x in diag)
            - 10*sum(entropy(ball(x)) for x in edges))


def sample_edges(rng, a, cutoff, try_tail):
    a0, _, _, a3, _ = a
    cap = min(a0,a3)
    unit = Fraction(rng.randrange(1, 1000), 1000)
    if try_tail and cap > cutoff:
        edge = cutoff + unit*(cap-cutoff)
    else:
        edge = unit*min(cap,cutoff)
    capacity = list(a)
    capacity[0] -= edge
    capacity[3] -= edge
    cross = {EDGE_03: edge}
    other_edges = [ij for ij in EDGES if ij != EDGE_03]
    for i,j in rng.sample(other_edges, len(other_edges)):
        q = min(capacity[i],capacity[j])*Fraction(rng.randrange(1001),1000)
        capacity[i] -= q
        capacity[j] -= q
        cross[i,j] = q
    return [cross[ij] for ij in EDGES]


def max_entropy_vertex(a, leaf_bound):
    """Check the raw rate near the optimizer and enclose the exact optimizer."""
    _, q = naive(np.array(a, dtype=float))
    scale = 10**16
    edges = [Fraction(floor(q[i,j]*scale),scale) for i,j in EDGES]
    rate = primal_rate(a,edges)
    if a[3] == 0:
        require(edges[INDEX_03] == 0, "maximum-entropy edge violates zero part-3 mass")
        return False
    edge = edges[INDEX_03]
    require(edge > 0 and rate+occupancy_rate(a[0],edge) <= leaf_bound,
            ("max-entropy numerical primal exceeds Case I bound", a))

    # Use the rounded fit as a positive tilt on the nonzero rows. If Q*
    # maximizes entropy, its KL to B is at most (dual - rate)/5.
    # Binary KL of the aggregated 03/30 cell is at least 2(x-b)^2:
    # its second derivative is at least 4 and it vanishes to first order at b.
    tilt = [arb(float(q[i,i])).sqrt() for i in range(5)]
    partition = sum(tilt[i]*tilt[j] for i,j in BLUE)
    dual = 5*partition.log() + sum(
        ball(x)*(9*ball(x).log()-10*tilt[i].log()) for i,x in enumerate(a) if x
    )
    gap = (dual-rate).upper()
    require(0 <= gap and gap < arb("1e-10"), ("max-entropy primal-dual gap", a, gap))
    edge_upper = tilt[0]*tilt[3]/partition + (gap/40).sqrt()
    edge_upper = edge_upper.min(ball(a[3]))
    a0 = ball(a[0])
    penalty = a0*(1-(1-edge_upper/a0)**10).log() if edge_upper < a0 else arb(0)
    require(dual+penalty <= leaf_bound, ("exact max-entropy Case I rate exceeds bound", a))
    return True


def case1_rates(rng):
    cert = json.loads(gzip.decompress(Path("cert_case1.json.gz").read_bytes()))
    pending = [verify.ROOT]
    samples = Counter()
    vertices = Counter()
    worst = arb(-1000)
    for record in cert["records"]:
        bounds = pending.pop()
        opcode = record[0]
        if opcode == "S":
            _, axis, cut = record
            left, right = bounds.copy(), bounds.copy()
            low, high = bounds[axis]
            left[axis], right[axis] = [low,cut], [cut,high]
            pending.extend((right,left))
        if opcode != "C":
            continue
        _, raw_tilt, raw_upper, payload, _ = record
        clipped = verify.clip(bounds, "C")
        _, tilt, partition = verify.check_profile(clipped, raw_tilt, raw_upper)
        leaf_bound = verify.check_occupancy("case1", clipped, tilt, partition, payload,
                                           arb(raw_upper)/verify.SCALE)
        points = sorted(verify.profile_vertices(clipped))
        cutoff = Fraction(payload[0],verify.MASS)
        for point in points:
            finite = max_entropy_vertex([Fraction(x,verify.MASS) for x in point], leaf_bound)
            vertices["positive 03" if finite else "zero 03"] += 1
        for try_tail in (False, True):
            picked = rng.sample(points,min(5,len(points)))
            weights = [rng.randrange(1,1000) for _ in picked]
            a = [Fraction(sum(w*x for w,x in zip(weights,column)),verify.MASS*sum(weights))
                 for column in zip(*picked)]
            require(all(Fraction(lo,verify.MASS) <= x <= Fraction(hi,verify.MASS)
                        for x,(lo,hi) in zip(a,clipped)), "sample outside Case I leaf")
            edges = sample_edges(rng,a,cutoff,try_tail)
            edge = edges[INDEX_03]
            require(edge > 0, "random Case I sample has a vacuous rate")
            true_rate = primal_rate(a,edges)+occupancy_rate(a[0],edge)
            require(true_rate <= leaf_bound, ("raw Case I rate exceeds bound", a, edges))
            worst = worst.max((true_rate-leaf_bound).upper())
            samples["tail" if edge > cutoff else "near"] += 1
    require(not pending and sum(samples.values()) >= 1000 and set(samples) == {"near", "tail"}
            and vertices["positive 03"] > 0, "insufficient Case I leaf controls")
    print(f"7 Case I raw-rate checks: {sum(samples.values())} randomized pairs {dict(samples)}; "
          f"{sum(vertices.values())} max-entropy vertex checks {dict(vertices)}; "
          f"max random true_rate minus leaf_bound {worst.str(12)}", flush=True)

    a = tuple(map(Fraction, ("0.37815", "0.034175", "0.4001", "0.12505", "0.062525")))
    q03, cutoff = Fraction("0.071671"), Fraction("0.055668")
    require(sum(a) == 1 and region(a) == "C" and cutoff < q03 <= min(a[0],a[3]),
            "regression fixture outside Case I")
    true = occupancy_rate(a[0], q03)
    false = occupancy_rate(a[0], cutoff)
    excess = true-false
    require(arb("0.03668") < excess < arb("0.03669"), "old lower-cutoff counterexample failed")
    print(f"7 old cutoff regression: true {true.str(12)}, false {false.str(12)}, "
          f"excess +{excess.str(12, radius=False)}", flush=True)


def corruptions():
    original = json.loads(gzip.decompress(Path("cert_case2.json.gz").read_bytes()))
    path = Path("control_corrupt.json.gz")
    require(not path.exists(), "temporary mutation file already exists")
    variants = ("tilt", "missing leaf", "split boundary", "inflated claim", "trailing child", "occupancy tilt")
    try:
        for variant in variants:
            cert = json.loads(json.dumps(original))
            tree = cert["records"]
            leaf = next(i for i,x in enumerate(tree) if x[0]=="N")
            if variant == "tilt":
                tree[leaf][1][0] = 1
            elif variant == "missing leaf":
                tree.pop()
            elif variant == "split boundary":
                tree[0][2] += 1
            elif variant == "inflated claim":
                tree[leaf][-1] += 1
            elif variant == "trailing child":
                tree.append(["X"])
            elif variant == "occupancy tilt":
                next(row for row in tree if row[0]=="C")[3][-1] = 1
            path.write_bytes(gzip.compress(json.dumps(cert).encode(),mtime=0))
            result = subprocess.run([sys.executable,"-B","verify.py","--coverage",str(path)],
                                    capture_output=True,text=True,timeout=20)
            require(result.returncode!=0, ("mutated certificate accepted",variant))
            print("5 certificate mutation",repr(variant),"rejected:",result.stderr.strip(),flush=True)
    finally:
        if path.exists():
            path.unlink()


def case1_corruptions():
    original = json.loads(gzip.decompress(Path("cert_case1.json.gz").read_bytes()))
    occupancy = next(i for i,x in enumerate(original["records"]) if x[0] == "C")
    variants = ("tilt", "upper cutoff", "grid", "deleted leaf", "inflated claim",
                "inflated profile bound", "legacy format", "trailing null")
    with TemporaryDirectory(dir=".") as temp:
        path = Path(temp)/"mutant.json.gz"
        for variant in variants:
            cert = json.loads(json.dumps(original))
            tree = cert["records"]
            leaf = tree[occupancy]
            if variant == "tilt":
                leaf[1][0] = 1
                expected = "profile vertex exceeds bound"
            elif variant == "upper cutoff":
                leaf[3][0] = 1
                expected = "upper cutoff on wrong side"
            elif variant == "grid":
                cert["grid"] += 1
                expected = "unexpected root or metadata"
            elif variant == "deleted leaf":
                tree.pop()
                expected = "missing child"
            elif variant == "inflated claim":
                leaf[-1] += 1
                expected = "inflated or altered leaf claim"
            elif variant == "inflated profile bound":
                leaf[2] = verify.SCALE
                expected = "edge-divergence tail does not close"
            elif variant == "legacy format":
                cert["format"] = 1
                expected = "unexpected root or metadata"
            elif variant == "trailing null":
                tree.append(None)
                expected = "trailing children"
            path.write_bytes(gzip.compress(json.dumps(cert).encode(),mtime=0))
            result = subprocess.run([sys.executable,"-B","verify.py","--coverage",str(path)],
                                    capture_output=True,text=True,timeout=20)
            require(result.returncode != 0 and expected in result.stderr,
                    ("Case I mutation did not fail as expected", variant, result.stderr))
            print("7 Case I mutation", repr(variant), "rejected:", result.stderr.strip(), flush=True)


def main():
    rng = random.Random(1182)
    coverage(rng)
    subprocess.run([sys.executable,"-B","verify.py","--reference","reference_table.json"],check=True,timeout=20)
    print("2 all fixed-point reference cells recorded in reference_table.json",flush=True)
    for d in (2,3,4):
        i, ip = exact_case1(d)
        sizes = [(2,2),(3,2),(4,2)]
        if d <= 3:
            sizes += [(2,3),(3,3),(4,3)]
        if d == 2:
            sizes += [(2,4),(3,4),(4,4)]
        j, jp, mgf = map(sum, zip(*(exact_case2(d,x,y) for x,y in sizes)))
        require(jp >= 10, ("too few positive Case II cells",d,jp))
        print(f"3 d={d}: Case I {i} inequalities ({ip} positive), "
              f"Case II {j} exact cells ({jp} positive), {mgf} moment inequalities; zero mismatches",flush=True)
    mutation(rng)
    subprocess.run([sys.executable,"-B","verify.py","--red-witness"],check=True,timeout=20)
    corruptions()
    subprocess.run([sys.executable,"-B","finite.py"],check=True,timeout=20)
    print("6 all supported K and R counted, finite bound verified",flush=True)
    case1_rates(random.Random(118203))
    case1_corruptions()
    print("all controls passed",flush=True)


if __name__=="__main__":
    main()
