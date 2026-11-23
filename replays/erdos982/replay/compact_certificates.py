"""Retain independently checked trimmed proofs when full proof archives are large."""
import argparse
import gzip
import json
from pathlib import Path
import shutil

from jobrun import ROOT, run
from run_case import CAKE_ARGS, DRAT, digest, sha256_file, compress

TRIM = ROOT / "upstream/cadical/build/lrat-trim"


def unpack(archive, raw):
    with gzip.open(archive, "rb") as source, raw.open("wb") as target:
        shutil.copyfileobj(source, target, 1 << 20)


def compact(folder):
    result_file = folder / "result.json"
    result = json.loads(result_file.read_text())
    if "proof_sha256" not in result or "trimmed_proof_sha256" in result:
        return
    cnf = folder / "formula.cnf"
    lrat, drat = (folder/file for file in ("proof.lrat", "proof.drat"))
    full_lrat, full_drat = (file.with_suffix(file.suffix+".gz") for file in (lrat,drat))
    trimmed_lrat, trimmed_drat = (folder/file for file in ("trimmed.lrat", "trimmed.drat"))

    unpack(full_lrat, lrat)
    assert digest(lrat) == result["proof_sha256"]["proof.lrat"]
    rc, reason = run([TRIM, cnf, lrat, trimmed_lrat], folder/"lrat-trim.log", 600)
    assert rc == 20 and not reason, (rc, reason)
    run([*CAKE_ARGS, cnf, trimmed_lrat], folder/"cake-trimmed.log", 600)
    assert "s VERIFIED UNSAT" in (folder/"cake-trimmed.log").read_text()
    lrat.unlink()

    unpack(full_drat, drat)
    assert digest(drat) == result["proof_sha256"]["proof.drat"]
    run([DRAT, cnf, drat, "-l", trimmed_drat, "-C"], folder/"drat-export.log", 600)
    assert "s VERIFIED" in (folder/"drat-export.log").read_text()
    run([DRAT, cnf, trimmed_drat], folder/"drat-trimmed.log", 600)
    assert "s VERIFIED" in (folder/"drat-trimmed.log").read_text()
    drat.unlink()

    retained = [trimmed_lrat, trimmed_drat]
    result["trimmed_proof_sha256"] = {path.name: digest(path) for path in retained}
    for path in retained:
        compress(path)
        with gzip.open(path.with_suffix(path.suffix+".gz"),"rb") as stream:
            assert sha256_file(stream) == result["trimmed_proof_sha256"][path.name]
    result_file.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    full_lrat.unlink()
    full_drat.unlink()
    print(folder.name, *(f"{p.name}.gz={p.with_suffix(p.suffix+'.gz').stat().st_size}"
                         for p in retained), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="+", type=Path)
    args = parser.parse_args()
    for folder in args.case:
        compact(folder.resolve())
