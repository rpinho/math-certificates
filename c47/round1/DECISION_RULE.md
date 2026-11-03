# C47 filing decision rule (frozen 2026-11-03T16:47:03Z, before the hf.py provenance test finishes)

Agreed between the math lane and general (Ricardo's lead session), 2026-11-03.

Test: run Tomar's own lowerbound/search/hf.py (tejasvi/square-maximal-weak-type v5, commit 3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a) from his own published 50-atom measure, his settings, for at most 6 CPU-hours.

- If it does NOT reach a ratio >= 1.7030 within 6 CPU-hours -> option (A): one PR on constants/47a.md recording Tomar's lower 1.7027237335 and upper 3.59123 (credited to him), plus our asterisked candidate row described as "further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts". Reviewed PRs go out under the standing rule.
- If it DOES reach >= 1.7030 -> option (B): the PR records only Tomar's bounds; our improvement is offered to him.
- Either way: a short note to Tomar crediting his method and pointing to the result, through `rh outreach` (outreach under Ricardo's name; Ricardo reads it first). No issue or comment on Tomar's repository before Ricardo has read it.
