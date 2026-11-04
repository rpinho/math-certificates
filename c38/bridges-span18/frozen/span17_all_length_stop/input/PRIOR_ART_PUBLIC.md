# C38 lower prior-art audit — math_c38_1104

Started 2026-11-04 01:25 UTC. Candidate research only, unrefereed; no novelty judgment.
This audit precedes implementation and mathematical search. Entries explicitly marked pending
will be completed before the bar is frozen and either method starts.

## Inputs read
- `workspace/_codex/RULES.md` (first).
- `target_sweep_1103/astra/SWEEP.md`, C38 section and common inputs/scope notes,
  and the corresponding `sweep.json` section.
- Linked local SURVEY.md, newtargets2_1103/ATTEMPTS.md and REPORT.md,
  and math-certificates/README.md are being read in full; no earlier C38
  enumeration is identified by the sweep. No baseline of ours is claimed.

## Primary sources reopened live
- https://teorth.github.io/optimizationproblems/constants/38a.html
- https://numaro.tech/research/self-avoiding-walk-connective-constant-2026/
  Numaro's span-17, length-260 coefficient certificate claims
  mu >= 2^128 / 129513673858566230428673965530967449326 = 2.627385640… .
  Its checker verifies coefficient hashes and renewal arithmetic, not the original enumeration.
- https://doi.org/10.5281/zenodo.21546041 : web tool retrieval failed;
  direct archival retrieval remains a mandatory pilot task.
- https://arxiv.org/html/cond-mat/0409381v2 : Iwan Jensen (2004), Kesten
  irreducible-bridge method, finite-span/length polynomials, 2.625622.
- https://arxiv.org/html/2211.16146 : Olivier Couronné, upper 2.662342426;
  opposite side.
- https://www.mefyi.com/papers/connective-constant-bound/ and linked PDF:
  Tejasvi Singh Tomar (October 2026), upper 2.6586513, opposite side,
  source labels preprint, not peer reviewed.
- PR 223 reopened with `gh (read-only CLI) pr view`: now CLOSED,
  updated 2026-11-03T14:24:27Z, unlike the sweep's open snapshot.
  Its C38 change concerns Couronné's upper side.

## Required remaining source checks before freeze
Live raw table/main, all current open PR/issue inventories, public code
(recently updated searches), named lab repositories, recent arXiv and
public community sources. Exact source receipts will be retained locally.

## Baseline and credit
The strongest applicable lower claim presently located is Numaro's exact
fraction above. Credit Harry Kesten, Iwan Jensen, Numaro, and the bridge
counting contributions of Hammersley–Morton, Guttmann, Alm–Parviainen
when used. Replaying a coefficient polynomial cannot certify its enumeration.
Any new checker will be described as separately written (same agent).

## Authorized acceptance target
Exact nonnegative counts of a justified, disjoint family of irreducible
bridges, satisfying sum a_n (400/1051)^n >= 1, with written proof,
frozen artifact, separately written verifier, and exact rejection controls.
Do not start search until BAR.json records the refreshed source state.

## Completed live inventory, 2026-11-04 01:28 UTC

The raw main constant page, raw README and live table were retrieved into sources/.
Main HEAD is stored in sources/main_HEAD.txt. All 57 currently open PRs were
retrieved with gh (read-only CLI) and every file list screened; two include
constants/38a.md: #313 (Couronné upper bound) and stacked #317 (inherited
#313 change; its substantive claim is C30 lower). Both full descriptions
and file lists were reopened in sources/pr313.json and pr317.json. All six actual open issues were screened; none concerns C38.
The former open #223 is closed; merged #135, its description and both (empty)
comment lists were reopened. No generator is attached to #135 or its fork tree.

Recently updated GitHub repository searches for self-avoiding walk, connective
constant, and self-avoiding 2026 are retained in sources/code_search*.json.
The code search for check_saw38a_L17.py located only table mirrors.
The mandatory lab inventories and READMEs were reopened live. Exact HEADs,
paths and truncation flags are in sources/audit/summary.json and sibling files:
BakeLab/Epi-results, google-deepmind/alphaevolve_results,
google-deepmind/alphaevolve_repository_of_problems, openai/math,
plasma-ai/erdos, kisonecat/openai-math, quasar17/Alpha_Omega_Agents,
JamesWeatherhead/CodexProLong. OpenAI's recursive tree is truncated; its
preprints listing supplements the check. Honeycomb bridge papers and older
SAW library entries are not applicable square-lattice lower improvements.
This is a bounded inventory/topic screen, not proof of absence.

Recent arXiv/topic searches and public Reddit/X/EinsteinArena searches were
performed through web search. No stronger applicable claim than the one
below was located. A public X mirror repeats Numaro; X was not exhaustively
accessible, private Discord/Telegram were not inspected, no accounts created.
The current primary papers above were reopened in full text/PDF where available.

### Additional public lower claim found BEFORE search

Vít Plánočka, *Two rigorous lower bounds for the connective constant of the
square lattice: an exact-integer transfer matrix, two pumping lemmas, and a
formal proof* (August 2026), public repository:
https://github.com/vitplanocka/saw-connective-constant

Pinned tree/commit 0ea6932a15924be370f253c32d204ac79521414a.
Its strongest reported bound is 2^27/51082227 = 2.627483880058713963…,
strictly stronger than Numaro and strictly below 1051/400. The source labels
its own results proved, but this job treats them as public unrefereed claims
until the relevant checks complete. The repository contains point-evaluation
transfer generators, exact dyadic directed-rounding sweeps, terminal-layer
pumping/subset branching, and a crossing-capped terminal-five supplement.
The code README, paper, literature audit, verification report, supplement
verification report, and open-problems report were freshly downloaded/read.
We do not adopt its novelty claims or literature errata as our findings.

This materially changes the best public method located. Numaro remains the
requested coefficient baseline, but comparison must additionally use
Plánočka's stronger fraction. His point-evaluation implementation provides
an available generator route where Numaro's archive does not. All use of it
must credit Vít Plánočka, plus Harry Kesten, Iwan Jensen, and Enting's
finite-lattice transfer framework. Pumping discussions also credit Madras
and Slade's bridge joining antecedent, with the source's incomplete book-access
caveat retained rather than inventing a fresh check of unavailable pages.

### Numaro archival access resolved

Direct https://zenodo.org/api/records/21546041 succeeds. Seven archived files
were downloaded and every file's published MD5 matched. SHA256 pins will be
in BAR.json. The archive contains the full b_(n,l) table through L=17,N=260,
two checkers, README and run log, but NO transfer generator. Its exact
arithmetic replay is feasible; that is not a replay or certification of the
large enumeration. Full enumeration provenance remains unresolved unless
another justified generator reproduces the necessary coefficients.

## Supplemental refresh, 2026-11-04 02:24 UTC

sources/refresh_0225/ reopens the live/raw table, Numaro page and Zenodo
record, every current open PR file list, relevant lab/public repository
HEADs/READMEs, and recently updated public code searches. It reports 57
open PRs, #313/#317 as the C38-touching branches, and no retrieval errors.
Relevant repository heads and comparison values are unchanged. This is
source monitoring; the acceptance bar remains the pre-search BAR.json.
Explicit supplemental awesome-list repository queries for self-avoiding
and connective-constant topics returned zero repositories; receipts are
sources/awesome_saw_search.json and awesome_connective_search.json. Those
supplementary queries were made after the initial freeze, not claimed as
part of the original pre-search snapshot. No novelty assessment follows.
