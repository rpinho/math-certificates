import argparse
from collections import defaultdict
import csv
from functools import cache
from math import comb
from pathlib import Path
import subprocess
import time


def read_position(text):
    if not (text.startswith("(") and text.endswith(")")):
        raise ValueError(f"invalid position: {text}")
    sizes = tuple(int(size) for size in text[1:-1].split(",") if size)
    if any(size <= 0 for size in sizes) or sizes != tuple(sorted(sizes, reverse=True)):
        raise ValueError(f"noncanonical position: {text}")
    return sizes


@cache
def number_of_partitions(total, max_part):
    if total == 0:
        return 1
    if max_part == 0:
        return 0
    if max_part > total:
        return number_of_partitions(total, total)
    return (number_of_partitions(total, max_part - 1)
            + number_of_partitions(total - max_part, max_part))


def table_rank(heaps):
    total = sum(heaps)
    index = sum(number_of_partitions(smaller, smaller) for smaller in range(total))
    for size in heaps:
        index += sum(number_of_partitions(total - smaller, smaller) for smaller in range(1, size))
        total -= size
    return index


def grid_rank(heaps):
    return sum(comb(heap + slots - 1, slots) for slots, heap in zip(range(4, 0, -1), heaps))


def main(paths, deadline):
    pairs = defaultdict(list)
    for path in paths:
        with path.open() as source:
            for row in csv.DictReader(source, delimiter="\t"):
                p = read_position(row["p_position"])
                n = read_position(row["n_position"])
                pairs[row["game"]].append((p, n, row["source"]))
    compared = 0
    for game, witnesses in pairs.items():
        heaps = [position for p, n, _ in witnesses for position in (p, n)]
        limit = max(map(sum, heaps))
        mode, rank = "table", table_rank
        if limit > 63:
            if any(len(position) > 4 for position in heaps):
                raise ValueError(f"no table for witnesses in {game}")
            mode, rank = "grid", grid_rank
            limit = max(h for position in heaps for h in position)
        timeout = None if deadline is None else deadline - time.time()
        if timeout is not None and timeout <= 0:
            raise RuntimeError("job deadline reached")
        table = subprocess.run(
            ["nice", "-n", "10", "./math_misere_1127_checker", game, mode, str(limit)],
            check=True, stdout=subprocess.PIPE, timeout=timeout,
        ).stdout
        for p, n, source in witnesses:
            actual_p, actual_n = table[rank(p)], table[rank(n)]
            if (actual_p, actual_n) != (ord("P"), ord("N")):
                raise ValueError(f"{game} {source}: {p} {chr(actual_p)}, {n} {chr(actual_n)}")
        compared += len(witnesses)
        print(f"{game}\t{len(witnesses)} witness pairs pass ({mode} {limit})")
    print(f"{compared} witness pairs pass for {len(pairs)} games")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=Path, nargs="+")
    parser.add_argument("--deadline", type=float)
    args = parser.parse_args()
    main(args.paths, args.deadline)
