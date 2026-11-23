# Prior art: clean-room replay of the Erdős #982 small-n verification (idea 63c49f6b)

Captured 2026-11-23 (UTC 00:55).

## The problem
- erdosproblems.com/982: in every convex n-gon some vertex has at least floor(n/2) distinct distances to the other vertices (the regular polygon shows floor(n/2) is best possible). Bounds: Moser ceil(n/3); Erdős–Fishburn floor(n/3+1); Dumitrescu ceil((13n-6)/36); Nivasch–Pach–Pinchasi–Zerbib (13/36 + 1/22701)n - O(1) (arXiv:1207.1266). Altman proved the weaker statement that n points in convex position determine floor(n/2) distinct distances in total. The record lists n = 8 as the smallest open case.
- Formal statement: google-deepmind formal-conjectures ErdosProblems/982 (Lean statement only, no proof).

## The claim being replayed
- Paulee314, plasma-ai/erdos#66 (2026-11-02, 0 comments): every strictly convex n-gon with n <= 13 has such a vertex; new orders n = 8, 10, 12 (odd n by deleting a vertex). Method: a SAT encoding with geometric clause families, DRUP/LRAT-checked, plus one exact algebraic certificate at n = 12 (details sealed from the producer). Their stated caveat: the hand proofs that the clause families are sound and the cover argument are not machine-checked; no Lean.
- Code: github.com/Paulee314/erdos982 (latest commit 19ca234 on 2026-11-22, co-authored by Claude Opus 5); n = 12 proofs: doi:10.5281/zenodo.23880465. Claimant used AI (Claude family) for computation, code, reviews and drafting.

## Baseline
- Only the claimant's own checks (DRUP/LRAT for their CNFs, their cover audit scripts). No independent encoding or soundness proof is public.

## This round's contribution
An encoding written from the problem statement by a non-Claude model, with its own soundness proof for every constraint family it uses, solved and certified (DRAT/LRAT) for n = 8 and n = 10, n = 12 if time allows; then a comparison with their pattern counts. Their code stays sealed from the producer.

## Search
- Web: "Erdős problem 982 convex polygon vertex distinct distances n=8 computer verification" (problem page, formal-conjectures statement, NPPZ arXiv:1207.1266; no replay found).
- GitHub: Paulee314/erdos982 (0 forks, 0 open issues).
- X live search (captured): "erdos 982 OR \"distinct distances\" convex polygon": no results.
Not an exhaustive claim.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Paulee314/erdos982@19ca234 claimant DRUP/LRAT + cover audit (plasma-ai/erdos#66)",
 "sources": {
  "github": {
   "status": "none",
   "query": "erdos 982 convex polygon distinct distances SAT",
   "searched_at": "2026-11-23T00:45:17+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "erdos 982 OR \"distinct distances\" convex polygon (X live search)",
   "searched_at": "2026-11-23T00:42:23Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-23T00:42:23Z) for key 63c49f6bbefc461e9765f9d6b641d95b; 0 posts. Key-level capture; no new X search was performed.",
   "capture_sha256": "dd64edd295db1939b640d44791a2744be3f46dc52dc7c77a0b28140adc3de8eb"
  },
  "papers": {
   "status": "hits",
   "query": "distinct distances vertex convex polygon",
   "searched_at": "2026-11-23T00:45:17+00:00",
   "hits": [
    "https://doi.org/10.1007/s00454-006-1262-y",
    "https://doi.org/10.1016/0925-7721(94)00020-v",
    "https://doi.org/10.1016/j.disc.2013.05.007",
    "https://doi.org/10.1016/s0925-7721(01)00037-2",
    "https://doi.org/10.1145/997817.997829",
    "https://doi.org/10.20382/jocg.v4i1a1"
   ],
   "note": "OpenAlex relevance search, top 6; the worker reads them before modelling.",
   "source": "OpenAlex"
  },
  "leaderboards": {
   "status": "none",
   "query": "erdos 982 convex polygon distinct distances SAT",
   "searched_at": "2026-11-23T00:45:17+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```


## Local replay update (2026-11-23 UTC)

This job used the supplied snapshot for the scoreboard, papers, code and community context. No live source or claimant materials were fetched. The official baseline in the snapshot is the strongest published asymptotic bound it lists, by Nivasch, Pach, Pinchasi and Zerbib. The exact small-order baseline is the claimant's reported result, with its materials sealed under this job's rules. The independent encoding and its own certificates reproduce the bounds at n = 8, 10 and 12, with their odd successors by deletion. The regular polygon supplies the matching exact upper construction. This is a reproduction of an announced result.

Sources from the snapshot: [official problem](https://www.erdosproblems.com/982), [Nivasch et al.](https://arxiv.org/abs/1207.1266), [formal conjecture](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/982.lean).
