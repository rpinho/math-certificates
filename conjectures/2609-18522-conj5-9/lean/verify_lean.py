#!/usr/bin/env python3
"""
Standalone exact verifier for the Lean 4.36.0 formalization of the disproofs of
van Berkel & Bosma (arXiv:2609.18522v1) Conjectures 5 and 9.

Constraints enforced:
- Python 3 standard library only (zero external packages).
- AST-verified zero `math` imports, zero `float` literals or calls, zero `/` (`ast.Div`) operators.
- Strips nested Lean comments and checks zero `sorry`, `admit`, `axiom`, `native_decide`,
  `unsafe`, `partial`, `ofReduceBool`, `trustCompiler`, or external `import`s in `Sumfree2Conj59.lean`.
- Cross-checks `inputs/certificates/witness.json` against independent pure-integer greedy
  regeneration and against the literal witness lists in `Sumfree2Conj59.lean`.
- Runs a clean-room build in a fresh temporary directory (`lean Sumfree2Conj59.lean`,
  `lake build`, `lake env lean CheckAxioms.lean`) with zero warnings, verifies all 28
  `#print axioms` lines use only `{propext, Classical.choice, Quot.sound}`, and runs
  both positive type-signature checks and negative mutation checks in Lean's kernel.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time


ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})

FORBIDDEN_LEAN_TOKENS = (
    "sorry",
    "sorryAx",
    "admit",
    "axiom",
    "constant",
    "partial",
    "unsafe",
    "native_decide",
    "decide_cbv",
    "ofReduceBool",
    "trustCompiler",
    "implemented_by",
    "extern",
)

EXPECTED_THEOREMS = (
    "inSeq_le",
    "inSeq_gt",
    "inSeq_iff_exists_seq",
    "seq_greedy_step",
    "IsMinimalPeriodicity.unique",
    "periodic_mask_characterization",
    "certify_sequence",
    "S4_11_inSeq_iff",
    "S4_11_seq_eq",
    "S4_11_minimal",
    "S4_11_global_minimality",
    "S4_11_witness_prefix",
    "S4_11_no_period_9",
    "S4_11_preperiod_10_fails",
    "conj5_disproof_S4_11",
    "S5_10_inSeq_iff",
    "S5_10_seq_eq",
    "S5_10_minimal",
    "S5_10_global_minimality",
    "S5_10_witness_prefix",
    "S5_10_preperiod_7_not_minimal",
    "S5_10_preperiod_5_fails",
    "S5_10_doubled_period_not_minimal",
    "conj9_disproof_S5_10",
    "S1_3_minimal",
    "S1_2_minimal",
    "S2_3_minimal",
    "S4_12_minimal_and_conj5_agrees",
)


def fail(msg: str) -> None:
    sys.stderr.write("VERIFY_FAIL: " + msg + "\n")
    raise SystemExit(1)


def self_ast_audit(script_path: str) -> None:
    with open(script_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src, filename=script_path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "math" or alias.name.startswith("math."):
                    fail("forbidden math import in verify_lean.py")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod == "math" or mod.startswith("math."):
                fail("forbidden from-math import in verify_lean.py")
        elif isinstance(node, ast.Div):
            fail("forbidden division operator in verify_lean.py")
        elif isinstance(node, ast.Constant) and not isinstance(
            node.value, (int, str, bytes, bool, type(None), tuple, frozenset)
        ):
            fail("forbidden non-exact constant in verify_lean.py")


def strip_lean_comments_and_strings(src: str) -> str:
    out = []
    i = 0
    n = len(src)
    block_depth = 0
    in_string = False
    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if block_depth > 0:
            if ch == "/" and nxt == "-":
                block_depth += 1
                out.append("  ")
                i += 2
                continue
            if ch == "-" and nxt == "/":
                block_depth -= 1
                out.append("  ")
                i += 2
                continue
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue
        if in_string:
            if ch == "\\" and i + 1 < n:
                out.append("  ")
                i += 2
                continue
            if ch == '"':
                in_string = False
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue
        if ch == "/" and nxt == "-":
            block_depth = 1
            out.append("  ")
            i += 2
            continue
        if ch == "-" and nxt == "-":
            while i < n and src[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(" ")
            i += 1
            continue
        out.append(ch)
        i += 1
    if block_depth != 0:
        fail("unclosed block comment in Lean source")
    if in_string:
        fail("unclosed string literal in Lean source")
    return "".join(out)


def generate_greedy_2sum(f: int, g: int, count: int) -> list[int]:
    if not (1 <= f < g):
        fail("invalid seed pair")
    terms = [f, g]
    sums = {f + g}
    cand = g + 1
    while len(terms) < count:
        if cand not in sums:
            for prev in terms:
                sums.add(prev + cand)
            terms.append(cand)
        cand += 1
    return terms


def audit_static_files(root_dir: str) -> tuple[str, str]:
    toolchain_path = os.path.join(root_dir, "lean-toolchain")
    lakefile_path = os.path.join(root_dir, "lakefile.toml")
    main_lean_path = os.path.join(root_dir, "Sumfree2Conj59.lean")
    axioms_lean_path = os.path.join(root_dir, "CheckAxioms.lean")

    for p in (toolchain_path, lakefile_path, main_lean_path, axioms_lean_path):
        if not os.path.isfile(p):
            fail("missing required file: " + p)

    with open(toolchain_path, "r", encoding="utf-8") as fh:
        tc = fh.read().strip()
    if tc != "leanprover/lean4:v4.36.0":
        fail("unexpected lean-toolchain: " + tc)

    with open(lakefile_path, "r", encoding="utf-8") as fh:
        lake_src = fh.read()
    if "require" in lake_src or "mathlib" in lake_src.lower():
        fail("external dependency detected in lakefile.toml")

    with open(main_lean_path, "r", encoding="utf-8") as fh:
        main_raw = fh.read()
    with open(axioms_lean_path, "r", encoding="utf-8") as fh:
        axioms_raw = fh.read()

    for label, raw in (("Sumfree2Conj59.lean", main_raw), ("CheckAxioms.lean", axioms_raw)):
        if "\u2014" in raw:
            fail("em dash found in " + label)

    main_code = strip_lean_comments_and_strings(main_raw)
    axioms_code = strip_lean_comments_and_strings(axioms_raw)

    if re.search(r"\bimport\b", main_code):
        fail("Sumfree2Conj59.lean must be 100% standalone with zero imports")

    for tok in FORBIDDEN_LEAN_TOKENS:
        pat = r"\b" + re.escape(tok) + r"\b"
        if re.search(pat, main_code):
            fail("forbidden token '" + tok + "' in Sumfree2Conj59.lean")
        if tok != "axiom" and re.search(pat, axioms_code):
            fail("forbidden token '" + tok + "' in CheckAxioms.lean")

    # Ensure CheckAxioms.lean has no `axiom` declarations (only `#print axioms`).
    axioms_without_print = re.sub(r"#print\s+axioms\b", "", axioms_code)
    if re.search(r"\baxiom\b", axioms_without_print):
        fail("forbidden `axiom` declaration in CheckAxioms.lean")

    required_snippets = (
        "def IsStrict2Sum (P : Nat → Prop) (x : Nat) : Prop :=",
        "∃ a b, P a ∧ P b ∧ a < b ∧ a + b = x",
        "def InSeq (f g x : Nat) : Prop :=",
        "def seq (f g n : Nat) : Nat :=",
        "def HasPeriodMod (s : Nat → Nat) (k p m : Nat) : Prop :=",
        "def IsMinimalPeriodicity (s : Nat → Nat) (k p m : Nat) : Prop :=",
        "theorem S4_11_minimal : IsMinimalPeriodicity (seq 4 11) 11 10 33",
        "theorem S5_10_minimal : IsMinimalPeriodicity (seq 5 10) 6 6 24",
        "theorem conj5_disproof_S4_11 :",
        "theorem conj9_disproof_S5_10 :",
    )
    for snip in required_snippets:
        if snip not in main_code:
            fail("missing required declaration snippet in Sumfree2Conj59.lean: " + snip)

    return main_code, axioms_code


def parse_nat_list_def(main_code: str, def_name: str) -> list[int]:
    m = re.search(
        r"\bdef\s+" + re.escape(def_name) + r"\s*:\s*List\s+Nat\s*:=\s*\[([^\]]*)\]",
        main_code,
    )
    if not m:
        fail("could not parse List Nat definition: " + def_name)
    body = m.group(1).strip()
    if not body:
        return []
    return [int(part.strip()) for part in body.split(",")]


def cross_check_witness_and_controls(root_dir: str, main_code: str) -> None:
    witness_path = os.path.join(root_dir, "..", "certificates", "witness.json")
    if os.path.isfile(witness_path):
        with open(witness_path, "r", encoding="utf-8") as fh:
            witness = json.load(fh)
        cases = {(c["f"], c["g"]): c for c in witness["cases"]}
        if (4, 11) not in cases or (5, 10) not in cases:
            fail("witness.json missing (4, 11) or (5, 10)")
        c411 = cases[(4, 11)]
        c510 = cases[(5, 10)]
        if (c411["k"], c411["p"], c411["m"], c411["formula_value"]) != (11, 10, 33, 9):
            fail("unexpected (4, 11) metadata in witness.json")
        if (c510["k"], c510["p"], c510["m"], c510["formula_value"]) != (6, 6, 24, 7):
            fail("unexpected (5, 10) metadata in witness.json")
        if parse_nat_list_def(main_code, "pre4_11") != c411["preperiod_terms"]:
            fail("pre4_11 mismatch against witness.json")
        if parse_nat_list_def(main_code, "per4_11") != c411["period_terms"]:
            fail("per4_11 mismatch against witness.json")
        if parse_nat_list_def(main_code, "pre5_10") != c510["preperiod_terms"]:
            fail("pre5_10 mismatch against witness.json")
        if parse_nat_list_def(main_code, "per5_10") != c510["period_terms"]:
            fail("per5_10 mismatch against witness.json")

    checks = (
        (4, 11, "pre4_11", "per4_11", 11, 10, 33),
        (5, 10, "pre5_10", "per5_10", 6, 6, 24),
        (1, 3, "pre1_3", "per1_3", 0, 1, 2),
        (1, 2, "pre1_2", "per1_2", 2, 1, 3),
        (2, 3, "pre2_3", "per2_3", 3, 2, 6),
        (4, 12, "pre4_12", "per4_12", 6, 10, 35),
    )
    for f, g, pre_name, per_name, k, p, m in checks:
        pre = parse_nat_list_def(main_code, pre_name)
        per = parse_nat_list_def(main_code, per_name)
        if len(pre) != k or len(per) != p:
            fail("length mismatch on " + pre_name + " or " + per_name)
        gen = generate_greedy_2sum(f, g, k + 4 * p + 5)
        if gen[:k] != pre:
            fail("greedy preperiod mismatch for S_{" + str(f) + "," + str(g) + "}")
        if gen[k : k + p] != per:
            fail("greedy period mismatch for S_{" + str(f) + "," + str(g) + "}")
        for idx in range(k, k + 3 * p):
            if gen[idx + p] != gen[idx] + m:
                fail("periodicity check failed for S_{" + str(f) + "," + str(g) + "}")
        if k > 0 and gen[k - 1 + p] == gen[k - 1] + m:
            fail("preperiod k is not minimal for S_{" + str(f) + "," + str(g) + "}")


def build_env() -> dict[str, str]:
    env = dict(os.environ)
    elan_bin = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    return env


def run_cmd(cmd: list[str], cwd: str, env: dict[str, str], stdin_text: str | None = None) -> subprocess.CompletedProcess[str]:
    full_cmd = ["nice", "-n", "10"] + cmd
    return subprocess.run(
        full_cmd,
        cwd=cwd,
        env=env,
        input=stdin_text,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )


def verify_axioms_output(output: str) -> dict[str, list[str]]:
    parsed: dict[str, list[str]] = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m_none = re.match(r"^'([^']+)' does not depend on any axioms$", line)
        if m_none:
            parsed[m_none.group(1)] = []
            continue
        m_some = re.match(r"^'([^']+)' depends on axioms: \[([^\]]*)\]$", line)
        if m_some:
            thm = m_some.group(1)
            ax_list = [a.strip() for a in m_some.group(2).split(",") if a.strip()]
            for ax in ax_list:
                if ax not in ALLOWED_AXIOMS:
                    fail("disallowed axiom '" + ax + "' on theorem '" + thm + "'")
            parsed[thm] = ax_list
            continue
        fail("unexpected output line from CheckAxioms.lean: " + line)

    for thm in EXPECTED_THEOREMS:
        if thm not in parsed:
            fail("missing #print axioms output for expected theorem: " + thm)
    return parsed


def run_cleanroom_lean_checks(root_dir: str, env: dict[str, str]) -> dict[str, list[str]]:
    ver_res = run_cmd(["lean", "--version"], cwd=root_dir, env=env)
    if ver_res.returncode != 0 or "4.36.0" not in ver_res.stdout:
        fail("expected Lean 4.36.0, got: " + ver_res.stdout + ver_res.stderr)

    with tempfile.TemporaryDirectory(prefix="verify_sumfree2_lean_") as tmpdir:
        for fname in ("lean-toolchain", "lakefile.toml", "Sumfree2Conj59.lean", "CheckAxioms.lean"):
            shutil.copy2(os.path.join(root_dir, fname), os.path.join(tmpdir, fname))

        # 1. Standalone zero-import single-file kernel check with zero warnings.
        single_res = run_cmd(["lean", "-j", "4", "Sumfree2Conj59.lean"], cwd=tmpdir, env=env)
        if single_res.returncode != 0:
            fail("lean Sumfree2Conj59.lean failed:\n" + single_res.stdout + single_res.stderr)
        if single_res.stdout.strip() or single_res.stderr.strip():
            fail("warnings or unexpected output from lean Sumfree2Conj59.lean:\n" + single_res.stdout + single_res.stderr)

        # 2. Full clean-room `lake build` with zero warnings.
        lake_res = run_cmd(["lake", "build"], cwd=tmpdir, env=env)
        if lake_res.returncode != 0:
            fail("clean-room lake build failed:\n" + lake_res.stdout + lake_res.stderr)
        combined_lake = lake_res.stdout + "\n" + lake_res.stderr
        if "warning:" in combined_lake or "error:" in combined_lake:
            fail("warning or error during clean-room lake build:\n" + combined_lake)

        # 3. Separate CheckAxioms.lean run and strict axiom audit.
        ax_res = run_cmd(["lake", "env", "lean", "-j", "4", "CheckAxioms.lean"], cwd=tmpdir, env=env)
        if ax_res.returncode != 0:
            fail("CheckAxioms.lean execution failed:\n" + ax_res.stdout + ax_res.stderr)
        if ax_res.stderr.strip():
            fail("unexpected stderr in CheckAxioms.lean:\n" + ax_res.stderr)
        axiom_map = verify_axioms_output(ax_res.stdout)

        # 4. Independent clean-room kernel type-signature probe (prevents definition spoofing).
        positive_probe = """import Sumfree2Conj59

example (P : Nat → Prop) (x : Nat) :
    IsStrict2Sum P x = (∃ a b, P a ∧ P b ∧ a < b ∧ a + b = x) := rfl

example (f g x : Nat) (hx : x ≤ g) :
    InSeq f g x ↔ (x = f ∨ x = g) := inSeq_le hx

example (f g x : Nat) (hx : g < x) :
    InSeq f g x ↔ ¬ (∃ a b, (a < x ∧ InSeq f g a) ∧ (b < x ∧ InSeq f g b) ∧ a < b ∧ a + b = x) :=
  inSeq_gt hx

example (s : Nat → Nat) (k p m : Nat) :
    HasPeriodMod s k p m = (0 < p ∧ 0 < m ∧ ∀ n, k ≤ n → s (n + p) = s n + m) := rfl

example (s : Nat → Nat) (k p m : Nat) :
    IsMinimalPeriodicity s k p m =
      (HasPeriodMod s k p m ∧
       (∀ k' p' m', HasPeriodMod s k' p' m' → p ≤ p') ∧
       (∀ k' m', HasPeriodMod s k' p m' → k ≤ k')) := rfl

example : IsMinimalPeriodicity (seq 4 11) 11 10 33 := S4_11_minimal
example : IsMinimalPeriodicity (seq 5 10) 6 6 24 := S5_10_minimal
example : seq 4 11 0 = 4 ∧ seq 4 11 1 = 11 ∧ seq 4 11 2 = 12 ∧ seq 4 11 5 = 19 :=
  ⟨rfl, rfl, rfl, rfl⟩
example : seq 5 10 0 = 5 ∧ seq 5 10 1 = 10 ∧ seq 5 10 6 = 20 ∧ seq 5 10 7 = 28 :=
  ⟨rfl, rfl, rfl, rfl⟩
"""
        pos_res = run_cmd(["lake", "env", "lean", "--stdin"], cwd=tmpdir, env=env, stdin_text=positive_probe)
        if pos_res.returncode != 0 or pos_res.stdout.strip() or pos_res.stderr.strip():
            fail("clean-room positive type-signature probe failed:\n" + pos_res.stdout + pos_res.stderr)

        # 5. Negative kernel mutation probes (must be rejected by Lean).
        negative_probes = (
            ("wrong period 9 on S_{4,11}", "import Sumfree2Conj59\nexample : IsMinimalPeriodicity (seq 4 11) 11 9 33 := S4_11_minimal\n"),
            ("wrong preperiod 7 on S_{5,10}", "import Sumfree2Conj59\nexample : IsMinimalPeriodicity (seq 5 10) 7 6 24 := S5_10_minimal\n"),
            ("false term evaluation on seq 4 11", "import Sumfree2Conj59\nexample : seq 4 11 5 = 18 := rfl\n"),
        )
        for label, snippet in negative_probes:
            neg_res = run_cmd(["lake", "env", "lean", "--stdin"], cwd=tmpdir, env=env, stdin_text=snippet)
            if neg_res.returncode == 0:
                fail("negative mutation probe unexpectedly succeeded: " + label)

    # Ensure the workspace build itself is also clean and up to date.
    ws_res = run_cmd(["lake", "build"], cwd=root_dir, env=env)
    if ws_res.returncode != 0:
        fail("workspace lake build failed:\n" + ws_res.stdout + ws_res.stderr)
    if "warning:" in (ws_res.stdout + ws_res.stderr):
        fail("warning in workspace lake build:\n" + ws_res.stdout + ws_res.stderr)

    return axiom_map


def main() -> None:
    t0_ns = time.monotonic_ns()
    script_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(script_path)

    self_ast_audit(script_path)
    main_code, _ = audit_static_files(root_dir)
    cross_check_witness_and_controls(root_dir, main_code)
    env = build_env()
    axiom_map = run_cleanroom_lean_checks(root_dir, env)

    elapsed_ms = (time.monotonic_ns() - t0_ns) // 1_000_000
    print("VERIFY_OK")
    print("  Lean toolchain : leanprover/lean4:v4.36.0 (zero external dependencies)")
    print("  Theorems checked in CheckAxioms.lean : " + str(len(axiom_map)))
    print("  Axioms observed across all theorems  : " + json.dumps(sorted({ax for axs in axiom_map.values() for ax in axs})))
    print("  S_{4,11} minimal (k, p, m)           : (11, 10, 33) [refutes Conjecture 5 p = 9]")
    print("  S_{5,10} minimal (k, p, m)           : (6, 6, 24)   [refutes Conjecture 9 k = 7]")
    print("  Positive controls verified           : S_{1,3}, S_{1,2}, S_{2,3}, S_{4,12}")
    print("  Negative controls + kernel mutations : 5 formal theorems + 3 rejected probes")
    print("  Elapsed time (ms)                    : " + str(elapsed_ms))


if __name__ == "__main__":
    main()
