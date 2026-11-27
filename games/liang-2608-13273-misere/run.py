import argparse
import csv
from hashlib import sha256
from itertools import product
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


JOB = "math_misere_1127"
TOKEN_LIMIT = 48
DEADLINE = None


def execute(binary, code, mode, *arguments, timing=False):
    command = ["nice", "-n", "10", f"./{JOB}_{binary}", code, mode, *map(str, arguments)]
    if timing:
        command = ["/usr/bin/time", "-l", *command]
    timeout = None if DEADLINE is None else DEADLINE - time.time()
    if timeout is not None and timeout <= 0:
        raise RuntimeError("job deadline reached")
    with subprocess.Popen(command, stdout=subprocess.PIPE, start_new_session=True) as process:
        try:
            output, _ = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
            raise
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        return output


def partitions(remaining, maximum):
    if remaining == 0:
        yield ()
    else:
        for h in range(1, min(remaining, maximum) + 1):
            for tail in partitions(remaining - h, h):
                yield (h, *tail)


def partition_range(limit):
    for total in range(limit + 1):
        yield from partitions(total, total)


def four_heaps(maximum, slots):
    if slots == 0:
        yield ()
    else:
        for h in range(maximum + 1):
            for tail in four_heaps(h, slots - 1):
                yield (h, *tail)


def compare_tables(code, mode, limit, expected_count, timing=False):
    direct = execute("direct", code, mode, limit, timing=timing)
    checker = execute("checker", code, mode, limit, timing=timing)
    if len(direct) != expected_count or len(checker) != expected_count:
        raise RuntimeError(f"{code}: unexpected table length {len(direct)}, {len(checker)}")
    if direct != checker:
        difference = next(i for i, (a, b) in enumerate(zip(direct, checker)) if a != b)
        raise RuntimeError(f"{code}: solver disagreement at table index {difference}")
    if set(direct) - {ord("P"), ord("N")}:
        raise RuntimeError(f"{code}: invalid outcome byte")
    print(f"{code}\t{mode}\t{limit}\t{expected_count}\t{sha256(direct).hexdigest()}", file=sys.stderr)
    return direct.decode("ascii")


def reduce_position(position, params):
    p1, t1, p2, t2 = params
    if not position or position[0] < p1 + t1:
        return None
    if len(position) < 2 or position[1] < p2 + t2:
        changed = (position[0] - t1, *position[1:])
        branch = 1
    else:
        changed = (position[0] - t2, position[1] - t2, *position[2:])
        branch = 2
    if min(changed) < 0:
        raise RuntimeError(f"the printed rule leads to a negative heap at {position}")
    return branch, tuple(sorted((heap for heap in changed if heap > 0), reverse=True))


def show(position):
    return "(" + ",".join(map(str, position)) + ")"


def control():
    controls = (
        ("0.355", (20, 2, 1, 1), (22, 3, *([2] * 8)), (21, *([2] * 9)), 44, 18994, 4),
        ("0.716", (22, 2, 2, 1), (24, 3, 1), (23, 2, 1), 36, 890, 109),
        ("0.717", (22, 2, 2, 1), (24, 3, 1), (23, 2, 1), 36, 890, 109),
    )
    for code, params, p, n, bound, expected_cases, expected_bad in controls:
        positions = list(partition_range(bound))
        outcomes = dict(zip(positions, compare_tables(code, "table", bound, len(positions), timing=True)))
        query = execute("direct", code, "query", ",".join(map(str, p)), ",".join(map(str, n)))
        if (outcomes[p], outcomes[n], query, reduce_position(p, params)) != ("P", "N", b"PN", (2, n)):
            raise RuntimeError(f"{code}: public control failed")
        cases = bad = 0
        for position in positions:
            reduced = reduce_position(position, params)
            if reduced is not None:
                cases += 1
                bad += outcomes[position] != outcomes[reduced[1]]
        if (cases, bad) != (expected_cases, expected_bad):
            raise RuntimeError(f"{code}: public sweep expected {expected_cases}/{expected_bad}, got {cases}/{bad}")
        print(f"{code}\t{show(p)} P\t{show(n)} N\t{bound}\t{cases}\t{bad}", flush=True)


RULE_COLUMNS = (
    "game", "source", "printed_rule", "test_range", "comparisons", "disagreements",
    "verdict", "counts_or_detail",
)
WITNESS_COLUMNS = (
    "game", "source", "comparison", "p_position", "n_position",
    "original_or_mismatching_position", "detail",
)


def write_rows(name, header, rows):
    with Path(name).open("w", newline="") as output:
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def expanded_codes(label):
    digits = []
    for symbol in label:
        if symbol == ".":
            digits.append(".")
        elif symbol == "˙":
            digits.append((0, 1))
        elif symbol == "¨":
            digits.append((0, 2))
        elif symbol == "¯":
            digits.append((0, 1, 2, 3))
        elif digits and isinstance(digits[-1], tuple):
            digits[-1] = [str(int(symbol) + offset) for offset in digits[-1]]
        else:
            digits.append(symbol)
    return ("".join(code) for code in product(*digits))


def tuple_rule(params):
    p1, t1, p2, t2 = params
    return (
        f"(p1,t1,p2,t2)={params}; a1>={p1+t1}: "
        f"if a2<{p2+t2}, a1→a1−{t1}; otherwise (a1,a2)→(a1−{t2},a2−{t2})"
    )


def verdict(differences):
    return "refuted" if differences else "agrees on stated range"


def add_pair(witnesses, code, source, comparison, original, other, outcome, detail):
    first, second = original, other
    if outcome(original) == "N":
        first, second = second, first
    assert outcome(first) == "P" and outcome(second) == "N"
    witnesses.append((code, source, comparison, show(first), show(second), show(original), detail))


def template_test(rules, witnesses, code, source, rule, scope, positions, exact, predicted):
    correct = {}
    first_bad = {}
    first_exact = {}
    wrong = {"P": 0, "N": 0}
    count = 0
    for position in positions:
        expected = predicted(position)
        actual = exact(position)
        first_exact.setdefault(actual, position)
        count += 1
        if actual == expected:
            correct.setdefault(expected, position)
        else:
            wrong[expected] += 1
            first_bad.setdefault(expected, position)
    differences = sum(wrong.values())
    rules.append((code, source, rule, scope, count, differences, verdict(differences),
                  f"incorrect printed P: {wrong['P']}; incorrect printed N: {wrong['N']}"))
    for expected, position in first_bad.items():
        opposite = correct.get(expected, first_exact[expected])
        add_pair(witnesses, code, source, "outcome template", position, opposite, exact,
                 f"First listed heap position in the hypothesis check {show(position)} is printed {expected}; "
                 f"comparison {show(opposite)} is printed {predicted(opposite)}.")


def formula_734(position):
    if not position or position[0] <= 2:
        return "P" if position == (1,) * len(position) and len(position) % 2 else "N"
    total = sum(position)
    difference = 2 * position[0] - total
    odd = sum(h % 2 for h in position)
    base = total if difference <= 1 else difference
    return "P" if base % 2 == 0 and (base + odd) % 4 == 0 else "N"


def classical(code, position):
    if not position:
        return "N"
    lead = position[0]
    grundy = 0
    if code == "0.26":
        def t(h):
            if h <= 4:
                return int(h >= 3)
            return (h - 5) // 2

        if lead <= 10:
            w = int(lead >= 9)
        else:
            w = (lead - 7) // 2 if lead % 2 else (lead - 12) // 2
        for h in position:
            grundy ^= (h - 1) % 4
        outer = 2
    else:
        def t(h):
            return 1 if h == 2 else max(0, h - 3)

        w = 1 if lead == 5 else max(0, lead - 6)
        for h in position:
            grundy ^= 1 if h % 2 else 2
        outer = 3
    rest = sum(t(h) for h in position[1:])
    weight = rest + t(lead)
    previous_wins = (
        (weight == 0 and grundy == 1)
        or (weight > 0 and w <= rest and grundy == 0)
        or (weight > 0 and w >= rest + 2 and grundy == outer)
    )
    return "P" if previous_wins else "N"


def main_sweep(timing, limit=TOKEN_LIMIT, only_codes=None):
    positions = list(partition_range(limit))
    index = {position: i for i, position in enumerate(positions)}
    rules = []
    witnesses = []
    eligible_cache = {}
    with Path("TABLE.tsv").open() as source:
        table = list(csv.DictReader(source, delimiter="\t"))
    for row in table:
        label = row["printed_code"]
        codes = [code for code in expanded_codes(label) if only_codes is None or code in only_codes]
        if not codes:
            continue
        params = tuple(int(row[name]) for name in ("p1", "t1", "p2", "t2"))
        pre, period = (int(row["singleton_" + key]) for key in ("preperiod", "period"))
        letters = row["letters_from_heap_1"]

        def printed(position):
            h = position[0]
            return letters[h - 1 if h <= len(letters) else pre + (h - 1 - pre) % period]

        if params not in eligible_cache:
            eligible = []
            for i, position in enumerate(positions):
                reduced = reduce_position(position, params)
                if reduced:
                    eligible.append((i, index[reduced[1]], reduced[0]))
            eligible_cache[params] = eligible
        eligible = eligible_cache[params]
        for code in codes:
            outcomes = compare_tables(code, "table", limit, len(positions), timing=timing)

            def exact(position):
                return outcomes[index[position]]

            count = {1: 0, 2: 0}
            bad = {1: 0, 2: 0}
            first = {}
            source = f"2608.13273v2 p.27 {label}"
            for original, reduced, branch in eligible:
                count[branch] += 1
                if outcomes[original] != outcomes[reduced]:
                    bad[branch] += 1
                    first.setdefault(branch, (original, reduced))
            rules.append((code, source, tuple_rule(params), f"all eligible partitions, total≤{limit}",
                          sum(count.values()), sum(bad.values()), verdict(sum(bad.values())),
                          f"branch 1: {bad[1]}/{count[1]}; branch 2: {bad[2]}/{count[2]}"))
            for branch, (original, reduced) in first.items():
                add_pair(witnesses, code, source, f"Def. 3.4 branch {branch}",
                         positions[original], positions[reduced], exact,
                         f"Expected equality after one reduction. Original total {sum(positions[original])}.")
            if only_codes is not None:
                continue
            source = f"2608.13273v2 p.28 {label}"
            singleton = [(h,) for h in range(1, TOKEN_LIMIT + 1)]
            template_test(rules, witnesses, code, source,
                          f"size 1 starts {letters}; repeat with (preperiod,period)=({pre},{period})",
                          f"heap sizes 1–{TOKEN_LIMIT}", singleton, exact, printed)
            differences = [h for h in range(pre + 1, TOKEN_LIMIT - period + 1)
                           if exact((h,)) != exact((h + period,))]
            rules.append((code, source, f"o(h)=o(h+{period}) for h>{pre}",
                          f"lower heap sizes {pre+1}–{TOKEN_LIMIT-period}",
                          TOKEN_LIMIT - period - pre, len(differences), verdict(differences),
                          "period equality checked independently of the printed letters"))
            if differences:
                h = differences[0]
                add_pair(witnesses, code, source, "singleton period", (h,), (h + period,), exact,
                         f"Expected equality starting above preperiod {pre}.")
            if label == "0.73˙4":
                template_test(
                    rules, witnesses, code, "2608.13273v2 p.27 explicit P formula",
                    "max≤2: odd number of 1s, no other heaps; max>2: 2|B and 4|(B+Ω), "
                    "where B=Σ if Δ≤1, and B=Δ if Δ>1",
                    f"all partitions of total≤{TOKEN_LIMIT}", positions, exact, formula_734,
                )
            if code in ("0.260", "4.70"):
                base_code = {"0.260": "0.26", "4.70": "4.7"}[code]
                test_classical(rules, witnesses, base_code, positions, exact)

    return rules, witnesses


def test_classical(rules, witnesses, code, positions, exact):
    source, formula = {
        "0.26": ("0705.2404 Fact B.1 / Theorem B.2",
                 "t=0,g=1; or t>0,w≤t(rest),g=0; or t>0,w≥t(rest)+2,g=2"),
        "4.7": ("0705.2404 Fact B.4 / Theorem B.5",
                "t=0,g=1; or t>0,w≤t(rest),g=0; or t>0,w≥t(rest)+2,g=3"),
    }[code]
    template_test(rules, witnesses, code, source, formula,
                  f"all partitions of total≤{TOKEN_LIMIT}", positions, exact,
                  lambda position: classical(code, position))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("control", "sweep", "followup"))
    parser.add_argument("--deadline", type=float)
    parser.add_argument("--timing", action="store_true")
    args = parser.parse_args()
    DEADLINE = args.deadline
    if args.mode == "control":
        control()
    elif args.mode == "sweep":
        rules, witnesses = main_sweep(args.timing)
        write_rows("PRIMARY_RULES.tsv", RULE_COLUMNS, rules)
        write_rows("PRIMARY_WITNESSES.tsv", WITNESS_COLUMNS, witnesses)
    else:
        surviving_codes = {"0.512", "0.513", "0.552", "0.553", "0.734", "0.735"}
        rules, witnesses = main_sweep(args.timing, limit=56, only_codes=surviving_codes)
        write_rows("FOLLOWUP_RULES.tsv", RULE_COLUMNS, rules)
        write_rows("FOLLOWUP_WITNESSES.tsv", WITNESS_COLUMNS, witnesses)
