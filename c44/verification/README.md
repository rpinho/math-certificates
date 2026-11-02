# Verification receipts

Both exact checkers were rerun from a fresh extraction of the approved
source archive, using Python 3.12 with python-flint 0.9.0 and mpmath 1.3.0.
Their sources and inputs were unchanged. Both returned PASS and proved
an exact bound strictly below 4.3576549226.

The original review rejection harness was also run from that extraction
without edits. Every C44 case rejected as expected: seven mutations through
each of two checkers, for 14 C44 combinations. `rejection_controls.json`
contains those C44 receipts. No edited rejection harness was used. The
original review harness is not included in this public distribution.

`c44_exact.log` and `c44_fraction.log` contain raw successful checker output.
`live_source_receipts.json` records URLs, fetch times, byte counts and
SHA-256 digests of the live-source responses; full snapshots were retained
in the publication workspace. The audit's interpretation and limits are
in `../FINAL_LIVE_CHECK.md`.

Both checking programs were written by the same AI agent. These receipts
are computational evidence, without independent human review or formalization.
