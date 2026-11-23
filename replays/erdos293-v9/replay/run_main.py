"""Run and resume the sealed Erdős 293 shard manifest."""
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from hashlib import sha256
from math import ceil, isqrt
from pathlib import Path
from queue import Empty, Queue
import argparse
import json
import os
import signal
import subprocess
import threading
import time

from geometry import TARGET

DEADLINE = int(Path("deadline.epoch").read_text())
MANIFEST = Path(f"build/manifest-{TARGET}.tsv")
SHARDS = Path("logs/shards")
CONFIG = ("solver.c", "geometry.py", "run_main.py", "Makefile", "build/solver",
          "controls.py", "logs/controls.log", str(MANIFEST))
STOP = threading.Event()
CHILDREN = {}
LOCK = threading.Lock()


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def sha_lines(paths):
    return "".join(f"{digest(p)}  {p}\n" for p in paths)


def atomic(path, content):
    path = Path(path)
    temp = path.with_suffix(path.suffix + ".part")
    with temp.open("w") as output:
        output.write(content)
    temp.replace(path)


def status(line):
    with open("STATUS.md", "a") as stream:
        print(f"\n{time.strftime('%H:%M UTC', time.gmtime())}. {line}", file=stream)


def read_manifest():
    rows = {}
    with MANIFEST.open() as stream:
        assert stream.readline() == "shard\tweight\ttask\n"
        for expected_id, line in enumerate(stream):
            name, weight, task = line.rstrip("\n").split("\t")
            assert name == f"{expected_id:06d}"
            weight = int(weight)
            m, k, *prefix, lo, hi = map(int, task.split())
            assert (m, k) == (TARGET, 9) and 0 < weight <= 200000
            assert 4 <= len(prefix) <= 5 and 2 <= lo <= hi <= 12806327
            rows[name] = (task, weight, tuple(prefix), lo, hi)
    assert rows
    return rows


def range_at(r, left, previous):
    """Verifier's bounds from inequalities in the rational remainder."""
    lower = max(previous + 1, int(1/r) + 1)
    upper = ceil(left/r) - 1
    power_unit = Fraction(1, TARGET)
    if r.denominator % TARGET == 0 and r > power_unit:
        upper = min(upper, int((left - 1)/(r - power_unit)))
    return lower, upper


def exact_partition(manifest):
    assert all(TARGET % n for n in range(2, isqrt(TARGET) + 1))
    at_four, at_five = defaultdict(list), defaultdict(list)
    for name, (_, _, prefix, lo, hi) in manifest.items():
        (at_four if len(prefix) == 4 else at_five)[prefix].append((lo, hi, name))
    leaves = dict.fromkeys(manifest, 0)
    seen = set()

    def follow(prefix, r):
        lo, hi = range_at(r, 8 - len(prefix), prefix[-1] if prefix else 1)
        if len(prefix) < 4:
            for n in range(lo, hi + 1):
                follow((*prefix, n), r - Fraction(1, n))
            return
        four = at_four.pop(prefix, [])
        routed = {}
        for a, b, name in four:
            assert lo <= a <= b <= hi and name not in seen
            seen.add(name)
            for n in range(a, b + 1):
                assert n not in routed
                routed[n] = name
        for n in range(lo, hi + 1):
            child = (*prefix, n)
            a, b = range_at(r - Fraction(1, n), 3, n)
            five = at_five.pop(child, [])
            if n in routed:
                assert not five
                leaves[routed[n]] += max(0, b - a + 1)
                continue
            cursor = a
            for x, y, name in sorted(five):
                assert cursor == x <= y <= b and name not in seen
                seen.add(name)
                leaves[name] = y - x + 1
                cursor = y + 1
            assert cursor == b + 1, (child, a, b, five)

    follow((), 1 - Fraction(1, TARGET))
    assert not at_four and not at_five and seen == set(manifest)
    return leaves


def validated(record, name, task, expected_leaves):
    assert record["id"] == name and record["task"] == task
    tag, *metrics = record["result"].split()
    metrics = tuple(map(int, metrics))
    assert tag == "R" and len(metrics) == 17, record
    m, k, solutions, probes, skips, *extra = metrics
    nodes = extra[:9]
    assert (m, k, skips) == (TARGET, 9, 0) and solutions == len(record["solutions"]), record
    assert all(v >= 0 for v in metrics) and nodes[1] == expected_leaves, record
    assert 0 < extra[-3] <= 80 and extra[-1] <= 12806327, record
    for solution in record["solutions"]:
        terms = tuple(map(int, solution.split()))
        assert len(terms) == 9 and tuple(sorted(set(terms))) == terms
        assert TARGET in terms and terms[0] >= 2
        assert sum((Fraction(1, n) for n in terms), Fraction()) == 1
    return metrics


def record_path(name):
    return SHARDS / f"{name}.json"


def load(name, manifest, leaves):
    record = json.loads(record_path(name).read_text())
    validated(record, name, manifest[name][0], leaves[name])
    return record


def register(child, phase, number):
    with LOCK:
        assert not STOP.is_set()
        CHILDREN[child.pid] = child
        with open("logs/main-processes.tsv", "a") as stream:
            print(f"{phase}\t{number}\t{child.pid}", file=stream)


def terminate(child):
    try:
        os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def stop_workers():
    STOP.set()
    with LOCK:
        for child in CHILDREN.values():
            terminate(child)


def interrupt(signum, _frame):
    raise InterruptedError(f"interrupted or deadline signal {signum}")


def run_worker(queue, manifest, leaves, phase, number, measured):
    cmd = ["build/solver", "1", "0"]
    if measured:
        cmd = ["/usr/bin/time", "-l", *cmd]
    err = Path(f"logs/{phase}-worker-{number}.stderr")
    with err.open("a") as diagnostics, subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=diagnostics,
        text=True, start_new_session=True
    ) as child:
        try:
            register(child, phase, number)
            while not STOP.is_set() and time.time() < DEADLINE:
                try:
                    name = queue.get_nowait()
                except Empty:
                    break
                task = manifest[name][0]
                start = time.monotonic()
                child.stdin.write(task + "\n")
                child.stdin.flush()
                solutions = []
                for line in child.stdout:
                    if line.startswith("S "):
                        solutions.append(line.strip()[2:])
                        continue
                    record = {"id": name, "task": task, "result": line.strip(),
                              "solutions": solutions, "elapsed": time.monotonic() - start}
                    validated(record, name, task, leaves[name])
                    atomic(record_path(name), json.dumps(record, sort_keys=True) + "\n")
                    break
                else:
                    raise RuntimeError(f"unfinished shard {name}; inspect {err}")
            child.stdin.close()
            assert child.wait() == 0, f"{phase} worker {number}; inspect {err}"
        except BaseException:
            terminate(child)
            raise
        finally:
            with LOCK:
                CHILDREN.pop(child.pid, None)


def run_phase(names, manifest, leaves, phase, count, measured=False):
    pending = [name for name in names if not record_path(name).exists()]
    if not pending:
        return
    queue = Queue()
    for name in pending:
        queue.put(name)
    with ThreadPoolExecutor(max_workers=min(count, len(pending))) as pool:
        workers = [pool.submit(run_worker, queue, manifest, leaves, phase, i, measured)
                   for i in range(min(count, len(pending)))]
        try:
            for worker in workers:
                worker.result(timeout=max(0.001, DEADLINE - time.time()))
        except BaseException:
            stop_workers()
            raise
    assert queue.empty()


def choose_pilot(manifest):
    names = list(manifest)
    count = ceil(len(names)/100)
    sample = [names[(2*i+1)*len(names)//(2*count)] for i in range(count)]
    sample[0] = names[0]
    assert len(set(sample)) == count
    return sample


def harvest(manifest, leaves, outputs=True):
    header = "shard\tsolutions\tskipped\tdivisor_probes\t" + "\t".join(
        f"nodes_left_{i}" for i in range(1, 10))
    header += "\tmax_q_bits\tmax_b_bits\tmax_prefix\telapsed_seconds\n"
    lines = [header]
    solutions = []
    nodes = [0] * 9
    count = probes = elapsed = max_q = max_b = max_prefix = 0
    for name, (task, _, _, _, _) in manifest.items():
        if not record_path(name).exists():
            continue
        row = load(name, manifest, leaves)
        metrics = validated(row, name, task, leaves[name])
        _, _, solved, divisors, skips, *extra = metrics
        probes += divisors
        nodes = [a + b for a, b in zip(nodes, extra[:9])]
        max_q = max(max_q, extra[-3])
        max_b = max(max_b, extra[-2])
        max_prefix = max(max_prefix, extra[-1])
        elapsed += row["elapsed"]
        count += 1
        solutions.extend(row["solutions"])
        lines.append("\t".join(map(str, (name, solved, skips, divisors, *extra, f'{row["elapsed"]:.6f}'))) + "\n")
    assert len(set(solutions)) == len(solutions) and nodes[1] <= sum(leaves.values())
    summary = (f"shards_completed={count}/{len(manifest)}\nsolutions={len(solutions)}\nskipped_in_completed=0\n"
               f"dfs_nodes={sum(nodes)}\ntwo_term_nodes={nodes[1]}\n"
               f"divisor_probes={probes}\ncounted_events={sum(nodes)+probes}\n"
               f"nodes_by_terms_left={nodes}\nmax_q_bits={max_q}\nmax_b_bits={max_b}\n"
               f"max_prefix={max_prefix}\nsummed_shard_seconds={elapsed:.3f}\n")
    if outputs:
        atomic("logs/main-shards.tsv", "".join(lines))
        atomic("logs/main-summary.txt", summary)
        atomic("logs/main-solutions.txt", "".join(s + "\n" for s in sorted(solutions)))
    return count, solutions, summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job", choices=["math_e293v9_1123"])
    parser.add_argument("--workers", type=int, default=8, choices=range(1, 9))
    args = parser.parse_args()
    assert Path("logs/controls.log").read_text().endswith("controls=PASS\n")
    assert time.time() < DEADLINE
    SHARDS.mkdir(exist_ok=True)

    freeze = Path("MAIN_INPUTS.sha256")
    hashes = sha_lines(CONFIG)
    if freeze.exists():
        assert freeze.read_text() == hashes
    else:
        atomic(freeze, hashes)
    manifest = read_manifest()
    leaves = exact_partition(manifest)
    atomic("logs/manifest-check.log",
           f"exact_partition=PASS shards={len(manifest)} expected_two_term_nodes={sum(leaves.values())}\n")
    known = {p.stem for p in SHARDS.glob("*.json")}
    assert known <= set(manifest)
    for name in known:
        load(name, manifest, leaves)
    pilot = choose_pilot(manifest)
    count, _, _ = harvest(manifest, leaves, outputs=False)
    status(f"Main inputs sealed. Exact manifest has {len(manifest)} shards and {sum(leaves.values()):,} two-term calls. "
           f"Starting from {count} completed shards with {args.workers} workers.")
    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGALRM, interrupt)
    signal.alarm(ceil(DEADLINE - time.time()))
    try:
        run_phase(pilot[:1], manifest, leaves, "rss-pilot", 1, measured=True)
        time_log = Path("logs/rss-pilot-worker-0.stderr").read_text()
        peak = max(int(line.split()[0]) for line in time_log.splitlines() if "maximum resident set size" in line)
        assert peak * args.workers < 4_000_000_000
        run_phase(pilot[1:], manifest, leaves, "pilot", args.workers)
        pilot_rows = [load(name, manifest, leaves) for name in pilot]
        observed = sum(row["elapsed"] for row in pilot_rows)
        total_weight = sum(row[1] for row in manifest.values())
        sample_weight = sum(manifest[name][1] for name in pilot)
        seconds = observed * total_weight / sample_weight / args.workers
        atomic("logs/pilot.log", f"shards={len(pilot)}/{len(manifest)} ids={','.join(pilot)}\n"
               f"sample_weight={sample_weight} total_weight={total_weight} worker_seconds={observed:.3f}\n"
               f"workers={args.workers} projected_wall_seconds={seconds:.1f} measured_peak_rss_bytes={peak}\n")
        status(f"Pilot finished {len(pilot)} shards. Measured worker RSS {peak:,} bytes. "
               f"Throughput projects {seconds:.1f} seconds for {args.workers} workers. Completing remaining shards.")
        ordered = sorted(manifest, key=lambda name: (-manifest[name][1], name))
        run_phase(ordered, manifest, leaves, "main", args.workers)
    finally:
        signal.alarm(0)
        stop_workers()
        count, _, summary = harvest(manifest, leaves)
        status(f"Main harvest recorded {count}/{len(manifest)} shards. See logs/main-summary.txt.")
    assert count == len(manifest)
    atomic("OWN.sha256", sha_lines(("MAIN_INPUTS.sha256", "logs/manifest-check.log", "logs/main-shards.tsv",
                                    "logs/main-summary.txt", "logs/main-solutions.txt")))
    print(summary, end="")


if __name__ == "__main__":
    main()
