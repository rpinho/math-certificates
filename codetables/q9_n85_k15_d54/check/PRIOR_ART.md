> Packaged copy, lightly edited: four wordings say "clean-room" or "written from scratch" where the referee's original said "independent", because the referee is part of our own pipeline. No factual claim was changed. The raw fetch logs and response bodies it cites (`live_85_15.html`, `sources/`) are not packaged.

# Prior-art record (started before checker code)

Search started 2026-11-08 00:50 UTC. This is a clean-room verification, not a new construction search.

## Live scoreboard

Fetched https://www.codetables.de/BKLC/BKLC.php?q=9&n=85&k=15 with curl at approximately 00:50–00:53 UTC; raw HTML is live_85_15.html. Lower bound 53, upper bound 63. The published construction is a subcode of a [85,16,53] Construction XX code using BCH [80,15,51], [80,13,52], [80,16,50], plus auxiliary [4,3,2] and [1,1,1]. Construction last modified 2001-12-17. Table maintained by Markus Grassl; the entry does not name the original discoverer. The public baseline is therefore 53, not a statistical predictor. Reconstructing the unrelated full Construction XX generator is outside this single-matrix referee job; its component BCH bounds will inform the clean-room algebraic check. No predictive performance claim is made; SBS is inapplicable.

The web open tool returned HTTP 429 for the exact entry; direct curl retrieved it successfully. https://codetables.de/updates.html was accessible. Its GF(9) updates include 2026-09-29 codes [31,6,22] and [41,9,26] and 2024 skew-cyclic codes of length 48, not the target. No public issue/PR interface is linked from the table.

## Initial searches

Web searches: `"85,15,54" code`, `"85, 15, 54" code`, `"85" "15" "54" "GF(9)" code`, `"85,15" "code" "9"`, `GF(9) codes improvements Chen quasi twisted MinT 85 15`, `site:github.com "codetables" "2026"`, `site:github.com "codetables.de" code improvement`, `site:arxiv.org "GF(9)" "2026"`, `site:arxiv.org "linear codes" "2026" "9"`, `"codetables" "BakeLab" OR "alphaevolve" OR "EinsteinArena"`, and `"codetables" "reddit" OR "x.com" OR "Epi-results" OR "openai/math"`.

No target report found. Search exposed a different [85,14,54] table entry (dimension 14 is insufficient), older GF(9) quasi-cyclic papers, and arXiv:2603.06309 on quasi-twisted/additive constacyclic structure. GitHub results included m-webster/CSSLO (a table parser, not target prior art) and tretoef-estrella (other claimed coding improvements; to inspect). GitHub's repository search sorted by recently updated was attempted at https://github.com/search?q=codetables&type=repositories&s=updated&o=desc; web tool restricted it. Initial MinT https://mint.sbg.ac.at timed out. Chen https://databases.cs.hkr.se/qtcodes/ was inaccessible via web tool. Follow-up direct fetches and focused searches are pending.

## Limitations

No earlier target report has yet been found. A search that finds nothing is not proof of absence. This record will be extended with focused database, repository, paper and community checks and a final recheck.

## Completed database checks

All times below are UTC on 2026-11-08. Exact requests and HTTP outcomes are in `sources/fetches*.json`; the corresponding response bodies are retained in `sources/`.

- **codetables.de:** the exact target fetched at 00:56:22 and re-fetched at **01:00:38.935** still has **53–63**, with construction date 2001-12-17. The GF(9) section of [the update history](https://www.codetables.de/updates.html) has no target report. Its recent 2026 entries concern [31,6,22] and [41,9,26]. The [full rectangular table](https://www.codetables.de/BKLC/Tables.php?q=9&n0=1&n1=85&k0=1&k1=15), fetched at 00:56:22.398755, supplies all neighbouring comparisons in `bound_comparison.json`. Only the original target improves.
- **MinT:** HTTPS failed, but the ordinary HTTP interface worked. [Exact query](http://mint.sbg.ac.at/query.php?i=c&de=1&b=9&s=85&n=15&d=&t=), fetched at **00:56:59.884541**, gives **53–63**. Its lower-bound derivation shortens a Construction X [86,16,53] code. The homepage and [history](http://mint.sbg.ac.at/history.php) identify the database update as 2024-09-05. The initial accessibility limitation is resolved.
- **Chen:** HTTPS timed out, but HTTP worked. [Exact query](http://databases.cs.hkr.se/qtcodes/searchqc2.php?n=85&k=15&q=9&m=&p=&author=), fetched at **00:57:34.880160**, says no such codes were found. [All dimension results for length 85 over GF(9)](http://databases.cs.hkr.se/qtcodes/searchqc2.php?n=85&k=&q=9&m=&p=&author=) returns one code, **[85,10,59]**, citing Daskalov, Metodieva and Hristov (2004). This page reports 5,057 stored codes and last modification 2026-10-26. Dimension 10 does not imply the target. The initial accessibility limitation is resolved.

## Public repository checks

The public GitHub API succeeded where the browser search failed. [Repository search for `codetables`, sorted by updated descending](https://api.github.com/search/repositories?q=codetables&sort=updated&order=desc&per_page=30) returned 18 repositories, including these relevant records:

| Repository / text read | Finding |
|---|---|
| [IgnacioBolivarCenteno/linear-code-records](https://github.com/IgnacioBolivarCenteno/linear-code-records), README | Thirteen GF(4) codes reported 2026-11-05, including records not yet in the official table. No GF(9) target. |
| [Foundation-0/gfq-codes](https://github.com/Foundation-0/gfq-codes), README and [open issues/PR descriptions](https://github.com/Foundation-0/gfq-codes/issues) | GF(7) upper-bound certificates and planned nonbinary construction/checker work. No [85,15,≥54] GF(9) claim in the inspected text. |
| [Leo-Strijbos/codetables](https://github.com/Leo-Strijbos/codetables), README | [74,13,47] over GF(8), not this target. |
| [MarinAndreGirard/qubit-stabilizer-codes-2026](https://github.com/MarinAndreGirard/qubit-stabilizer-codes-2026), search metadata | Binary quantum stabilizer codes, outside the target alphabet and code class. |
| [tretoef-estrella](https://github.com/tretoef-estrella), public profile | Its coding discussion concerns the unresolved [22,6,13] GF(4) problem, not a GF(9) report. |

The GitHub repository search for the exact string `"85,15,54"` returned zero repositories. This is repository metadata search, **not** a comprehensive search of all GitHub file contents. Additional indexed web searches used `site:github.com "85,15,54"`, `site:github.com "codetables.de" code improvement`, and `"codetables" "2026" "improvements" github`; no target report was found. No repository code was downloaded or executed.

Required AI-lab/agent record checks:

- [BakeLab/Epi-results](https://github.com/BakeLab/Epi-results): README result catalogue; no target or GF(9) record.
- [google-deepmind/alphaevolve_results](https://github.com/google-deepmind/alphaevolve_results): README; no target report.
- The initially guessed `google-deepmind/repository_of_problems` address returns 404. The actual [alphaevolve_repository_of_problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems) README was found through a scoped API query and read. It describes 67 problems; no target report in this text. The new [alphaevolve](https://github.com/google-deepmind/alphaevolve) README was also inspected; the listed mathematical results do not include this code.
- [openai/math](https://github.com/openai/math): README and the complete `CONTENTS.md` catalogue; no `codetables`, `GF(9)`, or `85,15` target match. [kisonecat/openai-math](https://github.com/kisonecat/openai-math) is a searchable index of that collection; its README was inspected.
- [plasma-ai/erdos](https://github.com/plasma-ai/erdos) / [erdosproblems.ai](https://erdosproblems.ai): public repository overview describes the Erdős-problem record; no target claim in the inspected overview.
- [EinsteinArena result catalogue](https://github.com/togethercomputer/EinsteinArena-new-SOTA): README read; records in geometry, inequalities and related extremal problems, no target linear code. Public API repository search for EinsteinArena also inspected; coding-related hit concerns binary deletion codes, not the target.

These are scoped catalogue/README checks, not assertions that every historical file or discussion in these repositories was searched.

## Papers and community

The arXiv API query `(all:"GF(9)" OR all:"quasi-twisted") AND submittedDate:[202511080000 TO 202611082359]`, sorted by submission date, returned three items:

1. [Abdukhalikov and Verma, arXiv:2603.06309v2](https://arxiv.org/abs/2603.06309): quasi-twisted/additive constacyclic duality; abstract and HTML text inspected, no target parameter claim.
2. [Generalized ovals, 2.5-dimensional additive codes, and multispreads, arXiv:2511.15843v2](https://arxiv.org/abs/2511.15843): abstract concerns small-dimensional additive codes, including dimension 2.5 over GF(9), not dimension-15 GF(9)-linear codes. The local HTML snapshot hit an 8 MB retrieval cap; it is not represented as a complete full-text review.
3. [Generalized Spectral Bound for Quasi-Twisted Codes, arXiv:2511.10066v1](https://arxiv.org/abs/2511.10066): abstract and HTML text inspected; no target parameter claim.

Also inspected [Yu et al., arXiv:2608.18664](https://arxiv.org/abs/2608.18664), including its HTML parameter tables (no target), and the abstract of [Evolving Towards Better Codes, arXiv:2609.37056](https://arxiv.org/abs/2609.37056), which reports binary linear-code improvements. The API query searches indexed metadata/abstract fields, not every paper's full text; notation such as F_9 can escape an exact GF(9) query. Indexed web searches additionally used GF(9), linear codes, 2025, 2026, and the exact parameter strings with and without spaces.

The older GF(9) paper identified by Chen was traced to its primary [Math-Net record](https://www.mathnet.ru/eng/ppi120) and [publisher record](https://doi.org/10.1023/B:PRIT.0000024876.30498.f4): Daskalov, Metodieva and Hristov, *New Minimum Distance Bounds for Linear Codes over GF(9)*, Problems of Information Transmission 40 (2004), 13–24. Its abstract reports 31 constructions; the Chen record identifies its [85,10,59] construction. The full-text link redirected to metadata, so this is not claimed as an exhaustive paper review. The live target entry provides no specific author reference for Construction XX beyond its construction chain.

Community searches included `site:x.com "85" "15" "GF(9)"`, `site:reddit.com "GF(9)" "codetables"`, and `"codetables" "reddit" OR "x.com" OR "Epi-results" OR "openai/math"`. No relevant earlier report or public Discord/Telegram summary surfaced. No account was created and nobody was contacted.

## Method credit and final recheck

The checker is written from scratch, without reading the producer's code. Its methods are the classical BCH/Vandermonde distance bound and Brouwer–Zimmermann information-set enumeration; the latter's standard relative-rank formulation is documented, for example, in [An Extension of the Brouwer–Zimmermann Algorithm for Calculating the Minimum Weight of a Linear Code (2021)](https://www.mdpi.com/2227-7390/9/19/2354). No implementation from this or another source was used.

At **01:00:38–01:00:39 UTC**, re-fetched the exact live table, update history, GitHub repository search sorted by updated date, and the Épi, AlphaEvolve, OpenAI catalogue, and Foundation-0 texts. The table remains **53–63**. The six re-fetched document bodies compared with their initial snapshots are unchanged; no new relevant repository appeared. `sources/fetches_final.json` records the requests.

**Earlier [85,15,≥54] GF(9) report found: no.** This is a finite public-record search, not proof of absence. The supplied code beats the printed bound under the same n, k, q and distance definition. This job verified the supplied construction in a clean room; it did not invent that matrix or prove historical priority.
