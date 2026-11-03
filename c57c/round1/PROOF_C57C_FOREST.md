# Composite finite certificate and exhaustive part verification

Candidate, unrefereed; no novelty judgment. A full 0.61230 statement requires
complete global coverage AND every arithmetic leaf of every immutable part.
This supplements PROOF_C57C_PARABOLIC.md, PROOF_C57C_SCALED_BLOCH.md and
PROOF_C57C_MOVING_PHASE.md. It changes only the finite artifact packaging.

The artifact is a manifest and a finite list of gzip JSONL part files.
Every part has the same exact radius, transform parameter, center, bump,
mu and coefficient caps. Supported format tags distinguish optional witness
evaluations but do not change those mathematical parameters. Each part has
its own ordered witness-definition list. A leaf consists of its GLOBAL
binary-bisection path and an index into that part's definition list.
Unused definitions may be removed and referenced indices renumbered before
verification; a separately checked compact artifact is then immutable.
Diagnostic search points are not mathematical inputs.

For a path, start from [0,1]^4. Digit 2j replaces coordinate j's interval
by its closed lower half; digit 2j+1 uses its closed upper half. If that
coordinate is [n/2^d,(n+1)/2^d], the children have pairs (2n,d+1) and
(2n+1,d+1). Thus every endpoint is an exact dyadic rational, independent
of floating arithmetic. Overlapping boundary faces belong to both boxes.

To check global coverage, collect every path from every manifest part,
sort them, and recursively consume the complete list. At prefix p, either
the next path equals p (one leaf), or its next digit must be an even digit
2j. Recursively consume p+(2j), then p+(2j+1). A wrong prefix, odd first
child, missing record or leftover record is rejection. Induction on this
recursion shows that every accepted internal node has both complete
children for the SAME axis. Their boxes cover their parent. The root is
the whole unit cube, so successful consumption proves coverage. Duplicate
leaves, ancestor/descendant overlaps and gaps cannot pass this recursion.
No search stack or approximate volume statistic is trusted.

The separate arithmetic checker reconstructs each leaf box from its global
path and checks precisely the necessary inequality specified by that
part's referenced witness. Every definition is validated, including all
positive weights, vector dimensions, transform modes, coefficient caps,
scaled-radius descriptors and permitted phase rule. The analytic proofs
above apply to that exact box and witness, whether another part supplies
its neighboring boxes or a different Grunsky vector.

The part-only mode makes NO global-coverage claim. A range mode additionally
checks only an exact interval [lo,hi) in the part's leaf order and states
that limited scope. Its record includes the part byte SHA256, every local
checker-source hash, exact mathematical parameters, precision, total leaf
count and number of leaves actually checked. The checker requires the
artifact and its own sources to remain unchanged throughout the pass.
Every internally subdivided leaf requires both closed children.

For a complete verification, arithmetic ranges for each frozen part must
cover [0,N_part) exactly, without gaps or overlaps, and must have identical
part bytes, checker sources, parameters and precision. Their verified-leaf
counts must equal the interval lengths. Every manifest part must appear;
no receipt for an extra part is allowed. Independently recheck the global
coverage recursion described above. It then follows by finite union that
every actual parameter tuple and direction has an accepted inequality.
The omitted-value contradiction and simply connected winding-number
argument of the analytic proof yield U>=R.

verify_c57c_forest.py supplies both a complete fresh verification command
and bounded range commands. Its receipt-assembly mode is bookkeeping of
ACTUAL exhaustive arithmetic runs, not a way to trust arbitrary supplied
receipts as mathematical certificate inputs. A fresh reviewer must rerun
all ranges or use the complete fresh command. Structure-only, selected
leaf checks and unfinished queues never establish a constant bound.

The fast checker changes no mathematical criterion. Its four-component
chain rule omits derivative operations only for exactly zero derivatives;
active derivatives use the same product, inverse and trigonometric chain
rules. Its fixed exact congruence may be multiplied with Arb matrices
instead of Python scalar loops; both evaluate the same R^T(-G)R with
rigorous ball enclosures. Strict positive diagonal/Gershgorin or interval
Cholesky tests are still required. Its phase factor is evaluated directly
as cos(k*theta)+i*sin(k*theta), the identical exponential in the moving-
phase proof. No floating Cholesky proposal itself is acceptance evidence.
The separately written formal-series, Gram and chain-rule implementations
remain distinct from the discovery recurrences and numerical SDP search.
