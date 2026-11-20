#!/usr/bin/env python3
# writes replay/REPLAY.json (hashes of inputs, checker, report); usage: make_replay_json.py STATUS
import sys, json, hashlib, os
here = os.path.dirname(os.path.abspath(__file__))
job = os.path.dirname(here)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
inputs = {k: sha(os.path.join(job, "inputs", k)) for k in ("CLAIM.md", "PROOF.md", "certificates/certificate.json")}
out = {"model": "claude-opus-5-5", "author": "math_c82r12ref_1120 (clean-room)", "status": sys.argv[1],
       "value": "0.2519694759", "arithmetic": "interval", "inputs": inputs,
       "inputs_hash": hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(),
       "read_producer_code": False, "ran_producer_code": False,
       "checker": "replay/check.py", "checker_sha256": sha(os.path.join(here, "check.py")),
       "report": "replay/report.md", "report_sha256": sha(os.path.join(here, "report.md"))}
open(os.path.join(here, "REPLAY.json"), "w").write(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
