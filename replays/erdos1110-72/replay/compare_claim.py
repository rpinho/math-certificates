"""Compare the completed certificate sweep with the staged README's claim."""

from hashlib import sha256
import json
from pathlib import Path
import re

expected_hashes = {
    "inputs/README.md": "64550a366613eb3da43081a0a97457c7d6300433947606a855130427f3253caa",
    "inputs/V_s11_it8.bin.xz": "90db9ac0f2da9ac6ad76497de73288e341a8ca8d63e715b037caa29eac7c7d97",
    "replay_table.f32": "f7f832116362b96db8ba42884e61803aa5e7cd02071a45f3353072ee4bdd9258",
}
observed_hashes = {}
for path, expected_hash in expected_hashes.items():
    raw = Path(path).read_bytes()
    observed_hashes[path] = sha256(raw).hexdigest()
    if observed_hashes[path] != expected_hash:
        raise ValueError(f"digest mismatch: {path}")
text = Path("inputs/README.md").read_text()
match = re.search(r"\$(\d+)\$, attained at state \$\(c,b\)\s*=\s*\((\d+),(\d+)\)\$", text)
chain_match = re.search(r"is (\d+ \d+) chains in total", text)
if not match or not chain_match:
    raise ValueError("could not extract the maximum, witness, and chain count from README")
maximum, c, b = map(int, match.groups())
expected = {"maximum": maximum, "argmax": [c, b],
            "chains": int(chain_match[1].replace(" ", ""))}
observed = json.loads(Path("logs/full_cb_away.json").read_text())
agrees = all(observed[key] == value for key, value in expected.items())
coverage = observed["states"] == 2**22 and observed["lookaheads"] == 2**33
configuration = (observed["layout"], observed["rounding"], observed["rule"], observed["window"])
passes = agrees and coverage and configuration == ("cb", "away", "standard", 3)
passes = passes and 73 * observed["maximum"] < 286 * 2**31 and 7**26 < 2**73
output = {"input_sha256": observed_hashes, "readme_expectation": expected, "claim_matches_raw_replay": agrees,
          "coverage_complete": coverage, "passes": passes}
Path("logs/claim.json").write_text(json.dumps(output, indent=2) + "\n")
if not passes:
    raise ValueError("the full replay did not reproduce the staged README claim")
print(json.dumps(output))
