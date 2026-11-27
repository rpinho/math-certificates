import argparse

import run


CODES = ("0.512", "0.513")
SMALL_CONTEXT_TOTAL = 10
QUOTIENT_ORDER = 8
QUOTIENT_PERIOD = 6
PERIOD_START = 16


def joined(*positions):
    return tuple(sorted((h for position in positions for h in position), reverse=True))


def certify(code, timing):
    contexts = list(run.partition_range(SMALL_CONTEXT_TOTAL))
    limit = 2 * (PERIOD_START + QUOTIENT_PERIOD - 1) + SMALL_CONTEXT_TOTAL
    positions = list(run.partition_range(limit))
    indices = {position: i for i, position in enumerate(positions)}
    outcomes = run.compare_tables(code, "table", limit, len(positions), timing)

    def outcome(*positions):
        return outcomes[indices[joined(*positions)]]

    representatives = {}
    for left in contexts:
        signature = "".join(outcome(left, right) for right in contexts)
        representatives.setdefault(signature, left)
    if len(representatives) != QUOTIENT_ORDER:
        raise RuntimeError(f"{code}: expected {QUOTIENT_ORDER} distinguishable classes, "
                           f"found {len(representatives)}")
    compared = 0
    differences = []
    # Check the seam at 16 explicitly, so either convention for reporting
    # the first periodic index in Figure 4 gives the same conclusion.
    for context in representatives.values():
        original = outcome((PERIOD_START + QUOTIENT_PERIOD,), context)
        reduced = outcome((PERIOD_START,), context)
        compared += 1
        if original != reduced:
            differences.append((PERIOD_START + QUOTIENT_PERIOD, PERIOD_START, context, original, reduced))
    for first in range(PERIOD_START, PERIOD_START + QUOTIENT_PERIOD):
        for second in range(9, PERIOD_START + QUOTIENT_PERIOD):
            for context in representatives.values():
                original = outcome((first, second), context)
                reduced = outcome((first, second - QUOTIENT_PERIOD), context)
                compared += 1
                if original != reduced:
                    differences.append((first, second, context, original, reduced))
    print(f"{code}\t{len(contexts)}\t{compared}\t{len(differences)}\t"
          + ",".join(run.show(rep) for rep in representatives.values()), flush=True)
    if differences:
        raise RuntimeError(f"{code}: exceptional quotient comparison failed at {differences[0]}")
    return compared


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deadline", type=float)
    parser.add_argument("--timing", action="store_true")
    args = parser.parse_args()
    run.DEADLINE = args.deadline
    print("game\tdistinguishing_contexts\tboundary_comparisons\tmismatches\trepresentatives", flush=True)
    rules = []
    for game in CODES:
        count = certify(game, args.timing)
        rules.append((game, "2608.13273v2 p.27 0.51˙2 via Plambeck–Siegel Fig. 4",
                      run.tuple_rule((16, 6, 3, 6)), "all finite heap positions", count, 0,
                      "proved using published quotient",
                      "624 boundary cases; 8 seam cases; eight distinguishable quotient classes"))
    run.write_rows("QUOTIENT_RULES.tsv", run.RULE_COLUMNS, rules)
