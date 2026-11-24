"""Sweep the checked release gaps, keeping shard logs and exact witnesses."""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from math import ceil, isqrt
from pathlib import Path
from queue import Empty, Queue
import json
import os
import re
import signal
import subprocess
import threading
import time

from geometry import TARGET, campaign_bounds, write_manifest

JOB = "math_e293gaps_1123"
DEADLINE = int(Path("deadline.epoch").read_text())
SEARCH_END = DEADLINE - 1200
RESULT_HEADER = "shard\tseconds\texpected_two_term\tresult\tcertificate\n"
GAP_HEADER = "m\tfactorization\tverdict\tcertificate_or_shard_summary\n"


def checkpoint(message):
    with Path("STATUS.md").open("a") as stream:
        print(f"\n{time.strftime('%H:%M:%S UTC', time.gmtime())}. {message}", file=stream)
    print(message, flush=True)


def factor_powers(m):
    """Reference trial division, separate from the manifest generator."""
    powers = []
    remaining = m
    for p in range(2, isqrt(m) + 1):
        if p * p > remaining:
            break
        power = 1
        while remaining % p == 0:
            remaining //= p
            power *= p
        if power > 1:
            powers.append(power)
    if remaining > 1:
        powers.append(remaining)
    return powers


def exact_partition(m, manifest):
    """Replay coverage from exact fractions without using the geometry bounds."""
    powers = tuple(Fraction(1, p) for p in factor_powers(m))
    at_four, at_five = defaultdict(list), defaultdict(list)
    for name, (_, _, prefix, lo, hi) in manifest.items():
        (at_four if len(prefix) == 4 else at_five)[prefix].append((lo, hi, name))
    leaves = {}

    def bounds(r, left, previous):
        lo = max(previous + 1, int(1/r) + 1)
        hi = ceil(left/r) - 1
        for unit in powers:
            if r.denominator % unit.denominator == 0 and r > unit:
                hi = min(hi, int((left - 1)/(r - unit)))
        return lo, hi

    def follow(prefix, r):
        lo, hi = bounds(r, 8 - len(prefix), prefix[-1] if prefix else 1)
        if len(prefix) < 4:
            for n in range(lo, hi + 1):
                if n != m:
                    follow((*prefix, n), r - Fraction(1, n))
            return
        routed = {}
        for a, b, name in at_four.pop(prefix, []):
            assert lo <= a <= b <= hi and name not in leaves
            leaves[name] = 0
            for n in range(a, b + 1):
                assert n not in routed
                routed[n] = name
        for n in range(lo, hi + 1):
            if n == m:
                continue
            child = (*prefix, n)
            a, b = bounds(r - Fraction(1, n), 3, n)
            pieces = at_five.pop(child, [])
            if n in routed:
                assert not pieces
                leaves[routed[n]] += max(0, b - a + 1)
                continue
            cursor = a
            for x, y, name in sorted(pieces):
                assert cursor == x <= y <= b and name not in leaves
                leaves[name] = y - x + 1
                cursor = y + 1
            assert cursor == max(a, b + 1), (child, a, b, pieces)

    follow((), 1 - Fraction(1, m))
    assert not at_four and not at_five and set(leaves) == set(manifest)
    return leaves


def read_manifest(m, path, cap):
    rows = {}
    with path.open() as stream:
        assert stream.readline() == "shard\tweight\ttask\n"
        for i, line in enumerate(stream):
            name, weight, task = line.rstrip("\n").split("\t")
            n, k, *prefix, lo, hi = map(int, task.split())
            assert (n, k, name) == (m, 9, f"{i:06d}")
            assert 0 < int(weight) <= 200_000
            assert 4 <= len(prefix) <= 5 and tuple(sorted(set(prefix))) == tuple(prefix)
            assert 2 <= min(prefix) < max(prefix) < lo <= hi <= cap < m
            rows[name] = task, int(weight), tuple(prefix), lo, hi
    assert rows
    return rows


def exact_certificate(m, cert):
    terms = tuple(map(int, cert.split()))
    assert len(terms) == 9 and terms == tuple(sorted(set(terms))) and terms[0] >= 2
    assert m in terms and sum((Fraction(1, n) for n in terms), Fraction()) == 1
    return terms


def validate(m, result, cert, expected, maximum, bits):
    tag, *words = result.split()
    fields = tuple(map(int, words))
    assert tag == "R" and len(fields) == 17 and all(n >= 0 for n in fields), result
    n, k, solutions, _, skips, *extra = fields
    assert (n, k, skips) == (m, 9, 0) and solutions == bool(cert), result
    assert 0 < extra[-3] <= bits and extra[-1] <= maximum, result
    if cert:
        exact_certificate(m, cert)
        assert extra[1] <= expected, result
    else:
        assert extra[1] == expected, (result, expected)
    return fields


def atomic(path, content):
    temp = path.with_suffix(path.suffix + ".part")
    temp.write_text(content)
    temp.replace(path)


class Sweep:
    def __init__(self, m, workers):
        self.m, self.workers = m, workers
        self.dir = Path(f"logs/k9-{m}")
        self.dir.mkdir(exist_ok=True)
        caps, self.bits = campaign_bounds(m)
        self.maximum = max(caps)
        manifest_path = self.dir / "manifest.tsv"
        if not manifest_path.exists():
            write_manifest(m, 9, 4, 200_000)
            Path(f"build/manifest-{m}.tsv").rename(manifest_path)
        self.manifest = read_manifest(m, manifest_path, self.maximum)
        self.leaves = exact_partition(m, self.manifest)
        self.results = self.dir / "shards.tsv"
        if not self.results.exists():
            self.results.write_text(RESULT_HEADER)
        self.records = self.harvest()
        self.active = {}
        self.lock = threading.Lock()
        self.stop = threading.Event()

    def harvest(self):
        records = {}
        with self.results.open() as stream:
            assert stream.readline() == RESULT_HEADER
            for row in stream:
                name, seconds, expected, result, cert = row.rstrip("\n").split("\t")
                assert name not in records and int(expected) == self.leaves[name]
                fields = validate(self.m, result, cert, self.leaves[name], self.maximum, self.bits)
                assert float(seconds) >= 0
                records[name] = float(seconds), fields, cert
        return records

    @staticmethod
    def kill(child):
        if child.args[0] != "/usr/bin/time":
            child.kill()
            return
        if child.poll() is not None:
            return
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def cancel(self, winner=None):
        self.stop.set()
        with self.lock:
            for child in self.active.values():
                if child is not winner:
                    self.kill(child)

    def worker(self, queue, phase, index, mode, measure):
        cmd = ["build/solver", str(mode), "0"]
        if measure:
            cmd = ["/usr/bin/time", "-l", *cmd]
        err = self.dir / f"{phase}-{index}.stderr"
        with err.open("a") as diagnostics, subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=diagnostics,
            text=True, start_new_session=True
        ) as child:
            try:
                with self.lock:
                    if self.stop.is_set():
                        self.kill(child)
                        return
                    self.active[child.pid] = child
                    with Path("logs/worker-pids.tsv").open("a") as stream:
                        print(self.m, phase, index, child.pid, sep="\t", file=stream)
                while not self.stop.is_set():
                    try:
                        name = queue.get_nowait()
                    except Empty:
                        break
                    start = time.monotonic()
                    try:
                        child.stdin.write(self.manifest[name][0] + "\n")
                        child.stdin.flush()
                        cert = ""
                        for line in child.stdout:
                            if line.startswith("S "):
                                assert not cert and mode == 2
                                cert = line.strip()[2:]
                            else:
                                result = line.strip()
                                break
                        else:
                            if self.stop.is_set():
                                return
                            raise RuntimeError(f"unfinished shard {self.m}/{name}. See {err}")
                    except BrokenPipeError:
                        if self.stop.is_set():
                            return
                        raise
                    elapsed = time.monotonic() - start
                    expected = self.leaves[name]
                    validate(self.m, result, cert, expected, self.maximum, self.bits)
                    if cert:
                        terms = exact_certificate(self.m, cert)
                        _, _, prefix, lo, hi = self.manifest[name]
                        reduced = tuple(n for n in terms if n != self.m)
                        assert reduced[:len(prefix)] == prefix and lo <= reduced[len(prefix)] <= hi
                    with self.lock, self.results.open("a") as stream:
                        print(name, f"{elapsed:.6f}", expected, result, cert, sep="\t", file=stream)
                    if cert:
                        self.cancel(child)
                        break
                child.stdin.close()
                rc = child.wait()
                assert rc == 0 or self.stop.is_set(), (self.m, phase, index, rc, err)
            except BaseException:
                self.kill(child)
                raise
            finally:
                with self.lock:
                    self.active.pop(child.pid, None)

    def phase(self, names, phase, mode, measure=False):
        pending = [name for name in names if name not in self.records]
        if not pending:
            return
        assert time.time() < SEARCH_END
        queue = Queue()
        for name in pending:
            queue.put(name)
        self.stop.clear()
        count = min(1 if measure else self.workers, len(pending))
        with ThreadPoolExecutor(max_workers=count) as pool:
            futures = [pool.submit(self.worker, queue, phase, i, mode, measure) for i in range(count)]
            try:
                for future in as_completed(futures, timeout=max(0, SEARCH_END - time.time())):
                    future.result()
            except BaseException:
                self.cancel()
                raise
        assert not self.active
        self.records = self.harvest()

    def summary(self, reason="", work_capped=False):
        self.records = self.harvest()
        rows = list(self.records.values())
        certs = [cert for _, _, cert in rows if cert]
        skips = sum(fields[4] for _, fields, _ in rows)
        refusals = sum(
            int(count)
            for path in self.dir.glob("*.stderr")
            for count in re.findall(r"(?:^|\n)skipped=(\d+)", path.read_text())
        )
        expected = sum(self.leaves.values())
        observed = sum(fields[6] for _, fields, _ in rows)
        work_cap_skips = len(self.manifest) - len(rows) if work_capped and not certs else 0
        result = {
            "m": self.m, "shards": len(self.manifest), "completed_shards": len(rows) - len(certs),
            "witness_shards": len(certs), "skipped": skips + refusals + work_cap_skips,
            "solver_skips": skips + refusals, "work_cap_skips": work_cap_skips,
            "expected_two_term": expected, "observed_two_term": observed,
            "divisor_probes": sum(fields[3] for _, fields, _ in rows),
            "max_q_bits": max((fields[-3] for _, fields, _ in rows), default=0),
            "max_prefix": max((fields[-1] for _, fields, _ in rows), default=0),
            "worker_seconds": round(sum(seconds for seconds, _, _ in rows), 3),
            "verdict": "unsettled", "reason": reason,
        }
        if certs and not result["skipped"]:
            result["verdict"], result["certificate"] = "found", certs[0]
        elif not reason and not result["skipped"] and len(rows) == len(self.manifest) and not certs:
            assert observed == expected
            result["verdict"] = "missing"
        atomic(self.dir / "summary.json", json.dumps(result, sort_keys=True) + "\n")
        return result

    def run(self, mode, measure=False):
        names = list(self.manifest)
        count = ceil(len(names) / 100)
        pilot = [names[(2*i + 1)*len(names) // (2*count)] for i in range(count)]
        pilot[0] = names[0]
        assert len(set(pilot)) == count
        prior = self.summary()
        if prior["verdict"] != "unsettled":
            return prior
        checkpoint(f"m={self.m} exact manifest covers {sum(self.leaves.values()):,} "
                   f"two-term states in {len(names):,} shards. Starting the pilot.")
        try:
            if measure:
                self.phase(pilot[:1], "rss-pilot", mode, measure=True)
                data = (self.dir / "rss-pilot-0.stderr").read_text()
                peak = max(int(line.split()[0]) for line in data.splitlines()
                           if "maximum resident set size" in line)
                assert self.workers * peak < 4_000_000_000
                checkpoint(f"m={self.m} measured peak worker RSS {peak:,} bytes "
                           f"({self.workers * peak:,} projected across {self.workers} workers).")
            if any(cert for _, _, cert in self.records.values()):
                return self.summary()
            self.phase(pilot, "pilot", mode)
            if any(cert for _, _, cert in self.records.values()):
                checkpoint(f"m={self.m} exact witness found during the pilot.")
                return self.summary()
            seconds = sum(self.records[name][0] for name in pilot)
            sample_weight = sum(self.manifest[name][1] for name in pilot)
            pending = [name for name in names if name not in self.records]
            total_weight = sum(self.manifest[name][1] for name in pending)
            eta = seconds * total_weight / sample_weight / self.workers
            remaining = SEARCH_END - time.time()
            with (self.dir / "pilot.tsv").open("a") as stream:
                if stream.tell() == 0:
                    print("sample_ids\tsample_weight\tremaining_weight\tworker_seconds\t"
                          "workers\testimated_remaining_seconds\tbudget_seconds", file=stream)
                print(",".join(pilot), sample_weight, total_weight, f"{seconds:.3f}",
                      self.workers, f"{eta:.1f}", f"{remaining:.1f}", sep="\t", file=stream)
            if pending and eta > remaining:
                reason = f"pilot ETA {eta:.1f}s exceeded {remaining:.1f}s remaining"
                checkpoint(f"m={self.m} unsettled. {reason}.")
                return self.summary(reason, work_capped=True)
            checkpoint(f"m={self.m} pilot estimates {eta:.1f}s for the remaining shards.")
            self.phase(sorted(pending, key=lambda name: (-self.manifest[name][1], name)), "main", mode)
        except TimeoutError as exc:
            return self.summary(f"work cap reached; {exc}", work_capped=True)
        except BaseException as exc:
            self.summary(f"search error; {type(exc).__name__}: {exc}")
            raise
        return self.summary()


def control_runs(workers):
    regression = Sweep(TARGET, workers).run(mode=0, measure=True)
    assert regression["verdict"] == "missing" and regression["skipped"] == 0, regression
    assert regression["completed_shards"] == regression["shards"] == 1412
    assert regression["observed_two_term"] == 76_472_707
    assert regression["divisor_probes"] == 487_525_854_050
    checkpoint(f"Regression m={TARGET} reproduced zero with zero skips over 1,412 shards.")
    controls = list(map(int, Path("logs/nearby-control-targets.txt").read_text().split()))
    assert len(controls) == 6 and len(set(controls)) == 6
    rows = ["m\tverdict\tcertificate\n"]
    for m in controls:
        row = Sweep(m, workers).run(mode=2)
        assert row["verdict"] == "found" and row["skipped"] == 0, row
        exact_certificate(m, row["certificate"])
        rows.append(f'{m}\tfound\t{row["certificate"]}\n')
    atomic(Path("logs/nearby-controls.tsv"), "".join(rows))
    checkpoint("All six nearby composite k=9 controls produced verified witnesses.")


def search_gaps(workers):
    path = Path("gaps.tsv")
    lines = path.read_text().splitlines(keepends=True)
    assert lines[0] == GAP_HEADER
    rows = [line.rstrip("\n").split("\t") for line in lines[1:]]
    assert [int(row[0]) for row in rows] == sorted(set(int(row[0]) for row in rows))
    first_zero = next((int(row[0]) for row in rows if row[2] == "missing"), None)
    for row in rows:
        m = int(row[0])
        if row[2] in ("found", "missing"):
            continue
        if time.time() >= SEARCH_END:
            row[3] = "search cutoff reached before pilot"
            atomic(path, GAP_HEADER + "".join("\t".join(r) + "\n" for r in rows))
            checkpoint(f"m={m} remains unsettled at the search cutoff.")
            break
        try:
            result = Sweep(m, workers).run(mode=2)
        except BaseException as exc:
            row[3] = f"search failed: {type(exc).__name__}; see logs/k9-{m}/ and logs/gap-driver.log"
            atomic(path, GAP_HEADER + "".join("\t".join(r) + "\n" for r in rows))
            raise
        row[2] = result["verdict"]
        if row[2] == "found":
            row[3] = result["certificate"]
        else:
            row[3] = (
                f'{result["completed_shards"]}/{result["shards"]} shards; '
                f'{result["witness_shards"]} witnesses; {result["skipped"]} skips; '
                f'{result["observed_two_term"]}/{result["expected_two_term"]} tail states; '
                f'logs/k9-{m}/summary.json'
            )
            if result["reason"]:
                row[3] += f'; {result["reason"]}'
        atomic(path, GAP_HEADER + "".join("\t".join(r) + "\n" for r in rows))
        checkpoint(f"m={m} {row[2]}. {row[3]}")
        if row[2] == "unsettled":
            break
        if row[2] == "missing" and first_zero is None:
            first_zero = m
            checkpoint(f"First exhaustive zero above {TARGET}: {m}. "
                       "Proceeding through the next gaps in ascending order.")


def interrupt(signum, _frame):
    raise TimeoutError(f"signal {signum}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("job", choices=[JOB])
    parser.add_argument("--workers", type=int, choices=range(1, 9), default=8)
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    assert time.time() < SEARCH_END
    assert Path("logs/controls.log").read_text().endswith("controls=PASS\n")
    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGALRM, interrupt)
    signal.alarm(ceil(SEARCH_END - time.time()))
    try:
        control_runs(args.workers)
        if not args.controls_only:
            search_gaps(args.workers)
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    main()
