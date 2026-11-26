"""Clean-room exact referee for the supplied van Berkel–Bosma boundary family.

Run from this directory with nice -n 10 python3 referee_verify.py.
A disagreement with any scientific witness field produces a nonzero exit.
"""
import gzip
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "inputs"
DIGEST = "a8921373a9f3540ccb6cecf7adbebbc6e4fbc96a659ff4e187c7bb727499e8b6"
CASES = (*range(3, 41), 50, 100)


def require(test, explanation):
    if not test:
        raise ValueError(explanation)


def seeds(d):
    return (1, d - 1, 2 * d - 1)


def greedy(initial, end):
    """Bit n means a sum n. Update in descending cardinality for distinctness."""
    first, second, third = initial
    one = two = three = 0
    cap = (1 << (end + 1)) - 1
    for n in range(1, end + 1):
        if n <= third:
            if n not in (first, second, third):
                continue
        elif (three >> n) & 1:
            continue
        three |= (two << n) & cap
        two |= (one << n) & cap
        one |= 1 << n
    return one


def greedy_by_triples(initial, end):
    """Literal reference sieve. Enumerate triples when the largest term enters."""
    chosen = []
    blocked = bytearray(end + 1)
    for c in range(1, end + 1):
        if c <= initial[-1] and c not in initial:
            continue
        if blocked[c] and c > initial[-1]:
            continue
        for j, b in enumerate(chosen):
            if b + c + initial[0] > end:
                break
            for i in range(j):
                total = chosen[i] + b + c
                if total > end:
                    break
                blocked[total] = 1
        chosen.append(c)
    return tuple(chosen)


def positions(bits, lo, hi):
    return tuple(n for n in range(lo, hi + 1) if (bits >> n) & 1)


@dataclass(frozen=True)
class Tail:
    pre: tuple
    block: tuple
    m: int

    @property
    def K(self):
        return max(0, self.pre[-1] if self.pre else 0, self.block[-1] - self.m)

    @property
    def gaps(self):
        return differences(self.block + (self.block[0] + self.m,))

    def shape(self):
        terms = self.pre + self.block
        require(self.m > 0 and self.block and terms[0] > 0, "empty or invalid tail")
        require(all(x < y for x, y in zip(terms, terms[1:])), "order")
        require(self.block[-1] < self.block[0] + self.m, "overlapping periods")

    def members(self, stop):
        return {x for x in self.pre if x <= stop}.union(
            *(range(x, stop + 1, self.m) for x in self.block)
        )


def differences(xs):
    return tuple(b - a for a, b in zip(xs, xs[1:]))


def discover(initial):
    """Try binary widths in increasing order, using only directly generated bits."""
    end = 128
    while end <= 65536:
        bits = greedy(initial, end)
        for m in range(1, end // 6 + 1):
            # Last unequal C[n], C[n+m] on the observed prefix (ignore n=0).
            mask = ((1 << (end - m + 1)) - 1) ^ 1
            unequal = (bits ^ (bits >> m)) & mask
            K = max(0, unequal.bit_length() - 1)
            Q = (end - K) // m
            if (Q - 6) * m < 2 * K or K + (Q - 1) * m < initial[-1]:
                continue
            block = positions(bits, K + 1, K + m)
            if block:
                return Tail(positions(bits, 1, K), block, m)
        end *= 2
    raise ValueError("no finite-cutoff certificate in the search interval")


def minimal(t):
    """Check binary period, index period, and both exact left boundaries."""
    t.shape()
    start = t.K + 1
    block = set(t.block)
    word = bytes(n in block for n in range(start, start + t.m))
    require(sum(word) == len(t.block), "block outside binary window")
    require((word + word).find(word, 1) == t.m, "binary period multiple")
    g = t.gaps
    require(all(g != g[r:] + g[:r] for r in range(1, len(g))), "gap period multiple")
    if t.pre:
        require(t.block[0] - t.pre[-1] != g[-1], "late difference boundary")
    if t.K:
        window = t.members(t.K + t.m)
        require((t.K in window) != (t.K + t.m in window), "late binary boundary")


def lemma(initial, t):
    """Test the claimed set through the exact cutoff. Check minimality separately."""
    t.shape()
    K, m = t.K, t.m
    Q = 6 + (2 * K + m - 1) // m
    cutoff = K + Q * m
    require(K + (Q - 1) * m >= initial[-1], "cutoff before seeds")
    actual = greedy(initial, cutoff)
    predicted = sum(1 << x for x in t.members(cutoff))
    diff = actual ^ predicted
    if diff:
        first = (diff & -diff).bit_length() - 1
        raise ValueError(f"greedy membership at n={first}")
    require(t.block and (Q - 6) * m >= 2 * K, "lemma hypotheses")
    return dict(K=K, M=m, Q=Q, cutoff=cutoff, lhs_minus_rhs=(Q - 6) * m - 2 * K,
                simulated_terms_up_to_cutoff=actual.bit_count())


def residue(initial, t):
    """Construct the entire strict triple-sum set as finite points and rays.

    For s terms of ONE ray b+jm the least sum is sb + binom(s,2)m.
    Every higher value of that residue follows by increasing the largest index.
    Distinct rays and isolated prefix entries are disjoint as sets of integers.
    """
    t.shape()
    m = t.m
    points = [{sum(xs) for xs in combinations(t.pre, i)} for i in range(4)]
    rays = [{} for _ in range(4)]
    for b in t.block:
        for count in range(3, 0, -1):
            targets = rays[count]
            for take in range(1, count + 1):
                offset = take * b + take * (take - 1) // 2 * m
                old = count - take
                for sources in (points[old], rays[old].values()):
                    for x in sources:
                        total = x + offset
                        r = total % m
                        if r not in targets or total < targets[r]:
                            targets[r] = total
    starts = rays[3]
    stop = max(initial[-1], t.block[-1], max(starts.values(), default=0),
               max(points[3], default=0))
    members = t.members(stop)
    require({x for x in members if x <= initial[-1]} == set(initial), "residue seeds")
    for n in range(initial[-1] + 1, stop + 1):
        r = n % m
        representable = n in points[3] or (r in starts and n >= starts[r])
        require((n in members) != representable, f"residue membership at n={n}")
    member_residues = {b % m for b in t.block}
    require(set(starts) == set(range(m)) - member_residues, "infinite residue mismatch")
    return stop


def gf_audit(initial, t):
    """Count triples directly, recover the producer's numerator by finite differences.

    Positive integer packing evaluates finite polys at a power of 256. Each
    ordered-triple coefficient is <= |A|^3. The final coefficients count
    ordered distinct triples and hence also fit with no inter-digit carry.
    """
    L = 6 * t.m
    # (1-x^L) A(x^e) is a polynomial of degree <= L + e*max(block).
    # Newton's identity thus bounds the cleared numerator by 3L+3*max(block).
    bound = 3 * (L + t.block[-1])
    end = bound + 3 * L
    members = t.members(end)
    width = max(1, ((len(members) ** 3).bit_length() + 7) // 8)

    def packed(e):
        digits = bytearray(width * (end + 1))
        for v in members:
            if e * v <= end:
                digits[width * e * v] = 1
        return int.from_bytes(digits, "little")

    a = packed(1)
    ordered = a ** 3 - 3 * a * packed(2) + 2 * packed(3)
    size = width * (end + 1)
    digits = (ordered & ((1 << (8 * size)) - 1)).to_bytes(size, "little")
    f = [int.from_bytes(digits[i:i + width], "little") for i in range(0, size, width)]
    # Multiplication by (1-x^L)^3 with zero coefficients at negative indices.
    padded = [0] * (3 * L) + f
    numerator = [padded[n + 3*L] - 3*padded[n + 2*L] + 3*padded[n + L] - padded[n]
                 for n in range(end + 1)]
    support = [i for i, coeff in enumerate(numerator) if coeff]
    deg = support[-1]
    require(deg <= bound, "rational numerator degree")
    start = max(deg, t.block[-1]) + 1
    for n in range(initial[-1] + 1, start):
        require((f[n] == 0) == (n in members), f"GF finite n={n}")
    for n in range(start, start + L):
        alpha = f[n]
        beta = f[n + L] - alpha
        gamma = f[n + 2*L] - 2*f[n + L] + alpha
        if n in members:
            require((alpha, beta, gamma) == (0, 0, 0), f"GF inclusion n={n}")
        else:
            require(alpha > 0 and beta >= 0 and gamma >= 0, f"GF gap n={n}")
    return dict(L=L, poly_degree_cutoff=deg, verification_start=start,
                nonzero_terms_in_T=len(support))


def finite_record(d, t, cutoff, gf):
    return dict(d=d, seeds=list(seeds(d)), k=len(t.pre), p=len(t.block), m=t.m,
                preperiod=list(t.pre), first_period_block=list(t.block),
                difference_preperiod=list(differences(t.pre + t.block[:1])),
                difference_period=list(t.gaps), lemma3=cutoff, generating_function=gf)


def shifted(t, count):
    """Advance the boundary by count terms, rotating the tail word accordingly."""
    block = list(t.block)
    pre = list(t.pre)
    for _ in range(count):
        b = block.pop(0)
        pre.append(b)
        block.append(b + t.m)
    return Tail(tuple(pre), tuple(block), t.m)


def rejected(fn, *args):
    try:
        fn(*args)
    except ValueError as exc:
        return str(exc)
    raise ValueError(f"accepted a mutant in {fn.__name__}")


def compare(path, actual, expected, errors):
    if actual != expected:
        errors.append(f"{path}: supplied {actual!r}, independently expected {expected!r}")


def field_bytes(name, value):
    """Recover a complete top-level field, including the source indentation."""
    return json.dumps({name: value}, indent=2).encode()[2:-2]


def small_certificate(d, t):
    """Enumerate canonical smallest (sum,a,b,c) for each unbounded gap ray."""
    finite = set(t.pre)
    starts = []
    for b in t.block:
        while b - t.m in finite:
            b -= t.m
            finite.remove(b)
        starts.append(b)
    rays = {b % t.m: b for b in starts}
    want = set(range(t.m)) - rays.keys()
    end = 2 * t.block[-1]
    while True:
        min_cover, triples = {}, {}
        for a, b, c in combinations(sorted(t.members(end)), 3):
            n = a + b + c
            if n > end:
                continue
            triples.setdefault(n, [a, b, c])
            r = n % t.m
            if r in want and c % t.m in rays and c >= rays[c % t.m]:
                w = (n, a, b, c)
                if r not in min_cover or w < min_cover[r]:
                    min_cover[r] = w
        if min_cover.keys() == want:
            break
        end *= 2
        require(end <= 65536, "small-case ray cover")
    cut = max(w[0] for w in min_cover.values())
    members = t.members(cut)
    gaps = [n for n in range(seeds(d)[-1] + 1, cut) if n not in members]
    return dict(d=d, modulus=t.m, isolated_finite_elements=sorted(finite),
                infinite_progressions={str(r): rays[r] for r in sorted(rays)},
                max_periodic_cover_threshold=cut,
                nonmember_residue_cover={str(r): dict(zip(("threshold", "a", "b", "c0"),
                                                            min_cover[r])) for r in sorted(want)},
                finite_gap_triples_below_threshold={str(n): triples[n] for n in gaps})


def boundaries(t):
    """Recover all named interval endpoints from sets of distinct summands."""
    one, second, *inside, last = t.pre
    first_tail, last_tail = t.block[0], t.block[-1]
    pairs = {a + b for a, b in combinations(inside, 2)}
    triples = {a + b + c for a, b, c in combinations(inside, 3)}

    def interval(numbers):
        values = set(numbers)
        lo, hi = min(values), max(values)
        require(len(values) == hi - lo + 1, "hole in claimed sum interval")
        return (lo, hi)

    def translate(values, by):
        return interval(n + by for n in values)

    def plus_tail(values):
        lo, hi = interval(values)
        return (lo + first_tail, hi + last_tail)

    g1 = translate(inside, one + second)
    bs = [translate(pairs, one), translate(pairs, second), translate(inside, one + last),
          interval(triples), translate(pairs, last)]
    cs = [plus_tail([one + second]), plus_tail(one + x for x in inside),
          plus_tail(second + x for x in inside), plus_tail(pairs),
          plus_tail(x + last for x in inside)]
    g2 = last + 1, first_tail - 1
    gj = last_tail + 1, first_tail + t.m - 1
    require(g1 == (inside[-1] + 1, last - 1), "seed gap")
    for cover, (lo, hi) in ((bs, g2), (cs, gj)):
        require(set().union(*(range(a, b + 1) for a, b in cover)) == set(range(lo, hi + 1)),
                "interval coverage")
    return dict(U1=(one, one), U2=(second, second), I_star=(inside[0], inside[-1]),
                U3=(last, last), T_j_base=(first_tail, last_tail), G_pre_1=g1,
                G_pre_2=g2, G_j_base=gj, **{f"B{i}": v for i, v in enumerate(bs, 1)},
                **{f"C{i}": v for i, v in enumerate(cs, 1)})


def quotient_check(d, t):
    """All unordered residue multisets, allowing equal residues at different heights."""
    fixed = {1, d-1, 3*d-2, 4*d-1}
    free = set(range(2*d-2, 3*d-2))
    zero = set(t.pre)
    count = 0
    for rs in combinations_with_replacement(sorted(fixed | free), 3):
        if any(rs.count(r) > 1 for r in rs if r in fixed):
            continue
        count += 1
        q, r = divmod(sum(rs), t.m)
        for u in set(rs) & free:
            mult = rs.count(u)
            q += mult * int(u == 2*d-2) + mult*(mult-1)//2
        require(q > 0 or r not in zero, f"zero-level collision at d={d}: {rs}")
        can_be_positive = q > 0 or any(u in free for u in rs)
        require(not can_be_positive or r not in free, f"tail collision at d={d}: {rs}")
    return count


def symbolic_exclusion():
    """Separate all 20 legal block types on the whole half-line d >= 6.

    For a fixed choice of blocks, every endpoint below is affine in d.
    Comparing its values at 6 and 7 gives its exact slope, not an estimate.
    """
    def bounds(d, chosen):
        parts = {"u": 1, "v": d-1, "w": 4*d-1}
        singles = sum(parts.get(name, 0) for name in chosen)
        i, t = chosen.count("I"), chosen.count("T")
        # i distinct entries of I cost 0+...+(i-1) above its minimum.
        # Tail residues may coincide, since their levels can differ.
        distinct = i*(i-1)//2
        lo = singles + i*(2*d-1) + distinct + t*(2*d-2)
        hi = singles + i*(3*d-2) - distinct + t*(3*d-3)
        if not t:
            targets = [(x, x) for x in parts.values()] + [(2*d-1, 3*d-2)]
            ceiling = 10*d-5  # first actual tail member
        else:
            m = 8*d-3
            targets = [(2*d-2+s, 3*d-3+s) for s in (0, m)]
            ceiling = 2*m  # no further positive-level residue interval
        return ceiling-hi, [(a-hi, lo-b) for a, b in targets]

    def positive_at_all_d(x6, x7):
        return x6 > 0 and x7 >= x6

    count = 0
    for chosen in combinations_with_replacement(("u", "v", "w", "I", "T"), 3):
        if any(chosen.count(s) > 1 for s in ("u", "v", "w")):
            continue
        count += 1
        ceiling6, margins6 = bounds(6, chosen)
        ceiling7, margins7 = bounds(7, chosen)
        require(positive_at_all_d(ceiling6, ceiling7), f"sum ceiling for {chosen}")
        for (below6, above6), (below7, above7) in zip(margins6, margins7):
            require(positive_at_all_d(below6, below7) or positive_at_all_d(above6, above7),
                    f"symbolic target intersection for {chosen}")
    return count


def affine_pair(at6, at7):
    slope = at7 - at6
    return [slope, at6 - 6*slope]


def check_affine(w, results, errors):
    boundary_ds = [6, 7, 8, 9, 10, 50, 100]
    compare("boundary_check_d_values", w["boundary_check_d_values"], boundary_ds, errors)
    all_bounds = {d: boundaries(results[d]) for d in boundary_ds}
    # Endpoints are proved affine separately in REFEREE.md. Two evaluations
    # uniquely determine each coefficient. Check the remaining five evaluations too.
    b6, b7 = all_bounds[6], all_bounds[7]
    expected = {k: [affine_pair(x, y) for x, y in zip(v, b7[k])] for k, v in b6.items()}
    for d, bounds in all_bounds.items():
        for k, values in bounds.items():
            require(tuple(a*d+b for a, b in expected[k]) == values, f"endpoint {d},{k}")
    for name in ["U1", "U2", "I_star", "U3", "T_j_base"]:
        compare("blocks." + name, w["blocks"][name], expected[name], errors)
    for name, prop in [("modulus", lambda t: t.m), ("minimal_preperiod_k", lambda t: len(t.pre)),
                       ("minimal_period_p", lambda t: len(t.block)),
                       ("characteristic_preperiod_K", lambda t: t.K)]:
        compare(name, w[name], affine_pair(prop(results[6]), prop(results[7])), errors)
    covering = w["part_B_covering"]
    for g in ("G_pre_1", "G_pre_2", "G_j_base"):
        compare(g, covering[g]["target"], expected[g], errors)
    for g, prefix in (("G_pre_2", "B"), ("G_j_base", "C")):
        for i, item in enumerate(covering[g]["subintervals"], 1):
            name = prefix + str(i)
            compare(g + ".name", item["name"], name, errors)
            compare(name, item["range"], expected[name], errors)
        require(len(covering[g]["subintervals"]) == 5, "cover arity")
    for d in (3, 4, 5):
        t = results[d]
        s0 = t.members(4*d - 1)
        sums = {sum(xs) for xs in combinations(s0, 3)}
        holes = sorted(set(range(4*d, 10*d-5)) - sums)
        supplied = covering["G_pre_2"]["small_d_failures"][str(d)]
        compare(f"first hole d={d}", supplied["first_uncovered_in_G_pre_2"], holes[0], errors)
        print(f"d={d} all seed-only holes in [{4*d},{10*d-6}]: {holes}")
    return sum(quotient_check(d, results[d]) for d in boundary_ds)


def apply_controls(w, ts):
    tests = [
        (seeds(4), Tail(ts[4].pre, ts[4].block + (ts[4].block[0] + ts[4].m,), 31)),
        (seeds(6), Tail(ts[6].pre, ts[6].block, 47)),
        (seeds(6), Tail(ts[6].pre[:-1] + (ts[6].pre[-1]+1,), ts[6].block, ts[6].m)),
        (seeds(6), Tail(ts[6].pre, ts[6].block + tuple(b+ts[6].m for b in ts[6].block),
                              2*ts[6].m)),
        (seeds(6), shifted(ts[6], len(ts[6].block))),
    ]
    require(len(w) == len(tests), "control count")
    for i, ((initial, mutant), claim) in enumerate(zip(tests, w)):
        require((tuple(claim["seeds"]), tuple(claim["preperiod"]),
                 tuple(claim["first_period_block"]), claim["m"]) ==
                (initial, mutant.pre, mutant.block, mutant.m), "control input mismatch")
        if i < 3:
            print(claim["id"], rejected(lemma, initial, mutant), rejected(residue, initial, mutant),
                  rejected(gf_audit, initial, mutant))
        else:
            lemma(initial, mutant)
            residue(initial, mutant)
            gf_audit(initial, mutant)
            print(claim["id"], "same set;", rejected(minimal, mutant))
    # All nontrivial cyclic boundary phases, a one-place early start and
    # value shifts in each direction, plus nonminimal factors 2 and 3.
    counts = dict(late=0, early=0, value_shift=0, multiple=0)
    for d, t in ts.items():
        initial = seeds(d)
        for n in range(1, len(t.block) + 1):
            rejected(minimal, shifted(t, n))
            counts["late"] += 1
        early = Tail(t.pre[:-1], (t.pre[-1],) + t.block[:-1], t.m)
        rejected(lemma, initial, early)
        counts["early"] += 1
        for by in (-1, 1):
            moved = Tail(t.pre, tuple(x+by for x in t.block), t.m)
            rejected(lemma, initial, moved)
            counts["value_shift"] += 1
        for factor in (2, 3):
            repeated = tuple(b+j*t.m for j in range(factor) for b in t.block)
            rejected(minimal, Tail(t.pre, repeated, factor*t.m))
            counts["multiple"] += 1
    print("Additional rejected mutants", counts, "total", sum(counts.values()))


def written_examples(ts, small):
    """Re-add the numerical triples printed in the prose, including noncanonical choices."""
    lines = (INPUT / "PROOF.md").read_text().splitlines()
    t = ts[4]
    members = t.members(61)
    wanted = set(range(8, 61)) - members
    finite = []
    for values in re.findall(r"(\d+) \+ (\d+) \+ (\d+)", lines[139]):
        abc = tuple(map(int, values))
        finite.append((sum(abc), *abc))
    compact = r"(\d+) = (\d+)\+(\d+)\+(\d+)"
    for values in re.findall(compact, "\n".join(lines[140:144])):
        finite.append(tuple(map(int, values)))
    require({n for n, *xs in finite} == wanted and len(finite) == len(wanted),
            "written d=4 finite gaps")
    for n, a, b, c in finite:
        require(a < b < c < n and {a, b, c} <= members and a+b+c == n,
                f"written d=4 triple for {n}")
    pattern = r"(\d+) \\bmod 27\$ \(\$\\ge (\d+)\$\): \$(\d+) \+ (\d+) \+ \((\d+) \+ 27j\)"
    covered = set()
    for row in re.findall(pattern, "\n".join(lines[145:151])):
        r, n, a, b, c = map(int, row)
        require(a < b < c and {a, b, c} <= members and a+b+c == n <= 61 and n % t.m == r,
                f"written d=4 ray for residue {r}")
        start = small["4"]["infinite_progressions"].get(str(c % t.m))
        require(start is not None and c >= start, f"bounded c for d=4 residue {r}")
        covered.add(r)
    require(covered == set(range(t.m)) - {b % t.m for b in t.block}, "written d=4 gap rays")
    fixed = small["4"]["isolated_finite_elements"]
    print("d=4 proof lines 140–151:", len(finite), "finite triples and", len(covered), "gap rays")
    print("d=4 line 130 +2 intersection:",
          sorted({(sum(ab)+2) % t.m for ab in combinations(fixed, 2)} & set(fixed)))
    print("d=4 line 135 isolated sums:", sorted(sum(xs) for xs in combinations(fixed, 3)))
    t = ts[5]
    members = t.members(221)
    starts = small["5"]["infinite_progressions"].values()
    strict_minimum_base_cover = {(a+b+c) % t.m for c in starts
                                 for a, b in combinations(sorted(x for x in members if x < c), 2)}
    missing = set(range(t.m)) - {b % t.m for b in t.block} - strict_minimum_base_cover
    print("d=5 line 171 least-base cover misses", sorted(missing))
    print("d=5 all strict triples for 221:", [xs for xs in combinations(sorted(members), 3)
                                               if sum(xs) == 221])


def main():
    require(sys.version_info >= (3, 10), "Python 3.10+ required")
    tex_name, tex = json.loads(gzip.decompress((INPUT / "2609.16843v2.tex.json.gz").read_bytes()))[0]
    require(tex_name == "main.tex", "source file")
    envs = re.findall(r"\\begin\{(theorem|conjecture|lemma|example|corollary|remarks?)\}", tex)
    require(envs[:7] == ["theorem", "conjecture", "theorem", "conjecture", "conjecture",
                         "theorem", "lemma"], "v2 shared numbering")
    shared = r"\\newtheorem\{(?:lemma|conjecture)\}\[theorem\]"
    require(len(re.findall(shared, tex)) == 2, "shared theorem counter")
    conjecture = tex.split(r"\begin{conjecture}\label{conj:except}", 1)[1].split(
        r"\end{conjecture}", 1)[0]
    statement = " ".join(conjecture.split())
    quoted = (INPUT / "PROOF.md").read_text().splitlines()[21].split("> ", 1)[1]
    normalized = statement.replace(r"d\geq", r"d \ge")
    require(quoted == normalized, "conjecture after TeX normalization")
    for initial, baseline in [((1, 2, 3), (6, 5, 23)), ((1, 2, 6), (6, 6, 28))]:
        t = discover(initial)
        lemma(initial, t)
        residue(initial, t)
        minimal(t)
        require((len(t.pre), len(t.block), t.m) == baseline, "v2 positive control")
        print("v2 positive control", initial, baseline)
    ts, records = {}, []
    for d in CASES:
        initial = seeds(d)
        t = discover(initial)
        minimal(t)
        cutoff = lemma(initial, t)
        direct = greedy_by_triples(initial, cutoff["cutoff"])
        require(direct == tuple(sorted(t.members(cutoff["cutoff"]))), f"literal triples at d={d}")
        stop = residue(initial, t)
        gf = gf_audit(initial, t)
        row = finite_record(d, t, cutoff, gf)
        records.append(row)
        ts[d] = t
        if d >= 6:
            expected = Tail((1, d-1, *range(2*d-1, 3*d-1), 4*d-1),
                            tuple(range(10*d-5, 11*d-5)), 8*d-3)
            require(t == expected, f"general formula differs at d={d}")
        print(f"d={d:3} k={len(t.pre):3} p={len(t.block):3} m={t.m:3} K={t.K:3} "
              f"Q={cutoff['Q']} cutoff={cutoff['cutoff']:4} residue_cutoff={stop:4} "
              f"GF_degree={gf['poly_degree_cutoff']}")
    raw = (INPUT / "witnesses.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    print(f"witnesses.json: {len(raw)} bytes, SHA-256 {digest}")
    require(digest == DIGEST, "wrong witness bytes")
    w = json.loads(raw)
    require(json.dumps(w, indent=2).encode() == raw, "witness serialization")
    errors = []
    compare("conjecture_statement", w["conjecture_statement"],
            normalized.replace("$", "").replace(r"\ge", ">="), errors)
    supplied = w["finite_cutoff_certificates"]
    compare("finite rows count", len(supplied), 38, errors)
    for row, their_row in zip(records[:38], supplied):
        compare(f"d={row['d']} finite certificate", their_row, row, errors)
    finite_bytes = field_bytes("finite_cutoff_certificates", records[:38])
    compare("finite field matches raw bytes", finite_bytes in raw, True, errors)
    for d in (4, 6):
        entry = w["disproof_summary"][f"d{d}_counterexample"]
        row = records[d-3]
        compare("d", entry["d"], d, errors)
        compare("sequence", entry["sequence"], "S_{%s,%s,%s}" % seeds(d), errors)
        compare("conjectured", entry["conjectured"], dict(k=d+3, p=d, m=8*d-1), errors)
        compare("actual", entry["actual"], {p: row[p] for p in ["k", "p", "m"]}, errors)
        for name, key in [("preperiod", "preperiod"), ("first_period_block", "first_period_block"),
                          ("repeating_difference_block", "difference_period")]:
            compare(name, entry[name], row[key], errors)
    small = {}
    for d in (3, 4, 5):
        sc = small_certificate(d, ts[d])
        small[str(d)] = sc
        compare(f"small residue certificate {d}", w["small_exceptional_residue_certificates"][str(d)],
                sc, errors)
        print(f"d={d} reproduced {len(sc['nonmember_residue_cover'])} residue triples and "
              f"{len(sc['finite_gap_triples_below_threshold'])} finite-gap triples")
    small_bytes = field_bytes("small_exceptional_residue_certificates", small)
    compare("small certificate field matches raw bytes", small_bytes in raw, True, errors)
    print(f"Compared raw certificate fields of {len(finite_bytes)} and {len(small_bytes)} bytes.")
    written_examples(ts, small)
    print("All-d exclusion, legal block types:", symbolic_exclusion())
    print("exact residue multisets", check_affine(w["general_theorem_d_ge_6"], ts, errors))
    apply_controls(w["negative_controls"], ts)
    print(f"Completed {len(ts)} exact cases, {len(supplied)} finite witness rows compared.")
    for issue in errors:
        print("WITNESS DISAGREEMENT", issue)
    print(f"Total scientific witness disagreements: {len(errors)}")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
