# PACKAGING: where every file came from

AI work, no new result claimed (see README.md). Source paths are relative to the Lean audit job (GPT-6.2 Astra)'s directory, which is not part of the packet.

## Files copied from the job (under `audit/`)

| packet file | source | status |
|---|---|---|
| `audit/Axioms.lean` | `Axioms.lean` | byte-identical copy |
| `audit/Bridge.lean` | `Bridge.lean` | byte-identical copy |
| `audit/BridgeChallenge.lean` | `BridgeChallenge.lean` | byte-identical copy |
| `audit/Mutants.lean` | `Mutants.lean` | byte-identical copy |
| `audit/NonVacuity.lean` | `NonVacuity.lean` | byte-identical copy |
| `audit/PRIOR_ART.md` | `PRIOR_ART.md` | **edited**: local capture-file path replaced by a placeholder |
| `audit/REPORT.md` | `REPORT.md` | **edited**: links retargeted: lake-build-final.log -> .log.gz; links to STATUS.md and third_party.jsonl (not shipped) removed; LeanChecker.lean link points to leanprover/lean4 at v4.33.0 instead of the local toolchain |
| `audit/SPEC.sha256` | `SPEC.sha256` | byte-identical copy |
| `audit/STATEMENT_TABLE.md` | `STATEMENT_TABLE.md` | byte-identical copy |
| `audit/Spec.lean` | `Spec.lean` | byte-identical copy |
| `audit/audit-lean.sh` | `audit-lean.sh` | byte-identical copy |
| `audit/bounded.py` | `bounded.py` | byte-identical copy |
| `audit/build-local.py` | `build-local.py` | byte-identical copy |
| `audit/compare-exports.lean` | `compare-exports.lean` | byte-identical copy |
| `audit/comparison-inputs.py` | `comparison-inputs.py` | byte-identical copy |
| `audit/env.sh` | `env.sh` | byte-identical copy |
| `audit/logs/axioms.log` | `logs/axioms.log` | byte-identical copy |
| `audit/logs/bridge-a-final.log` | `logs/bridge-a-final.log` | byte-identical copy |
| `audit/logs/bridge-a.log` | `logs/bridge-a.log` | byte-identical copy |
| `audit/logs/bridge-b.log` | `logs/bridge-b.log` | byte-identical copy |
| `audit/logs/build-local.log` | `logs/build-local.log` | byte-identical copy |
| `audit/logs/cache-bytecheck.log` | `logs/cache-bytecheck.log` | byte-identical copy |
| `audit/logs/challenge-resume.log` | `logs/challenge-resume.log` | byte-identical copy |
| `audit/logs/comparator-corruption.log` | `logs/comparator-corruption.log` | byte-identical copy |
| `audit/logs/comparator-functions.log` | `logs/comparator-functions.log` | byte-identical copy |
| `audit/logs/comparator-stock.log` | `logs/comparator-stock.log` | byte-identical copy |
| `audit/logs/corruption.diff` | `logs/corruption.diff` | **edited**: local absolute job path replaced by `$JOB` |
| `audit/logs/definitions.diff` | `logs/definitions.diff` | byte-identical copy |
| `audit/logs/export-sha256.txt` | `logs/export-sha256.txt` | byte-identical copy |
| `audit/logs/exports-lake.log` | `logs/exports-lake.log` | byte-identical copy |
| `audit/logs/exports.log` | `logs/exports.log` | byte-identical copy |
| `audit/logs/final-audit.log` | `logs/final-audit.log` | byte-identical copy |
| `audit/logs/lake-build-final.log.gz` | `logs/lake-build-final.log` | **edited**: `gzip -9n` of logs/lake-build-final.log (6.4 MB); content byte-identical after gunzip |
| `audit/logs/lake-build.log` | `logs/lake-build.log` | **edited**: local absolute job path replaced by `$JOB` |
| `audit/logs/lake-export-match.log` | `logs/lake-export-match.log` | byte-identical copy |
| `audit/logs/lake-single.log` | `logs/lake-single.log` | byte-identical copy |
| `audit/logs/leanchecker-final.log` | `logs/leanchecker-final.log` | byte-identical copy |
| `audit/logs/leanchecker.log` | `logs/leanchecker.log` | **edited**: local absolute job path replaced by `$JOB` |
| `audit/logs/mutants-final.log` | `logs/mutants-final.log` | byte-identical copy |
| `audit/logs/mutants-first.log` | `logs/mutants-first.log` | byte-identical copy |
| `audit/logs/pins-resume.log` | `logs/pins-resume.log` | byte-identical copy |
| `audit/logs/platform.log` | `logs/platform.log` | **edited**: local absolute job path replaced by `$JOB` |
| `audit/logs/source-scan-command.txt` | `logs/source-scan-command.txt` | byte-identical copy |
| `audit/logs/source-scan.log` | `logs/source-scan.log` | byte-identical copy |
| `audit/logs/third-party-check.log` | `logs/third-party-check.log` | byte-identical copy |
| `audit/logs/tree-scan.log` | `logs/tree-scan.log` | byte-identical copy |
| `audit/own-lean.sh` | `own-lean.sh` | byte-identical copy |
| `audit/prepare-deps.py` | `prepare-deps.py` | byte-identical copy |
| `audit/recheck-audit.sh` | `recheck-audit.sh` | byte-identical copy |
| `audit/replay-kernel.py` | `replay-kernel.py` | byte-identical copy |
| `audit/replay-standard-build.py` | `replay-standard-build.py` | byte-identical copy |
| `audit/run-stock.sh` | `run-stock.sh` | byte-identical copy |
| `audit/upstream.sh` | `upstream.sh` | byte-identical copy |

## Files written for this packet

| packet file | note |
|---|---|
| `CLAIMS.json` | written for this packet (every number in the prose, labelled) |
| `CREDITS.json` | written for this packet |
| `CREDITS.md` | written for this packet |
| `PACKAGING.md` | this file |
| `PUBLISH.json` | written for this packet (house metadata) |
| `README.md` | written for this packet |
| `SHA256SUMS` | generated last |
| `sources/publish-trees/allenibiapina__LeanShadow@19deb3ed555cc8404958c1804f9b29898a918d10.json` | `gh api repos/OWNER/REPO/git/trees/COMMIT?recursive=1` output for the pinned commit |

Edits only redact local paths, retarget links to files that are not shipped, or make the runner portable. No proof, certificate, script logic or result was changed.

## Not shipped

Build objects (`*.olean`), the toolchain, dependency checkouts, the authors' repository, temporary exports, the job's STATUS.md and its sandbox receipts (third_party.jsonl). Logs not linked from `audit/REPORT.md` are not shipped.
