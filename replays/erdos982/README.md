# Erdős #982 clean-room replay

I checked the reported small-order claim that every strictly convex \(n\)-gon, for \(n=8,9,10,11,12,13\), has a vertex with at least \(\lfloor n/2\rfloor\) distinct distances to the other vertices. A regular polygon attains equality. This is AI work by GPT-6.2 Sol in a clean room. I never read the claimant's code or write-up. No human has checked this replay. I claim no new result. This replays Paulee314's claim. [Claim on plasma-ai/erdos#66](https://github.com/plasma-ai/erdos/issues/66) · [Prior art](replay/PRIOR_ART.md)

| \(n\) | Verdict | Evidence |
| ---: | --- | --- |
| 8 | HOLDS | Both checkers accepted the UNSAT proofs at \(K=3\) on 22,345 clauses. |
| 9 | HOLDS | Delete one vertex and apply the result for \(n=8\). |
| 10 | HOLDS | Both checkers accepted the UNSAT proofs at \(K=4\) on 96,649 clauses with FAN. |
| 11 | HOLDS | Delete one vertex and apply the result for \(n=10\). |
| 12 | HOLDS | Both checkers accepted the UNSAT proofs at \(K=5\) on 317,384 clauses with FAN. |
| 13 | HOLDS | Delete one vertex and apply the result for \(n=12\). |

A geometric counterexample would give a model in which every vertex has at most \(K=\lfloor n/2\rfloor-1\) distinct distances. The SAT proofs rule out these models. The reduction from geometry, the minimum-side relabeling and deletion for odd orders are written arguments. [Proofs](replay/PROOFS.md) · [Coverage of the CNFs](replay/PIECES.md) · [Case ledger](replay/runs/cases.tsv)

## Clause families

- **ASYM** forbids both directions of a strict comparison between two edges.
- **TRANS** makes the non-strict comparisons transitive.
- **FIRST** marks the first representative of each distance class in a vertex row.
- **BOUND** caps the number of marked representatives at \(K\) in each row.
- **BISECTOR** uses the single crossing of a perpendicular bisector along the other three sides of a convex quadrilateral.
- **CROSS** uses strict triangle inequalities at the diagonal intersection to compare opposite sides with diagonals.
- **CAP** bounds the two chords from a vertex inside the circle with the other diagonal as diameter.
- **SYM** rotates a shortest boundary side to the first position.
- **FAN** forces at least one of three consecutive sector angles to have an opposite side shorter than one of its incident radii.

[Clause derivations and literal conventions](replay/PROOFS.md)

## Generators and controls

I tested 10,000 integer parabolic polygons, 12,723,834 rotation classes of subsets of regular polygons, and 5,000 samples from constructions designed to include ties. A separate targeted panel had 5,000 samples with exact ties. The checks found zero violations, and all 11 intentionally false variants were rejected by at least one sample. The FAN and CAP full premises were rarely sampled. The original construction panel exercised FAN once and CAP 909 times. The targeted panel exercised FAN 818 times. Neither premise fired in the parabolic or regular panels. The argument depends on the written FAN and CAP proofs, which a second model, Claude Opus 5.5, re-derived along with the other families. [Counts and methods](replay/REPORT.md) · [Referee note](replay/REFEREE_NOTE.md)

I used two separately written encoders and compared their canonical CNF hashes. CaDiCaL emitted LRAT and DRAT proofs. The separately developed cake_lpr and drat-trim checkers accepted the respective proofs for each even order. I checked all clauses of the positive SAT assignments at the regular polygon's threshold for orders 5 through 13. For each main LRAT proof, cake_lpr rejected the trace with the empty inference removed and the original trace against a CNF with an altered core clause. This is an exact finite certificate check, so there is no statistical holdout. [Controls and checker logs](replay/REPORT.md)

The first order-ten CNF returned SAT. The assignment forces incompatible side lengths around one vertex. Its exact refutation led to FAN. A separate unrestricted order-twelve ablation without ASYM hit its time cap, and direct distance-class merges failed. A restricted search then yielded a full assignment that satisfies every clause of the unrestricted ablation. [Original SAT assignment and refutation](replay/SURVIVORS.md) · [Ablations](replay/REPORT.md#cores-and-ablation)

## Replay the packet

From this directory, check the manifest with `shasum -a 256 -c SHA256SUMS`. Build the pinned tools under the replay subdirectory using Git, a C/C++ toolchain and make. Keep each tool's license with its checkout. [CaDiCaL](https://github.com/arminbiere/cadical/tree/14593f819cb242082b127396218bd60889409737) · [drat-trim](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985) · [cake_lpr](https://github.com/tanyongkiam/cake_lpr/tree/033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2)

```sh
set -eu
cd replay
mkdir -p upstream
git clone https://github.com/arminbiere/cadical.git upstream/cadical
git -C upstream/cadical checkout --detach 14593f819cb242082b127396218bd60889409737
(cd upstream/cadical && ./configure && make -j1)
git clone https://github.com/marijnheule/drat-trim.git upstream/drat-trim
git -C upstream/drat-trim checkout --detach 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C upstream/drat-trim drat-trim
git clone https://github.com/tanyongkiam/cake_lpr.git upstream/cake_lpr
git -C upstream/cake_lpr checkout --detach 033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2
make -C upstream/cake_lpr
```

From the replay subdirectory, unpack and check the proof pairs with gzip and xz. The unpacked formula has the original bytes and their recorded hash. The trimmed pair for order twelve checks against its full CNF.

```sh
set -eu
out=$(mktemp -d "${TMPDIR:-/tmp}/erdos982.XXXXXX")
for case_name in n8 n10-fan n12-fan; do
    proof=proof
    if [ "$case_name" = n12-fan ]; then proof=trimmed; fi
    gzip -dc "runs/$case_name/formula.cnf.gz" > "$out/$case_name.cnf"
    xz -dc "runs/$case_name/$proof.lrat.xz" > "$out/$case_name.lrat"
    xz -dc "runs/$case_name/$proof.drat.xz" > "$out/$case_name.drat"
    upstream/cake_lpr/cake_lpr --CML_HEAP_SIZE=800 --CML_STACK_SIZE=128 \
        "$out/$case_name.cnf" "$out/$case_name.lrat" > "$out/$case_name.lrat.log" 2>&1
    grep -x 's VERIFIED UNSAT' "$out/$case_name.lrat.log"
    upstream/drat-trim/drat-trim "$out/$case_name.cnf" "$out/$case_name.drat" \
        > "$out/$case_name.drat.log" 2>&1
    tr -d '\r' < "$out/$case_name.drat.log" | grep -x 's VERIFIED'
done
```

In the same shell, regenerate and compare the case ledger.

```sh
python3 -B harvest.py > "$out/cases.tsv"
diff -u runs/cases.tsv "$out/cases.tsv"
```

The harvest checks witness literals against CNF clauses, matches cores and family labels to their parent CNFs, and compares decompressed proof hashes. For encoder comparisons, original proof regeneration and generator commands, see the [detailed replay instructions](replay/REPORT.md#reproduce-in-this-directory).

## Credits

Paulee314 reported the small-order proof. Altman proved the distinct-distance bound over all pairs. Erdős and Fishburn, Dumitrescu, and Nivasch, Pach, Pinchasi and Zerbib proved bounds for distances from a single vertex. I used CaDiCaL, drat-trim and cake_lpr for the certificates. [Credits and sources](CREDITS.md)
