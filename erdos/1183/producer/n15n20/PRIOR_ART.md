# Prior art for Erdős #1183 n=15..20 (planning note, 17 Nov 2026)

Best public: exact f(n) known publicly only for n <= 10 (Bhattacharjee–Mandal–Bhattacharya tables, arXiv:2610.02833); our candidate packet (math-certificates c763c6a, erdos/1183) adds f(11)=7, f(12)=7, f(13)=8, f(14)=8. Lower bounds for n=15..20 from BMB prop:flower / omega note / chain: 9, 9, 10, 10, 11, 11. No public upper bound below the trivial for n >= 15 found in our 16-17 Nov searches (erdos_sat3/PRIOR_ART.md: problem page and forum, anaxia-research/Erdos-1183 incl. issue #20, omega note, arXiv, GitHub search). X: browser capture, no #1183 posts. The job rechecks all sources at start.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Public exact f(n) only for n<=10 (BMB); our candidate f(11)..f(14) (packet c763c6a); lower bounds n=15..20: 9,9,10,10,11,11 (BMB prop:flower, omega, chain)",
 "sources": {
  "github": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T13:19:07+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "hits",
   "query": "\"Erdos 1183\" OR \"Erd\u0151s 1183\" OR \"erdosproblems.com/1183\" OR \"Erdos-Ulam\" (Latest)",
   "searched_at": "2026-11-17T13:19:02Z",
   "hits": [
    "https://x.com/EZtelchar/status/1452233277432082436",
    "https://x.com/Lim_Rim_/status/1807080641303126392",
    "https://x.com/littmath/status/1613271607329300503",
    "https://x.com/littmath/status/1613299206944432131",
    "https://x.com/tsatie/status/955750924034572291"
   ],
   "note": "Captured X search (browser, 2026-11-17T13:19:02Z) for key e755334cb3cc417d9bc9853357b515b4; 5 posts. Key-level capture; no new X search was performed.",
   "capture_sha256": "b18ce896e055bf04275049109489c2ae88d4e0205b8087df840ad13877d70afc"
  },
  "papers": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T13:19:07+00:00",
   "hits": [],
   "note": "Europe PMC relevance search, top 0 (after OpenAlex: HTTP 429, retry-after 38456s; Semantic Scholar: HTTP 429); the worker reads them before modelling.",
   "source": "Europe PMC"
  },
  "leaderboards": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T13:19:07+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## This run: initial correction (2026-11-17 13:31 UTC)
The full referee source contains a further bound omitted by the planning brief: BMB `thm:f20`, ceil((n+1+2 floor((n+1)/20)+[remainder>=12])/2), gives **12 at n=20**, not 11. Live source retrieval is in progress before mathematical search. The requested expected lower-bound vector is therefore provisional. The existing public method reproduced here is the referee's weighted-poset decision procedure, with its n=13/14 words as baseline data; it is not a predictive model and no SBS score is applicable.

## Live initial check (2026-11-17 13:34 UTC)
All 18 requested public reads succeeded (sources/start_fetch.json). The problem page and forum contain no f(15)..f(20) exact values. Issue #20 now has Ricardo's 12:03:55 UTC comment with candidate f(13)=f(14)=8 (packet c763c6a); no higher values. The GitHub paper is unchanged from the referee's copy (SHA256 dd6dbb0971c4d9a86123edd5223c431168b2fe14a1076380bb73de0f95ccc81c). Its `thm:f20` corrects the n=20 bound to 12; lower bounds used here are **9,9,10,10,11,12**. ArXiv still lists only v1, submitted 2 October 2026; the GitHub text is later and must be distinguished from that version. No journal/refereed status found. The omega note states the odd bound for all odd n>=11 and claims Lean verification; we do not rerun Lean. It adds no stronger number in this range than prop:flower.

AI-repository trees checked: BakeLab/Epi-results, google-deepmind/alphaevolve_results, openai/math, kisonecat/openai-math, plasma-ai/erdos (SHAs saved in raw sources). OpenAI's recursive tree is truncated, so its absence of path hits is not exhaustive. No new relevant exact value found. The relevant plasma paths are the E1183 wiki, not the geometric Erdős–Ulam distance problem. The existing X capture above is inherited, not a fresh search. Network limits exclude fresh X/Reddit queries. The best existing finite construction remains the n=14 word in the public candidate packet and the referee's weighted-poset method.

## Final public recheck, 2026-11-17 13:42:36 UTC
All eighteen reads repeated successfully (sources/final_fetch.json). Paper, README, issue list, issue #20 and its f(13)/f(14) comment, omega note, repository search, candidate-certificate tree, and all five AI-result trees are byte-for-byte unchanged. Problem and forum HTML changed only outside the normalized visible text (sources/final_compare.json: both visible texts identical). No exact f(15)..f(20) settlement found; none was dropped.

Additional reads: arXiv v1 source, arXiv searches for “Erdos Ulam union” and “Bhattacharjee Mandal”, the plasma E1183 wiki, and OpenAI/math CONTENTS.md (the latter avoids relying solely on the truncated tree). No newer relevant finite value found. The arXiv source was opened: it has neither prop:flower nor thm:f20; it asks whether the chain ceiling is always sharp. The stronger bounds used here must be attributed specifically to the revised GitHub manuscript, commit 2842ef3a58604a8f4b35271d5753c2bf9bdecd0b, dated 14 October 2026. The omega note is unchanged and explicitly claims a Lean proof for all odd n>=11; no Lean run was performed here. No journal publication or human refereeing status was established.

Novelty assessment: the six numerical equalities in this job are candidate additions relative to the bounded public sources checked; the method is an extension of our referee's existing method. No claim of a new general method or a priority “first” is made. At n=20 the candidate equality uses the revised manuscript's computational theorem for its lower bound; without that dependency, the result is an upper bound twelve and an unrestricted gap 11..12.

## Immediately before reporting: 2026-11-17 14:06:27 UTC
Fourteen further reads all returned HTTP 200 and unchanged mathematical content or repository root SHA: problem, forum, revised paper, issue #20 and its comments, all issues, omega note, arXiv landing page, anaxia latest commit, and the five named AI-result repository roots. Details: sources/pre_report_fetch.json; log: logs/late_sources.log. No n=15..20 public settlement appeared. Source bodies are losslessly retained in sources/captures.tar.xz; dated metadata remain directly readable. Identical final bodies share initial captures within that archive.
