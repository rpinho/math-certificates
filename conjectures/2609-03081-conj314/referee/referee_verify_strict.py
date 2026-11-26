from fractions import Fraction
"""Independent integer verification for Lewis and Won, arXiv:2609.03081v1."""
import gzip
import json
import os
import re
import resource
import signal
import sys
from time import monotonic_ns, time_ns
from functools import cache, lru_cache
from itertools import combinations, groupby, permutations
from pathlib import Path

INPUT = Path(__file__).resolve().parent.joinpath("inputs")
ARTICLE = INPUT.joinpath("2609.03081v1.tex.json.gz")


def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def grid(w):
    n = len(w)
    check(n and all(type(j) is int for j in w)
          and sorted(w) == list(range(1, n + 1)), "invalid permutation")
    return [[int(j == black) for j in range(1, n + 1)] for black in w]


def word_runs(cells):
    """Each iterable entry is (coordinate, color), with black encoded as one."""
    return [tuple(cell for cell, _ in run)
            for black, run in groupby(cells, key=lambda item: item[1])
            if not black]


def incidence(board):
    n = len(board)
    across = []
    down = []
    for i in range(n):
        across.extend(word_runs(((i, j), board[i][j]) for j in range(n)))
    for j in range(n):
        down.extend(word_runs(((i, j), board[i][j]) for i in range(n)))
    owner = {cell: d for d, word in enumerate(down) for cell in word}
    check(len(across) == len(down), "unequal numbers of words")
    return tuple(sum(1 << owner[cell] for cell in word) for word in across)


def matching_permanent(rows):
    """Assign one unused column per row. Retain a column only while it is live."""
    n = len(rows)
    future = [0] * (n + 1)
    for i in reversed(range(n)):
        future[i] = future[i + 1] | rows[i]
    states = {0: 1}
    for i, row in enumerate(rows):
        live = future[i + 1]
        ending = row & ~live
        following = {}
        for used, multiplicity in states.items():
            required = ending & ~used
            if required and required & (required - 1):
                continue
            choices = required or (row & ~used)
            while choices:
                bit = choices & -choices
                choices -= bit
                key = (used | bit) & live
                following[key] = following.get(key, 0) + multiplicity
        states = following
    return states.get(0, 0)


def ryser_permanent(rows):
    """Independent inclusion-exclusion. Each equal-column class has binomial weights."""
    matrix = [[int(bool(row & (1 << j))) for j in range(len(rows))] for row in rows]
    while matrix:
        degree = [sum(row) for row in matrix]
        col_degree = list(map(sum, zip(*matrix)))
        if 0 in degree or 0 in col_degree:
            return 0
        if 1 in degree:
            i = degree.index(1)
            j = matrix[i].index(1)
        elif 1 in col_degree:
            j = col_degree.index(1)
            i = next(r for r, row in enumerate(matrix) if row[j])
        else:
            break
        matrix.pop(i)
        for row in matrix:
            row.pop(j)
    if not matrix:
        return 1

    # For grouped column subsets, constrain sparse rows first. When no unvisited
    # column can cover a still-uncovered row, its Ryser product is zero.
    columns = list(zip(*matrix))
    groups = {column: columns.count(column) for column in set(columns)}
    pending = set(range(len(matrix)))
    ordered = []
    while groups:
        r = min(pending, key=lambda i: (sum(c[i] for c in groups), i))
        for c in sorted(c for c in groups if c[r]):
            ordered.append((c, groups.pop(c)))
        pending.remove(r)
        pending = {i for i in pending if any(c[i] for c in groups)}

    last = [max(k for k, (col, _) in enumerate(ordered) if col[i])
            for i in range(len(matrix))]
    sums = [0] * len(matrix)
    terms = []
    for k, (col, copies) in enumerate(ordered):
        support = [i for i, entry in enumerate(col) if entry]
        finished = [i for i, final in enumerate(last) if final == k]
        weights = [1]
        for j in range(1, copies + 1):
            weights.append(-weights[-1] * (copies - j + 1) // j)
        terms.append((support, finished, weights))

    def visit(k):
        if k == len(terms):
            return 1
        support, finished, weights = terms[k]
        subtotal = 0
        for j, weight in enumerate(weights):
            if j:
                for r in support:
                    sums[r] += 1
            factor = weight
            for r in finished:
                factor *= sums[r]
            if factor:
                subtotal += factor * visit(k + 1)
        for r in support:
            sums[r] -= len(weights) - 1
        return subtotal

    return (-1) ** len(matrix) * visit(0)


def layered(shape):
    w = []
    for size in shape:
        check(type(size) is int and size > 0, "invalid composition part")
        start = len(w)
        w.extend(range(start + size, start, -1))
    return tuple(w)


def recover_shape(w):
    ends = [i for i in range(1, len(w)) if w[i - 1] < w[i]] + [len(w)]
    shape = tuple(b - a for a, b in zip([0] + ends, ends))
    check(layered(shape) == tuple(w), "permutation is not layered")
    return shape


def endpoint_shape(n, a, b):
    check(a >= 1 and b >= 1 and a + b <= n, "inadmissible endpoint pair")
    return (a,) + (1,) * (n - a - b) + (b,)


@cache
def stirling(n, k):
    if k == 0 or k > n:
        return int(n == k)
    return k * stirling(n - 1, k) + stirling(n - 1, k - 1)


def factorial(n):
    product = 1
    for i in range(2, n + 1):
        product *= i
    return product


def proposition(n, a, b):
    return sum(stirling(a, k) * stirling(b, k)
               * (k ** (n - a - b) * factorial(k)) ** 2
               for k in range(1, min(a, b) + 1))


def direct(w):
    return matching_permanent(incidence(grid(w)))


def dual_count(w):
    rows = incidence(grid(w))
    first = matching_permanent(rows)
    second = ryser_permanent(rows)
    check(first == second, f"matching/Ryser disagreement for {w}: {first}, {second}")
    check(first == fixed_cut_count(w), f"word-incidence/cut disagreement for {w}")
    return first


def controls():
    total = 0
    for n, expected in enumerate((1, 1, 1, 5, 17, 73, 469, 3493), 1):
        largest = -1
        count = 0
        for w in permutations(range(1, n + 1)):
            largest = max(largest, dual_count(w))
            count += 1
        check(largest == expected and count == factorial(n), f"control n={n}")
        endpoint_values = {m: direct(layered(endpoint_shape(n, m, m)))
                           for m in range(1, n // 2 + 1)}
        if n == 1:
            endpoint_values[0] = direct((1,))  # Read the identity as the degenerate shape.
        check(max(endpoint_values.values()) == largest, f"small-order maximizer shape n={n}")
        print("control", n, "permutations", count, "maximum", largest, "attained at",
              [m for m in endpoint_values if endpoint_values[m] == largest], flush=True)
        total += count
    value = dual_count((2, 7, 4, 8, 1, 6, 3, 5))
    check(value == 155, "order-eight 155 control")
    print("paired counts", total, "separate order-eight example", value, flush=True)


def family(n, asymmetric):
    pairs = ((a, b) for a in range(1, n) for b in range(1, n + 1 - a)
             if asymmetric or a == b)
    values = {}
    for a, b in pairs:
        w = layered(endpoint_shape(n, a, b))
        count = direct(w)
        check(count == fixed_cut_count(w) == proposition(n, a, b), f"Proposition 3.15 n={n}, pair={(a, b)}")
        values[a, b] = count
    expected = n * (n - 1) // 2 if asymmetric else n // 2
    check(len(values) == expected, "endpoint coverage")
    best = max(values.values())
    best_pairs = [pair for pair in values if values[pair] == best]
    print("n", n, "matching/horizontal-cut/formula pairs", len(values), "maximum", best, "at", best_pairs)
    print("symmetric counts", [values[m, m] for m in range(1, n // 2 + 1)])
    if asymmetric:
        unequal = {pair: v for pair, v in values.items() if pair[0] != pair[1]}
        next_best = max(unequal.values())
        print("unequal endpoint pairs", len(unequal), "maximum", next_best,
              "at", [p for p in unequal if unequal[p] == next_best])
        empty = [values[a, n - a] for a in range(1, n)]
        print("no singletons between endpoints", len(empty), "pairs, maximum", max(empty))
    return values


def paper_fields():
    with gzip.open(ARTICLE, "rt") as stream:
        ((name, source),) = json.load(stream)
    title = re.search(r"^\\title\{([^}]+)\}", source, re.M)[1]
    authors = re.search(r"^\\author\{([^}]+)\}", source, re.M)[1].split(" and ")
    counter_envs = set(re.findall(r"\\newtheorem\{(\w+)\}\[conj\]", source))
    check(r"\newtheorem{conj}{Conjecture}[section]" in source, "section counter declaration")
    counter_envs.add("conj")
    section = item = 0
    labels = {}
    for number, line in enumerate(source.splitlines(), 1):
        line = line.partition("%")[0]
        if re.search(r"\\section\{", line):
            section += 1
            item = 0
        if any(env in counter_envs for env in re.findall(r"\\begin\{(\w+)\}", line)):
            item += 1
        for label in re.findall(r"\\label\{([^}]+)\}", line):
            if label in ("conj:maxlayered", "prop:countlayered"):
                labels[label] = (f"{section}.{item}", number)
    check(labels == {"conj:maxlayered": ("3.14", 753), "prop:countlayered": ("3.15", 760)},
          "source numbering or label")
    print("TeX member", name, "label counters and lines", labels)
    return {"paper": "arXiv:" + ARTICLE.name.split(".tex.")[0],
            "authors": authors, "title": title, "conjecture": labels["conj:maxlayered"][0],
            "conjecture_label": "conj:maxlayered"}


def audit_record(record, paper, values):
    # The search-history note is reviewed against the producer report below.
    check("minimality_note" in record, "missing minimality_note")
    w = tuple(record["permutation"])
    board = grid(w)
    n = len(board)
    best = max(count for (a, b), count in values.items() if a == b)
    winners = [a for (a, b), count in values.items() if a == b and count == best]
    check(len(winners) == 1, "baseline not unique")
    m, = winners
    count = matching_permanent(incidence(board))
    check(count > best, f"strict inequality fails: {count} <= {best}")
    shape = recover_shape(w)
    expected = {**paper, "n": n, "permutation": list(layered(shape)),
                "layered_shape": list(shape), "rook_placements": count,
                "best_m_1_m_shape": list(endpoint_shape(n, m, m)), "best_m_1_m_m": m,
                "best_m_1_m_rook_placements": best, "excess_over_best_m_1_m": count - best}
    check(record.keys() == expected.keys() | {"minimality_note"}, "witness field set")
    for key, value in expected.items():
        # JSON encoding also distinguishes booleans from integers.
        check(json.dumps(record[key]) == json.dumps(value), f"field mismatch: {key}")
    return expected


def audit_note(note):
    report = (INPUT.joinpath("REPORT.md")).read_text()
    table = dict((int(n), int(thousands) * 1000) for n, thousands in re.findall(
        r"^\| (15|16) \|[^\n]*?, (\d+)k SA \|$", report, re.M))
    check(set(table) == {15, 16} and ">300,000 SA/2-opt" in note, "search history text changed")
    claimed = list(map(int, re.search(r"r\(10\.\.14\) = ([\d, ]+)\)", note)[1].split(", ")))
    attained = [max(proposition(n, m, m) for m in range(1, n // 2 + 1))
                for n in range(10, 15)]
    check(claimed == attained, "attained values in minimality_note")
    print("minimality_note: attained family values 10..14", attained,
          "search history: note >300000, report SA by order", table,
          "(historical evaluations unavailable)")


def negatives(record, paper, values):
    w = list(record["permutation"])
    broken = dict(record, permutation=[w[1], *w[1:]])
    swap = w.copy()
    swap[0], swap[1] = swap[1], swap[0]
    best_shape = record["best_m_1_m_shape"]
    cases = [
        ("duplicate entry", broken, "invalid permutation"),
        ("swap first two entries", dict(record, permutation=swap), "strict inequality fails"),
        ("witness count +1", dict(record, rook_placements=record["rook_placements"] + 1),
         "field mismatch: rook_placements"),
        ("family maximum +1", dict(record, best_m_1_m_rook_placements=
                                   record["best_m_1_m_rook_placements"] + 1),
         "field mismatch: best_m_1_m_rook_placements"),
        ("best symmetric grid presented as strict win",
         dict(record, permutation=list(layered(best_shape)), layered_shape=best_shape,
              rook_placements=record["best_m_1_m_rook_placements"], excess_over_best_m_1_m=0),
         "strict inequality fails"),
    ]
    for label, mutated, reason in cases:
        try:
            audit_record(mutated, paper, values)
        except ValueError as error:
            check(str(error).startswith(reason), f"wrong rejection of {label}: {error}")
            print("REJECT", label, str(error))
        else:
            raise ValueError(f"accepted negative control: {label}")


def half_grid_counts(outer, inner):
    """Open east and south words on one side of a palindromic layered grid."""
    counts = [0] * (outer + inner)
    for h in range(1, outer + 1):
        for a in range(1, min(inner, h) + 1):
            ways = (stirling(outer, h) * stirling(inner, a)
                    * (factorial(h) // factorial(h - a)) ** 2)
            for b in range(1, inner + 1):
                counts[h - a + b] += ways * stirling(inner, b)
    return counts


def join_halves(counts, singletons):
    return sum((v * factorial(h) * h ** singletons) ** 2 for h, v in enumerate(counts))


def certificate():
    paper = paper_fields()
    values = family(17, asymmetric=True)
    check(values[1, 1] == direct(tuple(range(1, 18))) == 1, "empty endpoint interpretation")
    higher = family(18, asymmetric=False)
    record = json.loads((INPUT.joinpath("witness.json")).read_text())
    w = tuple(record["permutation"])
    check(w == layered((5, 3, 1, 3, 5)), "specified order-17 witness")
    count = dual_count(w)
    check(count == 104476798194769 and max(values.values()) == 103460138813701
          and count - max(values.values()) == 1016659381068, "order-17 claim")
    rows = incidence(grid(w))
    print("n 17", len(rows), "across and down words, intersections", sum(r.bit_count() for r in rows),
          "matching = Ryser =", count, "excess", count - max(values.values()))
    fields = audit_record(record, paper, values)
    print("verified certificate fields", len(fields), list(fields))
    audit_note(record["minimality_note"])
    higher_count = dual_count(layered((5, 3, 1, 1, 3, 5)))
    check(higher_count == 2949333362474113 and max(higher.values()) == 2445624351454501,
          "order-18 spot check")
    print("n 18 matching = Ryser =", higher_count, "excess", higher_count - max(higher.values()))
    half = half_grid_counts(5, 3)
    check(join_halves(half, 1) == count and join_halves(half, 2) == higher_count,
          "palindromic half-grid calculation")
    print("half-grid coefficients for blocks (5,3), by open-word count 1..7", half[1:])
    print("n 17 square roots of summands", [v * factorial(h) * h
                                            for h, v in enumerate(half) if h])
    for order, inside, t, reported, reported_best in (
            (19, 3, 3, 88247151321075649, 61054032594828497),
            (20, 4, 2, 2955493257611103149, 1967312926737499985)):
        score = join_halves(half_grid_counts(5, inside), t)
        baseline = max(proposition(order, m, m) for m in range(1, order // 2 + 1))
        check((score, baseline) == (reported, reported_best), f"order-{order} table check")
        print("n", order, "palindromic count", score, "symmetric maximum", baseline)
    symmetric_w = layered(endpoint_shape(17, 5, 5))
    fixed = [[i for i, v in enumerate(u, 1) if i == v] for u in (symmetric_w, w)]
    print("diagonal black squares baseline, witness", fixed)
    check(dual_count(tuple(range(17, 0, -1))) == 1, "single decreasing block edge case")
    w10 = layered(endpoint_shape(10, 4, 4))
    reflected = tuple(11 - v for v in w10)
    value = dual_count(reflected)
    check(value == direct(w10) == 255569, "reflected order-10 maximizer")
    check(reflected[0] > 1 and reflected[0] < reflected[1], "reflected non-layered witness")
    print("non-layered order-10 column reflection", reflected, "count", value,
          "producer table's non-family entry", 226409)
    negatives(record, paper, values)


def orbit(w):
    n = len(w)
    inverse = [0] * n
    for i, value in enumerate(w, 1):
        inverse[value - 1] = i
    images = set()
    for transform in (w, tuple(inverse)):
        complement = tuple(n + 1 - v for v in transform)
        images.update((transform, transform[::-1], complement, complement[::-1]))
    return images


def small_census(n):
    """Square symmetries only. No score-based pruning."""
    largest = -1
    attaining = covered = representatives = 0
    started = monotonic_ns()
    for first in range(1, (n + 1) // 2 + 1):
        for rest in permutations(i for i in range(1, n + 1) if i != first):
            # The least representative cannot have a smaller first entry under
            # either a horizontal reflection or a half-turn.
            if min(rest[-1], n + 1 - rest[-1]) < first:
                continue
            w = (first, *rest)
            images = orbit(w)
            if w != min(images):
                continue
            score = direct(w)
            covered += len(images)
            representatives += 1
            if score > largest:
                largest, attaining = score, 0
            if score == largest:
                attaining += len(images)
        print("census", n, "through initial value", first, "covered", covered,
              "elapsed seconds", (monotonic_ns() - started) // 10**9, flush=True)
    check(covered == factorial(n), "symmetry orbit weights fail to cover S_n")
    baseline = max(proposition(n, m, m) for m in range(1, n // 2 + 1))
    check(largest == baseline, f"census contradiction at n={n}: {largest} vs {baseline}")
    print("census", n, "permutations", covered, "orbits", representatives,
          "maximum", largest, "maximizers", attaining, flush=True)


def layered_census(n):
    largest = -1
    winners = []
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i for i in range(1, n) if mask & (1 << (i - 1))] + [n]
        shape = tuple(b - a for a, b in zip(cuts, cuts[1:]))
        score = direct(layered(shape))
        if score > largest:
            largest, winners = score, []
        if score == largest:
            winners.append(shape)
    baseline = max(proposition(n, m, m) for m in range(1, n // 2 + 1))
    check(largest == baseline, f"layered census contradiction n={n}: {largest} vs {baseline}")
    print("layered census", n, "compositions", mask + 1, "maximum", largest,
          "winning shapes", winners, flush=True)


def middle_census(n, empty_endpoint=False):
    """Count bounded middle permutations with positive endpoints or one empty endpoint."""
    largest = -1
    covered = representatives = 0
    for k in range(9):
        previous = covered
        sizes = (0,) if empty_endpoint else range(1, (n - k) // 2 + 1)
        for a in sizes:
            b = n - k - a
            first, last = tuple(range(a, 0, -1)), tuple(range(n, n - b, -1))
            for middle in permutations(range(1, k + 1)):
                inverse = [0] * k
                for i, value in enumerate(middle, 1):
                    inverse[value - 1] = i
                same_ends = {middle, tuple(inverse)}
                if a == b:
                    same_ends.update(tuple(k + 1 - v for v in reversed(u))
                                     for u in tuple(same_ends))
                if middle != min(same_ends):
                    continue
                w = first + tuple(a + v for v in middle) + last
                largest = max(largest, direct(w))
                representatives += 1
                # A half-turn exchanges endpoints a,b when a < b.
                covered += len(same_ends) * (1 if a == b else 2)
        splits = 2 if empty_endpoint else n - k - 1
        check(covered - previous == splits * factorial(k), "central orbit coverage")
        print("middle census", n, "k", k, "covered", covered - previous,
              "running maximum", largest, flush=True)
    baseline = max(proposition(n, m, m) for m in range(1, n // 2 + 1))
    check(largest <= baseline if empty_endpoint else largest == baseline,
          f"middle family contradiction n={n}: {largest} vs {baseline}")
    print("middle census", n, "empty endpoint", empty_endpoint, "total", covered, "representatives", representatives,
          "maximum", largest, flush=True)


def advance_half(states, black, full, first_row):
    """Scan inward from one edge. A set bit marks an already filled vertical word."""
    west = black - 1
    east = full & ~(west | black)
    out = {}
    for mask, ways in states.items():
        if not first_row and not mask & black:
            continue
        base = mask & ~black
        left = west & ~mask
        right = east & ~mask
        # A sentinel outside the board models the one choice in an absent word.
        if west == 0:
            left = full + 1
        if east == 0:
            right = full + 1
        while left:
            x = left & -left
            left -= x
            partial = base | (x & full)
            choices = right
            while choices:
                y = choices & -choices
                choices -= y
                key = partial | (y & full)
                out[key] = out.get(key, 0) + ways
    return out


def fixed_cut_count(w):
    """Count a fixed board from its black columns, independently of word labels."""
    if len(w) == 1:
        return 1  # The all-black board has no words that could cross a cut.
    full = (1 << len(w)) - 1
    split = len(w) // 2

    def scan(sequence):
        states = {0: 1}
        for i, column in enumerate(sequence):
            states = advance_half(states, 1 << (column - 1), full, i == 0)
        return states

    top = scan(w[:split])
    bottom = scan(reversed(w[split:]))
    return sum(value * bottom.get(full ^ mask, 0) for mask, value in top.items())


def half_vectors(columns, full, flip):
    def build(remaining, states):
        if not remaining:
            if flip:
                return [{full ^ m: v for m, v in states.items()}]
            return [states]
        vectors = []
        for i, bit in enumerate(remaining):
            next_states = advance_half(states, bit, full, remaining == columns)
            vectors.extend(build(remaining[:i] + remaining[i + 1:], next_states))
        return vectors

    return build(columns, {0: 1})


def envelope(vectors):
    upper = {}
    for vector in vectors:
        for i, value in vector.items():
            if value > upper.get(i, 0):
                upper[i] = value
    return upper


def dot(left, right):
    return sum(value * right.get(i, 0) for i, value in left.items())


def halves_census(n):
    """Exhaustive even-order comparison using exact horizontal cuts."""
    full = (1 << n) - 1
    k = n // 2
    attained = max(direct(layered(endpoint_shape(n, m, m))) for m in range(1, k + 1))
    boundary_sets = groups = exact_pairs = 0
    largest = attained
    for a in combinations(range(n), k):
        b = tuple(j for j in range(n) if j not in a)
        images = {a, b, tuple(n - 1 - j for j in reversed(a)),
                  tuple(n - 1 - j for j in reversed(b))}
        if a != min(images):
            continue
        left = half_vectors(tuple(1 << j for j in a), full, False)
        right = half_vectors(tuple(1 << j for j in b), full, True)
        check(len(left) == len(right) == factorial(k), "half-order coverage")
        if n == 8:
            # Compare the unbounded dot product to a full-board count before
            # using any envelope for the larger census.
            for p, x in zip(permutations(a), left):
                for q, y in zip(permutations(b), right):
                    w = tuple(j + 1 for j in p + q[::-1])
                    check(dot(x, y) == direct(w), f"horizontal-cut control {w}")
        left_upper, right_upper = envelope(left), envelope(right)
        left = [v for v in left if dot(v, right_upper) > largest]
        if left:
            right = [v for v in right if dot(v, left_upper) > largest]
            for x in left:
                for y in right:
                    exact_pairs += 1
                    largest = max(largest, dot(x, y))
        boundary_sets += len(images)
        groups += 1
        if groups % 50 == 0:
            print("horizontal cuts", n, "classes", groups, "top sets covered",
                  boundary_sets, "largest", largest, flush=True)
    covered = boundary_sets * factorial(k) ** 2
    check(covered == factorial(n), "horizontal-cut coverage")
    check(largest == attained, f"horizontal-cut counterexample {largest} > {attained}")
    print("horizontal cuts", n, "permutations", covered, "top sets", boundary_sets,
          "classes", groups, "unpruned pairs evaluated", exact_pairs, "maximum", largest, flush=True)


def bounded_census(n):
    """Refine the same cut bound by fixing the ordered rows nearest the cut."""
    full = (1 << n) - 1
    k = n // 2
    attained = max(direct(layered(endpoint_shape(n, m, m))) for m in range(1, k + 1))
    # Start one below the construction, so at least one exact leaf must recover it.
    largest = attained - 1
    exact_leaves = groups = covered = 0

    def bits(mask):
        while mask:
            bit = mask & -mask
            yield bit
            mask -= bit

    @lru_cache(maxsize=384)
    def upper(unknown):
        if unknown == 0:
            return {0: 1}
        result = {}
        for bit in bits(unknown):
            previous = unknown ^ bit
            child = advance_half(upper(previous), bit, full, previous == 0)
            for mask, value in child.items():
                if value > result.get(mask, 0):
                    result[mask] = value
        return result

    def cut_vector(unknown, tail):
        vector = upper(unknown)
        for i, bit in enumerate(tail):
            vector = advance_half(vector, bit, full, unknown == 0 and i == 0)
        return vector

    def visit(a, a_tail, x, b, b_tail, y):
        nonlocal largest, exact_leaves
        ac, bc = a.bit_count(), b.bit_count()
        bound = sum(value * y.get(full ^ mask, 0) for mask, value in x.items())
        if bound <= largest:
            return factorial(ac) * factorial(bc)
        if ac <= 1 and bc <= 1:
            # Both row orders are determined. Check the exact leaf from its grid.
            top = tuple(bits(a)) + a_tail
            bottom = tuple(bits(b)) + b_tail
            w = tuple(bit.bit_length() for bit in top + bottom[::-1])
            check(direct(w) == bound, "fixed horizontal-cut leaf")
            largest = bound
            exact_leaves += 1
            return 1
        if ac < bc:
            return visit(b, b_tail, y, a, a_tail, x)
        total = 0
        for bit in bits(a):
            rest = a ^ bit
            tail = (bit,) + a_tail
            total += visit(rest, tail, cut_vector(rest, tail), b, b_tail, y)
        return total

    for cols in combinations(range(n), k):
        a = sum(1 << j for j in cols)
        b = full ^ a
        reflected = sum(1 << (n - 1 - j) for j in cols)
        images = {a, reflected}
        if n == 2 * k:
            images.update((b, full ^ reflected))
        if a != min(images):
            continue
        total = visit(a, (), upper(a), b, (), upper(b))
        check(total == factorial(k) * factorial(n - k), "row-order partitions at cut")
        covered += len(images) * total
        groups += 1
        if groups % 100 == 0:
            print("refined cut", n, "classes", groups, "covered", covered,
                  "largest", largest, flush=True)
    check(covered == factorial(n) and exact_leaves and largest == attained,
          f"refined census n={n}: covered={covered}, largest={largest}, construction={attained}")
    print("refined cut", n, "permutations", covered, "classes", groups,
          "improving exact leaves", exact_leaves, "maximum", largest, flush=True)
    upper.cache_clear()


if __name__ == "__main__":
    seconds = 45 * 60
    if "ROOK_STOP_EPOCH" in os.environ:
        seconds = min(seconds, int(os.environ["ROOK_STOP_EPOCH"]) - time_ns() // 10**9)
        check(seconds > 0, "job deadline passed")
    signal.alarm(seconds)
    if len(sys.argv) == 1:
        controls()
        certificate()
    elif sys.argv[1] == "--census" and len(sys.argv) > 2:
        for order in map(int, sys.argv[2:]):
            check(8 <= order <= 11, "small census supports n=8..11")
            small_census(order)
    elif sys.argv[1] == "--layered" and len(sys.argv) > 2:
        for order in map(int, sys.argv[2:]):
            check(order in (15, 16), "layered census supports n=15,16")
            layered_census(order)
    elif sys.argv[1] == "--bounded" and len(sys.argv) > 2:
        for order in map(int, sys.argv[2:]):
            check(order in (8, 10, 12, 13, 14), "refined census supports n=8,10,12..14")
            bounded_census(order)
    elif sys.argv[1] == "--halves" and len(sys.argv) > 2:
        for order in map(int, sys.argv[2:]):
            check(order in (8, 10, 12), "even census supports n=8,10,12")
            halves_census(order)
    elif sys.argv[1] in ("--middle", "--empty-end") and len(sys.argv) > 2:
        for order in map(int, sys.argv[2:]):
            check(order in (15, 16), "middle census supports n=15,16")
            middle_census(order, empty_endpoint=sys.argv[1] == "--empty-end")
    else:
        raise SystemExit("usage: referee_verify.py [--census 9 10 11 | --layered 15 16 | --middle 15 16 | --empty-end 15 16 | --halves 8 10 12 | --bounded 8 10 12 13 14]")
    print("PASS: requested checks complete. Peak RSS (macOS bytes)",
          resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
