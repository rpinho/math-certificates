# Verification scope and implementation independence

Candidate and unrefereed. All round-4 code and argument were prepared by the
same AI agent; no separate agent, human referee or external review is claimed.
Round 3's separate review was read and its inherited arithmetic/base machinery
is reused. Its numerical result was independently replayed in this job lane.

The new search generator and the frozen checker share mathematical definitions
but no implementation imports, graph files, state map, optimized eigenvector
computation or partition. The frozen checker requires only its JSON artifact,
its adjacent C++ file, Python-flint and a C++17 compiler. In particular:

| Component | Search | Frozen checker |
|---|---|---|
| Forbidden-word canonical key | Backward scalar cost/gap DP and greedy operation choice | Forward DP of complete (cost,gaps,operation string) keys |
| Matcher | Trie with failure links | Direct suffix membership in forbidden/proper-prefix sets |
| Run and history state | Packed inherited integer run memory, leading-bit history sentinel | Private run encoding and semantic history lengths/bits |
| Competing prefixes | Search triples; minimum mismatch shortcuts across buffered positions | Independently written explicit source/diagonal-position enumeration |
| Unknown gap count | Search gap sentinel 999, five-way cost-stride encoding | Private gap sentinel 1,000,000, eight-way bit encoding and int16 state fields |
| Labeled minimization | Hash refinement, ordered signatures | Sorted signatures, canonical first-appearance renumbering, all-member checks |
| Intersection | Search BFS on packed pair keys | Separately written BFS on semantic component pairs |
| Potential palette | Hash refinement of sorted weighted multisets | Sorted refinement; every complete product row is checked |
| Numerical inequalities | Floating Perron search, optional repair | Strict unsigned integer rows plus independent 256-bit Arb exponent |
| Potential storage | Binary32 bytes, optionally transposed by NumPy | Standard-library byte-plane inversion and integer decoding of IEEE bits |

The checker copies the already reviewed round-3 arbitrary-precision integer
primitives, word/run infrastructure, and rational coefficient machinery. Its
new transition, minimization and product portions were written separately from
the search. This is implementation independence by one author, rather than
independent external authorship or proof formalization.

The new proof maintains a real witness at each frontier entry. Cost remains
exact even if gap-count information is replaced by infinity. Finite gap bounds
carry a conditional order promise; saturating an extra gap saving never invents
an earlier operation. Each rejection is either strictly cheaper, has strictly
fewer gaps at equal cost, or has a proved earlier first operation difference.
The literal-path audit retains full alternative words and checks these claims
against their actual strings and complete keys. It is independent of both
compiled transition engines and derives scores from the literal paths.

Tests include exhaustive canonical input pairs, longer random pairs, direct
feature increments, literal witness checks and malformed/corrupted frozen
artifacts. Controls include integer and exact dyadic potentials, homogeneity
and lossless byte-plane encoding. They supplement the written invariant and
complete exact replay; they do not replace either.

One initial factored-checker adapter assumed 37 literal run-memory states.
The actual rule implementation has 19. That first small replay correctly
rejected. Replacing the hard-coded count by an independent run-graph BFS fixed
the adapter without changing the certificate or competitor update. Both
receipts are retained. No failed receipt is represented as a pass.

Resource restrictions are operational, not proof premises. The original
concurrent search exceeded the requested memory budget once (sampled 50.7 GB);
REPORT.md and STATUS.md disclose it. Subsequent large phases are serialized,
with separate parent/child address-space limits, and ordinary work has two
bounded slots. These limits can cause a replay to fail, but cannot make an
invalid inequality pass.
