"""Cross-check the C replay, exercise the specified controls, and record exact results."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random
import signal
import struct
import subprocess
import tempfile
import time

from reference import ROUNDINGS, canonical_rows, chain_family, drift, little_endian_digest, read_roundings

LOGS = Path("logs")
RAW = Path("replay_table.f32")
CANONICAL_TABLE = Path("V_hat.i64le")
P = 2**11
LAYOUTS = ("cb", "bc")
RULES = ("low-value", "last-gamma", "positive-gamma")
SEED = 1110


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expired(signum, frame):
    raise TimeoutError("replay deadline reached")


def as_json(path):
    return json.loads(path.read_text())


def save_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def file_digest(path):
    with open(path, "rb") as data:
        return sha256(data.read()).hexdigest()


def run_c(*arguments, reject=None):
    command = ["nice", "-n", "10", "./e1110_verify", *map(str, arguments)]
    result = subprocess.run(command, text=True, capture_output=True)
    if reject is not None:
        require(result.returncode != 0 and result.stderr.strip() == reject,
                f"expected rejection {reject!r}, got {result}")
        return {"exit": result.returncode, "diagnostic": result.stderr.strip(), "refused": True}
    require(result.returncode == 0, f"command failed: {command}: {result.stderr}")
    return json.loads(result.stdout)


def full_reference(s, family, tables, layout, rounding):
    p = 2**s
    return [drift(tables[rounding], family, c, b, layout) for c in range(p) for b in range(p)]


def check_chains(temp, family):
    c_path = temp / "chains.txt"
    counts = run_c("chains", 11, 10, 3, "standard", c_path)
    text = "".join(canonical_rows(family))
    raw = c_path.read_bytes()
    expected_count = sum(map(len, family))
    require(raw == text.encode("ascii"), "chain sets differ")
    require(counts == {"chains": expected_count, "residues": P}, "chain counts differ")
    require(run_c("check", 11, 10, c_path) == counts, "canonical structural check failed")
    require([c.pairs for c in family[0]] == [()], "residue zero is not forced empty")
    first, rest = text.split("\n", 1)
    require(first == "0 0", "unexpected first chain")

    def invalid_row(pairs):
        residue = sum((2**a) * pow(7, -g, P) for a, g in pairs) % P
        fields = [residue, len(pairs), *(x for pair in pairs for x in pair)]
        return " ".join(map(str, fields)) + "\n"

    invalid_lists = (
        ("drop_empty", rest, "uncovered residue 0"),
        ("wrong_residue", text + "2 1 0 0\n", "chain residue mismatch"),
        ("height_11", text + invalid_row(((0, 10),)), "height exceeds H"),
        ("non_chain", text + invalid_row(((0, 1), (1, 0))), "pairs do not form a chain"),
        ("duplicate_alpha", text + invalid_row(((0, 0), (0, 1))), "duplicate alpha"),
    )
    rejects = {}
    for name, contents, diagnostic in invalid_lists:
        malformed = temp / f"{name}.txt"
        malformed.write_text(contents)
        rejects[name] = run_c("check", 11, 10, malformed, reject=diagnostic)
    histogram = Counter(chain.h for group in family for chain in group)
    details = dict(counts, canonical_sha256=sha256(raw).hexdigest(), byte_identical=True,
                   zero_residue_chains=1, height_histogram=histogram)
    return details, rejects


def check_rounding(temp, tables, metadata):
    results = {}
    for rounding, table in tables.items():
        target = CANONICAL_TABLE if rounding == "away" else temp / f"{rounding}.i64le"
        c_stats = run_c("round", 11, 10, 3, "standard", RAW, rounding, target)
        digest = file_digest(target)
        require(digest == little_endian_digest(table), f"{rounding} table digests differ")
        ref_stats = {key: metadata[key] for key in ("finite", "ties", "negative_ties", "positive_ties")}
        ref_stats.update(minimum=min(table), maximum_table_value=max(table))
        require(c_stats == ref_stats, f"{rounding} rounding statistics differ")
        differences = sum(a != b for a, b in zip(table, tables["away"]))
        results[rounding] = dict(c_stats, sha256_i64le=digest, differences_from_away=differences)
    return results


def synthetic_binary32(s):
    rng = random.Random(SEED + s)
    # Include signed zeros and subnormals, and values just to either side of a scaled tie.
    edge_bits = (0, 1 << 31, 1, (1 << 31) | 1, 0x34FFFFFF, 0x35000001,
                 0xB4FFFFFF, 0xB5000001)
    raw = bytearray().join(struct.pack("<I", bits) for bits in edge_bits)
    for _ in range((1 << (2*s)) - len(edge_bits)):
        numerator = rng.randrange(-16*(1 << 20), 16*(1 << 20))
        raw.extend(struct.pack("<f", numerator / (1 << 22)))
    return raw


def check_synthetic(temp, deadline):
    result = {}
    for s in (4, 5, 6):
        H = s + 1
        p = 2**s
        family = chain_family(s, H, 3)
        source, output = temp / f"s{s}.f32", temp / f"s{s}.i64le"
        source.write_bytes(synthetic_binary32(s))
        tables, stats = read_roundings(source, s)
        cases = {}
        for layout in LAYOUTS:
            for rounding in ROUNDINGS:
                c_result = run_c("full", s, H, 3, "standard", source, layout, rounding,
                                 1, deadline, output)
                computed = [value for (value,) in struct.iter_unpack("<q", output.read_bytes())]
                reference = full_reference(s, family, tables, layout, rounding)
                require(computed == reference, f"synthetic discrepancy at s={s}, {layout}/{rounding}")
                best = max(reference)
                require([best, list(divmod(reference.index(best), p)), reference.count(best)] ==
                        [c_result["maximum"], c_result["argmax"], c_result["argmax_count"]],
                        "synthetic maximum reduction disagrees")
                require((c_result["states"], c_result["lookaheads"]) == (p*p, p**3),
                        "synthetic sweep incomplete")
                require(all(c_result[key] == stats[key] for key in
                            ("finite", "ties", "negative_ties", "positive_ties")),
                        "synthetic rounding metadata disagrees")
                cases[f"{layout}/{rounding}"] = dict(c_result, agreeing_states=len(reference),
                                                      drift_sha256_i64le=file_digest(output))
        result[s] = {"raw_sha256": stats["raw_sha256"], "cases": cases}
    return result


def read_sweep(name):
    result = as_json(LOGS / f"full_{name}.json")
    require((result["s"], result["H"], result["residues"], result["threads"]) == (11, 10, P, 6),
            f"incorrect sweep metadata for {name}")
    require((result["states"], result["lookaheads"]) == (P*P, P**3), f"incomplete sweep {name}")
    return result


def probe_c(temp, table_args, states, delta=None):
    path = temp / "probes.txt"
    path.write_text("".join(f"{c} {b}\n" for c, b in states))
    command = ("probe", 11, 10, *table_args[:2], RAW, *table_args[2:], path)
    observed = run_c(*command) if delta is None else run_c(*command, delta)
    require([tuple(row[:2]) for row in observed] == list(states), "C returned different probe states")
    return observed


def check_samples(temp, tables, family, baseline):
    rng = random.Random(SEED)
    c_star, b_star = baseline["argmax"]
    states = [(c_star, b_star), (0, 0), (0, P-1), (P-1, 0), (0, b_star), (c_star, 0)]
    while len(states) < 112:
        query = (rng.randrange(P), rng.randrange(P))
        if query not in states:
            states.append(query)
    probes = {}
    for layout in LAYOUTS:
        for rounding in ROUNDINGS:
            sweep = read_sweep(f"{layout}_{rounding}")
            require((sweep["layout"], sweep["rounding"], sweep["rule"], sweep["window"]) ==
                    (layout, rounding, "standard", 3), "sweep labels disagree with requested case")
            options = (3, "standard", layout, rounding)
            winner = tuple(sweep["argmax"])
            queries = list(states)
            if winner not in queries:
                queries.append(winner)
            observed = probe_c(temp, options, queries)
            reference = [drift(tables[rounding], family, c, b, layout) for c, b in queries]
            require([item[2] for item in observed] == reference, f"sample disagreement for {options}")
            require(reference[queries.index(winner)] == sweep["maximum"],
                    f"full winner differs from Python for {options}")
            probes[f"{layout}/{rounding}"] = {
                "agreeing_states": len(queries), "winner": winner, "winner_drift": sweep["maximum"],
                "states": [{"c": c, "b": b, "c_drift": item[2], "python_drift": value}
                           for ((c, b), item, value) in zip(queries, observed, reference)],
            }
    return probes


def check_corruption(temp, table, family, baseline):
    c, b = baseline["argmax"]
    target = c*P + b
    original = table[target]
    expected = {}
    for edit in (-1000, -13748, -20000):
        base, prediction, reachable = drift(table, family, c, b, "cb", target_delta=edit)
        require(base == baseline["maximum"], "corruption baseline differs")
        expected[edit] = (prediction, reachable)
    results = {}
    for edit, (prediction, reachable) in expected.items():
        observed = probe_c(temp, (3, "standard", "cb", "away"), [(c, b)], delta=edit)[0]
        table[target] = original + edit
        try:
            direct = drift(table, family, c, b, "cb")
        finally:
            table[target] = original
        delta = observed[2] - baseline["maximum"]
        require(delta == prediction and direct == observed[2], "corruption drift does not match prediction")
        passes = 73 * direct < 286 * (1 << 31)
        require(observed[3] == passes and passes == (edit == -1000),
                f"wrong threshold result for edit {edit}")
        results[edit] = {
            "state": [c, b], "original_entry": original, "edited_entry": original + edit,
            "lookaheads_that_can_reach_target": reachable, "predicted_delta": prediction,
            "observed_delta": delta, "c_drift": observed[2], "python_drift": direct,
            "passes_threshold_at_witness": passes, "lhs_73_times_drift": 73 * direct,
            "rhs_286_times_2pow31": 286 * (1 << 31),
        }
    return results


def check_mutations(temp, table, family, baseline):
    outcomes = {}
    for rule in RULES:
        mutant_family = chain_family(11, 10, 3, positive_gamma=True) if rule == "positive-gamma" else family
        sweep = read_sweep(rule)
        winner = tuple(sweep["argmax"])
        states = list(dict.fromkeys([winner, tuple(baseline["argmax"])]))
        c_results = probe_c(temp, (3, rule, "cb", "away"), states)
        comparisons = []
        for (c, b), observed in zip(states, c_results):
            standard = drift(table, family, c, b, "cb")
            mutated = drift(table, mutant_family, c, b, "cb", rule)
            require(observed[2] == mutated, f"C and Python disagree about {rule} implementation")
            comparisons.append({"state": [c, b], "python_standard": standard,
                                "python_mutant": mutated, "c_mutant": observed[2]})
        require((sweep["rule"], sweep["chains"]) == (rule, sum(map(len, mutant_family))),
                f"incorrect mutant metadata for {rule}")
        require(sweep["maximum"] == comparisons[0]["python_mutant"], "mutant winner drift mismatched")
        changed = sweep["maximum"] != baseline["maximum"]
        disagrees = any(row["python_standard"] != row["c_mutant"] for row in comparisons)
        require(changed and disagrees, f"{rule} did not trip both required controls")
        outcomes[rule] = {"sweep": sweep, "comparisons": comparisons,
                          "maximum_changed": changed, "disagrees_with_standard_python": disagrees}
    return outcomes


def check_windows(table, baseline):
    results = {}
    for window in (2, 4):
        sweep = read_sweep(f"window{window}")
        c, b = sweep["argmax"]
        family = chain_family(11, 10, window)
        exact = drift(table, family, c, b, "cb")
        require((sweep["window"], sweep["chains"], sweep["maximum"]) ==
                (window, sum(map(len, family)), exact), "height-window replay differs")
        results[window] = {"sweep": sweep, "python_at_winner": exact,
                           "difference_from_baseline": exact - baseline["maximum"]}
    require(results[2]["difference_from_baseline"] > 0, "dropping +3 did not raise the max")
    require(results[4]["difference_from_baseline"] <= 0, "adding +4 increased the max")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deadline", required=True, type=int)
    args = parser.parse_args()
    remaining = args.deadline - time.time()
    require(remaining > 0, "deadline already reached")
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, remaining)
    baseline = read_sweep("cb_away")
    family = chain_family(11, 10, 3)
    tables, stats = read_roundings(RAW, 11)
    controls = {}
    ranking = {}
    with tempfile.TemporaryDirectory(prefix=".e1110_", dir=".") as directory:
        temp = Path(directory)
        ranking["chains"], controls["structural"] = check_chains(temp, family)
        ranking["rounding"] = check_rounding(temp, tables, stats)
        ranking["raw_sha256"] = stats["raw_sha256"]
        ranking["synthetic_exhaustive"] = check_synthetic(temp, args.deadline)
        ranking["s11_probes"] = check_samples(temp, tables, family, baseline)
        save_json(LOGS / "reference.json", ranking)
        table = tables["away"]
        controls["corruption"] = check_corruption(temp, table, family, baseline)
        controls["mutations"] = check_mutations(temp, table, family, baseline)
        controls["height_windows"] = check_windows(table, baseline)
        controls["rational"] = {
            "7pow26": 7**26, "2pow73": 2**73, "2pow72": 2**72,
            "7pow26_lt_2pow73": 7**26 < 2**73,
            "7pow26_lt_2pow72": 7**26 < 2**72,
            "73_times_g_num": 73 * baseline["maximum"], "286_times_2pow31": 286 * 2**31,
            "73_g_num_lt_286_2pow31": 73 * baseline["maximum"] < 286 * 2**31,
        }
        rational = controls["rational"]
        require(rational["7pow26_lt_2pow73"] and not rational["7pow26_lt_2pow72"] and
                rational["73_g_num_lt_286_2pow31"], "rational check or mutant failed")
        save_json(LOGS / "controls.json", controls)
    print("C and Python agree on the exact chain list, rounding bytes, all synthetic states, "
          "and the s=11 comparisons. All requested controls produced the required outcomes.")


if __name__ == "__main__":
    main()
