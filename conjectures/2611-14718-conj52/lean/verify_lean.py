#!/usr/bin/env python3
"""Independently replay the exact witness and verify the standalone Lean build."""

import argparse
from collections import Counter
from fractions import Fraction
from functools import cache
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time


ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLCHAIN = "leanprover/lean4:v4.36.0"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REQUIRED = {
    "F3_numEdges", "F3_maxDegreeLe3", "F3_isTree", "F3_connected",
    "F3_chain_iso", "F3_static_counts", "F3_Nstat", "F3_Nseq",
    "F3_cross_product", "conj52_disproof_F3",
    "Fm_isTree", "Fm_maxDegreeLe3", "Fm_static_min", "Fm_static_total", "Fm_Nstat",
    "Fm_Nseq", "Fm_cross_product", "infinite_family_Fm_disproof",
    "P3_control", "P4_control", "P5_control", "Claw_control",
    "F1_control", "F2_control", "degree4_control",
}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as stream:
        return stream.read()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge_set(n, edges):
    result = set()
    for u, v in edges:
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n,
                "Invalid edge endpoint")
        require(u != v, "Loop in edge list")
        edge = tuple(sorted((u, v)))
        require(edge not in result, "Duplicate edge")
        result.add(edge)
    return result


def laws(n, edges):
    edges = edge_set(n, edges)
    adjacent = [0] * n
    for u, v in edges:
        adjacent[u] |= 1 << v
        adjacent[v] |= 1 << u
    closed = [neighbors | (1 << v) for v, neighbors in enumerate(adjacent)]
    full = (1 << n) - 1
    covers = [0] * (1 << n)
    independent = bytearray(1 << n)
    independent[0] = 1
    static = Counter()
    for selected in range(1 << n):
        if selected:
            vertex = (selected & -selected).bit_length() - 1
            rest = selected ^ (1 << vertex)
            covers[selected] = covers[rest] | closed[vertex]
            independent[selected] = independent[rest] and not (rest & adjacent[vertex])
        if independent[selected] and covers[selected] == full:
            static[selected.bit_count()] += 1

    factorial = [1]
    for k in range(1, n + 1):
        factorial.append(k * factorial[-1])

    @cache
    def permutation_counts(active):
        if not active:
            return (1,)
        remaining = active
        size = active.bit_count()
        counts = [0] * (size + 1)
        while remaining:
            vertex = (remaining & -remaining).bit_length() - 1
            remaining ^= 1 << vertex
            residual = active & ~closed[vertex]
            multiplicity = factorial[size - 1] // factorial[residual.bit_count()]
            for k, count in enumerate(permutation_counts(residual)):
                counts[k + 1] += multiplicity * count
        return tuple(counts)

    counts = permutation_counts(full)
    require(sum(counts) == factorial[n], "RSA permutation count did not normalize")
    sequential = {k: Fraction(count, factorial[n]) for k, count in enumerate(counts) if count}
    seen = 1 if n else 0
    while True:
        grown = seen
        for v in range(n):
            if (seen >> v) & 1:
                grown |= adjacent[v]
        if grown == seen:
            break
        seen = grown
    return static, sequential, max(map(int.bit_count, adjacent), default=0), seen == full


def cdf(histogram, threshold):
    return Fraction(sum(v for k, v in histogram.items() if k <= threshold), sum(histogram.values()))


def chain(m):
    edges = [(5 * i + u, 5 * i + v) for i in range(m)
             for u, v in ((0, 1), (1, 2), (1, 3), (3, 4))]
    return edges + [(5 * i + 2, 5 * (i + 1)) for i in range(m - 1)]


def replay():
    witness = json.loads(read("..", "certificates", "witness.json"))
    lean_source = read("SubcubicConj52.lean")
    edge_declaration = re.search(r"def F3Edges\b.*?:=\s*\[(.*?)\]", lean_source, re.S)
    require(edge_declaration is not None, "Lean witness edge list is missing")
    lean_edges = [tuple(map(int, pair)) for pair in
                  re.findall(r"\((\d+)\s*,\s*(\d+)\)", edge_declaration[1])]
    n = witness["n"]
    raw = edge_set(n, witness["edges"])
    require(n == 15 and raw == edge_set(n, lean_edges), "Lean and JSON edge lists differ")
    chain_to_raw = [7, 5, 4, 6, 13, 1, 0, 2, 3, 12, 8, 9, 11, 10, 14]
    require(sorted(chain_to_raw) == list(range(n)), "Chain relabeling is not bijective")
    require(raw == edge_set(n, [(chain_to_raw[u], chain_to_raw[v]) for u, v in chain(3)]),
            "Family construction does not match the witness")
    public_to_raw = [5, 4, 1, 0, 2, 8, 9, 6, 13, 3, 12, 10, 14, 7, 11]
    public_edges = [(i, i + 1) for i in range(6)] + [
        (0, 7), (7, 8), (3, 9), (9, 10), (6, 11), (11, 12), (0, 13), (6, 14)]
    require(raw == edge_set(n, [(public_to_raw[u], public_to_raw[v]) for u, v in public_edges]),
            "Public and supplied witnesses differ")
    static, seq, degree, connected = laws(n, raw)
    require(connected and len(raw) == 14 and degree == 3, "Witness topology differs")
    require((len(raw), degree, connected, connected and len(raw) == n - 1) ==
            (witness["num_edges"], witness["max_degree"], witness["connected"], witness["is_tree"]),
            "Certificate topology labels differ")
    require(static == {6: 1, 7: 50, 8: 4}, "Static witness histogram differs")
    require(static == {int(k): v for k, v in witness["mis_size_counts"].items()},
            "Certificate static histogram differs")
    require(seq == {int(k): Fraction(v) for k, v in witness["rsa_pmf"].items()},
            "Certificate RSA histogram differs")
    ss, st = cdf(seq, 6), cdf(static, 6)
    excess = ss.numerator * st.denominator - st.numerator * ss.denominator
    require((ss, st, excess, ss - st) == (Fraction(64, 3375), Fraction(1, 55), 145,
                                         Fraction(29, 37125)), "Witness gap differs")
    require((6, ss, st, excess, ss - st, sum(static.values())) ==
            (witness["violating_k"], Fraction(witness["P_seq_le_k"]),
             Fraction(witness["P_stat_le_k"]), witness["cross_product_diff"],
             Fraction(witness["J_exact"]), witness["total_mis"]),
            "Certificate threshold labels differ")
    require(cdf(seq, 7) < cdf(static, 7), "Missing opposite crossing at threshold 7")
    print(f"F3: n={n}, edges={len(raw)}, max degree={degree}, MIS={dict(sorted(static.items()))}")
    print(f"F3: sequential CDF {ss} > static CDF {st}; excess {excess}")
    print(f"F3 k=7: sequential {cdf(seq, 7)} < static {cdf(static, 7)}")
    controls = [("P3", 3, [(0, 1), (1, 2)]),
                ("P4", 4, [(0, 1), (1, 2), (2, 3)]),
                ("P5", 5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
                ("claw", 4, [(0, 1), (0, 2), (0, 3)]),
                ("F1", 5, chain(1)), ("F2", 10, chain(2)),
                ("degree 4", 6, [(0, 1), (0, 2), (0, 3), (0, 4), (4, 5), (1, 2)])]
    for label, order, edges in controls:
        static, seq, degree, _ = laws(order, edges)
        failures = [k for k in range(order + 1) if cdf(seq, k) > cdf(static, k)]
        expected = [2] if label == "degree 4" else []
        require(failures == expected and (degree == 4 if expected else degree <= 3),
                f"Control {label} differs")
        print(f"{label}: static {dict(sorted(static.items()))}; RSA "
              + ", ".join(f"{k}:{v}" for k, v in seq.items()))
    static, seq, degree, connected = laws(20, chain(4))
    require(degree == 3 and connected and cdf(static, 8) == Fraction(1, 229)
            and cdf(seq, 8) == Fraction(256, 50625), "F4 spot check differs")
    print("F4: sequential CDF 256/50625 > static CDF 1/229")


def commands():
    elan_dir = os.path.expanduser("~/.elan/bin")
    for name in ("lean", "lake"):
        local = os.path.join(elan_dir, name)
        executable = local if os.path.isfile(local) else shutil.which(name)
        require(executable is not None, f"{name} is missing")
        yield executable


def run(command):
    env = dict(os.environ, LEAN_NUM_THREADS="1")
    process = subprocess.Popen(
        ["nice", "-n", "10", *command], cwd=ROOT, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True,
    )
    deadline = time.monotonic_ns() + 60_000_000_000
    peak_kib = 0
    try:
        while True:
            try:
                output, _ = process.communicate(timeout=1)
                break
            except subprocess.TimeoutExpired:
                require(time.monotonic_ns() < deadline, f"Deadline exceeded for {command}")
                rows = subprocess.check_output(["ps", "-axo", "pid=,ppid=,rss="], text=True)
                processes = [tuple(map(int, row.split())) for row in rows.splitlines()]
                family = {process.pid}
                changed = True
                while changed:
                    descendants = {pid for pid, parent, _ in processes if parent in family}
                    changed = not descendants.issubset(family)
                    family.update(descendants)
                rss = sum(kib for pid, _, kib in processes if pid in family)
                peak_kib = max(peak_kib, rss)
                require(rss < 1_850_000, f"RSS guard reached for {command}")
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
    print(output, end="")
    print(f"Observed peak RSS {peak_kib:,} KiB for {os.path.basename(command[0])}")
    require(process.returncode == 0, f"Failed command {command}")
    require(re.search(r"\bwarning:", output, re.I) is None, f"Lean warnings in {command}")
    return output


def verify_lean():
    require(read("lean-toolchain").strip() == TOOLCHAIN, "Toolchain pin differs")
    config = read("lakefile.toml")
    require(not re.search(r"\[\[require\]\]|\bmathlib\b", config, re.I), "External Lake dependency")
    prohibited = re.compile(r"\b(sorry|axiom|admit|native_decide|unsafe|extern|implemented_by)\b")
    lean_source = read("SubcubicConj52.lean")
    for name in ("SubcubicConj52.lean", "CheckAxioms.lean"):
        code = re.sub(r"/-.*?-/", "", read(name), flags=re.S)
        code = re.sub(r"--[^\n]*", "", code)
        require(prohibited.search(code) is None, f"Forbidden declaration in {name}")
        if name != "CheckAxioms.lean":
            for line in re.findall(r"^import\s+(.+)$", code, flags=re.M):
                require(all(module.split(".")[0] in {"Init", "Lean", "Std"}
                            for module in line.split()), f"External import {line}")
    lean, lake = commands()
    require("version 4.36.0," in run([lean, "--version"]), "Active Lean version differs")
    run([lake, "build", "--no-ansi"])
    run([lean, "-j", "1", "-M", "1200", "-D", "Elab.async=false", "SubcubicConj52.lean"])
    output = run([lake, "env", lean, "-j", "1", "CheckAxioms.lean"])
    results = {}
    for name, payload in re.findall(r"'SubcubicConj52\.([^']+)' depends on axioms: \[(.*?)\]", output):
        results[name] = {item.strip() for item in payload.split(",") if item.strip()}
    for name in re.findall(r"'SubcubicConj52\.([^']+)' does not depend on any axioms", output):
        results[name] = set()
    extras = {name: axioms - AXIOMS for name, axioms in results.items() if axioms - AXIOMS}
    require(not extras, f"Nonstandard dependencies {extras}")
    missing = REQUIRED.difference(results)
    require(not missing, f"Missing required declarations or axiom output {sorted(missing)}")
    require("infinite_family_Fm_disproof" in lean_source, "All-parameter proof is missing")
    print(f"Checked {len(results)} declarations with standard axioms only")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-only", action="store_true", help="check the raw certificate and controls")
    args = parser.parse_args()
    try:
        replay()
        if not args.replay_only:
            verify_lean()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
