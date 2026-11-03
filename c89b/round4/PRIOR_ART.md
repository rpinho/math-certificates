# Prior art for the round-4 K5 upper package

Candidate and unrefereed. This package releases only the exact K5 upper
certificate. It builds on the folded-Hamming ideas of Thomason, the
Cayley constructions of Parczyk–Pokutta–Spiegel–Szabó
([PPSS](https://arxiv.org/abs/2206.04036)), Jeetu SK's
[#277](https://github.com/teorth/optimizationproblems/pull/277), and the
preceding symmetry-breaking and round-3 candidates in
[#307](https://github.com/teorth/optimizationproblems/pull/307).
Kiem–Pokutta–Spiegel ([KPS](https://arxiv.org/abs/2312.08049), section 7)
provide relevant flag-algebra methodology and an uncertified numerical
lower estimate; that estimate is not a competing upper bound. Razborov
is credited for flag algebras. No lower certificate is included here.

Noam Feinstein announced c5 < 0.001652 at the [Technion seminar on
21 January 2026](https://math.technion.ac.il/events/noam-feinstein/).
The [RSA 2025 abstract](https://dmg.tuwien.ac.at/rsa2025/) describes this
as joint work with Chaim Even-Zohar. This is an announcement with no
public certificate we could check. The displayed threshold is stronger
than our round-3 0.001653032 and weaker than this round's 0.001648970526.
The RSA abstract announces improvements without giving this numerical value;
the numerical threshold comes from the Technion abstract.

Fresh release audit on 3 November 2026: the main 89b source/rendered page
returns 404, so the proposed page at PR #307 head
468daa26b0977ea6da605b0b72ec5b584650357a was read. All 47 open PR file
inventories were screened, including C89 #270, #276, #277, #279, #307, #308.
Public repository searches sorted by update time, nine AI/agent/certificate
repository root comparisons against the frozen audit, recent arXiv and
public community searches located no further public K5 upper value stronger
than this candidate. The release REPORT.md records scope and limitations;
this is a bounded audit, not an exhaustive priority claim.

Both selected exact counting paths and the literal/rejection controls are
rerun for this package. No new numerical search is involved. The two exact
counters are separately written (same agent); no human referee has checked
the result. No optimality or exhaustive novelty claim is made.
