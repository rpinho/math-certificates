HOLDS
Referee: gpt-6.1-sol

The official short Solomon c104 TOPTW has optimum 1260 with at most four vehicles.
I independently reconstructed the official model and verified both bounds; no claimant search or verifier code was imported or read.
The freshly downloaded official raw file matches the claim's SHA256 exactly.
Travel truncation, service-start windows, depot return and disjoint customers match the official definitions.

Published comparison: Ševeček 2026 Table C.6 (printed 68/PDF 76) reports 1260 for c104 with four vehicles.
The university thesis record and PDF title page authenticate Jan Ševeček as its author.
Fresh thesis downloads were challenged; I inspected the retained actual PDF, not the challenge HTML.
Fresh Peng 2025 Table 6 reports 1260 in regular font at 7200 seconds, hence unproved by that run.
The convention is §5.5, printed 27; CLAIM.md's §5.4 citation is a harmless typo.

What I ran on mscr: new Fraction route replay, new C++ integer closure checker, simple greedy control, and exhaustive small-instance adversarial checks.
The witness has 47 distinct customers on four feasible routes, scoring 330+310+300+320=1260.
All 44,166 states and 3,130,101 transitions close, with zero unresolved cases.
Nonnegative penalties sum to 542092 and weighted route upper bound 181976 gives 1000*score<=1269996.
All prizes are multiples of 10, so score<=1260. No floating solver status enters the proof.
Greedy insertion scores 1180; 216 exhaustive-fixture checks pass and four corrupted real certificates reject.
There is no statistical hold-out: c104 was selected from a public c103/c104 panel. Selection does not weaken this per-instance exact certificate.

Relative to the cited papers, the added result is the upper-bound certificate, not a higher score.
The same 1260 already appears in Ševeček 2026, Peng 2025 and Amarouche 2020; universal priority was not established.
Strongest objection: sparse closure needs a sound induction connecting forgotten ng memories to distinct elementary suffixes; tests alone cannot supply it.
I checked that induction and implemented a separately derived exact suffix bound; REPORT.md explains both.
Evidence, independent code and reproduction instructions are saved here; no referee workers remain and the pod folder is under 1 GB.
NEXT BAR: Mechanize the elementary-suffix induction for this certificate format in a proof assistant.
