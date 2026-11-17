# Aggregate original referee records

The original clean-room reports conclude HOLDS for four supplied candidate finite equalities: f(11)=7, f(12)=7, f(13)=8 and f(14)=8. These are separate historical reviews. The packaging session has read producer code and is not a new clean-room referee.

REPLAY.json preserves the original per-result records and hashes. Its top-level input map is the union of data and proof inputs named by the packet, not a claim that a single historical session read every listed file. The new referee read only its producer’s report/prior-art and the two new colourings, and wrote its own code. The old records retain their own original report/checker identities. The top-level exact checker is the new generic weighted-poset search; it accepts arbitrary dimension, rank word and threshold. The original old-dimensions checks remain described in REPLAY_NOTES.md.

The new referee proves upper bound eight for each new word by exhausting threshold nine, and checks all 3,432 balanced words at threshold eight for the n=13 lower bound. The n=14 lower bound is the fifteen-set chain. Its byte-preserved report is referee/n13n14/REFEREE.md and ends VERDICT: HOLDS. The original standalone ledger verdict is absent from the supplied directory.

The n=13/n=14 referee ran on Claude Opus 5.5, a different model family from the producer (GPT-6.1 Sol), per the launcher records. Candidate, no human review; the chain-exchange and representation arguments are not kernel formalizations.

Round 5 adds the original clean-room n=21..24 report and own code at referee/n21n24/, recorded in REPLAY.json. Its verdict is HOLDS WITH CAVEATS: n=22 equality requires BMB window20, n=24 uses flower without window20, and n=23 remains open between 13 and 14. No human review.
