# Adversarial referee (AI) for C68 >= 0.447

An independent adversarial referee was run on GPT-6 Astra, a different model from the producer (GPT-6.1 Sol). It was told to break the claim, wrote its own checks (`*.py`, `intervals.py`), and did not run the producer's verifiers as evidence.

- `REFEREE.md`: the report, covering (a) the definition match, (b) the contact-row lemma with a 200,000-configuration counterexample hunt, (c) the 23/200 Schur-complement correction, (d) an independent recomputation of every finite moment and the full scalar cover, and (e) old-setting dependencies.
- `results/`: its recorded outputs. `REPRODUCE.sh` reruns them.

Verdict: HOLDS. This is an AI review, not a human or second-party referee.

Path note: the report cites the source job's local paths. `../c68r3/` is published here as `../contact-row/`.
