# Implementation independence

The independent checker is a separately written C++/Python implementation by
the same AI agent, not an independent human or external referee. It was written
before freezing the main candidate. It imports no search or inherited code and
reads no search-built graph, quotient map, or optimizer file.

The search uses backwards scalar canonical tests, Aho–Corasick matching,
hash-based partition refinement, packed histories, and frontier recurrences.
The checker uses forward whole canonical keys, direct suffix membership,
sorted state signatures, semantic history lengths/bits, and explicit source-
position enumeration for short competing edit paths. Every full reachable row
is checked in exact integer arithmetic, even though its potential is compressed
by independently reconstructed colors. Arb checks the asymptotic exponent.

A third Python audit retains literal full replacement paths and recomputes
strings, cost, gaps and operation words. All its observed rejections have a
direct better witness. This does not replace the mathematical induction or
the frozen full-row replay.

The review_c91r2 PASS is an external-to-this-job check of the inherited round-2
candidate only. It does not referee this round's new method. All new results
remain candidate and unrefereed.
