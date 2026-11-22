# PACKAGING: where every file came from

Candidate, unrefereed, AI work; no new bound is claimed (see README.md). Paths below are relative to the producer job directory (the Claude Opus 5.5 gap job) or the referee job directory (the cross-family referee job). Neither job directory is part of the packet.

## 1. Files copied from the two jobs

| packet file | source | status |
|---|---|---|
| `certificates/certK_r105.json` | producer job: `work/gap/certK_r105.json` | byte-identical copy |
| `producer/data/nearext_h128.npy` | producer job: `work/nearext_h128.npy` | byte-identical copy |
| `producer/dint2/dint2.py` | producer job: `work/gap/dint2/dint2.py` | **edited for portability** (section 3) |
| `producer/dint2/load.py` | producer job: `work/gap/dint2/load.py` | **edited for portability** (section 3) |
| `producer/dint2/res_main.json` | producer job: `work/gap/dint2/res_main.json` | byte-identical copy |
| `producer/dint2/run_main.log` | producer job: `work/gap/dint2/run_main.log` | byte-identical copy |
| `producer/fixtures_K.py` | producer job: `work/gap/fixtures_K.py` | **edited for portability** (section 3) |
| `producer/ledger/assembly.py` | producer job: `work/gap/ledger/assembly.py` | **edited for portability** (section 3) |
| `producer/ledger/c_check.py` | producer job: `work/gap/ledger/c_check.py` | **edited for portability** (section 3) |
| `producer/ledger/ledger_arb.py` | producer job: `work/gap/ledger/ledger_arb.py` | **edited for portability** (section 3) |
| `producer/ledger/n0_ledger.py` | producer job: `work/gap/ledger/n0_ledger.py` | **edited for portability** (section 3) |
| `producer/ledger/paid_rows.py` | producer job: `work/gap/ledger/paid_rows.py` | **edited for portability** (section 3) |
| `producer/ledger/scatter.py` | producer job: `work/gap/ledger/scatter.py` | **edited for portability** (section 3) |
| `producer/ledger/scatter_exact.py` | producer job: `work/gap/ledger/scatter_exact.py` | **edited for portability** (section 3) |
| `producer/make_K.py` | producer job: `work/gap/make_K.py` | **edited for portability** (section 3) |
| `producer/verify_K.py` | producer job: `work/gap/verify_K.py` | **edited for portability** (section 3) |
| `referee/REFEREE.md` | referee job: `REFEREE.md` | **edited for portability** (section 3) |
| `referee/fixtures.json` | referee job: `fixtures.json` | byte-identical copy |
| `referee/fixtures.log` | referee job: `fixtures.log` | byte-identical copy |
| `referee/referee_check.py` | referee job: `referee_check.py` | **edited for portability** (section 3) |
| `referee/referee_data.py` | referee job: `referee_data.py` | **edited for portability** (section 3) |
| `referee/referee_fixtures.py` | referee job: `referee_fixtures.py` | **edited for portability** (section 3) |
| `referee/referee_kernel.py` | referee job: `referee_kernel.py` | byte-identical copy |
| `referee/replay.json` | referee job: `replay.json` | byte-identical copy |
| `referee/replay.log` | referee job: `replay.log` | byte-identical copy |
| `results/ctrl_drop.json` | producer job: `work/gap/ctrl_drop.json` | byte-identical copy |
| `results/ctrl_drop.log` | producer job: `work/gap/ctrl_drop.log` | byte-identical copy |
| `results/ctrl_flip.json` | producer job: `work/gap/ctrl_flip.json` | byte-identical copy |
| `results/ctrl_flip.log` | producer job: `work/gap/ctrl_flip.log` | byte-identical copy |
| `results/ctrl_nocap.json` | producer job: `work/gap/ctrl_nocap.json` | byte-identical copy |
| `results/ctrl_nocap.log` | producer job: `work/gap/ctrl_nocap.log` | byte-identical copy |
| `results/ctrl_raiseL.json` | producer job: `work/gap/ctrl_raiseL.json` | byte-identical copy |
| `results/fixtures_K.json` | producer job: `work/gap/fixtures_K.json` | byte-identical copy |
| `results/vK_N0shift.json` | producer job: `work/gap/vK_N0shift.json` | byte-identical copy |
| `results/vK_main.json` | producer job: `work/gap/vK_main.json` | byte-identical copy |
| `results/vK_main.log` | producer job: `work/gap/vK_main.log` | byte-identical copy |

## 2. Files written for this packet

| packet file | note |
|---|---|
| `README.md` | written for this packet |
| `PACKAGING.md` | this file |
| `SHA256SUMS` | generated last |
| `replay_all.sh` | written for this packet (runs every command below, no path outside the packet) |
| `compare_replay.py` | written for this packet (compares a replay with the shipped results) |
| `check_inputs.py` | written for this packet (sha256 check of the fetched inputs) |
| `producer/build_float_cache.py` | written for this packet from the producer job's `work/kernel_var.py`, `work/kernel_var2.py`, `work/kernel_norm.py` and `work/gap/gmap.py`; its Phi_Z.npy and g_fine.npy are bit-identical (`numpy.array_equal`) to the originals |
| `replay/` | output of `sh replay_all.sh` on a fresh copy of this packet with the pinned inputs (section 4); `fetch.sh`/`fetch.log` are the README fetch commands and their output |

## 3. Edits made for portability (no numerical logic changed)

- **All scripts:** every absolute local path was removed. Input files are read from the directory in the environment variable `E36_INPUTS` (default `inputs`; it must contain `unktok/` and `wetch/`, README section 4). Float caches go to `E36_CACHE` (default `cache`). Imports and default outputs are relative to the script's own directory.
- `producer/verify_K.py`: path edits; new option `--dint2 FILE` (default `producer/dint2/res_main.json`); worker pool 5 → 4 (4-core cap); usage line.
- `producer/dint2/dint2.py`: import path and output file relative to the script; worker pool 5 → 4. `producer/dint2/load.py`: input directory from `E36_INPUTS`.
- `producer/ledger/*.py`: `import os` added as the first line; the input directory `I` comes from `E36_INPUTS`.
- `producer/make_K.py`: `g_fine.npy` read from `E36_CACHE` (and `import os`). `producer/fixtures_K.py`: float caches and outputs under `E36_CACHE`; certificate and `vK_main.json` read from the packet (`E36_VK` overrides the latter); the round-1 near-extremal 128-step density is read from `producer/data/nearext_h128.npy`.
- `referee/referee_data.py`: input directory from `E36_INPUTS`. `referee/referee_check.py`: the certificate and the output directory are command-line arguments; a `sys.path` line lets it run under `python -I`. `referee/referee_fixtures.py`: output directory is an argument.
- `referee/REFEREE.md`: three link targets changed. The two links into the claimant's documents became plain text, `given/certs/vK_main.json` became `../results/vK_main.json`, and `REPORT.md` became `../README.md`. The referee's own text calls itself a "Codex" review.
- The shipped outputs in `results/` and `referee/` come from the original, non-portable scripts. The portable scripts reproduce them (replay/compare_replay.log): identical per-bin results, identical ledger, controls and fixtures, and a search output that is byte-identical to the certificate.

## 4. Not included, and why

- The claimant's code and data files and Wetch's two certificates: not ours and not redistributable here. The scripts read them from your own fetched copy (README section 4).
- Regenerable caches: `Phi_*.npy`, `K_float.npy`, `base.npy`, `Zp.npy`, `rowk.npy` (8 MB each), `g_fine.npy` (2 MB), `fix_m*.npy`. `producer/build_float_cache.py` regenerates `Phi_Z.npy` and `g_fine.npy` from the pinned inputs; `producer/fixtures_K.py` regenerates `fix_m*.npy`. They are needed only by the search and the 16 fixtures, never by the verifiers.
- `__pycache__`, scratch probes (`dual_probe.py`, `odd_probe.py`, `U_probe.npy`, `peek*.py`) and the type-O reach analysis (`outer_lp.*`, `wetch_central_bins.*`, `wetch_central_family.json`). `odd_probe.py` is the failed plain-odd-functional experiment (gain about 5e-11 where 5.9e-9 was needed); it is described in the producer's report, not replayed here.
- Round 1 (kernel builders other than the above, outer cover, PSD witnesses): carried forward in README section 3, not part of this packet.
- The producer's and the referee's own `REPORT*.md`, `PRIOR_ART.md` and `STATUS.md`: they contain local paths and process notes; README.md replaces them.

## 5. Resources measured

The commands in `replay_all.sh` run one at a time, nice 10, at most 4 workers. Peak resident memory measured with `/usr/bin/time -l` in an earlier run of the same commands (log not kept): `dint2.py` 241 MB (19 s), `verify_K.py` 203 MB (23 s each, 6 runs), `referee_check.py` 207 MB (8 s), `referee_fixtures.py` 85 MB, `fixtures_K.py` 169 MB (29 s), `make_K.py` 52 MB (9 s), every ledger script at most 192 MB. Whole `replay_all.sh`: about 5 minutes.

## 6. egress-gate

**Result: BLOCKED (exit 2). It does not PASS.** Command, run from the job directory: `egress-gate scan packet/`.
Self-test: `egress-gate self-test` printed PASS. The scan found 2 582 signals, **all of class `[card]`** (a long digit run that passes a Luhn check) and **all inside exact-rational data**:

| file | signals | what the flagged text is |
|---|---|---|
| `certificates/certK_r105.json` | 2 580 | exact rational slopes and multipliers (`"num/den"` strings); the digit runs are numerators |
| `referee/replay.json` | 1 | the `second_moment` field, a 16-digit rational numerator over 5·10^15 |
| `replay/referee/replay.json` | 1 | the same line, regenerated by the replay |

No other file in the packet is flagged: no private path, name, address, secret shape or agent-file signal (each file was also scanned on its own). Printed output, trimmed to its first lines (the full list is 63 lines of the same kind; the last line, which names the owner's allow-list file, is omitted here):

```
egress-gate: BLOCKED, 2582 signal(s) in packet/:
  [card] packet/referee/replay.json:5: "second_moment": "<16-digit numerator>/5000000000000000",
  [card] packet/certificates/certK_r105.json:1: {"type": "K", "target_lo": "0", "target_hi": "1/160", "ratio": 1.05, "safety": [0.99, 3e-07], "bins": [{"lo": "0", "hi": " …
  [card] packet/certificates/certK_r105.json:1: {"type": "K", "target_lo": "0", "target_hi": "1/160", "ratio": 1.05, "safety": [0.99, 3e-07], "bins": [{"lo": "0", "hi": " …
  ... and 2522 more
  ... (further [card] lines, 59 for the certificate file in the first 25 shown)
```

These are false positives of the same kind the owner has already allowed for other exact-rational certificates in the destination repository, but an allow rule is the owner's decision and was **not** added by this job (the file lives outside the job directory). The certificate cannot be reformatted to avoid the match without changing the bytes that the hashes and the byte-identity check refer to. To clear the gate, the owner adds scoped rules such as:

```
*math-certificates*<TAB>card<TAB>erdos/36/certificates/certK_r105.json<TAB>exact rational certificate data, not a card (FP, same class as the 11-01 certificate rules)
*math-certificates*<TAB>card<TAB>erdos/36/*replay.json<TAB>exact rational second moment, not a card (FP)
```

and the same two for the job's working tree if the packet is scanned there. Until then this packet must not be copied to the repository or pushed.

## Metadata added at publish time

CLAIMS.json, CREDITS.json and CREDITS.md were written at publish time for rh publish-lint; README.md wording changed from "we" to "I" in three sentences and the issue 67 credit now links the issue. PUBLISH.json and sources/publish-trees/ (GitHub tree listings of the two pinned upstream commits) were added by the packaging step.
