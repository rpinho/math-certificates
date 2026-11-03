# Prior art: math_gap1_1101

First file written, before code or mathematical computation. Initial reading
2026-11-01 21:00--21:07 UTC. Machine RULES.md and the user's limits apply.
All mathematical computation will run under /root/os/math_gap1_1101 on
math-cpu-8, nice 10, one BLAS thread, <=10 workers and <=40 GB. Job deadline
03:00 UTC Nov 2 (six hours), earlier than the pod margin 05:35 UTC.

## Live sources and starting point

The raw official table was fetched live:
https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md
It defines C44=sup_d R_d/2^d and lists lower 3/2 (CHS/Shinkar--Tal), published
upper 4.394 (Wellens), unrefereed table upper 4.3576549226 (Pinho).
https://github.com/teorth/optimizationproblems/pulls was read live; relevant
visible entries include #294 (Pinho upper 4.1225323803), #285 (citation),
#283 (Koshta quartic sensitivity), and #284 (26a family). A full diff audit
and repository-head receipts will follow before search.

PR284 was fetched using its public API. It is a ternary, not Boolean,
degree-d polynomial on 3d variables, with support 1-2^-d. It does not
immediately give a Boolean C44 witness. Repository:
https://github.com/DennisKoshta/c26a-bohnenblust-hille-cube-family
pinned in the PR at 2557cdb23d08cd45414e4dc312b5a81d629e0b20.

Read the current public Towell repository:
https://github.com/queelius/boolean-degree-sensitivity . It explicitly leaves
the full degree-five sensitivity-fourteen problem open. Conditional
exclusions are not universal variable caps.

The CHS primary paper https://par.nsf.gov/servlets/purl/10201042 and
https://arxiv.org/abs/1801.08564 gives the lower construction
L_d=2L_(d-1)+2=3*2^(d-1)-2 and corrected final weighted extremal identity.
The corrected simultaneous-duplication proof also appears at pp.116--117 in
https://sites.math.rutgers.edu/~zeilberg/Theses/JohnChiarelli.pdf .
R3=10 is credited to Tarannikov--Kirienko 2000 and discussed in
https://arxiv.org/abs/2311.05566 (Krotov--Valyuzhenich 2024).

Read local c44r4/PROOF.md and c44r5/PROOF.md. The latter, completed around
21:00 UTC today, already proves candidate R4<=24 via the binary Reed--Muller
second-weight gap and candidate C44<3.1674542553. This is inherited work,
not a result of this job. It uses Kasami--Tokura's second-weight theorem,
https://arxiv.org/pdf/0902.0058 and
https://backoffice.biblio.ugent.be/download/2140143/2939938 , and the complete
minimum-support classification https://arxiv.org/html/2303.10995 .
The public baseline to reproduce is CHS counts 22,46,94; the stronger local
baseline to replay is the frozen c44r5 packet. The search target is now
R4<=23 or R4<=22, or a Boolean witness with >=23 variables.

## Coverage and limitations

Initial web searches covered degree-four relevant variables, Boolean degree
2026, the primary CHS references and ternary low-support polynomials. A
Peking University workshop abstract by Tarannikov discusses the best known
construction and resilient-function equivalence. This is a lead, not an
additional theorem. The broader recent-repository, rival, recent-arXiv and
indexed community audit is pending and will be appended here before search.
No account creation or private-community access. No priority claim.

Every prospective result is candidate and unrefereed pending independent
verification of frozen artifacts and the written proof. No commits, pushes,
PRs, posts, uploads or messages are authorized or planned.

## Initial gate completed

Pod audit receipt: sources/public_initial_summary.json, UTC
2026-11-01T21:02:37.286540+00:00. All 43 visible open PR diffs, the raw table,
issues, eleven rival repository HEADs and README/index files, and recent
repository metadata searches were fetched with zero errors. Main HEAD is
87b4ebbd426ff8db597a2004cc45da17903bdcf2; applicable C44 diffs are #285 and
#294. No stronger public lower or upper result was found in this coverage.
The audit includes the specified BakeLab, DeepMind, OpenAI, EinsteinArena,
plasma-ai, kisonecat repositories and an awesome-AI-for-math list.

Recent primary-paper searches located Valyuzhenich arXiv:2609.12540 (q>=3
Hamming graphs), Potapov arXiv:2410.21937 / Cryptography and Communications
2025 (discrete functions), and Krotov--Valyuzhenich's cubic classification.
Searches of indexed X/Reddit and degree-four Boolean relevant variables
yielded no stronger applicable bound. Private communities and authenticated
global GitHub code search were not available. This is bounded coverage.
Valyuzhenich 2303.10995 and CHS 1801.08564v3 HTML were opened directly.

## Cubic classification added before the cap argument

Rasoolzadeh, *Classification of All t-Resilient Boolean Functions with t+4
Variables*, ToSC 2023(3), DOI 10.46586/tosc.v2023.i3.213-226, supplies the
complete 761-class catalogue on ten inputs. Public source:
https://gitlab.science.ru.nl/shahramr/ResilientFunctions , HEAD
eace0ce0edcb664cd5e4f84d7f5cb56dc7400925. Direct raw URLs tried initially
failed because the data lives in `t = n -4/`; a read-only clone succeeded.
The copied F10T6.txt hash is
d0ca4026c3bfa61f7c40945e4627feecd9264d7854114806c533d64e06836ba0.
The primary paper was downloaded from https://d-nb.info/1307299091/34 .
The parity correspondence from resilient functions to real cubic functions
is explained in Krotov--Valyuzhenich 2311.05566v2, Lemma 1 and Remark 1.
The primary paper says 761; one secondary passage says 961. This job relies
on the primary 761-class statement and its actual supplied list.

The resulting finite cubic energy envelope and quartic proof build directly
on this published classification, in addition to the r5 Reed--Muller gap and
Valyuzhenich minimum-support theorem. No claim that the classification or
its computation is new. A fresh final audit remains required.

## Final source recheck

The final audit repeated all 43 visible open-PR diffs, table source, issues,
eleven rival HEADs and indexes, and recently updated repository searches.
Receipts: sources/public_final.json.gz and public_final_summary.json. No
fetch errors; main and the applicable C44 PRs are unchanged. Targeted web
searches for quartic relevant-variable counts 22/23 also found no stronger
applicable public statement in the indexed coverage. This is not a proof of
priority, and no novelty or record claim is made.

The PR284 repository was cloned read-only and its HEAD matches the PR's
2557cdb23d08cd45414e4dc312b5a81d629e0b20. Its proof and format were read;
the committed degree-2/3/4 ternary examples were checked with separately
written exact transforms, as were their elementary Boolean completions.
They supply no improved C44 lower witness by that completion route.
