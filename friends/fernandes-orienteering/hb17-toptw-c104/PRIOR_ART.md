# Independent referee prior-art record — 2026-11-03

Scope: authenticate HB17, not establish novelty. This file precedes all referee code.

Starting evidence (claimant's statements, not yet independently confirmed):
- Official benchmark: https://www.mech.kuleuven.be/en/mim/op ; format /instances/TOPTWformat ; archive /instances/righiniTOPTW2.
- Jan Ševeček, 2026 thesis https://is.muni.cz/th/uuuxx/thesis.pdf Table C.6 reports c104, four vehicles, 1260. Public SISRs branch https://github.com/hankarudova/open-source-sisr-routing/tree/toptw is the claimed executable baseline.
- Peng et al. 2025 accepted paper https://lirias.kuleuven.be/retrieve/ec847f07-8b23-4cf1-9c91-b459df258a7a reportedly lists 1260 without an optimality proof (Table 6).
- Amarouche 2020 supplement https://ars.els-cdn.com/content/image/1-s2.0-S0305054820301568-mmc1.pdf reportedly has the same value.

Best known score supplied: 1260, equal to HB17. The proposed contribution is a proof of optimality, not a better heuristic score. Independent primary-source and bounded public-code/paper/community checks follow below. I will reconstruct the primal and upper-bound logic independently; I will not import the worker's search/verifier implementation. No held-out statistical experiment is claimed.

Independent checks completed 2026-11-03 (~16:00–16:15 UTC):
- Official library and format read live; official short archive downloaded on mscr. c104 is byte-identical to the claim. Fresh Peng PDF confirms1260 is nonbold/unproved at7200s; convention is §5.5 printed27 (claim's §5.4 reference is wrong). Retained Ševeček PDF confirms TableC.6 c104m4=1260; public university and theses.cz records authenticate author/title/2026. Fresh thesis binary URL is challenged; retained PDF is not labelled a fresh fetch.
- Current best score authenticated in these sources:1260, held jointly by several heuristics, including Ševeček's +F2. The referee reconstructs that score from the raw instance and witness, rather than rerunning the stochastic public implementation; there is no heuristic speed or score-improvement claim to validate. The new evidence relative to Peng's table is exact closure of this one upper bound.
- Public GitHub repository search sorted by updated,30 hits, inspected. Most recent examples include AndresCatalanPhD/mbh-toptw (a different heterogeneous model), tripagent (application), and various heuristic homework/solver repositories. No authenticated replacement classical c104m4 proof was identified. Public SISRs branch is available and identifies Pajerský/Sobotka/Rudová as the original implementation authors; this does not contradict Ševeček's thesis attribution. Its branch page shows0issues/0pulls. API branch/issues/pulls calls were rate-limited; HTML was also checked. Awesome-orienteering repository found and inspected. Code-search coverage is not exhaustive.
- AI results: BakeLab/Epi-results README/index, google-deepmind/alphaevolve_results README, openai/math CONTENTS, kisonecat/openai-math README, plasma-ai/erdos README and EinsteinArena front page inspected. No classical c104m4 proof appeared in those bounded reads. Epi's vehicle-routing entry is distinct from this TOPTW certificate. Guessed google-deepmind/repository_of_problems URL unavailable; recursive API requests rate-limited. These are explicit coverage limits.
- Last12months arXiv API query for TOPTW yielded0entries. A broader team-orienteering query and web-index results show stochastic/dynamic/quantum variants, not authenticated replacement classical c104m4 evidence. Fresh2026 INFORMSJoC/2025.1516 concerns bivariate time-varying profits; MBH-TOPTW is also a different model.
- Public X/Reddit web-index queries for exact TOPTW/c104 found no relevant result. No accounts, contact, submissions or posting. This absence is not a priority finding.
- Prior results actually encountered: the same1260 score in Ševeček2026, Peng2025, and the older Amarouche2020 supplement. Standard ng-path and Lagrangian bounds already appear in Peng's method. Gedik2017 per-instance status remains unauthenticated; no claim of first proof is made.

Raw retrieval receipts and the final refresh are retained under evidence/. The first-source checks, original-source reconstruction and present certificate are sufficient for this mechanical verdict; universal priority/novelty and taste remain outside its scope.
