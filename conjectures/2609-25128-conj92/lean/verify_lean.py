#!/usr/bin/env python3
"""Standalone verifier for the Lean 4.36.0 formalization of Conjecture 9.2.

Uses only the Python standard library (with integer arithmetic and os.path).
Checks:
  1. Zero forbidden tokens in all .lean files and zero Mathlib imports.
  2. Required definitions and theorems exist in SubQuorumNG.lean.
  3. Clean compilation via `lake build` and standalone `lean SubQuorumNG.lean`
     with zero warnings and zero errors.
  4. `lean CheckAxioms.lean` succeeds and every checked theorem depends only
     on standard Lean core axioms (subset of {propext, Classical.choice, Quot.sound}).
"""

import os
import re
import subprocess
import sys
import time


FORBIDDEN_TOKENS = (
    "sorry",
    "admit",
    "axiom ",
    "native_decide",
    "unsafe",
)

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})

REQUIRED_AXIOM_TARGETS = (
    "class_size_lower_bound",
    "handshaking_weight_bound",
    "theorem_1",
    "conjecture_9_2",
    "sharpness_Kn",
)

REQUIRED_DECLARATIONS = (
    "structure SimpleGraph",
    "def compl",
    "structure SubQuorumColoring",
    "theorem class_size_lower_bound",
    "theorem handshaking_weight_bound",
    "theorem theorem_1",
    "theorem conjecture_9_2",
    "theorem sharpness_Kn",
)


def build_env():
    env = dict(os.environ)
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    if os.path.isdir(elan_bin):
        cur_path = env.get("PATH", "")
        env["PATH"] = elan_bin + (os.pathsep + cur_path if cur_path else "")
    return env


def run_checked(cmd, cwd, env, label):
    t0 = time.monotonic_ns()
    proc = subprocess.run(
        ["nice", "-n", "10"] + list(cmd),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    elapsed_ms = (time.monotonic_ns() - t0) // 1_000_000
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        sys.stderr.write(f"FAIL [{label}]: exit code {proc.returncode}\n{combined}\n")
        sys.exit(1)
    for line in combined.splitlines():
        lower = line.lower()
        if "warning:" in lower or "error:" in lower:
            sys.stderr.write(f"FAIL [{label}]: diagnostic emitted:\n{line}\n")
            sys.exit(1)
    return proc.stdout, proc.stderr, elapsed_ms


def check_lean_sources(root):
    lean_files = sorted(
        name for name in os.listdir(root) if name.endswith(".lean")
    )
    if "SubQuorumNG.lean" not in lean_files or "CheckAxioms.lean" not in lean_files:
        sys.stderr.write(
            f"FAIL: missing required .lean files (found: {lean_files})\n"
        )
        sys.exit(1)

    line_counts = {}
    for name in lean_files:
        fpath = os.path.join(root, name)
        with open(fpath, "r", encoding="utf-8") as fh:
            text = fh.read()
        line_counts[name] = len(text.splitlines())
        for tok in FORBIDDEN_TOKENS:
            if tok in text:
                sys.stderr.write(
                    f"FAIL: forbidden token {tok!r} found in {name}\n"
                )
                sys.exit(1)
        if re.search(r"^\s*import\s+Mathlib\b", text, flags=re.MULTILINE):
            sys.stderr.write(f"FAIL: Mathlib import found in {name}\n")
            sys.exit(1)

    main_path = os.path.join(root, "SubQuorumNG.lean")
    with open(main_path, "r", encoding="utf-8") as fh:
        main_text = fh.read()
    for decl in REQUIRED_DECLARATIONS:
        if decl not in main_text:
            sys.stderr.write(
                f"FAIL: required declaration {decl!r} missing from SubQuorumNG.lean\n"
            )
            sys.exit(1)

    return lean_files, line_counts


def parse_and_verify_axioms(output):
    axiom_re = re.compile(
        r"^'([^']+)' depends on axioms: \[([^\]]*)\]\s*$"
    )
    no_axiom_re = re.compile(
        r"^'([^']+)' does not depend on any axioms\s*$"
    )
    parsed = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m_ax = axiom_re.match(line)
        if m_ax:
            thm = m_ax.group(1)
            items = [x.strip() for x in m_ax.group(2).split(",") if x.strip()]
            parsed[thm] = items
            continue
        m_no = no_axiom_re.match(line)
        if m_no:
            parsed[m_no.group(1)] = []
            continue
        sys.stderr.write(
            f"FAIL: unexpected output line from CheckAxioms.lean: {line!r}\n"
        )
        sys.exit(1)

    for target in REQUIRED_AXIOM_TARGETS:
        if target not in parsed:
            sys.stderr.write(
                f"FAIL: missing `#print axioms {target}` output\n"
            )
            sys.exit(1)

    for thm, axs in parsed.items():
        disallowed = [a for a in axs if a not in ALLOWED_AXIOMS]
        if disallowed:
            sys.stderr.write(
                f"FAIL: theorem {thm!r} uses non-standard axioms: {disallowed}\n"
            )
            sys.exit(1)

    return parsed


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    env = build_env()

    lean_files, line_counts = check_lean_sources(root)
    print(f"OK [tokens]: checked {lean_files} (zero forbidden tokens, zero Mathlib imports)")
    for name in lean_files:
        print(f"  {name}: {line_counts[name]} lines")

    _, _, lake_ms = run_checked(["lake", "build"], root, env, "lake build")
    print(f"OK [lake build]: 0 warnings, {lake_ms} ms")

    out_sa, err_sa, sa_ms = run_checked(
        ["lean", "-j", "4", "SubQuorumNG.lean"],
        root,
        env,
        "lean SubQuorumNG.lean",
    )
    if out_sa.strip() or err_sa.strip():
        sys.stderr.write(
            f"FAIL [lean SubQuorumNG.lean]: unexpected output:\n{out_sa}{err_sa}\n"
        )
        sys.exit(1)
    print(f"OK [lean SubQuorumNG.lean]: standalone check clean, {sa_ms} ms")

    lp_out, _, _ = run_checked(
        ["lake", "env", "printenv", "LEAN_PATH"],
        root,
        env,
        "lake env printenv LEAN_PATH",
    )
    ax_env = dict(env)
    ax_env["LEAN_PATH"] = lp_out.strip()
    ax_out, _, ax_ms = run_checked(
        ["lean", "-j", "4", "CheckAxioms.lean"],
        root,
        ax_env,
        "lean CheckAxioms.lean",
    )
    parsed_axioms = parse_and_verify_axioms(ax_out)
    print(f"OK [lean CheckAxioms.lean]: verified standard axioms ({ax_ms} ms):")
    for thm, axs in parsed_axioms.items():
        print(f"  {thm}: {axs}")

    print("PASS: all Lean 4.36.0 verification gates succeeded.")


if __name__ == "__main__":
    main()
