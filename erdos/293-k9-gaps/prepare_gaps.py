"""Build the ordered target list from the two exact release checker runs."""
import re
from pathlib import Path

from geometry import TARGET, factorization

END = 20_000_000
RECORD = re.compile(r"missing m=(\d+) seen_as_term=(\d+)")


def read_check(path):
    lines = Path(path).read_text().splitlines()
    omissions = {}
    for line in lines[:-1]:
        match = RECORD.fullmatch(line)
        assert match, (path, line)
        m, seen_as_term = map(int, match.groups())
        assert m not in omissions
        omissions[m] = seen_as_term
    totals = {k: int(v) for k, v in (term.split("=") for term in lines[-1].split())}
    assert not any(totals[k] for k in ("bad", "duplicate_labels", "target_found", "input_error"))
    assert totals["missing"] == len(omissions)
    assert totals["last"] - totals["first"] + 1 == totals["covered"] + len(omissions)
    assert totals["valid"] == totals["covered"] + totals["outside"]
    return omissions, totals


def main():
    gaps, scope = read_check("logs/certificate-check.log")
    full, release = read_check("logs/certificate-check-full-range.log")
    assert (scope["first"], scope["last"]) == (TARGET + 1, END)
    assert (release["first"], release["last"]) == (10_000_001, END)
    assert full == {TARGET: 0, **gaps}
    assert not any(gaps.values()) and len(gaps) == len(full) - 1
    assert list(gaps) == sorted(gaps)
    first = min(gaps)
    nearby = []
    for direction in (-1, 1):
        candidates = range(first + direction, TARGET if direction == -1 else END + 1, direction)
        side = []
        for m in candidates:
            if m not in full and factorization(m) != [(m, 1)]:
                side.append(m)
                if len(side) == 3:
                    break
        assert len(side) == 3
        nearby.extend(side)
    with Path("gaps.tsv").open("x") as output:
        print("m\tfactorization\tverdict\tcertificate_or_shard_summary", file=output)
        for m in gaps:
            factors = "*".join(str(p) if e == 1 else f"{p}^{e}" for p, e in factorization(m))
            print(f"{m}\t{factors}\tunsettled\tunprocessed", file=output)
    with Path("logs/nearby-control-targets.txt").open("x") as output:
        print(*sorted(nearby), sep="\n", file=output)
    print(f"Full release omissions {len(full)}. Above {TARGET} omissions {len(gaps)}. First gap {first}.")
    print("Nearby certified composite controls", *sorted(nearby))


if __name__ == "__main__":
    main()
