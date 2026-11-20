# Prior art: C82 (Tao 82a), essential minimum of the Zhang–Zagier height, upper bound

Checked 2026-11-20 (math lane). Search limits stated; "not found" is not evidence of absence.

- Table 82a (teorth main): PR #87, merged 2026-06-12 (maaxgrin, [Gri26]) C82 <= 0.2536331090204145, Doche polynomials P1..P9, Q1, Q2 plus perturbative factors; replayed by arhancanli 11-19. Earlier: 0.25444 (Doche 2001, J. Théor. Nombres Bordeaux 13, 103-110); PR #229 0.2534449 (10-18).
- Open candidates: PR #280 (vidigoat) v6, 14 Nov, C82 < 0.2519694883*, built on our #330 round-10 denominators (six monic degree-104), 37 numerators incl. 16 new (degree 24-42) from dual-weighted LLL; Arb checker; replayed by arhancanli with two programs (14 Nov). Our PR #330 printed 0.2519696460* (round 10, 13 Nov), replayed by arhancanli. Our PR #301 (degree-44 denominators, 0.253091834*). PR #242 replays.
- Ours, unpublished: round 11 (math_wave_1030/c82r11) certified 0.2519695579, above #280 v6.
- GitHub (PR search "C82" on teorth/optimizationproblems, all states): #87, #229, #242, #280, #298, #301, #330. No other C82 candidate below 0.2519694883 located.
- X (browser, @rpinho_sci, Latest): "Zhang-Zagier" and "Zhang-Zagier" OR "C82" height: no results.
- Authors' other repos (rule 11-17): maaxgrin/zhang-zagier-c82-bound (cb88f92, data for #87); vidigoat certificate commit 56f41fc on the #280 branch.

Baseline: #280 v6 (vidigoat), C82 < 0.2519694883* (six degree-104 denominators from #330 round 10, 37 numerators), replayed by arhancanli.

```rh-prior-art
{
 "schema": 1,
 "baseline": "#280 v6 (vidigoat): C82 < 0.2519694883*, six degree-104 denominators, 37 numerators",
 "sources": {
  "github": {
   "status": "hits",
   "query": "Zhang-Zagier height",
   "searched_at": "2026-11-20T09:29:10+00:00",
   "hits": [
    "https://github.com/rpinho/c82-height-certificate",
    "https://github.com/tejasvi-releases/zhang-zagier-lower-bound",
    "https://github.com/tejasvi-releases/zhang-zagier-lower-bound-v2",
    "https://github.com/tejasvi/zhang-zagier-lower-bound"
   ],
   "note": "GitHub repository search, top 4 by best match."
  },
  "x": {
   "status": "none",
   "query": "\"Zhang-Zagier\" (Latest); \"Zhang-Zagier\" OR \"Zhang\u2013Zagier\" OR \"C82\" height (Latest)",
   "searched_at": "2026-11-20T09:26:21Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-20T09:26:21Z) for key 1fdfd82a2bbd43f69aed4b622fae4b91; 0 posts. Key-level capture; no new X search was performed.",
   "capture_path": "x_capture/frozen/1fdfd82a2bbd43f69aed4b622fae4b91_4e4eead1c43e.jsonl",
   "capture_sha256": "4e4eead1c43ee61c79cda7bf36e8c91a1ffc5e0e5651c93d6fcc6d10e47dca9e"
  },
  "papers": {
   "status": "none",
   "query": "Zhang-Zagier height essential minimum",
   "searched_at": "2026-11-20T09:29:10+00:00",
   "hits": [],
   "note": "Europe PMC relevance search, top 0 (after OpenAlex: HTTP 429, retry-after 52275s; Semantic Scholar: HTTP 429); the worker reads them before modelling.",
   "source": "Europe PMC"
  },
  "leaderboards": {
   "status": "none",
   "query": "Zhang-Zagier height",
   "searched_at": "2026-11-20T09:29:10+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

Round-12 read of the #87 discussion on 20 November found a second-party replay of the Grinsztajn packet, with both computed intervals below its stated number. The issue thread and review list gave no maintainer explanation for the order in which candidates were merged. [Replay on #87](https://github.com/teorth/optimizationproblems/pull/87#issuecomment-7020721846).

The precise #280 v6 data import was from the pinned optimization-records tree e3bae2ea40c8b1f764a1ba08bcd21fe513b2c45d. The hash fragment 56f41fc in the pre-launch notes refers to the #280 branch. [Pinned data](https://github.com/vidigoat/optimization-records/tree/e3bae2ea40c8b1f764a1ba08bcd21fe513b2c45d/tao/certificates/c82/v6).
