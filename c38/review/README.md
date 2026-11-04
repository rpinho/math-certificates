# C38 adversarial AI referee (GPT-6 Astra), 2026-11-04

[REFEREE.md](REFEREE.md) is the report of an independent referee job run on a different model from the producer, told to break the claim `μ(Z²) >= 8388608/3192535 = 2.62756963...` in [../bridges-span18](../bridges-span18/). It wrote its own enumerators (`independent_*.cpp`, `literal_walks.cpp`) and audits (`*.py`) and did not execute producer code.

**Verdict: HOLDS WITH CAVEATS.** No mismatch through span 15 or in either rectangle recount; the exact k = 1353 slack is positive (about 1.14372e-7). **Caveat:** five span 16–18 primitive evaluations (point b spans 16, 17, 18; point c spans 16, 17) were checked as source/data/hash claims only and were not independently regenerated. Their numerical validity remains a premise of the bound.

Path note: the report was written in the referee's working layout, where `../c38/` is the producer packet. In this repository that packet is [`../bridges-span18/`](../bridges-span18/). Run logs and process-ID files were omitted; `results/` keeps the JSON outputs. Saved third-party source pages are not republished.

This is an AI review, not a second party, and not a human mathematical review.
