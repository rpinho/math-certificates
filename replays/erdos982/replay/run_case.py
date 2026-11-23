"""Build one canonical case, solve it, and harvest independent checker evidence."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys

from jobrun import ROOT, run

CADICAL = ROOT / "upstream/cadical/build/cadical"
CAKE = ROOT / "upstream/cake_lpr/cake_lpr"
DRAT = ROOT / "upstream/drat-trim/drat-trim"
CAKE_ARGS = [CAKE, "--CML_HEAP_SIZE=1400", "--CML_STACK_SIZE=256"]


def digest(path):
    with path.open("rb") as stream:
        return sha256_file(stream)


def sha256_file(stream):
    h = sha256()
    while data := stream.read(1 << 20):
        h.update(data)
    return h.hexdigest()


def dimacs(path):
    clauses = []
    with path.open() as stream:
        for line in stream:
            row = line.split()
            if not row or row[0] in ("c", "p"):
                continue
            assert row[-1] == "0"
            clauses.append(tuple(sorted(map(int, row[:-1]))))
    return clauses


def proof_controls(folder, cnf, lrat, core, baseline_clauses):
    bad_proof = folder / "corrupted.lrat"
    # Embedded LRAT declarations can occur after the final addition. Remove the
    # actual empty addition and preserve every other byte.
    removed = []
    with lrat.open("rb") as source, bad_proof.open("wb") as target:
        for line in source:
            parts = line.split(maxsplit=2)
            if len(parts) >= 2 and parts[1] == b"0":
                removed.append(int(parts[0]))
            else:
                target.write(line)
    if not removed:
        raise RuntimeError("no empty addition to corrupt")
    run([*CAKE_ARGS, cnf, bad_proof], folder / "corrupted.log", 300)
    corruption = (folder / "corrupted.log").read_text()
    if "s VERIFIED UNSAT" in corruption or "empty clause not derived" not in corruption:
        raise RuntimeError("proof corruption was not rejected as expected")
    bad_proof.unlink()
    original_ids = {clause: i for i, clause in enumerate(baseline_clauses, 1)}
    in_core = {original_ids[clause] for clause in core}
    candidates = []
    with lrat.open() as stream:
        for line in stream:
            parts = line.split()
            if not parts or parts[1] == "d":
                continue
            end_literals = parts.index("0", 1)
            ids = map(int, parts[end_literals+1:-1])
            for ref in ids:
                if ref in in_core and ref not in candidates:
                    candidates.append(ref)
                    if len(candidates) >= 16:
                        break
            if len(candidates) >= 16:
                break
    bad_cnf = folder / "altered.cnf"
    for cid in candidates:
        with cnf.open() as source, bad_cnf.open("w") as target:
            target.write(next(source))
            for i, line in enumerate(source, 1):
                target.write("-1 1 0\n" if i == cid else line)
        run([*CAKE_ARGS, bad_cnf, lrat], folder / f"altered_{cid}.log", 300)
        result = (folder / f"altered_{cid}.log").read_text()
        if "s VERIFIED UNSAT" not in result and ("failed" in result or "error" in result.lower()):
            print("altered control rejected:", cid, baseline_clauses[cid-1])
            return {"removed_empty_ids": removed, "altered_core_id": cid,
                    "original_clause": baseline_clauses[cid-1], "replacement": [-1,1],
                    "altered_cnf_sha256": digest(bad_cnf)}
    raise RuntimeError("no attempted core mutation was specifically rejected")


def build(folder, n, k, omit, fan=False):
    cnf = folder / "formula.cnf"
    second = folder / "reference.cnf"
    mapping = folder / "families.tsv"
    skip = [argument for family in omit for argument in ("--omit", family)]
    if fan:
        skip.append("--fan")
    for script, target, extra in (("encoder.py", cnf, ["--families", str(mapping)]),
                                  ("encoder_reference.py", second, [])):
        rc, reason = run([sys.executable, script, n, k, target, *extra, *skip],
                         folder / (script + ".log"), 180)
        if rc or reason:
            raise RuntimeError(f"{script} failed: {rc} {reason}")
    left, right = digest(cnf), digest(second)
    if left != right:
        raise RuntimeError("Canonical CNFs disagree")
    (folder / "CNF_SHA256.txt").write_text(f"{left}  formula.cnf\n{right}  reference.cnf\n")
    second.unlink()
    return cnf, mapping, left


def compress(proof):
    target = proof.with_suffix(proof.suffix+".gz")
    with proof.open("rb") as source, target.open("wb") as raw, \
            gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=3) as output:
        shutil.copyfileobj(source, output, 1 << 20)
    with gzip.open(target, "rb") as stream:
        assert sha256_file(stream) == digest(proof)
    proof.unlink()


def case(n, k, name, budget, omit, controls, fan=False):
    folder = ROOT / "runs" / name
    folder.mkdir(exist_ok=False)
    cnf, mapping, hash_cnf = build(folder, n, k, omit, fan)
    lrat = folder / "proof.lrat"
    drat = folder / "proof.drat"
    rc, reason = run([CADICAL, "--lrat", "--no-binary", cnf, lrat],
                     folder / "cadical-lrat.log", budget, solve=True)
    stats = {"n":n, "k":k, "omitted":omit, "cnf_sha256":hash_cnf, "fan":fan}
    if rc == 10:
        clauses = dimacs(cnf)
        model = {int(literal) for line in (folder/"cadical-lrat.log").read_text().splitlines()
                 if line.startswith("v ") for literal in line[2:].split() if literal != "0"}
        assert model and all(-literal not in model for literal in model)
        assert all(any(literal in model for literal in clause) for clause in clauses)
        stats["verification"] = "SAT model checked against every canonical clause"
        (folder / "model.txt").write_text(" ".join(map(str, sorted(model, key=abs)))+"\n")
        lrat.unlink(missing_ok=True)
    elif rc == 20:
        cake_log = folder / "cake.log"
        run([*CAKE_ARGS, cnf, lrat], cake_log, 600)
        if "s VERIFIED UNSAT" not in cake_log.read_text():
            raise RuntimeError("cake_lpr failed")
        rc2, reason2 = run([CADICAL, cnf, drat], folder / "cadical-drat.log", budget, solve=True)
        if rc2 != 20:
            raise RuntimeError(f"DRAT run failed: {rc2} {reason2}")
        core_file = folder / "core.cnf"
        drat_log = folder / "drat-trim.log"
        run([DRAT, cnf, drat, "-c", core_file], drat_log, 600)
        if "s VERIFIED" not in drat_log.read_text():
            raise RuntimeError("drat-trim failed")
        original = dimacs(cnf)
        index = {clause: i for i, clause in enumerate(original, 1)}
        core = dimacs(core_file)
        assert len(set(core)) == len(core)
        families = dict(line.split("\t") for line in mapping.read_text().splitlines())
        core_counts = Counter()
        with (folder/"core_families.tsv").open("w") as output:
            print("clause_id\tfamilies", file=output)
            for cid in sorted(index[clause] for clause in core):
                family = families[str(cid)]
                print(cid, family, sep="\t", file=output)
                core_counts.update(family.split(","))
        stats.update(verification="UNSAT via cake_lpr LRAT and drat-trim DRAT",
                     core_clauses=len(core), core_families=core_counts)
        if controls:
            stats["negative_controls"] = proof_controls(folder, cnf, lrat, core, original)
        stats["proof_sha256"] = {proof.name: digest(proof) for proof in (lrat,drat)}
        for proof in (lrat,drat):
            compress(proof)
    else:
        stats["verification"] = "UNRESOLVED"
        stats["stop_reason"] = reason or f"solver exit {rc}"
        if lrat.exists():
            stats["partial_lrat_sha256"] = digest(lrat)
            lrat.unlink()
    (folder / "result.json").write_text(json.dumps(stats, indent=2, sort_keys=True)+"\n")
    print(name, stats["verification"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("k", type=int)
    parser.add_argument("name")
    parser.add_argument("--budget", type=int, default=180)
    parser.add_argument("--omit", action="append", default=[])
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--fan", action="store_true")
    args = parser.parse_args()
    case(args.n, args.k, args.name, args.budget, args.omit, args.controls, args.fan)
