# Packaging and provenance

This packet preserves the clean-room audit of Jean-Roch Bécart’s pinned Erdős #1110 (7,2) claim. The replay checks the written reduction and the fixed finite certificate.

## Replay artifacts

The files below are byte-identical to their sources in the replay job.

| Packet file | Source relative to the replay job |
| --- | --- |
| `replay/LEMMAS.md` | `LEMMAS.md` |
| `replay/VERDICT_for_ledger.txt` | `VERDICT_for_ledger.txt` |
| `replay/compare_claim.py` | `compare_claim.py` |
| `replay/e1110_verify.c` | `e1110_verify.c` |
| `replay/encoder.py` | `encoder.py` |
| `replay/logs/claim.json` | `logs/claim.json` |
| `replay/logs/controls.json` | `logs/controls.json` |
| `replay/logs/encoder.json` | `logs/encoder.json` |
| `replay/logs/encoder.time` | `logs/encoder.time` |
| `replay/logs/full_bc_away.json` | `logs/full_bc_away.json` |
| `replay/logs/full_bc_away.time` | `logs/full_bc_away.time` |
| `replay/logs/full_bc_even.json` | `logs/full_bc_even.json` |
| `replay/logs/full_bc_even.time` | `logs/full_bc_even.time` |
| `replay/logs/full_bc_up.json` | `logs/full_bc_up.json` |
| `replay/logs/full_bc_up.time` | `logs/full_bc_up.time` |
| `replay/logs/full_cb_away.json` | `logs/full_cb_away.json` |
| `replay/logs/full_cb_away.time` | `logs/full_cb_away.time` |
| `replay/logs/full_cb_even.json` | `logs/full_cb_even.json` |
| `replay/logs/full_cb_even.time` | `logs/full_cb_even.time` |
| `replay/logs/full_cb_up.json` | `logs/full_cb_up.json` |
| `replay/logs/full_cb_up.time` | `logs/full_cb_up.time` |
| `replay/logs/full_last-gamma.json` | `logs/full_last-gamma.json` |
| `replay/logs/full_last-gamma.time` | `logs/full_last-gamma.time` |
| `replay/logs/full_low-value.json` | `logs/full_low-value.json` |
| `replay/logs/full_low-value.time` | `logs/full_low-value.time` |
| `replay/logs/full_positive-gamma.json` | `logs/full_positive-gamma.json` |
| `replay/logs/full_positive-gamma.time` | `logs/full_positive-gamma.time` |
| `replay/logs/full_window2.json` | `logs/full_window2.json` |
| `replay/logs/full_window2.time` | `logs/full_window2.time` |
| `replay/logs/full_window4.json` | `logs/full_window4.json` |
| `replay/logs/full_window4.time` | `logs/full_window4.time` |
| `replay/logs/reference.json` | `logs/reference.json` |
| `replay/logs/reference.time` | `logs/reference.time` |
| `replay/reference.py` | `reference.py` |
| `replay/replay_checks.py` | `replay_checks.py` |

## Files prepared for this packet

| Packet file | Source |
| --- | --- |
| `README.md` | Public summary of the replay report, lemma audit, verifier outputs and controls, with replay commands. |
| `PUBLISH.json` | Destination, target, replay scope, and model attribution. |
| `CLAIMS.json` | Numeric labels and provenance from the verifier scripts and captured replay results. |
| `CREDITS.json` and `CREDITS.md` | Contributions in the pinned claim and the replay’s prior-art and verdict records. |
| `PACKAGING.md` | File inventory and provenance. |
| `replay/PRIOR_ART.md` | Public summary of the original replay’s dated problem, repository, literature and community survey. |
| `replay/INPUTS.sha256` | Hashes computed on the staged input and the two table encodings, with pinned public sources and derivation notes. |
| `sources/publish-trees/Jrbecart-uo__erdos-1110-72@f26cb9a2506fef170b110b6226fe294d1b9d04e8.json` | Complete GitHub recursive tree response for the pinned commit, with the commit recorded explicitly. |
| `SHA256SUMS` | SHA-256 of every other file in this folder. |

The claimant’s README and compressed input are available from the pinned public URLs in [the input manifest](replay/INPUTS.sha256). The uncompressed float32 table and the rounded integer table are deterministic derivatives. Build the verifier locally from the included C source. The replay’s internal status and configuration stay with the original job. The packet includes public summaries of the original report and prior-art record.
