# Independent referee prior-art audit

Started 2026-11-03 20:41 UTC, before writing referee code.

The claim concerns FiFAR (2025 Scientific Data, Table 7) and Marco Sampaio.
The claimant reports original best costs 138.1, 142.0, 126.2, 141.6, 132.0,
and stronger pre-existing public LP/retraining values 133.3, 133.6, 116.0,
134.4, 131.7 at https://github.com/nguyetvo/l2d-prediction-vs-assignment.
These are leads, not independently accepted facts.

Plan: read the primary paper and released artifacts; check official code,
issues/PRs and the stronger public reproduction; search recent code, papers,
agent/lab repositories and public discussion before constructing a referee.
Reproduce the original benchmark as the baseline; no new method search or
novelty/priority judgment is intended. Public-source checks and their limits
will be recorded below. All numerical work runs only on the authorized pod.

20:42–20:44 UTC live primary-source reads succeeded on the pod. The paper's
Table 7 prints 138.1, 142.0, 126.2, 141.6, 132.0 as the best team cells
(Team 2 is OvA). Its equations define FN + lambda FP, lambda=.057;
the table uses total cost despite prose saying average cost. The released
results notebook confirms total cost, not percentage or per-alert cost.
The released-artifact and retrained LP tables at the URL above confirm the
stronger prior cells quoted at the start. Full retraining is unnecessary for
this limited referee; released decisions will be independently evaluated.

Fresh official README, issue and PR pages, GitHub FiFAR README search sorted
updated, arXiv FiFAR/DeCCaF query, and required lab repository landing pages
were retrieved; HTTP receipts are in source_fetch.json. repository_of_problems
and the guessed EinsteinArena GitHub address returned 404, not negative results.
Lab landing-page coverage is limited. Google returned a consent page, so public
discussion coverage remains incomplete. No novelty or record claim is made.
The claimant already credits Nguyet Vo's exact-assignment audit and the
Fatigue-aware-human-AI-triage project's class-conditional modelling suggestion.

Final public-source refresh completed before 21:12:27 UTC, after all candidate
choices were fixed and independently verified. The official Table 7 and both
raw prior-LP result tables returned HTTP 200 and were byte-identical to the
initial reads. Official issue/PR pages, the recent-code query and required
lab landing pages were requested again; individual successes/failures are
retained in FINAL_SOURCE_REFRESH.json. No candidate was changed in response.

Independent baseline reproduction: all 250 original OvA/DeCCaF source-result
costs match the printed table at its precision. All 250 saved released-LP
comparators were also evaluated directly and reproduce the claimant's exact
means. A new transportation solve changes 17 realized costs because objectives
are nearly tied (maximum summed-forecast objective gain only 7.571e-8 at
1e-12 precision). Its DeCCaF means are 133.31288,139.08064,119.60476,
133.78820,132.00812. This does not affect the conditional policy: all 125
headline assignments and exact costs reconstruct identically. Retrained
public baseline weights remain unavailable; no full retraining is claimed.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Table 7 best costs 138.11/141.97/126.17/141.58/132.01",
 "sources": {
  "github": {
   "status": "hits",
   "query": "bank account fraud dataset",
   "searched_at": "2026-11-03T21:21:24+00:00",
   "hits": [
    "https://github.com/Monika-Ashokkumar/Bank-Account-Fraud-Detection",
    "https://github.com/bao-jerry/Bank-Account-Fraud-Detection",
    "https://github.com/feedzai/bank-account-fraud",
    "https://github.com/ilyaravand/knn-and-kmeans-on-Bank-Account-Fraud-Dataset",
    "https://github.com/taradalaei/Bank-Account-Fraud-Dataset-processed"
   ],
   "note": "GitHub repository search, top 5 by best match."
  },
  "x": {
   "status": "hits",
   "query": "bank account fraud dataset",
   "searched_at": "2026-11-03T14:42:26+00:00",
   "hits": [
    "https://x.com/KirkDBorne/status/2117463469272539145",
    "https://x.com/arnaudmercier/status/2117285743932346663"
   ],
   "note": "Captured X search (browser, 2026-11-03T14:42:26+00:00) for the friend topic; 2 posts. Friend-level capture, not a per-target X search.",
   "capture_path": "friends_queue/x_capture/frozen/sampaio_9b37d9eb821a.jsonl",
   "capture_sha256": "9b37d9eb821a9e6628753f515548a98c81dd84f18b504cce3907676bd59ebf8a"
  },
  "papers": {
   "status": "hits",
   "query": "learning to defer fraud detection human-AI collaboration benchmark",
   "searched_at": "2026-11-03T21:21:24+00:00",
   "hits": [
    "https://doi.org/10.11591/ijai.v13.i2.pp1925-1934",
    "https://doi.org/10.1201/9781042025091-8",
    "https://doi.org/10.30574/wjaets.2025.15.2.0627",
    "https://doi.org/10.37591/njitm.v9i2.1910",
    "https://doi.org/10.52710/cfs.873",
    "https://doi.org/10.71443/9789349552005-08"
   ],
   "note": "Crossref (OpenAlex daily quota exhausted) relevance search, top 6; the worker reads them before modelling."
  },
  "leaderboards": {
   "status": "none",
   "query": "bank account fraud dataset",
   "searched_at": "2026-11-03T21:21:24+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```
