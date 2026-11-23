# Prior art: independent exhaustive check of v(9) = 13,856,993 for Erdős #293 (idea 60fb004f)

Captured 2026-11-23 (UTC 14:40).

## The problem
- erdosproblems.com/293: v(k) = the least integer m > 1 that is a denominator in no representation 1 = 1/n_1 + ... + 1/n_k with n_1 < ... < n_k distinct (van Doorn–Tang convention, arXiv:2512.22083; their Lemma 2.1: D_k is contained in D_{k+1}). OEIS A400352: 4, 11, 17, 103, 733, 27539, 13856993 (k = 3..9). Counts of representations: OEIS A006585 = 1, 0, 1, 6, 72, 2320, 245765, 151182379 (k = 1..8).

## History (teorth/erdosproblems#368 and #403, the HELP WANTED issue)
- k <= 8: papanokechi (#368); recomputed by the #403 author (jonathanwxh-cell, with Claude) with two implementations and 28,395 exact certificates; EconLearn full enumeration matching A006585(8) = 151,182,379 (github.com/EconLearn/erdos293-check).
- k = 9 positive half: certificates for every m in [2, 13,856,992] by EconLearn (release v9-certificates, files to 20M) and ntysdd (hard cases, results_500/1124/2248 zips), all re-checked by EconLearn with fractions.Fraction.
- k = 9 negative half: EconLearn, 2026-09-23, code/findm_complete.c, 2,000 prefix shards, 0 solutions, 0 skipped branches, 406,906,925,247 nodes, about 29 min on a 10-core laptop; controls at k = 6, 7, 8 (27538 -> 474 representations, 27539 -> 0, 733 -> 0, 103 -> 0, 79 -> 2). ntysdd: bounded search (largest term < 1e20), also found none; not exhaustive by the author's own account.
- k = 10: doge-th (2026-11-22), certified coverage to about 13.87M, sampled density to 1e9, asks for shard help; v(10) open.

## Baseline
- One exhaustive absence proof for 13,856,993 at k = 9 (EconLearn), plus a bounded second search. No second independently written exhaustive search found.

## Method facts from the issue (mathematics, public)
- m in D_k iff (m-1)/m is a sum of k-1 distinct unit fractions none equal to 1/m.
- One term left: p/q is a unit fraction iff p = 1 after reduction. Two terms left: 1/a + 1/b = p/q iff (pa - q)(pb - q) = q^2.
- Deficit identity: from remaining 1/k, the next denominator d gives remaining 1/k' with k' = k + k^2/(d - k), integral iff (d - k) | k^2.

## Search
- GitHub issues #368, #403 (54 comments read), EconLearn/erdos293-check (README and log only), OEIS A400352 and A006585.
- X live search (captured): 13856993 OR "erdos 293" OR A400352: nothing relevant.
Not an exhaustive claim.

```rh-prior-art
{
 "schema": 1,
 "baseline": "EconLearn findm_complete.c exhaustive 2000-shard run (v(9)=13856993, 0 solutions) + ntysdd bounded search",
 "sources": {
  "github": {
   "status": "none",
   "query": "erdos 293 v(9) 13856993 unit fractions",
   "searched_at": "2026-11-23T14:24:33+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "13856993 OR \"erdos 293\" OR A400352 (X live search)",
   "searched_at": "2026-11-23T14:22:50Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-23T14:22:50Z) for key 60fb004fd51d40db8f95dffe1bd0e9e6; 0 posts. Key-level capture; no new X search was performed.",
   "capture_sha256": "ca058c8255a075610db156e6d9b40c8f8823fbbbb5d94a3fdef53cca5b4c9d8f"
  },
  "papers": {
   "status": "hits",
   "query": "unit fraction representations of 1 denominators van Doorn Tang",
   "searched_at": "2026-11-23T14:24:33+00:00",
   "hits": [
    "https://doi.org/10.68040/2025331.3454",
    "https://europepmc.org/article/PMC/PMC13439031"
   ],
   "note": "Europe PMC relevance search, top 2 (after OpenAlex: HTTP 429, retry-after 34550s; Semantic Scholar: HTTP 429); the worker reads them before modelling.",
   "source": "Europe PMC"
  },
  "leaderboards": {
   "status": "none",
   "query": "erdos 293 v(9) 13856993 unit fractions",
   "searched_at": "2026-11-23T14:24:33+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## Replay scope (2026-11-23)

Sources preserved from the supplied capture: [Erdős #293](https://www.erdosproblems.com/293), [computation thread](https://github.com/teorth/erdosproblems/issues/403), [earlier thread](https://github.com/teorth/erdosproblems/issues/368), [van Doorn–Tang](https://arxiv.org/abs/2512.22083), [A400352](https://oeis.org/A400352), [A006585](https://oeis.org/A006585), and [EconLearn's certificate release](https://github.com/EconLearn/erdos293-check/releases/tag/v9-certificates). The supplied capture is the evidence for the baseline and public discussion. This job's network restriction precludes refreshing the scoreboard or papers. It also prohibits fetching, reading, or replaying the baseline implementation. The local reproduction uses a new implementation of the public exact unit-fraction reduction and identity, with separate certificate verification. Local outcomes are recorded in REPORT.md when available.

## Local reproduction outcome (2026-11-23)

The separately written solver completed all 1,412 local shards with zero solutions and zero skipped branches. The exact checker verified all 13,856,991 required labels with zero bad or missing lines. All specified controls matched. This reproduces the published value, with no new value claimed. See [REPORT.md](REPORT.md) for the sealed run and the node-count comparison.
