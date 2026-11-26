# Prior Art Snapshot — Erdős #1182 Upper Bound via Kempe-Swap Dichotomy

Initial search on **2026-11-25 UTC**. Repair recheck on **2026-11-26 UTC**.

## Problem Statement
[Erdős Problem #1182](https://www.erdosproblems.com/1182) (Burr, Erdős, Faudree, Rousseau, Schelp 1980):
- $F(n)$ is the largest integer $q$ such that every connected graph $G$ on $n$ vertices with at most $q$ edges is $K_3$-good, i.e., $R(K_3, G) = 2n - 1$.
- Equivalently, if there exists a connected simple graph $G$ on $n$ vertices with $e(G)$ edges and a triangle-free graph $H$ on $2n - 1$ vertices such that $G \not\subseteq \overline{H}$, then $R(K_3, G) > 2n - 1$ and hence $F(n) \le e(G) - 1$.

## Published Literature
1. **Burr, Erdős, Faudree, Rousseau, Schelp (1980)** (`[BEFRS80]`): proved $\frac{17n+1}{15} \le F(n) \le \left(\frac{27}{4} + o(1)\right) n (\log n)^2$ for $n \ge 4$.
2. **Stephan Brandt (1996)** (`[Br96]`, *Expanding graphs and Ramsey numbers*, FU Berlin preprint `pr-a-96-24`): proved $F(n) \le 84n$ for sufficiently large $n$ (settling $F(n)/n \not\to \infty$), remarked without proof that a refined analysis gives $11.75n$ (cited as $12n$ in Brandt–Brinkmann–Harmuth 1998), and conjectured $2n < F(n) < 6n$ for all large $n$.
3. **Brandt, Brinkmann, Harmuth (1998)** (*Electron. J. Combin.* 5 #R7) and **Brinkmann, Goedgebeur, Schlage-Puchta (2012)** (`arXiv:1208.0501`): exact values of $F(n)$ for $n \le 12$ ($1, 2, 5, 7, 8, 11, 11, 16, 18, 23, 23$ for $n = 2,\dots,12$).

## Unrefereed Community Claims (checked 2026-11-25 UTC)
1. **Pravar Kataria with Claude Fable 5.1** ([`Sovi11/erdos-1182@6d4f78c`](https://github.com/Sovi11/erdos-1182/tree/6d4f78cfb15296297450618dde6fea8b15478ccc), forum claim 377, Sep–Nov 2026; independently replayed by us in `rpinho/math-certificates/replays/erdos1182`):
   - Proves (unrefereed) $F(n) \le 11n/2$ (11-regular random graph against balanced $C_5$ blow-up, explicit $n_0 = 10^6$ in our replay) and $F(n) \le 5.03n$ (10-regular random graph plus $0.03n$ extra random edges, explicit $n_0 = 10^9$ in our replay; `BOUNDS.md` also notes a `5.025n` check).
   - Also proves $F(n) \ge n + \lfloor(n-1)/6\rfloor$ using Sidorenko's theorem.
   - Explicitly notes that bare $d = 10$ ($5n$ edges) FAILS under the unrestricted (naive) first moment over $C_5$ part assignments (exponent $\approx +0.0033635$ at cap $0.4$, $+0.0040314$ at cap $0.4001$), concluding *"about 5.02n is the limit of the method."*
2. **Qiyuan Gu** (forum claim, Sep 2026): addresses $f(n) = \Theta(n^{3/2}\sqrt{\log n})$ via Sudakov's conjecture, not the linear constant of $F(n)$.

## Live Searches (2026-11-25 UTC)
- `https://www.erdosproblems.com/1182` and `https://www.erdosproblems.com/forum/thread/1182/proof-claims`: checked 2026-11-25 UTC; only the two claims above.
- `Sovi11/erdos-1182`: latest commit remains `6d4f78cf` (2026-11-13).
- arXiv search (`"triangle-good" OR "1182" Ramsey "2n-1"`): checked 2026-11-25 UTC; no newer upper bound on $F(n)$.
- X search via `grok-x-search` (`("erdos 1182" OR "Erdős 1182" OR "triangle-good" OR "Sovi11/erdos-1182") ("5.03" OR "5n" OR "F(n)" OR "Ramsey" OR "Kataria")`): 0 hits (`20261125T085602.389041Z-b1a8dec819836888.json` in `X_SEARCHES.jsonl`).

## Baseline & Target
- The problem page cites Brandt's $84n$. Brandt announced $11.75n$ without a proof. [Official problem](https://www.erdosproblems.com/1182), [Brandt preprint](https://ftp.math.fu-berlin.de/pub/math/publ/pre/1996/pr-a-96-24.ps)
- The best published upper bound located is $F(n)\le50n-1$ for all sufficiently large $n$. Theorem 5.1 of Nikiforov and Rousseau states that almost all connected 100-regular graphs on $n$ vertices fail 3-goodness for sufficiently large $n$. Their definition in §1 uses $R(K_3,G)=2n-1$. The family is nonempty for $n>100$, since the circulant with differences $\pm1,\ldots,\pm50$ is connected and 100-regular. Each graph in the family has $50n$ edges, so the theorem gives the stated bound. [Theorem 5.1 and §1 in the authors' version](https://arxiv.org/pdf/math/0703653), [journal publication](https://doi.org/10.1007/s00493-009-2409-2)
- Kataria's pinned bounds page reports the unrefereed $F(n) \le 5.025n$ and foregrounds $5.03n$. The unrestricted first moment for bare degree 10 has positive rate. [Kataria's bounds](https://raw.githubusercontent.com/Sovi11/erdos-1182/6d4f78c/BOUNDS.md)
- **Round 1 target:** $F(n)\le 5n-1$ via a Kempe-swap dichotomy for potential-minimal part maps of bare degree 10. Credit Brandt (1996) and Kataria (2026) for the balanced $C_5$ and random-regular framework.

```rh-prior-art
{
 "schema": 1,
 "baseline": "Published: Nikiforov and Rousseau (2009), Theorem 5.1 implies F(n) <= 50n-1 eventually; scoreboard cites Brandt (1996) F(n) <= 84n (11.75n announced without proof). Unrefereed: Kataria (Sovi11/erdos-1182@6d4f78c, 2026), 5.03n highlighted and 5.025n certified in BOUNDS.md. Naive d=10 barrier +0.0033635.",
 "sources": {
  "github": {
   "status": "none",
   "query": "Erdos 1182 triangle-good F(n) upper bound 5.03n Kataria Brandt C5",
   "searched_at": "2026-11-25T12:36:25+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "(\"erdos 1182\" OR \"Erd\u0151s 1182\" OR \"triangle-good\" OR \"Sovi11/erdos-1182\") (\"5.03\" OR \"5n\" OR \"F(n)\" OR \"Ramsey\" OR \"Kataria\") (grok-x-search)",
   "searched_at": "2026-11-25T08:56:02Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-25T08:56:02Z) for key df3f8bf974a74328b4db4febb66e5ba5; 0 posts. Key-level capture; no new X search was performed.",
   "capture_sha256": "dfbe1af46aeaf50c360a6c06d24dd6d64766a955edc000e9de45b7834262f917"
  },
  "papers": {
   "status": "hits",
   "query": "Erdos 1182 triangle-good F(n) upper bound 5.03n Kataria Brandt C5",
   "searched_at": "2026-11-25T12:36:25+00:00",
   "hits": [
    "https://doi.org/10.1016/j.dam.2015.06.031",
    "https://doi.org/10.1051/jp4:1991511",
    "https://doi.org/10.2210/pdb7oan/pdb",
    "https://doi.org/10.2307/2159512",
    "https://doi.org/10.2307/3647855",
    "https://doi.org/10.5194/egusphere-egu2020-8342"
   ],
   "note": "OpenAlex: unavailable: empty response; Semantic Scholar: unavailable: HTTP 429; Europe PMC: unavailable: empty response; arXiv: unavailable: empty response; Crossref: searched: 6 results",
   "source": "Crossref",
   "source_statuses": [
    "OpenAlex: unavailable: empty response",
    "Semantic Scholar: unavailable: HTTP 429",
    "Europe PMC: unavailable: empty response",
    "arXiv: unavailable: empty response",
    "Crossref: searched: 6 results"
   ]
  },
  "leaderboards": {
   "status": "none",
   "query": "Erdos 1182 triangle-good F(n) upper bound 5.03n Kataria Brandt C5",
   "searched_at": "2026-11-25T12:36:25+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## Recheck for this job

On 2026-11-26 UTC, the indexed official problem and discussion still showed Brandt's \(84n\). The live forum claims endpoint was inaccessible during the repair recheck. The public claim index listed Kataria's bound on \(F\) and Gu's separate claim on \(f\). Searches for Ramsey-goodness papers and an Erdős #1182 upper bound of \(5n-1\) located no matching or stronger bound under the same definition. Kataria's public repository had zero open pull requests. Its pinned bounds and Decimal replay code specify the extra-pair correction. [Official problem](https://www.erdosproblems.com/1182), [claim index](https://qed.bot/erdos-since-the-wiki), [open changes](https://github.com/Sovi11/erdos-1182/pulls), [public replay code](https://raw.githubusercontent.com/Sovi11/erdos-1182/6d4f78c/code/certify_exact.py)

The supplied prior replay verified Kataria's \(5.03n\) certificate. For this repair we reran the local row-scaling solve and reproduced the bare degree-10 rates of \(+0.00336352695\) at cap \(0.4\) and \(+0.00403132147\) at cap \(0.4001\). A rational witness at cap \(0.4\) certifies a rate above \(+0.0033635265\). Kataria's \(5.025n\) run is reported in the pinned bounds. [Fixed-point table](reference_table.json), [Arb replay](verify.log), [Kataria's bounds](https://raw.githubusercontent.com/Sovi11/erdos-1182/6d4f78c/BOUNDS.md)
