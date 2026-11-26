#!/usr/bin/env python3
"""Standalone verification script for SumfreeConj4 Lean 4.36.0 formalization.

Uses Python standard library only and integer-only operations.
Checks:
1. Toolchain lock (`leanprover/lean4:v4.36.0`) and zero external Lake dependencies.
2. Zero forbidden Lean tokens (`sorry`, `axiom`, `admit`, `native_decide`, `unsafe`,
   `implemented_by`, `extern`, `ofReduceBool`, `trustCompiler`) and zero em dashes.
3. Presence of required definitions and main theorems in `SumfreeConj4.lean`.
4. Clean `lake build` under `nice -n 10` with bounded threads (`<= 4`) and RSS (`<= 2 GB`).
5. `#print axioms` output from `CheckAxioms.lean` uses only standard Lean foundations
   (`propext`, `Classical.choice`, `Quot.sound`, or none).
"""

import os
import re
import subprocess
import sys


ALLOWED_AXIOMS = frozenset(["propext", "Classical.choice", "Quot.sound"])

FORBIDDEN_LEAN_PATTERNS = [
    r"\bsorry\b",
    r"\baxiom\b",
    r"\badmit\b",
    r"\bnative_decide\b",
    r"\bunsafe\b",
    r"\bimplemented_by\b",
    r"\bextern\b",
    r"\bofReduceBool\b",
    r"\btrustCompiler\b",
]

REQUIRED_DECLARATIONS = [
    r"def\s+IsStrict3Sum\s*\(S\s*:\s*Nat\s*→\s*Prop\)\s*\(x\s*:\s*Nat\)\s*:\s*Prop",
    r"def\s+InSeq\s*\(d\s*:\s*Nat\)\s*:\s*Nat\s*→\s*Prop",
    r"def\s+seq\s*\(d\s*:\s*Nat\)\s*:\s*Nat\s*→\s*Nat",
    r"def\s+HasPeriodMod\s*\(seq\s*:\s*Nat\s*→\s*Nat\)\s*\(k\s+p\s+m\s*:\s*Nat\)\s*:\s*Prop",
    r"def\s+IsMinimalPeriodicity\s*\(seq\s*:\s*Nat\s*→\s*Nat\)\s*\(k\s+p\s+m\s*:\s*Nat\)\s*:\s*Prop",
    r"theorem\s+d3_minimal\s*:\s*IsMinimalPeriodicity\s+\(seq\s+3\)\s+5\s+1\s+5",
    r"theorem\s+d4_minimal\s*:\s*IsMinimalPeriodicity\s+\(seq\s+4\)\s+7\s+3\s+27",
    r"theorem\s+d5_minimal\s*:\s*IsMinimalPeriodicity\s+\(seq\s+5\)\s+13\s+10\s+104",
    r"theorem\s+all_d_ge_6_minimal\s*\(d\s*:\s*Nat\)\s*\(hd\s*:\s*d\s*≥\s*6\)\s*:\s*"
    r"IsMinimalPeriodicity\s+\(seq\s+d\)\s+\(d\s*\+\s*3\)\s+d\s+\(8\s*\*\s*d\s*-\s*3\)",
]

REQUIRED_AXIOM_TARGETS = [
    "d3_minimal",
    "d4_minimal",
    "d5_minimal",
    "all_d_ge_6_minimal",
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def read_text(root: str, rel: str) -> str:
    full = os.path.join(root, rel)
    if not os.path.isfile(full):
        fail(f"Missing required file: {rel}")
    with open(full, "r", encoding="utf-8") as handle:
        return handle.read()


def build_env() -> dict:
    env = dict(os.environ)
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    cur_path = env.get("PATH", "")
    if elan_bin not in cur_path.split(os.pathsep):
        env["PATH"] = elan_bin + os.pathsep + cur_path
    return env


def parse_axiom_output(output: str) -> dict:
    found = {}
    no_ax_re = re.compile(r"^'([^']+)'\s+does not depend on any axioms\s*$")
    dep_ax_re = re.compile(r"^'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]\s*$")
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m_none = no_ax_re.match(line)
        if m_none:
            found[m_none.group(1)] = []
            continue
        m_dep = dep_ax_re.match(line)
        if m_dep:
            items = [tok.strip() for tok in m_dep.group(2).split(",") if tok.strip()]
            found[m_dep.group(1)] = items
            continue
        fail(f"Unexpected output line from CheckAxioms.lean: {line}")
    return found


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))

    # 1. Toolchain and standalone Lake config check
    toolchain = read_text(root, "lean-toolchain").strip()
    if toolchain != "leanprover/lean4:v4.36.0":
        fail(f"Expected lean-toolchain 'leanprover/lean4:v4.36.0', got '{toolchain}'")

    lakefile = read_text(root, "lakefile.toml")
    if "[[require]]" in lakefile or "git" in lakefile.lower():
        fail("lakefile.toml must have zero external dependencies")

    # 2. Forbidden token and em-dash scan
    lean_files = ["SumfreeConj4.lean", "CheckAxioms.lean"]
    for fname in lean_files:
        src = read_text(root, fname)
        if "\u2014" in src:
            fail(f"Em dash found in {fname}")
        for pat in FORBIDDEN_LEAN_PATTERNS:
            match = re.search(pat, src)
            if match:
                line_no = src[: match.start()].count("\n") + 1
                fail(f"Forbidden pattern '{pat}' found in {fname} at line {line_no}")

    for doc_name in ["STATUS.md", "REPORT.md", "PRIOR_ART.md"]:
        doc_full = os.path.join(root, doc_name)
        if os.path.isfile(doc_full):
            doc_txt = read_text(root, doc_name)
            if "\u2014" in doc_txt:
                fail(f"Em dash found in {doc_name}")

    # 3. Required declarations check
    main_src = read_text(root, "SumfreeConj4.lean")
    for decl_pat in REQUIRED_DECLARATIONS:
        if not re.search(decl_pat, main_src, flags=re.MULTILINE):
            fail(f"Missing required declaration matching: {decl_pat}")

    # 4. Clean Lake build (bounded threads and memory)
    env = build_env()
    build_cmd = ["nice", "-n", "10", "lake", "build", "--", "-j", "4", "-M", "1800"]
    proc_build = subprocess.run(
        build_cmd,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    combined_build = (proc_build.stdout or "") + "\n" + (proc_build.stderr or "")
    if proc_build.returncode != 0:
        fail(f"lake build failed with exit code {proc_build.returncode}:\n{combined_build}")
    if "warning:" in combined_build.lower() or "sorry" in combined_build.lower():
        fail(f"lake build emitted warnings or sorry diagnostics:\n{combined_build}")

    # 5. Exact #print axioms check via CheckAxioms.lean
    ax_cmd = [
        "nice",
        "-n",
        "10",
        "lake",
        "env",
        "lean",
        "-j",
        "4",
        "-M",
        "1800",
        "CheckAxioms.lean",
    ]
    proc_ax = subprocess.run(
        ax_cmd,
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_ax.returncode != 0:
        fail(
            f"CheckAxioms.lean failed with exit code {proc_ax.returncode}:\n"
            f"{proc_ax.stdout}\n{proc_ax.stderr}"
        )
    if proc_ax.stderr.strip():
        fail(f"CheckAxioms.lean emitted stderr diagnostics:\n{proc_ax.stderr}")

    axioms_map = parse_axiom_output(proc_ax.stdout)
    for thm in REQUIRED_AXIOM_TARGETS:
        if thm not in axioms_map:
            fail(f"Missing #print axioms output for '{thm}'")
        bad = [ax for ax in axioms_map[thm] if ax not in ALLOWED_AXIOMS]
        if bad:
            fail(f"Theorem '{thm}' uses disallowed axioms: {bad}")

    print("PASS: toolchain leanprover/lean4:v4.36.0 verified (standalone, zero external deps)")
    print("PASS: zero forbidden tokens and zero em dashes")
    print("PASS: required definitions and theorem signatures present")
    print("PASS: clean lake build succeeded with zero warnings")
    for thm in sorted(axioms_map.keys()):
        print(f"PASS: axioms({thm}) = {axioms_map[thm]}")


if __name__ == "__main__":
    main()
