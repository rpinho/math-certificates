# Credits

Erdős and Ulam posed the original problem. Deep Bhattacharjee, Priyabrata Mandal and Ushashi Bhattacharya supplied the published lower bound, finite constructions and membership-closure SAT method. The omega institute supplied the chain-bound refutation note and explicit open finite cases. ipezygj's SAT + DRAT treatment of #609 motivated this certificate workflow. CaDiCaL and kissat are by A. Biere et al.; drat-trim is by M. Heule et al.

The producer AI agents supplied the four rank colourings, encoders, proofs and separately written producer checkers. Those producer checkers are not independent referees. The clean-room referee AI agents supplied independently written encoders, checked independent proofs, and exact weighted-poset arguments, returning HOLDS for each finite equality. Their reports and scripts are archived without rewriting. Packaging assembled these materials and reran the stated checks; it did not originate a result or commission a new review.

Models, from the launcher records: producer GPT-6.1 Sol via Codex; n=11 referee GPT-6 Astra via Codex (a different model from the same provider); n=12 and n=13/n=14 referees Claude Opus 5.5 via Claude Code (a different model family). No human review is claimed. Third-party solver/checker sources are obtained separately from pinned upstream commits; no third-party research code or #609 data is bundled.

Crawford, Ginsberg, Luks and Roy supplied the lex-leader symmetry-breaking method (KR 1996). Birkhoff’s representation theorem for finite distributive lattices underlies the exact weighted-poset search. The new referee’s code, balanced-word output and report for the two round-3 results are preserved byte-for-byte in referee/n13n14.
