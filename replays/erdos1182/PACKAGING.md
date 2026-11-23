# PACKAGING: where every file came from

AI work, no new result claimed (see README.md). Source paths are relative to the #1182 replay job (GPT-6.2 Astra)'s directory, which is not part of the packet.

## Files copied from the job (under `replay/`)

| packet file | source | status |
|---|---|---|
| `replay/DERIVATION.md` | `DERIVATION.md` | byte-identical copy |
| `replay/LEMMAS.md` | `LEMMAS.md` | byte-identical copy |
| `replay/OWN.sha256` | `OWN.sha256` | byte-identical copy |
| `replay/PRIOR_ART.md` | `PRIOR_ART.md` | **edited**: local capture-file path replaced by a placeholder |
| `replay/REPORT.md` | `REPORT.md` | byte-identical copy |
| `replay/cert-11.json.gz` | `cert-11.json.gz` | byte-identical copy |
| `replay/cert-503-corrupt.json.gz` | `cert-503-corrupt.json.gz` | byte-identical copy |
| `replay/cert-503.json.gz` | `cert-503.json.gz` | byte-identical copy |
| `replay/check-11.log` | `check-11.log` | byte-identical copy |
| `replay/check-503.log` | `check-503.log` | byte-identical copy |
| `replay/control-0.json` | `control-0.json` | byte-identical copy |
| `replay/control-015.json` | `control-015.json` | byte-identical copy |
| `replay/controls.log` | `controls.log` | byte-identical copy |
| `replay/controls.py` | `controls.py` | byte-identical copy |
| `replay/coverage-11.log` | `coverage-11.log` | byte-identical copy |
| `replay/coverage-503.log` | `coverage-503.log` | byte-identical copy |
| `replay/finite.log` | `finite.log` | byte-identical copy |
| `replay/finite.py` | `finite.py` | byte-identical copy |
| `replay/float.json` | `float.json` | byte-identical copy |
| `replay/float.log` | `float.log` | byte-identical copy |
| `replay/float_search.py` | `float_search.py` | byte-identical copy |
| `replay/make-0.log` | `make-0.log` | byte-identical copy |
| `replay/make-015.log` | `make-015.log` | byte-identical copy |
| `replay/make-11.log` | `make-11.log` | byte-identical copy |
| `replay/make-503.log` | `make-503.log` | byte-identical copy |
| `replay/make_points.py` | `make_points.py` | byte-identical copy |
| `replay/matched-caps.log` | `matched-caps.log` | byte-identical copy |
| `replay/points.json` | `points.json` | byte-identical copy |
| `replay/produce.py` | `produce.py` | byte-identical copy |
| `replay/run` | `run` | **edited**: interpreter changed from a local virtualenv path to `${PYTHON:-python3}` |
| `replay/verify.py` | `verify.py` | byte-identical copy |

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
| `sources/publish-trees/Sovi11__erdos-1182@6d4f78cfb15296297450618dde6fea8b15478ccc.json` | `gh api repos/OWNER/REPO/git/trees/COMMIT?recursive=1` output for the pinned commit |

Edits only redact local paths, retarget links to files that are not shipped, or make the runner portable. No proof, certificate, script logic or result was changed.

## Not shipped

The author's documents given to the replay (`inputs/`: README.md, BOUNDS.md, note.pdf, preprint main.tex; link them at the pinned commit), the job's STATUS.md, and the `*.time` resource logs.
