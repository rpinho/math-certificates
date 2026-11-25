# Packaging and provenance

This folder packages an AI clean-room audit of Jinhao Huang’s PR #393. The replay retains the original lower-bound verdicts and the limited scope of the upper-bound check.

## Replay artifacts

These files are byte-identical copies from the clean-room replay job. Each source had the same basename at the top level of that job.

| Packet file | Source |
| --- | --- |
| `replay/LEMMAS.md` | `LEMMAS.md` |
| `replay/VERDICT_for_ledger.txt` | `VERDICT_for_ledger.txt` |
| `replay/check_hand_proof.py` | `check_hand_proof.py` |
| `replay/hand_proof_audit.json` | `hand_proof_audit.json` |
| `replay/stress_test.py` | `stress_test.py` |
| `replay/stress_test_results.json` | `stress_test_results.json` |
| `replay/verifier_a.py` | `verifier_a.py` |
| `replay/verifier_a_results.json` | `verifier_a_results.json` |
| `replay/verifier_b.py` | `verifier_b.py` |
| `replay/verifier_b_results.json` | `verifier_b_results.json` |
| `replay/t2_lite.py` | `t2_lite.py` |
| `replay/t2_lite_results.json` | `t2_lite_results.json` |

## Files prepared for this packet

| Packet file | Source |
| --- | --- |
| `README.md` | Public summary of the original replay report, lemma audit and result JSONs, with portable replay instructions. |
| `PUBLISH.json` | Destination, publication target, replay scope and model attribution. |
| `CLAIMS.json` | Claim labels and provenance from the manuscript, lemma audit, replay scripts and captured results. |
| `CREDITS.json` and `CREDITS.md` | Manuscript bibliography and contributions recorded by the replay job. |
| `PACKAGING.md` | This inventory. |
| `replay/PRIOR_ART.md` | New summary of dated scoreboard, literature, repository and community searches in the original prior-art document. |
| `replay/INPUTS.sha256` | Raw SHA-256 hashes of 11 external inputs read by the original audit, with public sources. |
| `sources/publish-trees/NikosVat__turan-c42@72703467aaac1082a123966b75f654a292c1e5f7.json` | GitHub recursive tree response for the pinned commit, with the queried commit recorded explicitly. |
| `SHA256SUMS` | SHA-256 of every other file in this folder. |

The original `REPORT.md` and `PRIOR_ART.md` contain machine-local paths and stay in the replay job. Their public summaries are listed above. The source job’s status, configuration and interpreter cache are outside the packet. The claimant TeX, PDF and trial JSON and Vatopoulos’s phase JSON are external inputs. Obtain them from the public sources in [the input manifest](replay/INPUTS.sha256) under their source terms.
