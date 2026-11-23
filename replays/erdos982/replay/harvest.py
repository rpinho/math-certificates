"""Recheck retained certificate hashes, witness clauses and drat-trim core labels."""
from collections import Counter
import csv
import gzip
import hashlib
import json
import lzma
from pathlib import Path
import re
from tempfile import TemporaryDirectory

from encoder import Encoding
from run_case import sha256_file

ROOT = Path("runs")


def open_data(path, binary=False):
    mode = "rb" if binary else "rt"
    if path.is_file():
        return path.open(mode)
    xz_path = path.with_suffix(path.suffix + ".xz")
    if xz_path.is_file():
        return lzma.open(xz_path, mode)
    return gzip.open(path.with_suffix(path.suffix+".gz"),mode)


def clauses(path):
    with open_data(path) as stream:
        for line in stream:
            fields = line.split()
            if fields and fields[0] not in ("p","c"):
                assert fields[-1] == "0", (path,fields)
                yield tuple(sorted(map(int,fields[:-1])))


def canonical_cnf_sha256(path):
    digest = hashlib.sha256()
    with open_data(path, binary=True) as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk.replace(b"\t", b" "))
    return digest.hexdigest()


def check_case(folder):
    result = json.loads((folder/"result.json").read_text())
    with TemporaryDirectory(prefix="harvest_", dir=ROOT) as temp:
        cnf = folder/"formula.cnf"
        families = folder/"families.tsv"
        has_cnf = cnf.is_file() or cnf.with_suffix(".cnf.gz").is_file()
        has_families = families.is_file() or families.with_suffix(".tsv.gz").is_file()
        if not has_cnf or not has_families:
            regenerated_cnf = Path(temp)/"formula.cnf"
            regenerated_families = Path(temp)/"families.tsv"
            Encoding(result["n"],result["k"],result["omitted"],result.get("fan",False)
                     ).build().write(regenerated_cnf,regenerated_families)
            if not has_cnf:
                cnf = regenerated_cnf
            if not has_families:
                families = regenerated_families
        return check_evidence(folder,result,cnf,families)


def check_evidence(folder,result,cnf,families):
    stated = (folder/"CNF_SHA256.txt").read_text().splitlines()
    assert len(stated) == 2 and all(line.split()[0] == result["cnf_sha256"] for line in stated)
    assert canonical_cnf_sha256(cnf) == result["cnf_sha256"], folder
    original = list(clauses(cnf))
    with open_data(cnf) as stream:
        _, _, variables, count = next(stream).split()
    assert int(count) == len(original)
    assert len(set(original)) == len(original) and sorted(original) == original

    checked = folder/"model.txt"
    for candidate in ("retry_model.txt", "restricted_model.txt", "regular_model.txt"):
        if (folder/candidate).is_file():
            checked = folder/candidate
    if checked.is_file():
        truth = set(map(int,checked.read_text().split()))
        assert len(truth) == int(variables) and {abs(lit) for lit in truth} == set(range(1,int(variables)+1))
        assert all(any(lit in truth for lit in clause) for clause in original)
        return result, "SAT", len(original), checked.name
    if "core_clauses" not in result:
        return result, "UNRESOLVED", len(original), result["stop_reason"]

    proof_folder = ROOT/result.get("proof_case",folder.name)
    assert "s VERIFIED UNSAT" in (proof_folder/"cake.log").read_text()
    drat_log = (proof_folder/"drat-trim.log").read_text()
    assert "s VERIFIED" in drat_log
    assert re.search(rf"\b{result['core_clauses']} of {len(original)} clauses",drat_log), proof_folder
    index = {clause:i for i,clause in enumerate(original,1)}
    core = {index[clause] for clause in clauses(proof_folder/"core.cnf")}
    assert len(core) == result["core_clauses"]
    with open_data(families) as stream:
        source = dict(line.rstrip("\n").split("\t") for line in stream)
    with (folder/"core_families.tsv").open() as stream:
        ids = {int(row["clause_id"]): row["families"]
               for row in csv.DictReader(stream, delimiter="\t")}
    assert set(ids) == core and all(source[str(index)] == family for index,family in ids.items())
    counted = Counter(family for names in ids.values() for family in names.split(","))
    assert dict(counted) == result["core_families"]

    controls = result["negative_controls"]
    cid = controls["altered_core_id"]
    assert cid in core and original[cid-1] == tuple(controls["original_clause"])
    bad = (proof_folder/"corrupted.log").read_text()
    altered = (proof_folder/f"altered_{cid}.log").read_text()
    assert "s VERIFIED UNSAT" not in bad and "empty clause not derived" in bad
    assert "s VERIFIED UNSAT" not in altered and ("failed" in altered or "error" in altered.lower())
    mutation = proof_folder/"altered.cnf"
    if mutation.exists() or mutation.with_suffix(".cnf.gz").exists():
        assert canonical_cnf_sha256(mutation) == controls["altered_cnf_sha256"]
        changes = list(clauses(mutation))
        assert changes == original[:cid-1] + [tuple(controls["replacement"])] + original[cid:]

    retained = result.get("trimmed_proof_sha256",result["proof_sha256"])
    retention = "both proofs retained"
    if (proof_folder/"retention.json").is_file():
        notes = json.loads((proof_folder/"retention.json").read_text())
        retention = notes["status"]
        assert set(notes["dropped"]).issubset(retained)
        retained = {name:value for name,value in retained.items() if name not in notes["dropped"]}
    for name,digest in retained.items():
        with open_data(proof_folder/name,binary=True) as stream:
            assert sha256_file(stream) == digest, (folder,name)
    if "trimmed_proof_sha256" in result:
        assert "s VERIFIED UNSAT" in (proof_folder/"cake-trimmed.log").read_text()
        assert "s VERIFIED" in (proof_folder/"drat-trimmed.log").read_text()
    return result, "UNSAT", len(original), retention


if __name__ == "__main__":
    writer = csv.writer(__import__("sys").stdout,delimiter="\t",lineterminator="\n")
    writer.writerow(["case","n","k","verdict","clauses","drat_core","cnf_sha256","evidence"])
    for folder in sorted(path.parent for path in ROOT.glob("*/result.json")):
        result, verdict, count, evidence = check_case(folder)
        writer.writerow([folder.name,result["n"],result["k"],verdict,
                         count,result.get("core_clauses",""),result["cnf_sha256"],evidence])
