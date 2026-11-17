# Prior art for Erdős #1183 n=21..24 (17 November 2026)

The public baseline is **exact f(n) through n=20**, stated in Bhattacharjee–Bhattacharya's BLLM manuscript, Theorem `fvalues`, in [creelie/eBLLM](https://github.com/creelie/eBLLM/blob/HEAD/paper/bllm/paper/sections/sec10d_crossing.tex). Its Lemma `levelposet` gives the same exact weighted-poset method. The n=20 word `000101100111001011100` reproduces here with exact maxima12/12 and checked trees. Our round-4 candidate packet supplies another word and internal clean-room review, not priority for the method or the values through20.

The revised BMB manuscript at `2842ef3a58604a8f4b35271d5753c2bf9bdecd0b` gives lower bounds12,13,13,14 for n=21..24. The bound13 at n=22 depends on `thm:f20` and its computer-assisted `lem:window20`; the other three also follow from `prop:flower`, whose twelve-level proof does not depend on that lemma. The odd lower bounds are additionally proved by this job's complete balanced-word witnesses and chain exchange.

The original pre-launch planning note and launcher snapshot below missed the BLLM finite-value theorem and understated public prior art as n<=10. They are preserved as a historical search record and are superseded by the dated execution reads following them. No n=21..24 value has appeared in the material read so far; the required final recheck will be recorded before REPORT.md.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Public exact f(n) only for n<=10 (BMB); our candidate f(11..19), f(20)<=12 (packet a0af345); lower bounds n=21..24: 12,13,13,14 (BMB prop:flower/thm:f20, chain)",
 "sources": {
  "github": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T16:18:54+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "\"Erdos 1183\" OR \"Erd\u0151s 1183\" OR \"erdosproblems.com/1183\" OR \"sublattice function\" (Latest)",
   "searched_at": "2026-11-17T16:18:50Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-17T16:18:50Z) for key 4bc659c0b87a4b7bac4e8e5588194713; 0 posts. Key-level capture; no new X search was performed.",
   "capture_sha256": "83debcb4f56601c31549d96a546fb3b9013c39b9ecc07aa7ba4208ef2ab7f29d"
  },
  "papers": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T16:18:54+00:00",
   "hits": [],
   "note": "cached search answer from Europe PMC, fetched 2026-11-17T13:19:06.875323+00:00 (TTL 30 days); the worker reads them before modelling.",
   "source": "Europe PMC"
  },
  "leaderboards": {
   "status": "none",
   "query": "Erdos 1183 sublattice two-colouring",
   "searched_at": "2026-11-17T16:18:54+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## Execution source check

2026-11-17: read round-4 PROOF.md, REPORT.md, REPRODUCE.md, the internal clean-room REFEREE.md and both pre-launch reviews. The baseline is their exact weighted-poset enumeration with concrete witnesses and separately written replay checker. This job extends its dimensions; it does not propose a new method. Live source bodies and dated fetch records will be retained in sources/. Network restricted to the domains in the spec.

### Initial live reads, 2026-11-17 16:26–16:35 UTC

Problem page and discussion/proof-claims thread: no exact n=21..24 values found. The paper remains arXiv:2610.02833v1 (2 October 2026); its revised GitHub manuscript remains 2842ef3a58604a8f4b35271d5753c2bf9bdecd0b (14 October). Source body `sources/initial_paper` confirms prop:flower uses only the twelve-level gadgets/window and separated stacking, **not lem:window20**. thm:f20 explicitly rests on that computer-assisted lemma. Bounds (chain, flower, twenty) are (11,12,12), (12,12,13), (12,13,13), (13,14,14).

GitHub repository search sorted updated returns anaxia-research/Erdos-1183 and QuanyuTang/erdos-problem-1183. The latter holds a March 2026 chat/translation giving asymptotic results, linked in the forum. Issue #20 still contains n=11..14, last updated 17 November 12:03:56 UTC. All 19 manuscript PRs were read by title/body; the most recent mathematical change is #17 (twenty levels), 14 October. A global issue body/title search additionally found anaxia-research/D7 and eBLLM (now creelie/eBLLM), which state exact values through n=20. Their level data and logs are captured; their claim is prior art and must be credited, not counted as a discovery here. The rpinho/math-certificates public packet now also includes round-4 n=15..20, so the planning paragraph's public-status wording above is historical.

Named result repositories read: BakeLab/Epi-results, google-deepmind/alphaevolve_results, kisonecat/openai-math, plasma-ai/erdos, togethercomputer/EinsteinArena-new-SOTA; no n=21..24 candidate found in returned paths/relevant text. The openai/math recursive tree is truncated; its root and CONTENTS.md were fetched to avoid treating truncation as absence. google-deepmind/repository_of_problems returned HTTP 404 (not an absence claim). formal-conjectures PR #7902, updated 11 November, proves only the chain lower bound. arXiv searches for monochromatic sublattice, Erdős Ulam, and monochromatic union were read; no later relevant exact-value paper was found in returned results. No new X read: only the planning note's captured empty search, because this job restricts network domains. This is a bounded search, not an exhaustive priority claim. Dated URLs and source hashes are in sources/*fetch.json. One parallel optional-source fetch stopped on the 404; later source reads use per-URL error handling.

Baseline locally reproduced: the round-4 word 110010110001101100110 has maxima 12/12 and no-family-at-13 trees of 3,577/7,471 nodes (`logs/baseline20.log`). Existing code is the method; this job extends it to larger dimensions.

The BLLM source was read in full for its relevant subsection (`sources/bllm_sec10d_crossing.tex`, lines 53–86). It explicitly states the same weighted-poset reduction (Lemma levelposet), exact f(n) through 20 (Theorem fvalues), and 59 optimal rank-word orbits at n=20. Its word 000101100111001011100 reproduces locally with both exact maxima 12 and both checked no-family-at-13 trees (`logs/public_baseline20.log`). This is a second baseline word, using the same standard method. The public baseline is not limited to n<=10, contrary to the historical planning note. This correction changes no n=21..24 target. No n=21..24 value appeared in the 40 BLLM section files retrieved and searched. Credit Bhattacharjee and Bhattacharya for this existing public computation, alongside BMB for the lower bounds.

### Finite upper-bound comparison

BMB Theorem thm:f prints min{n²+n+1,2n(L+K+3)+L+K+4}, L=floor(log2 n)+1, K=floor(log2 L)+1. At n=21..24 this is 463,496,518,540. A stronger control is an explicit inference from the public n=20 upper12 construction: ignoring k extra coordinates splits any monochromatic closed family into2^k closed slices of size at most12, so upper bounds24,48,96,192 follow. Product families attain those maxima in that particular colouring. This inference is not a quoted published n=21..24 table, and involves no non-rank search. The new candidate word bounds are compared with both the printed finite estimates and this simple inherited construction, without claiming a new method.

### Index bodies read, 2026-11-17 18:10–18:12 UTC

Read the AlphaEvolve mathematical-results notebook and the Epi, kisonecat and EinsteinArena READMEs. The notebook's 1183 substring hits were digits within unrelated numeric constructions, not the Erdős problem; no sublattice/Erdős–Ulam result appeared. The PLASMA E1183 index, its Chojecki/BMB claim notes, and associated library/evidence Markdown were also fetched and read for the f/F scope and finite n=21..24 values. They describe the asymptotic bounds and union-family claims, not new finite values here. Dated captures are in sources/index_fetch.json and sources/plasma_fetch.json. The official page/forum, BMB manuscript/issues/#20, BLLM finite-value theorem and arXiv are to be reread immediately before REPORT.md.

## Final public check before REPORT.md

Final full-source reads: 17 November 2026,19:04:34–19:05:27 UTC; immediate pre-report rereads:19:27:21–19:27:23 UTC. All returned200. Problem, discussion and the actual /proof-claims page have unchanged visible text. BMB manuscript, repository issues/PRs, #20 comments, BLLM finite-value theorem and arXiv/search bodies are unchanged. The proof-claims page has only the October5 union-family claim, not finite values here. Issue#20 still has only n=11..14, updated12:03:56 UTC. BMB HEAD remains2842ef3a58604a8f4b35271d5753c2bf9bdecd0b; BLLM HEAD is241326bbba4726afde74ae1858265878b2176c59 and still states finite values only through20. The final public packet tree has no n=21..24 files. The relevant final issue search gives no such finite values; named result-repository checks likewise found none in returned material. No priority “first” is asserted.

Source bodies are losslessly retained in sources/captures.tar.xz; dated URLs and SHA256 values stay in sources/*fetch.json. The archive includes the primary manuscript, BLLM section, official page/forum/proof claims, issue bodies/comments, arXiv and result-index captures. This is a bounded priority search. The new candidate bounds improve the printed finite estimates under the same definition; the exact weighted-poset method is existing public work.
