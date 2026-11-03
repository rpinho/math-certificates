# Conditional-square certificates for Ramsey multiplicity

Candidate and unrefereed. These are computational proof candidates, with separate exact implementations; there has been no external human referee review. Standard flag-algebra reasoning is credited to Razborov, PPSS, KPS and the preceding public certificates. See PRIOR_ART.md.

## Independence and limitations

The search generates numerical SDP matrices or graphons. Exact checkers use frozen integer factors or rational probabilities and do not call search routines. Separate implementations are not independent external authorship: all new code here was prepared in one Codex session, and remains unrefereed. Rejection controls, hashes and final receipts accompany the selected artifacts. Floating objectives, solver return codes, and numerical PSD diagnostics are not proof inputs.

## Explicit K5 upper construction

Partition [0,1] into256 equal parts indexed by (a,x), where a belongs to {0,1,2,3} and x belongs to F_2^6. Write w=popcount(x XOR y), and folded distance h=min(w,7-w), which is one of0,1,2,3. Define the red probability by this table; the blue probability is its complement.

| Layer relationship | h=0 | h=1 | h=2 | h=3 |
|---|---:|---:|---:|---:|
| a=b | 0 | 2/3 | 1 | 0 |
| a!=b | 1 | 0 | 0 | 35/36 |

The diagonal entries of the step matrix are0. The construction extends the folded-Hamming/Cayley ideas of Thomason and PPSS, and the preceding public fractional constructions, Jeetu SK's construction in PR #277 (SK2026) and Ricardo Pinho's subsequent symmetry-breaking construction in PR #307, to four layers with a second fractional orbit. PR #307's graphon is the three-layer member of this family. The full matrix is frozen in certificates/c5_upper_radial4.json.gz, with denominator36 and all256 block weights1.

Its exact monochromatic K5 density is

    t(K5,W)+t(K5,1-W)
      =10014541091180996983/6058287395472553279488
      =0.001653031696493139... <2405659597/1427496763392 (PR #307).

Two exact methods agree separately on the red and blue contributions. The generic matrix checker partitions all ordered five-tuples by distinct support and positive occupancies, multiplies edge numerators to the required occupancy powers, and weights each support by5!/product(occupancy!). It assumes no matrix symmetry beyond W_ij=W_ji, and no transitivity. For its accepted input range D<=64,n<=1024, each edge product is at most2^60 and the complete nonnegative sum is at most2^110, so unsigned128-bit accumulation is exact. GMP reduces the final fraction. Thirty literal ordered-tuple comparisons with arbitrary loops and probabilities, plus malformed-input controls, pass.

The separately written structured GMP checker reads no search profile or histogram. Translations of F_2^6 and permutations of the four layers act transitively, so fix the first sampled part to(0,0). Classify the other four binary vectors by the counts of their16 possible coordinate columns. Every count vector totaling6 is enumerated (54,264 vectors), with multiplicity6!/product(count!). For each count vector, enumerate all4^4 assignments of the other layers. This exactly enumerates all256^4 ordered remaining parts. Edge probabilities are rebuilt directly from distances and the two rational parameters. With common denominator36, the rooted integer sums are

    red  =13559225531043975390720,
    blue =12398464977297168789216,
    denominator =36^10 *256^4.

The generic full-matrix sums are exactly256 times these values, with denominator36^10*256^5. Four small geometric instances agree with the generic arbitrary-precision checker. The structured checker also reproduces the preceding exact public baseline2405659597/1427496763392 at three layers, p=5/7 and q=1. Invalid parameters, malformed matrices and a false stronger threshold are rejected.

For every N, independently sample each vertex's part uniformly and then each edge colour with the indicated probability. The expected monochromatic K5 density is the displayed exact fraction; hence some colouring has density no larger than it. Taking the asymptotic minimum proves the candidate upper bound. No numerical optimizer or solver status is a proof input.
