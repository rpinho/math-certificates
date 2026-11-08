# C47: centred Hardy–Littlewood maximal constant over squares

C47 is the optimal weak-type (1,1) constant of the centred Hardy–Littlewood maximal operator over axis-parallel squares in dimension d = 2, as defined on [Tao page 47a](https://teorth.github.io/optimizationproblems/constants/47a.html).

This packet gives the candidate lower bound **C47 ≥ 1.7040280575** (rigorous exact arithmetic, finite_instance.py with verify_exact.py; L0 for the bound as a whole). The printed bound improves Doldrums / SCiEL’s cited **1.7032090736** from [PR #341](https://github.com/teorth/optimizationproblems/pull/341) by exactly **0.0008189839**, and our published round-1 **1.70311** from [#321](https://github.com/teorth/optimizationproblems/pull/321) by exactly **0.0009180575** (rigorous decimal subtraction, comparison.py). The asterisk remains appropriate: the commissioned AI referee is not a human review or a second-party confirmation in the Tao PR.

The rational periodic ratio is **q = 1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000** (rigorous, verify_exact.py). Its decimal expansion begins 1.70402805756367672706384135011685550657560332493166213…; it is the periodic limit, obtained by the finite truncation-and-smearing argument in [PROOF.md](PROOF.md), not the finite value.

The directly checkable finite lower value is **81179170702072811560461937774649547472268267876630428381100034109236137/47639573975778160894755636560089704255253920609263650078720000000000000** (rigorous, finite_instance.py and referee/independent_check.py), approximately 1.70402805750000000000102915424912982456718329505136590703… for display. It strictly exceeds the printed bound. This finite construction has h = 2, N = 214084879817 and the positive rational smear radius in [the finite receipt](release_validation/finite.json); all terms are specified by formula, without expanding the block.

The certificate has 98 positive rational atoms and 1500 rectangle witnesses. Certificate SHA-256: `bc342d18f9fe219828856bcaa9531669a1051c2685394e41dfbeb3e794e818eb`.

Unpublished intermediate steps were 1.7032218573, 1.7033053786 (63 atoms), and 1.7033694707 (66 atoms); they are history, not separate public table entries.

The exact verifier was separately written by the same AI agent. A clean-room AI referee on a different model, GPT-6 Astra via Codex, wrote its own exact checker, reached the same fraction and concluded HOLDS, including the finite L1 reduction and the corrected half-open cell. It did not read or run producer code. This is an AI referee, not human review; see [its report](referee/REFEREE.md) and [scope](referee/README.md). The programs check finite rational inequalities; the written proof supplies the passage to the planar L1 constant. No optimality or exhaustive priority claim is made.

Credit: **Doldrums / SCiEL** for the public bar and moves/insertions/removals idea; our **#321**, by rpinho, as the start; **T. S. Tomar (Tejasvi Singh Tomar)** for the 50-atom measure and Lemma 6.2, following **Yongxi Lin**, for the periodic construction. No Tomar or Doldrums code was used for this construction, its verification or this release. The published round-1 work did use Tomar’s unchanged checker, as its historical record says. See [CREDITS.md](CREDITS.md) and [PRIOR_ART.md](PRIOR_ART.md).

Use [REPRODUCE.md](REPRODUCE.md) for replay commands and [release_validation/summary.json](release_validation/summary.json) for this release’s results. [MANIFEST.json](MANIFEST.json) and [SHA256SUMS](SHA256SUMS) inventory the package; publication manifests preserve claims, credits and referee input hashes.
