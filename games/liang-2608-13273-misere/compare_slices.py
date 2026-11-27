import argparse
from collections import defaultdict
from pathlib import Path

import run


GRID = 64
CONCRETE = {
    "0.3102": {(1, 2): (46, 12), (2, 3): (46, 12)},
    "0.3122": {
        (0, 0): (3, 3), (1, 0): (2, 2), (2, 0): (8, 8), (1, 1): (3, 3),
        (1, 2): (13, 13), (2, 2): (12, 3),
    },
    "0.3123": {
        (0, 0): (2, 2), (1, 0): (18, 12), (2, 0): (21, 15), (3, 0): (21, 21),
        (1, 1): (2, 2), (1, 2): (16, 13), (2, 2): (21, 14), (1, 3): (27, 21),
        (2, 3): (31, 21), (3, 3): (7, 7),
    },
}

KNOWN_RESIDUES = {
    (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (1, 6), (6, 1),
    (2, 4), (4, 2), (3, 5), (5, 3),
}


def canonical(*heaps):
    return tuple(sorted((h for h in heaps if h), reverse=True))


def all_xy(bound=GRID):
    return [(x, y) for x in range(bound + 1) for y in range(x + 1)]


def canonic_grid(exact, prefix):
    return {(x, y): exact(canonical(*prefix, x, y)) for x, y in all_xy()}


def concrete_rule(code, prefix, params, grid, exact, rules, witnesses):
    p1, t1, p2, t2 = params
    bad = {1: 0, 2: 0}
    count = {1: 0, 2: 0}
    first = {}
    source = "2611.29198v1 " + {
        "0.3102": "Remark 4.5",
        "0.3122": "Theorem 3.7 finite checks",
        "0.3123": "Theorem 3.8 finite checks or Remark 4.5",
    }[code]
    for (x, y), original in grid.items():
        if x < p1 + t1:
            continue
        if y < p2 + t2:
            comparison = (x - t1, y)
            branch = 1
        else:
            comparison = (x - t2, y - t2)
            branch = 2
        count[branch] += 1
        if original != grid[tuple(sorted(comparison, reverse=True))]:
            bad[branch] += 1
            first.setdefault(branch, ((x, y), comparison))
    total_bad = sum(bad.values())
    rules.append((code, source, f"fixed prefix {prefix}; {run.tuple_rule(params)} on variable heaps",
                  f"0≤y≤x≤{GRID}", sum(count.values()), total_bad, run.verdict(total_bad),
                  f"branch 1: {bad[1]}/{count[1]}; branch 2: {bad[2]}/{count[2]}"))
    for branch, (original, other) in first.items():
        run.add_pair(witnesses, code, source, f"Definition 4.2 branch {branch}",
                     canonical(*prefix, *original), canonical(*prefix, *other), exact,
                     f"Fixed prefix {prefix}, tuple {params}. Variable pair {original}→{other}.")


def fit_thresholds(grid, period):
    max_preperiod = GRID - 2 * period
    latest_axis = defaultdict(lambda: -1)
    latest_diagonal = defaultdict(lambda: -1)
    for (x, y), original in grid.items():
        if x < period:
            continue
        if original != grid[tuple(sorted((x - period, y), reverse=True))]:
            latest_axis[y] = max(latest_axis[y], x)
        if y >= period and original != grid[(x - period, y - period)]:
            latest_diagonal[y] = max(latest_diagonal[y], x)
    candidates = []
    for p2 in range(max_preperiod + 1):
        boundary = p2 + period
        last_bad = max(
            [latest_axis[y] for y in range(boundary)]
            + [latest_diagonal[y] for y in range(boundary, GRID + 1)]
        )
        p1 = max(0, last_bad + 1 - period)
        if p1 <= max_preperiod:
            candidates.append((p1, p2))
    return min(candidates, default=None)


def residue_rule(exact, rules, witnesses):
    source = "2611.29198v1 Conjecture 4.1"
    prefix = (2, 2)
    grid = canonic_grid(exact, prefix)
    outcomes_per_key = defaultdict(dict)
    for (x, y), outcome in grid.items():
        key = (x % 7, y % 7, x - y <= 4)
        outcomes_per_key[key].setdefault(outcome, (x, y))
    mixed = {key: lookup for key, lookup in outcomes_per_key.items() if len(lookup) != 1}
    rules.append(("0.3122", source, "o(2,2,x,y) depends only on (x mod 7,y mod 7,|x−y|≤4)",
                  f"0≤y≤x≤{GRID}; one check per residue key", len(outcomes_per_key), len(mixed),
                  run.verdict(len(mixed)), "count is of mixed keys; prior disproof is Zenodo 24568032"))
    published_p = canonical(14, 2, 2, 2)
    published_n = canonical(7, 2, 2, 2)
    assert exact(published_p) == "P" and exact(published_n) == "N"
    run.add_pair(witnesses, "0.3122", source, "published residue counterexample",
                 published_p, published_n, exact, "Both variable pairs have key (0,2,False). Zenodo 24568032.")
    for key, examples in mixed.items():
        run.add_pair(witnesses, "0.3122", source, "residue key",
                     canonical(*prefix, *examples["P"]), canonical(*prefix, *examples["N"]), exact,
                     f"Both have key {key}.")

    def proposed(x, y):
        residues = (x % 7, y % 7)
        close = abs(x - y) <= 4
        return "P" if (residues in KNOWN_RESIDUES or
                       (close and residues in {(0, 0), (4, 4)}) or
                       (not close and residues in {(0, 4), (4, 0)})) else "N"

    wrong = [(x, y) for x, y in grid if y >= 3 and grid[x, y] != proposed(x, y)]
    keys = {(x % 7, y % 7, abs(x - y) <= 4)
            for x in range(3, GRID + 1) for y in range(3, GRID + 1)}
    rules.append(("0.3122", "Zenodo 24568032 Thm 2", "98-entry threshold-3 residue formula",
                  f"3≤y≤x≤{GRID}", sum(y >= 3 for _, y in grid), len(wrong), run.verdict(len(wrong)),
                  f"{len(keys)} of 98 ordered keys represented"))
    if wrong:
        raise RuntimeError(f"published threshold-3 formula disagrees at {wrong[0]}")


def fold_test(code, period, exact, rules, witnesses):
    source = "2611.29198v1 Conjecture 4.4"
    checked = differences = 0
    first = None
    for a in range(0, 11):
        for b in range(0, 11):
            for x, y in all_xy():
                original = canonical(a, b, x, y)
                other = canonical(a + period, b, x, y)
                checked += 1
                if exact(original) != exact(other):
                    differences += 1
                    if first is None:
                        first = (original, other, (a, b, x, y))
    status = "confirmed failure of fixed-heap folding" if differences else "no counterexample on stated range"
    rules.append((code, source, f"some o(a+{period},b,x,y) differs from o(a,b,x,y)",
                  f"0≤a,b≤10; 0≤y≤x≤{GRID}", checked, differences, status,
                  "disagreements are counterexamples to folding"))
    if first:
        original, other, values = first
        run.add_pair(witnesses, code, source, "fixed heap folding", original, other, exact,
                     f"Expected inequality for some prefixes. Here (a,b,x,y)={values}.")


def known_theorems(code, exact, rules, witnesses):
    if code == "0.3102":
        pairs = [canonical(x, y) for x, y in all_xy() if y >= 3]
        run.template_test(rules, witnesses, code, "2611.29198v1 Theorem 3.1",
                          "o(x,y)=P iff |x−y| mod 5 is 0 or 3",
                          f"3≤y≤x≤{GRID}", pairs, exact,
                          lambda heaps: "P" if (heaps[0] - heaps[1]) % 5 in (0, 3) else "N")
    elif code in ("0.3122", "0.3123"):
        a = int(code[-1])
        theorem = "3.7" if a == 2 else "3.8"
        labels = {canonical(a, a, h, h): "P" for h in range(GRID + 1)}
        labels.update({canonical(a, a, h + 1, h): "N" for h in range(GRID)})
        run.template_test(rules, witnesses, code, f"2611.29198v1 Theorem {theorem}",
                          f"o({a},{a},h,h)=P and o({a},{a},h+1,h)=N",
                          f"max variable heap≤{GRID}", labels, exact, labels.__getitem__)


def main(timing):
    positions = list(run.four_heaps(GRID, 4))
    index = {heaps: i for i, heaps in enumerate(positions)}
    rules, witnesses = [], []
    for code, period in (("0.3102", 5), ("0.3122", 7), ("0.3123", 7), ("0.3312", 3)):
        raw = run.compare_tables(code, "grid", GRID, len(positions), timing)

        def exact(position):
            return raw[index[(position + (0,) * 4)[:4]]]

        for prefix, (p1, p2) in CONCRETE.get(code, {}).items():
            params = (p1, period, p2, period)
            concrete_rule(code, prefix, params, canonic_grid(exact, prefix), exact, rules, witnesses)
        known_theorems(code, exact, rules, witnesses)
        if code == "0.3122":
            residue_rule(exact, rules, witnesses)
        prefixes = [(0, 0), *((a, 0) for a in range(1, 11)), *((a, a) for a in range(1, 11))]
        for prefix in prefixes:
            grid = canonic_grid(exact, prefix)
            fitted = fit_thresholds(grid, period)
            source = "2611.29198v1 Conjecture 4.3"
            if fitted is None:
                verdict = "no fit with stated threshold cap"
                detail = "existential thresholds remain open"
                count = len(grid)
            else:
                p1, p2 = fitted
                count = sum(x >= p1 + period for x, _ in grid)
                verdict = "finite fit"
                detail = f"first fitting (p1,p2)={fitted}; only fit to this range"
            rules.append((code, source, f"fixed prefix {prefix}; both periods={period}; thresholds unspecified",
                          f"0≤y≤x≤{GRID}; 0≤p1,p2≤{GRID-2*period}", count,
                          0 if fitted else "", verdict, detail))
        fold_test(code, period, exact, rules, witnesses)
    run.write_rows("SLICE_RULES.tsv", run.RULE_COLUMNS, rules)
    run.write_rows("SLICE_WITNESSES.tsv", run.WITNESS_COLUMNS, witnesses)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deadline", type=float)
    parser.add_argument("--timing", action="store_true")
    args = parser.parse_args()
    run.DEADLINE = args.deadline
    main(args.timing)
