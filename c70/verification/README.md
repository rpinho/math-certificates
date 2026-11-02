# Verification receipts

Both C70 checkers ran from a fresh extraction of the approved source archive,
without changes to the checkers, certificate or original rejection harness.
Every execution used Python 3.12 with python-flint 0.9.0 and mpmath 1.3.0
through the pinned uv command in the repository README.

`c70_arb.log` and `c70_rational.log` record PASS for the finite witness
above 1.20194336 and the limiting decimal lower endpoint 1.20194336847.
`c70_original_baseline.log` records the unchanged Patankar script;
`c70_arb_baseline.log` records the independent parity-recurrence reproduction.

The original review rejection harness executed unchanged and rejected all
32 combinations, including all 18 C70 combinations. `rejection_controls.json`
contains those C70 receipts, selected from the completed harness output.
No extracted or edited replacement harness was executed. The original harness
also depends on another problem's inputs and is not included in this distribution.

`live_source_receipts.json` records request URLs, UTC times, byte counts
and SHA-256 digests. Full snapshots and open-PR screening records remain
in the publication workspace. The audit's interpretation and limits are
in `../FINAL_LIVE_CHECK.md`.

Both checkers were written by the same AI agent. These are algorithmic
cross-checks, without independent human review or formal verification.
