Shipped: candidate exact value f(12)=7 for Erdős #1183, with the full colouring, two retained CNFs/DRAT proofs and backward drat-trim VERIFIED outputs; unrefereed.

Problems tried: **2** (#1183 at n=12; #112 at 30 vertices). Certificates produced: **5** (two theorem DRAT proofs, one full colouring, two checked SAT control assignments); one public #112 witness was also reproduced. Values settled: **1 candidate**, f(12)=7. Did we find something new? **Yes, candidate:** an exact even-dimensional value left open in a public source. This extends an existing method; no new general SAT method or asymptotic result is claimed. [PRIOR_ART.md](PRIOR_ART.md) records the bounded source search and final re-check.

**Exact statement and construction.** For a two-colouring χ of all subsets of [n], let M(χ) be the largest cardinality of a nonempty monochromatic family closed under binary union and intersection. The original Erdős–Ulam function is

    f(n) = min over all two-colourings χ of M(χ).

The candidate result is **f(12)=7**, for this unrestricted function. Colour each set by its cardinality using the rank word, from rank 0 through 12,

    1100101100011.

Colour 1 has ranks **{0,1,4,6,7,11,12}**; colour 0 has ranks **{2,3,5,8,9,10}**. [The complete colouring](certificates/n12_coloring.json) lists all 4096 subsets as bit masks; bit i represents element i+1 of [12]. Python set-list outputs use labels 0 through 11. Its colour-1 seven-member chain has masks `0,1,15,63,127,2047,4095`.

Every colouring of 2^[12] restricts to a colouring of a maximal chain with 13 members. One colour occurs at least seven times on that chain. A subfamily of a chain is closed under union and intersection, so **f(12)≥7**. This elementary lower bound applies to every colouring, with no rank assumption. [check_n12.py](check_n12.py) checks the complete construction, its agreement with both base queries, the explicit seven-member chain, and the majority argument on all 8192 chain colourings. [Output](logs/n12.coloring_check).

The two UNSAT certificates below show that this particular complete colouring contains no monochromatic closed family with **at least eight** members. Thus f(12)≤7. Searching for a rank construction restricts discovery; the resulting complete-colouring certificate proves the unrestricted upper bound.

**Base encoding and its exact meaning.** [encode_family.py](encode_family.py), reused from our round-one job, assigns a member variable y_S to each set S of the chosen colour. For each incomparable pair S,T it writes

    ¬y_S ∨ ¬y_T ∨ y_(S∪T)
    ¬y_S ∨ ¬y_T ∨ y_(S∩T).

If the result has the other colour, the third literal is omitted. Comparable pairs give tautologies and need no clause. These implications impose precisely closure of the selected family; they do not require its endpoints to be ∅ or [12]. Duplicate clauses are retained.

A backwards sequential counter imposes at least eight selected members. A(i,j) means at least j of the first i members are selected. Its clauses encode

    A(i,j) → A(i−1,j) ∨ (y_i ∧ A(i−1,j−1)),

with A(i,0)=true and impossible indices false, plus the unit A(N,8). Induction forces at least eight selected members. Conversely every selection of at least eight extends by setting the auxiliaries to the actual prefix counts. The query covers families larger than eight as well as those of size eight.

[check_family.py](check_family.py) was written separately by the same agent in round one and reused here. It reconstructs subsets as frozensets, reconstructs every closure/counter clause, compares the complete clause multiset, and checks the local Boolean counter identity. Both base CNFs pass: [colour 0](logs/n12_1100101100011_c0.encoding_check), [colour 1](logs/n12_1100101100011_c1.encoding_check). These are separately written checks, **not independent verification**.

**Standard symmetry breaking for colour 0.** The direct colour-0 run was stopped unresolved after 686 seconds. Its base CNF and unfinished proof are retained, and the unfinished proof is not a certificate. [STATUS.md](STATUS.md) records the change before the next solver run. Adding ordinary lex-leaders reduced this query to about one second.

[add_lex.py](add_lex.py) appends comparisons of the member-bit vector with its image under each of the 66 transpositions of ground coordinates. Member variables are ordered by increasing set mask, with false before true. For one transposition, fixed positions are omitted, and each exchanged pair appears once, at its lower-index endpoint. This has the same lexicographic comparison as the full vectors: the first differing position must be the first endpoint of a pair whose two bits differ.

For those ordered pairs (a_i,b_i), a prefix variable p_i can record equality through pair i. With p_0=true, the three clauses per pair are

    ¬p_(i−1) ∨ ¬a_i ∨ b_i
    ¬p_(i−1) ∨ ¬a_i ∨ ¬b_i ∨ p_i
    ¬p_(i−1) ∨  a_i ∨  b_i ∨ p_i.

Equal bits force the next prefix true until the first difference. At that first difference, 1>0 is forbidden; 0<1 allows the remaining prefixes to be false. Hence a comparison is extendible exactly when the left vector is lexicographically no larger.

Soundness is an orbit argument. Ground-coordinate permutations preserve the rank colouring, family size, union and intersection. If an eight-or-more-member monochromatic lattice existed, take a globally lexicographically least member vector in its finite S12 orbit. It satisfies all 66 comparisons and extends to the base counter by its actual prefix counts. Therefore the symmetry clauses lose no possible counterexample. The counter auxiliary order itself need not be preserved by the permutation. Colour 1 uses no symmetry breaking.

[check_lex.py](check_lex.py), written separately by the same agent without encoder imports, checks that the entire base CNF is preserved and reconstructs every added comparison using actual set permutations. It also exhausts the comparator recurrence on lengths one through four; the induction and orbit argument above give the arbitrary-length justification. [Output](logs/n12_1100101100011_c0_lex.encoding_check). This argument is unformalised, and drat-trim is not a formally verified checker.

**Solver results and retained certificates.** All theorem checks use default backward drat-trim, without `-f`, on the exact listed CNF.

| Query | Variables | Clauses | CaDiCaL | Solve wall s | DRAT bytes | Check wall s |
|---|---:|---:|---|---:|---:|---:|
| Colour 0, ≥8, lex-leaders | 45,743 | 3,222,868 | UNSAT | 1.072 | 22,398,707 | 4.772 |
| Colour 1, ≥8, no symmetry | 20,105 | 4,878,914 | UNSAT | 140.357 | 1,162,120,960 | 123.968 |

Both checker logs contain **`s VERIFIED`**:

- Colour 0: [CNF](data/n12_1100101100011_c0_lex.cnf), [DRAT](certificates/n12_1100101100011_c0_lex.drat), [solver output](logs/n12_1100101100011_c0_lex.solve), [checker output](logs/n12_1100101100011_c0_lex.check). Its preserved [base CNF](data/n12_1100101100011_c0.cnf) has 16,703 variables and 3,135,748 clauses.
- Colour 1: [CNF](data/n12_1100101100011_c1.cnf), [DRAT](certificates/n12_1100101100011_c1.drat), [solver output](logs/n12_1100101100011_c1.solve), [checker output](logs/n12_1100101100011_c1.check).

**Requested rejection controls and positive control.** The deletion control removes exactly the at-least-eight unit `16703 0` from the final colour-0 lex CNF, retaining every symmetry clause. CaDiCaL returns SAT. [check_deletion.py](check_deletion.py) checks the single-clause deletion and directly evaluates every remaining clause under the complete assignment. Files: [deleted CNF](data/n12_control_deleted.cnf), [SAT assignment](logs/n12_control_deleted.solve), [check](logs/n12_control_deleted.check).

The corrupted proof keeps only the concluding empty clause, in textual DRAT, with all justifications erased. Backward drat-trim rejects it on the final colour-0 CNF, exit 1 and **`s NOT VERIFIED`**: [corruption](certificates/n12_corrupt.drat), [output](logs/n12_corrupt.check). This is the expected rejection.

The positive control asks for at least seven colour-0 members with the same 66 lex comparisons. It is SAT. [check_family.py](check_family.py) directly checks the seven returned actual sets for colour, distinctness, union and intersection; [check_model.py](check_model.py) evaluates all 3,219,164 clauses of this control. Files: [base](data/n12_positive7.cnf), [lex CNF](data/n12_positive7_lex.cnf), [assignment](logs/n12_positive7.solve), [family check](logs/n12_positive7.family_check), [full model check](logs/n12_positive7.model_check).

**Search region and second problem.** Both endpoint extensions of round one's n=11 colouring failed, with explicit eight-set counterexamples. The published counterexample-guided method then searched rank words, using checked closed families from round one embedded, reflected or translated into [12] as initial constraints. Each new learned family was checked by original set operations. The search found `1100101100011`; its colour-1 search verdict was then reproduced with the retained proof above. [Search log](logs/search_n12.jsonl). Neither unproved search UNSAT verdicts nor unfinished proofs enter the theorem.

For **#112**, let k(6,3) be the least N such that every oriented graph on N vertices has an independent six-set or a transitive three-vertex tournament. The November 11 public [29-vertex witness](https://github.com/rsvaultpudgy-create/erdos-112-lower-bounds) already gives k(6,3)≥30, superseding the spec's 29..33 interval. Our separately written [check_oriented.py](check_oriented.py) verifies its 140 arcs against all 475,020 six-sets and every ordered triple: [output](logs/k63_public_N29.check). This reproduction is not new.

The new region is **N=30**, with a direct [CNF](data/k63_N30.cnf) of 870 arc variables and 618,627 clauses. [encode_oriented.py](encode_oriented.py) forbids anti-parallel arcs, excludes each ordered transitive triple, and requires an arc among every six-set. Natural root symmetry sorts its star into out-neighbours, in-neighbours and non-neighbours, and fixes 0→1. Any admissible graph has an arc; rename its tail 0, head 1, and sort the remaining vertices, so these clauses are sound. The separately written complete-CNF check passes: [output](logs/k63_N30.encoding_check).

The 30-vertex run reached its 900-second limit without a SAT or UNSAT answer (900.108 seconds measured wall time); the process group was terminated. [Solver log](logs/k63_N30.solve), [stop record](logs/k63_N30.solve.json). The region tried was this complete N=30 instance with the stated root symmetry. It produced no certificate and no improved bound; its partial DRAT is retained as UNVERIFIED. SAT would raise the lower bound to 31, while checked UNSAT would settle k(6,3)=30. A longer campaign is left for a separate job after this requested one-case result is complete.

**Prior art and credit.** The [omega October 9 note](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md) explicitly leaves the even-n values open. Bhattacharjee–Mandal–Bhattacharya's [v1.0.0 paper](https://github.com/anaxia-research/Erdos-1183/blob/59e72f9511286e9e981b86eb3f7f9bc15e8d59ef/paper/Erdos.tex) gives exact f values through n=10 and describes the closure-SAT and counterexample-guided methods used here. Their current paper and live #1183 forum provide no matching f(12) upper bound in the retrieved sources. Round one's locally reproduced n=10 baseline and referee-supported f(11)=7 supply the preceding computations; this job starts at n=12.

The final November 14 source refresh covers the site/forum/proof claim, GitHub paper/commits/issues and recently updated repository search, Tao raw table and open PRs, and the named AI-result sources. It found a repository transfer from creelie to anaxia-research, with the same repository ID, README and October 14 commits, and no new finite construction. [PRIOR_ART.md](PRIOR_ART.md) records initial and final dates, URLs, source limitations and all other surveyed candidates. #1182 F(7)=11 and f(7)=16 were already published in the 1998 table through n=12 and were dropped; #531's F(4)≥397 is public; #555/#558's provisional R5(C4) interval lacked complete allowlisted primary-table clearance and was not selected. Search misses do not guarantee priority.

Credit Erdős and Ulam for the original problem (Erdős, 1978, *Problems and results in combinatorial analysis and combinatorial number theory*, p.39); Bhattacharjee, Mandal and Bhattacharya for the existing SAT/closure method and constructions; omega for the explicit even-dimensional question; and ipezygj for the #609 SAT-plus-checkable-proof workflow motivating this job. The #609 prose was read only. No ipezygj research script was copied, imported or run, and its already reproduced case was not recomputed. For #112 credit Erdős–Rado, Bermond, Ihringer–Rajendraprasad–Weinert, and the cited November 11 witness repository. All new code and checking here are by the same agent. This is candidate and unrefereed.

**Reproduction and resources.** From this directory, with Python 3.10+ and the retained tool builds:

```sh
sh replay.sh
```

That checks the full colouring/lower argument, both exact encodings including symmetry, both theorem DRAT proofs, the SAT controls, the rejected corrupted proof, and the #112 reproduction/encoding. Python programs use only the standard library. The actual run used the shared research Python environment.

To regenerate fresh theorem queries without overwriting retained files:

```sh
mkdir -p reproduce
nice -n 10 python3 encode_family.py 1100101100011 0 8 reproduce/c0.cnf
nice -n 10 python3 add_lex.py reproduce/c0.cnf reproduce/c0_lex.cnf
nice -n 10 python3 encode_family.py 1100101100011 1 8 reproduce/c1.cnf
nice -n 10 tools/cadical/build/cadical reproduce/c0_lex.cnf reproduce/c0.drat
# Expected solver exit 20; then:
nice -n 10 tools/drat-trim/drat-trim reproduce/c0_lex.cnf reproduce/c0.drat
nice -n 10 tools/cadical/build/cadical reproduce/c1.cnf reproduce/c1.drat
# Expected solver exit 20; then:
nice -n 10 tools/drat-trim/drat-trim reproduce/c1.cnf reproduce/c1.drat
```

`BUILD_COMMANDS.txt` gives sequential source-build commands. As instructed, this run copied our complete source trees and binaries from round one. Pins: CaDiCaL rel-3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`; kissat rel-4.0.4 `8af8e56f174b778aef3aa45af9f739b2a5f492c2`; drat-trim `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Actual copied HEADs are in [tools/COPIED_BUILDS.json](tools/COPIED_BUILDS.json).

At most two solvers ran concurrently, with brief separate checking work; fewer than six CPU cores were used. Commands requested nice 10; inherited niceness 15 made observed workers nice 20. `/usr/bin/time -l` and aggregate RSS samples are retained in logs. The observed aggregate peak is about 4.62 GB, below 8 GB. Each proof is below 20 GB and the directory is below 60 GB. Both unfinished proofs are retained and labelled unverified; no proof was deleted or compressed. SHA-256 hashes are recorded in `SHA256SUMS`. No predictive score was produced, so SBS does not apply.

No submission, commit, push, PR, post or external message was made. The requested one-case result is complete; the next useful work is mathematical review of this finite equality and its encoding/symmetry argument. A further #112 solver campaign is a separate target, not an implication of this result.
