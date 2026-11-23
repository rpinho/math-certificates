# Prior art: clean-room replay of the Erdős #1182 upper bound F(n) <= 5.03n (idea db708cdb)

Captured 2026-11-23 (UTC 01:10).

## The problem
- erdosproblems.com/1182: a connected graph G on n vertices has R(K3, G) >= 2n - 1 (Chvátal–Harary bound); G is *good* if equality holds. F(n) is the largest q such that every connected graph with n vertices and at most q edges is good. The page records (17n + 1)/15 <= F(n) <= 84n.
- Burr, Erdős, Faudree, Rousseau, Schelp (1980): the problem and the lower-bound reduction. Brandt (1996): F(n) <= 84n by counting embeddings of random regular graphs; announced 11.75n without proof; expected under 6n. Brandt, Brinkmann, Harmuth (EJC 5, 1998, #R7): exact F(n) and f(n) for n <= 12.

## The claim being replayed
- Pravar Kataria with Claude (Fable 5.1), erdosproblems.ai claim 2026-09-28 and forum proof-claim 377 (0 replies); package github.com/Sovi11/erdos-1182, revised commit 6d4f78cfb15296297450618dde6fea8b15478ccc. Claims F(n) <= 11n/2 for large n and F(n) <= 5.03n: a first-moment count of embeddings of a random d-regular graph (d = 10, plus 0.03n extra edges) into the complement of the balanced blow-up of C5 has negative exponent, certified by a branch and bound over a capped five-component simplex (74,710 accepted regions, worst bound -0.000500006371..., replayed in 100-digit decimal arithmetic; about 9 min). Also F(n) >= n + floor((n-1)/6) via Sidorenko's R(K3, H) <= 2e(H) + 1.
- The README says unrefereed, corrections welcome; the human author re-ran the code; no specialist check. Claimant-side differently written checks exist in the same repository.
- Inputs given to the replay: note.pdf, BOUNDS.md, preprint main.tex and README.md at that commit (mathematics and claims only). Their code/ directory is not given.

## Baseline
- Brandt's 84n (published) is the refereed upper bound; the claim's 5.03n and 11n/2 are unreplayed.

## Search
- QUEUE.md survey (math_wave_1030/erdosqueue, 2026-11-23): claim record, author tracker (empty), forum claim 377 (0 replies), web, arXiv and X-index: no replay found.
- X live search (captured): "Ramsey goodness" OR "erdos 1182" OR "R(K3" good: no posts.
Not an exhaustive claim.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Brandt 1996 F(n)<=84n (refereed); claimant Sovi11/erdos-1182@6d4f78c own checks",
 "sources": {
  "github": {
   "status": "none",
   "query": "erdos 1182 Ramsey goodness triangle upper bound",
   "searched_at": "2026-11-23T01:05:26+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "\"Ramsey goodness\" OR \"erdos 1182\" OR \"R(K3\" good (X live search)",
   "searched_at": "2026-11-23T01:04:22Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-23T01:04:22Z) for key db708cdbf4324616a9d7079a8bc1a019; 0 posts. Key-level capture; no new X search was performed.",
   "capture_path": "(local capture file, not published)",
   "capture_sha256": "dc7a590b49a12f0384a83be59c29e070904dfe22a736f9cedb7f7f1ab0b7d130"
  },
  "papers": {
   "status": "hits",
   "query": "Ramsey goodness triangle connected graphs sparse F(n)",
   "searched_at": "2026-11-23T01:05:26+00:00",
   "hits": [
    "https://doi.org/10.1002/jgt.70125",
    "https://doi.org/10.1002/rsa.21124",
    "https://doi.org/10.1016/j.disc.2025.114831",
    "https://doi.org/10.19086/aic.2023.4",
    "https://doi.org/10.46298/dmtcs.15817",
    "https://doi.org/10.48550/arxiv.2507.09832"
   ],
   "note": "OpenAlex relevance search, top 6; the worker reads them before modelling.",
   "source": "OpenAlex"
  },
  "leaderboards": {
   "status": "none",
   "query": "erdos 1182 Ramsey goodness triangle upper bound",
   "searched_at": "2026-11-23T01:05:26+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## Added 2026-11-23 (CS review f294eb07)
- Related, not a rival: github.com/FireflySentinel/erdos-1182 (Zenodo) concerns f(n), the maximum number of edges of a connected good graph, not F(n). Seen only as a search snippet.
- The formal-conjectures statement of #1182 notes that [BEFRS80] names these functions g and f (swapped).

## Local replay, 2026-11-23 UTC

The two requested upper constants were reproduced independently from the staged mathematics at the [pinned revision](https://github.com/Sovi11/erdos-1182/tree/6d4f78cfb15296297450618dde6fea8b15478ccc). The baseline on the [problem page](https://www.erdosproblems.com/1182) in the supplied survey is Brandt's proved 84n, with 11.75n announced. The [claim forum](https://www.erdosproblems.com/forum/thread/1182/proof-claims) and community searches above are dated snapshots. This offline job used those snapshots and the four staged documents. It did not perform fresh searches, reproduce Brandt's 1996 argument, or inspect any author's program. No novelty claim is made. See REPORT.md for independent exponents, evidence and limits.
