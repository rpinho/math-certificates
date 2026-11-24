"""Drive exact comparison controls without keeping millions of result rows."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import threading
import time

from geometry import FULL, factorization, shards

DEADLINE = int(Path("deadline.epoch").read_text())
SOLVER = "build/solver"
EXPECTED = {
    (6, 79): 2, (6, 102): 11, (6, 103): 0,
    (7, 732): 116, (7, 733): 0,
    (8, 27538): 474, (8, 27539): 0, (8, 27551): 4,
    (8, 32411): 0, (8, 53294): 0,
}
DEEP = (
    (13813799, (2, 3, 7, 47, 395, 826378), (258915405010, 5623917655365016250010)),
    (13336331, (2, 3, 7, 44, 925, 913227), (31781064967036, 55354798808706711571214075)),
)


def budget():
    left = DEADLINE - time.time()
    if left <= 0:
        raise TimeoutError("job deadline reached")
    return left


def task(m, k, prefix=(), bounds=FULL):
    return " ".join(map(str, (m, k, *prefix, *bounds))) + "\n"


def result(line):
    tag, *fields = line.split()
    values = tuple(map(int, fields))
    assert tag == "R" and len(values) == 17 and values[4] == 0, line
    return values


def solve(tasks, mutant=0):
    answers = []
    proc = subprocess.run([SOLVER, "1", str(mutant)], input="".join(tasks),
                          capture_output=True, text=True, timeout=budget(), check=True)
    assert not proc.stderr, proc.stderr
    solutions = []
    for line in proc.stdout.splitlines():
        if line.startswith("S "):
            solutions.append(tuple(map(int, line.split()[1:])))
        else:
            answers.append((result(line), solutions))
            solutions = []
    assert not solutions and len(answers) == len(tasks)
    return answers


def exact(rep, k, m):
    assert len(rep) == k and len(set(rep)) == k and min(rep) >= 2
    assert not m or m in rep
    assert sum((Fraction(1, n) for n in rep), Fraction()) == 1


def full_histograms():
    results = {}
    for k, target in zip(range(3, 8), (1, 6, 72, 2320, 245765)):
        hist = Counter()
        count = 0
        with open(f"build/enumerator-{k}.solutions") as rows:
            for row in rows:
                terms = tuple(map(int, row.split()))
                exact(terms, k, 0)
                hist.update(terms)
                count += 1
        assert count == target and sum(hist.values()) == k*target
        print(f"enumerator k={k} count={count} distinct_m={len(hist)} max_m={max(hist)} "
              f"incidences={sum(hist.values())}", flush=True)
        results[k] = hist
    return results


def scan(k, labels, expected):
    with subprocess.Popen([SOLVER, "0", "0"], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, text=True) as child:
        writer_errors = []

        def feed():
            try:
                with child.stdin:
                    for m in labels:
                        child.stdin.write(task(m, k))
            except Exception as exc:
                writer_errors.append(exc)

        writer = threading.Thread(target=feed, daemon=True)
        timer = threading.Timer(budget(), child.kill)
        timer.daemon = True
        timer.start()
        writer.start()
        actual_sum = 0
        try:
            for m in labels:
                line = child.stdout.readline()
                assert line, f"solver stream stopped at k={k} m={m}"
                fields = result(line)
                assert fields[:2] == (m, k) and fields[2] == expected[m], (m, fields, expected[m])
                actual_sum += fields[2]
            assert child.stdout.readline() == ""
            assert child.wait() == 0 and not writer_errors
        finally:
            if child.poll() is None:
                child.kill()
            timer.cancel()
            writer.join()
    return actual_sum


def canonical(path, solutions):
    ordered = sorted(solutions)
    assert len(set(ordered)) == len(ordered)
    content = "".join(" ".join(map(str, row)) + "\n" for row in ordered).encode()
    Path(path).write_bytes(content)
    return sha256(content).hexdigest()


def one(k, m, prefix=(), mutant=0):
    fields, reps = solve([task(m, k, prefix)], mutant)[0]
    assert fields[:2] == (m, k) and fields[2] == len(reps)
    if mutant == 0:
        for rep in reps:
            exact(rep, k, m)
    return fields, reps


def controls():
    print("fixed_control k m expected obtained skipped")
    answers = solve([task(m, k) for k, m in EXPECTED])
    for ((k, m), expected), (fields, reps) in zip(EXPECTED.items(), answers, strict=True):
        print(f"fixed_control {k} {m} {expected} {fields[2]} {fields[4]}", flush=True)
        assert fields[:2] == (m, k) and fields[2] == len(reps) == expected
        for rep in reps:
            exact(rep, k, m)

    k8_shards = [(prefix, lo, hi) for prefix, lo, hi, _ in shards(27538, 8, 3, 0, ()) if lo <= hi]
    shard_tasks = [task(27538, 8, prefix, (lo, hi)) for prefix, lo, hi in k8_shards]
    Path("build/control-27538.tasks").write_text("".join(shard_tasks))
    per_shard = solve(shard_tasks)
    unsharded = answers[list(EXPECTED).index((8, 27538))][1]
    sharded = [rep for _, rows in per_shard for rep in rows]
    digest_a = canonical("logs/k8-27538-unsharded.solutions", unsharded)
    digest_b = canonical("logs/k8-27538-sharded.solutions", sharded)
    assert digest_a == digest_b and len(sharded) == 474
    print(f"sharded k=8 m=27538 shards={len(k8_shards)} solutions=474 sha256={digest_a}", flush=True)
    missing_shard = next(i for i, (_, rows) in enumerate(per_shard) if rows)
    altered = [rep for i, (_, rows) in enumerate(per_shard) if i != missing_shard for rep in rows]
    altered_hash = canonical("build/k8-27538-missing-mutant.solutions", altered)
    assert digest_a != altered_hash and len(altered) < len(unsharded)
    print(f"mutant=missing-shard omitted_index={missing_shard} k=8 m=27538 "
          f"expected=474 observed={len(altered)} sha256={altered_hash}", flush=True)

    for m, prefix, tails in DEEP:
        expected = tuple(sorted((*prefix, m, *tails)))
        exact(expected, 9, m)
        fields, reps = one(9, m, prefix)
        assert expected in reps and fields[4] == 0
        print(f"deep m={m} observed={len(reps)} max_b_bits={fields[-2]} certificate="
              + " ".join(map(str, expected)), flush=True)

    sylvester = [2]
    product = 2
    for _ in range(7):
        sylvester.append(product + 1)
        product *= sylvester[-1]
    sylvester.append(product)
    expected = tuple(sylvester)
    exact(expected, 9, 2)
    fields, reps = one(9, 2, expected[1:-2])
    assert expected in reps and expected[-1].bit_length() == 174
    print(f"sylvester k=9 m=2 q_bits={fields[-3]} last_bits=174 count={len(reps)} certificate="
          + " ".join(map(str, expected)), flush=True)

    one_fields, single = one(4, 42, (2, 3))
    assert single == [(2, 3, 7, 42)] and one_fields[5] == 1
    print("one-term k=4 m=42 prefix=2,3 observed=1", flush=True)

    for name, mask, k, m, prefix in [
        ("M1", 1, 4, 42, ()),
        ("M2", 2, 4, 5, ()),
        ("M5", 4, 9, 2, expected[1:-2]),
        ("M6", 8, 4, 42, ()),
        ("floor(q/p)+2", 16, 6, 79, ()),
    ]:
        ordinary, _ = one(k, m, prefix)
        changed, mutated = one(k, m, prefix, mask)
        assert changed[2] != ordinary[2], (name, ordinary, changed)
        addition = ""
        if name == "M2":
            bad = next(rep for rep in mutated if len(set(rep)) < len(rep))
            addition = " duplicate=" + " ".join(map(str, bad))
        print(f"mutant={name} k={k} m={m} expected={ordinary[2]} observed={changed[2]}{addition}", flush=True)


def comparisons(workers):
    hist = full_histograms()
    positive = sorted(hist[7])
    gaps = [n for n in range(2, 5000) if n not in hist[7]][:32]
    sample = sorted({positive[i*(len(positive)-1)//255] for i in range(256)} | set(gaps))
    answers = solve([task(m, 7) for m in sample])
    for m, (fields, reps) in zip(sample, answers, strict=True):
        assert fields[:2] == (m, 7) and fields[2] == len(reps) == hist[7][m], (m, fields)
        for rep in reps:
            exact(rep, 7, m)
    print(f"per-m k=7 matched={len(sample)} positive={sum(m in hist[7] for m in sample)} "
          f"incidence_sum_from_full_enumerator={sum(hist[7].values())}", flush=True)

    # Test every reached label, including all composites, and the frozen gap sample.
    labels = sorted(hist[7].keys() | set(gaps))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        sections = [labels[i::workers] for i in range(workers)]
        jobs = [pool.submit(scan, 7, section, hist[7]) for section in sections]
        subtotal = sum(job.result() for job in jobs)
    assert subtotal == 7 * 245765
    composite = sum(factorization(m) != [(m, 1)] for m in hist[7])
    print(f"all-positive per-m k=7 matched={len(labels)} positive={len(hist[7])} "
          f"composite={composite} gaps={len(gaps)} incidence_sum={subtotal}", flush=True)

    maximum = max(hist[6])
    chunks = [(2 + i*(maximum-1)//workers, 1 + (i+1)*(maximum-1)//workers)
              for i in range(workers)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = [pool.submit(scan, 6, range(lo, hi + 1), hist[6]) for lo, hi in chunks]
        sums = []
        for (lo, hi), job in zip(chunks, jobs, strict=True):
            subtotal = job.result()
            sums.append(subtotal)
            print(f"per-m k=6 first={lo} last={hi} matched={hi-lo+1} incidences={subtotal}", flush=True)
    assert sum(sums) == 13920
    composite = sum(factorization(m) != [(m, 1)] for m in hist[6])
    print(f"per-m k=6 matched={maximum-1} positive={len(hist[6])} composite={composite} "
          f"incidence_sum={sum(sums)}", flush=True)


if __name__ == "__main__":
    controls()
    comparisons(int(sys.argv[1]))
    print("controls=PASS", flush=True)
