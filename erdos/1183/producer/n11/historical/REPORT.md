Shipped: candidate exact value f(11)=7 for Erdős #1183, with retained CNFs, DRAT proofs and checker outputs; unrefereed.

Problems tried: **2** (one open-case target, #1183; mandatory baseline reproduction, #609). Certificates produced: **6 verified UNSAT DRAT proofs and 1 newly generated SAT colouring**; the published #609 SAT witness was also rechecked. New finite values settled: **1 candidate**, f(11)=7. Did we find something new? **Yes, candidate:** an upper bound matching the previously known lower bound for an explicitly stated open finite question. This uses an existing SAT method; no new general method or asymptotic result is claimed. See [PRIOR_ART.md](PRIOR_ART.md).

## Exact result for #1183

For a two-colouring χ of all subsets of [n], let M(χ) be the largest cardinality of a nonempty monochromatic family closed under binary union and intersection. The original Erdős–Ulam function is

    f(n) = min over all such χ of M(χ).

**Candidate theorem: f(11)=7.** The result concerns all colourings of all 2048 subsets, with no restriction in the definition.

The upper-bound construction assigns colour 1 to ranks **0,4,7,8,9,11**, and colour 0 to ranks **1,2,3,5,6,10**. Its word, from rank 0 through rank 11, is `100010011101`. All 2048 colours are recorded in [certificates/1183_n11_coloring.json](certificates/1183_n11_coloring.json). A seven-member lattice in colour 0 has bit masks `1,3,5,7,31,63,1023`; its closure and colour are checked directly. The two UNSAT certificates below prove that neither colour contains a lattice with at least eight members.

The lower bound f(11)≥7 is already public: the omega institute's October 9 source explicitly asks whether equality holds, and Bhattacharjee–Mandal–Bhattacharya's current paper proves the bound. This job reproduces that lower bound with explicit lattice data, a short argument and a checked finite certificate, so the exact-value conclusion does not require trusting an unexamined citation.

### Direct upper-bound encoding and its exact meaning

[encode_family.py](encode_family.py) writes one variable y_S for each set S of the chosen colour. For every incomparable pair S,T, it includes

    ¬y_S ∨ ¬y_T ∨ y_(S∪T)
    ¬y_S ∨ ¬y_T ∨ y_(S∩T).

If the result has the other colour, its y literal is absent, giving a binary exclusion. For comparable pairs both implications are tautologies and are omitted. No symmetry breaking is used in either upper-bound CNF.

A backwards sequential counter imposes at least eight selected sets. For the i-th member variable x_i, auxiliary A(i,j) means that at least j of the first i members are selected. Its clauses encode

    A(i,j) → A(i−1,j) ∨ (x_i ∧ A(i−1,j−1)),

with A(i,0)=true, impossible indices false, and A(N,8) a unit. Induction proves that a true A(i,j) requires j selected members; conversely setting A to the actual prefix counts extends every selection of at least eight members. Thus each CNF is satisfiable **if and only if** the fixed colouring has a monochromatic union-and-intersection-closed family of at least eight sets in that colour. There is no approximation, size-eight-only assumption, or requirement that the family contain ∅ or [11].

[check_family.py](check_family.py) was written separately by this same agent. It reconstructs subsets as frozensets, checks every closure clause and counter clause against the CNF, and checks the counter's local Boolean identity. It imports no encoder. [check_coloring_certificate.py](check_coloring_certificate.py) checks the full colouring against both CNF memberships and the explicit seven-member witness. These are separately written checks, **not independent verification**.

| Query | Variables | Clauses | CaDiCaL result | Solve wall s | DRAT bytes | Backward drat-trim wall s |
|---|---:|---:|---|---:|---:|---:|
| Colour 0, at least 8 | 10,466 | 1,293,083 | UNSAT | 84.346 | 603,094,524 | 88.132 |
| Colour 1, at least 8 | 7,910 | 719,045 | UNSAT | 33.577 | 198,649,885 | 26.066 |

Both checker logs contain exactly the required verdict **`s VERIFIED`**. They use drat-trim's default backward mode, without `-f`. Files:

- [data/1183_n11_c0.cnf](data/1183_n11_c0.cnf), [proof](certificates/1183_n11_c0.drat), [solver output](logs/1183_n11_c0.solve), [checker output](logs/1183_n11_c0.check), [encoding check](logs/1183_n11_c0.encoding_check).
- [data/1183_n11_c1.cnf](data/1183_n11_c1.cnf), [proof](certificates/1183_n11_c1.drat), [solver output](logs/1183_n11_c1.solve), [checker output](logs/1183_n11_c1.check), [encoding check](logs/1183_n11_c1.encoding_check).

### Reproduced lower bound and the finite reduction

Suppose an arbitrary colouring of 2^[11] had no monochromatic lattice of seven or more members. Every maximal chain has 12 members. Each colour's members in a chain are themselves a lattice, so every maximal chain has exactly six sets of each colour.

For two r-element sets S,T differing by one element, choose a chain below S∩T and a chain above S∪T. Inserting S or T makes two maximal chains differing in just that slot. Their equal colour counts force χ(S)=χ(T). Single-element exchanges connect every pair of r-element sets. Hence χ must be constant on every rank. This is the earlier rank-rigidity argument, credited to the omega institute and also present in the current Bhattacharjee–Mandal–Bhattacharya paper.

It therefore suffices to cover the 4096 binary colourings of the 12 ranks. [certificates/1183_lower7_families.json](certificates/1183_lower7_families.json) lists **1254 actual lattices**, each with at least seven distinct sets. Every rank word makes at least one listed lattice monochromatic. The list includes 792 seven-member chains and witnesses for the 462 balanced words with colour(∅)=1. Colour exchange handles the other balanced words.

The rank CNF has 12 variables, the unit colour(∅)=1, and two clauses per listed family excluding its being monochromatic. Its **2509 clauses** are UNSAT with a **17,388-byte DRAT proof** and `s VERIFIED`. This CNF is the exact finite assertion that a rank word avoids the listed lattices; the written chain argument reduces the unrestricted lower-bound claim to that assertion. We do not mislabel this short rank CNF as a direct encoding of all 2^2048 arbitrary colourings.

[lower_1183.py](lower_1183.py) constructs the list by normalising, reflecting and translating the published `certs_11.txt` lattice data, then adjoining exterior chains. No third-party script is imported or run. [check_lower_1183.py](check_lower_1183.py), separately written by the same agent, checks every listed family by set operations, exhausts all 4096 rank words, checks the CNF against the list, and checks connectivity in every Johnson graph used in the argument. Its output is `VALID LOWER BOUND 7`. The final explicit list can be checked without the upstream data or construction script.

Files: [rank CNF](data/1183_lower7_rank.cnf), [DRAT](certificates/1183_lower7_rank.drat), [direct check](logs/1183_lower7.direct_check), [drat-trim output](logs/1183_lower7.check). The logical argument is short and unformalised; the C checker is not a formally verified LRAT checker.

### Baseline, attempted region and rejection controls

Before the new-case search, the published n=10 rank word `10011001011` was reproduced. Its two no-seven-member queries have 4475/3675 variables and 292667/193705 clauses; both are UNSAT with retained DRAT proofs and `s VERIFIED`. The chain bound gives f(10)≥6, so this reproduces the already known f(10)=6. Logs and proofs use the prefix `1183_n10_c0` / `1183_n10_c1`.

Both naive extensions of that word to n=11 failed: the solver returned monochromatic lattices of at least eight sets, checked against the original set operations. They are recorded in `logs/1183_n11_try*.family_check`. The published counterexample-guided method then found the successful word after 139 rejected proposals, in about 318 seconds. Search constraints were drawn only from directly checked closed families. Searching among rank constructions limits how constructions are found; a successful full-colouring certificate gives the unrestricted upper bound. No negative conclusion about arbitrary colourings is inferred from this search restriction.

The final-instance deletion control removes **exactly the last at-least-eight unit clause** from the colour-0 CNF. CaDiCaL returns SAT; [check_deleted_control.py](check_deleted_control.py) checks that exactly that clause was removed and its model satisfies every remaining clause. Output: `VALID DELETION CONTROL` in [the log](logs/1183_control_deleted.direct_check).

The corruption control truncates the proof to its terminal empty clause, omitting every justification. drat-trim rejects it with exit code 1 and **`s NOT VERIFIED`** against the final colour-0 CNF. Files: [corrupt proof](certificates/control_corrupt.drat), [rejection output](logs/1183_control_corrupt.check). The expected rejection is not a solver/encoder failure. These controls were also exercised on the n=10 baseline.

## Required reproduction of #609

Definition: f(k) is the least m such that every k-edge-colouring of K_(2^k+1) has a monochromatic odd cycle of length at most m. ipezygj's repository claims f(4)=7, candidate and unrefereed. It does not settle the asymptotic problem. The lower bound is Day–Johnson's construction (2017, arXiv:1602.07607); ipezygj's contribution is the computed upper bound.

The README, RESULT and PLAN describe one-hot edge colours, implied walk-layer variables forbidding short odd closed walks, independence number ≤8, walk-layer cardinality ≤8, and a low-degree lemma. Symmetry breaking chooses the vertex/colour with maximum monochromatic degree, sorts the remaining colour degrees, the root star and vertex 1's edges within root blocks. The 33 profiles are exhausted by cube-and-conquer, with profile (4,4,4,4) closed by hand. Reported tools: CaDiCaL rel-3.0.1 c6073042 and drat-trim 2e3b2dc0. Reported work: 372.6 solving CPU-hours, 118.1 checking CPU-hours; 5908 VERIFIED events, of which 5896 leaves are needed.

The main published proof **could not be replayed**. Its public GitHub tree has no CNF or DRAT files. The repository says 5338 original proofs were not retained and about 17 GB for 570 later nodes remain in S3, without a public allowlisted download URL. The log's individual verified-node proof lengths sum to 500,744,741,741 bytes, with largest 2,638,125,574 bytes; this includes redundant nodes and is not a retained archive size. Regenerating the missing part is estimated upstream at about 360 CPU-hours, outside this job. Hashes and verdict records do not substitute for proof files.

[encode_609.py](encode_609.py) is our own encoder from the statement. It uses edge colours, one-way walk implications and exclusions of an edge within each walk layer. If χ has no forbidden odd cycle, setting each walk variable to actual walk existence satisfies the formula. Conversely a forbidden shortest odd cycle gives, from a root on that cycle, two vertices in the same d-walk layer joined by a colour edge, contradicting an exclusion clause. An odd closed walk always contains an odd cycle of no greater length. The optional root-star symmetry is sound: choose any edge, rename its colour 0 and an endpoint 0, then sort the other vertices by their root-edge colour. No other normal form is imposed.

Our rebuilt K17/4-colour/no-odd-cycle≤7 CNF has 4012 variables and 66867 clauses. A byte-for-byte comparison with the original is impossible: the original CNF is absent, and the prose does not fix auxiliary numbering or sequential-counter serialisation. Our formula intentionally follows the same graph statement without the original redundant lemmas/profile machinery; we do not claim its hash matches the original.

Reproduction checks actually completed:

- Published K17 witness: `VALID`, edge counts 32,32,35,37 and all four odd girths 7, checked by [check_coloring.py](check_coloring.py), written separately here using BFS on the bipartite double cover. [Output](logs/609_published_witness_check.txt).
- Own K9/3-colour/no-odd-cycle≤5: 594 variables, 4270 clauses, UNSAT and **`s VERIFIED`**, retained [CNF](data/609_n3_L5.cnf), [proof](certificates/609_n3_L5.drat), [checker output](logs/609_n3_L5.check).
- Own K17/4-colour/no-odd-cycle≤5: 2856 variables, 39123 clauses, SAT; original-statement BFS check `VALID`, edge counts 38,27,34,37 and all odd girths 7. [Colouring](certificates/609_own_witness.json), [output](logs/609_n4_L5.witness_check).

These checks are reproductions. They do not re-establish the complete f(4)≤7 computation. No ipezygj scripts were downloaded, imported, copied or executed; the archived inputs read here are prose, data and the event log. Repository commit: `58472a0a0b0cb45a7804b4668011359ccf732689`.

## Sources, novelty and limits

The exact finite question f(11)=7 is explicitly open in the [omega source note](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md). The [v1.0.0 paper](https://github.com/creelie/Erdos-1183/blob/59e72f9511286e9e981b86eb3f7f9bc15e8d59ef/paper/Erdos.tex) lists exact values only through n=10; the current paper improves the lower bounds without giving an upper 7 at n=11. The November 14 source re-check found no matching earlier upper bound. This supports the candidate novelty statement; it is not an exhaustive proof of priority.

[PRIOR_ART.md](PRIOR_ART.md) gives the survey and dates for #112, #531, #555/#558, #1182 and #1183, including 2026 forum/GitHub/arXiv claims, CNF estimates and reasons not to pick settled cases. The broad source scan includes Tao's raw data and open PRs, BakeLab/Epi, AlphaEvolve, OpenAI/math, plasma-ai/erdos and kisonecat. Named endpoints returning 404 and sources outside the network allowlist are recorded as coverage limits.

Credit Erdős and Ulam for #1183 (Erdős, 1978, *Problems and results in combinatorial analysis and combinatorial number theory*, pp.29–40, p.39); Bhattacharjee, Mandal and Bhattacharya for the closure-SAT method, n≤10 baseline and lattice data; the omega institute for the earlier rank-rigidity/lower-7 argument; ipezygj for the #609 proof-certificate workflow, and Erdős–Graham / Day–Johnson for that original problem and lower construction. This is a candidate finite extension using existing methods. All code and checking here were produced by the same agent. Human mathematical review has not occurred.

## Tools, resources and exact replay

Pinned source builds inside `tools/`:

| Tool | Release / commit |
|---|---|
| CaDiCaL | rel-3.0.1, `c60730422e758ef1cebe7aeddf2dda31c996bf04` |
| kissat | rel-4.0.4, `8af8e56f174b778aef3aa45af9f739b2a5f492c2` |
| drat-trim | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` |

Build commands used `./configure` and `make` (CaDiCaL -j4, kissat -j2, drat-trim -j1). Those overlapping build launches allowed **seven compiler jobs briefly**, exceeding the requested six-core limit; actual instantaneous overlap was not measured. This was a scheduling mistake. Later scientific work used at most two heavy processes concurrently. Build logs are retained. Exact source-build commands are in `BUILD_COMMANDS.txt`. All scientific commands used `nice -n 10`. The launcher already had niceness 15, so macOS capped the resulting workers at 20; lowering absolute niceness was denied. This scheduling limitation is recorded, and no privilege escalation was attempted.

`run_limited.py` records process PIDs, time-limits process groups, and checks memory/proof/disk limits. Its final version counts the whole Codex job's descendants, stops its newest launched group near 7.8 GB, caps a proof near 19.5 GB, and the directory near 58 GB. The largest recorded aggregate sample was about **1.565 GB**; individual `/usr/bin/time -l` measurements are in the logs. The retained directory is about **1 GB**, with no compressed/deleted proof needed. No predictive model or score was used, so the predictive trivial/simple/SBS rule is inapplicable.

To replay the shipped theorem and controls, from this directory, use Python 3.10+ (the shared research venv was used here):

```sh
sh replay.sh
```

To regenerate either exact upper CNF and obtain a new proof without overwriting the retained certificate:

```sh
mkdir -p reproduce
PYTHON="$HOME/dev/open-science/.venv/bin/python"
for c in 0 1; do
  nice -n 10 "$PYTHON" encode_family.py 100010011101 "$c" 8 "reproduce/c$c.cnf"
  nice -n 10 "$PYTHON" check_family.py "reproduce/c$c.cnf"
  nice -n 10 tools/cadical/build/cadical "reproduce/c$c.cnf" "reproduce/c$c.drat"
  # CaDiCaL exits 20 for UNSAT; continue to the checker.
  nice -n 10 tools/drat-trim/drat-trim "reproduce/c$c.cnf" "reproduce/c$c.drat"
done
```

Regenerate the lower certificate with `nice -n 10 "$PYTHON" lower_1183.py`, check it with `check_lower_1183.py`, then solve/check `data/1183_lower7_rank.cnf` with the same solver/checker command pattern. Reproduce #609 with `encode_609.py 9 3 5 data/609_n3_L5.cnf --star` and `encode_609.py 17 4 5 data/609_n4_L5.cnf --star`; check SAT output with `check_coloring.py --n 17 --colors 4 --avoid 5 --model logs/609_n4_L5.solve`.

SHA-256 hashes are in `SHA256SUMS`. No submission, commit, push, PR, post or message was made. The run stops after completing one requested open finite case, with no need to exhaust the nine-hour ceiling. The next useful work is mathematical review of this exact statement and the two encoding arguments, then a separate job for f(12) or k(6,3); those cases are not claimed here.
