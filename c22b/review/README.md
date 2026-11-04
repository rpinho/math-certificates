# Adversarial referee (AI) for C22b <= 7.090412

An independent adversarial referee was run on GPT-6 Astra, a different model from the producer (GPT-6.1 Sol). It was told to break the claim. It wrote its own interval code (`independent_*.py`) from the definitions and the proof, and did not run the producer's verifiers as evidence.

- `REFEREE.md`: the report, covering (a) definition match, (b) thickness, reach and length, recomputed independently, (c) knot type for every n with independent n=1 invariants, and (d) the limit.
- `*.json`: its recorded results. `run_referee_checks.sh` reruns them.

Verdict: HOLDS WITH CAVEATS. The caveats are the two prose errata already recorded in `../round1/ERRATA.md`. This is an AI review, not a human or second-party referee.

Path note: the report cites the source job's local paths. `../c22br2/frozen/c22b_7090412_rational/` is the frozen packet published here as `../round1/` (with the two errata applied in the release copy), and `../c22br2/` is the unpublished source job folder. The scripts read those local paths, so to rerun them, point them at `../round1/`.
