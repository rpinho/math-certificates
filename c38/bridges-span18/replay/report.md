# C38 clean-room replay — PASS

Verdict: **PASS.** This independent clean-room computation reproduced the bound

**mu(Z²) >= 8388608/3192535**

with the complete frozen rational S(1353) reproduced exactly and S(1353) >= 1 checked using integers/Fractions. Every required native enumeration finished, including spans 16, 17, and 18. No certificate enclosure was left as an unverified numerical premise. The expanded coefficient vector was not materialized; this is a complete replay of the specified finite-family point enclosures and exact final assembly.

## Scope and independence

The mathematical inputs are exclusively the supplied files in `inputs/`, verified against `INPUTS_SHA256SUMS`. The machine rules and `POD.txt` were read for operational instructions. No producer source or executable was inspected or run, no excluded directory was searched, and no external coefficient table or historical replay receipt was adopted as an enumeration premise. References to unavailable producer files inside certificate JSON were treated only as data. No commits, pushes, posts, or public uploads were made. Only this job's explicitly authorized pod directory received job material.

The supplied proofs credit Kesten's irreducible bridge renewal, Jensen's span method, Enting's finite-lattice framework, Fekete's submultiplicative limit, Numaro, and Plánočka. This replay makes no novelty or record claim. The broad public-code search in the machine rules was excluded by the user's narrower clean-room instructions; see `../PRIOR_ART.md`.

## Independent enumeration

`transfer.hpp` implements local graph-degree rules using explicit component identities. Frontier slots encode empty edges, paired endpoints of terminal-free path components, and singleton endpoints of terminal-bearing components. Both terminal-introduction flags are retained. At each lattice vertex the code enumerates outgoing edge subsets, requires degree zero/two at ordinary vertices or degree one at the permitted terminal, rejects cycles, and accepts a completed path only when every other component is absent. It then canonically re-encodes the remaining components. Anonymous singleton identities are sufficient for the reason proved in the supplied state appendix: two distinct terminal-bearing components must contain the two distinct terminals.

`strip.cpp` constructs the complete reachable graph for every stage of a column sweep, starting from the empty state. A state is processed once; new successor keys are appended until a full cycle adds none. Hash collisions are resolved by full-key comparisons. The first-column surviving empty contribution is removed, fixing the minimum transverse coordinate to zero. Each completion is counted once; no reflection quotient is taken. The enumeration sums all bridges, and the renewal subtraction below bounds the irreducible subfamilies.

Finite point values use lower/upper integer numerators at scale 2^96. A transition adding k edges multiplies by `(M/2^27)^k` with an exact floor/ceiling. The product is evaluated by splitting the input into quotient and remainder at 27k bits. Checked 128-bit arithmetic suffices; no floating-point operation enters any mathematical decision. For spans 1–17, an upper potential at scale 2^-12 is constructed by monotone ceiling iterations from zero. A fully stabilized backward cycle proves every potential inequality. Pairing this potential with the remaining upper state vector bounds all omitted widths. Span 18 deliberately has no all-width upper potential: its tail field is an unused zero marker.

The span-specific numbers of transverse columns are
`41, 62, 82, 103, 125, 146, 168, 189, 212, 234, 257, 280, 303, 327, 351, 376, 401, 72`.
The corresponding range caps are one less. The maximum main-family degree is 6817, and span 18 has degree at most 18×72 = 1296.

`rectangle.cpp` sweeps along the bridge span, starting with each allowed initial height once. After each interior column it retains exactly 3 or 5 crossing edges. The final-column fork forbids right edges and introduces one terminal. It evaluates the two fixed frames separately; subtracting the smaller frame from the larger one normalizes transverse translation. The required frames are ranges 22 and 21 with terminal spans 18–30, and ranges 23 and 22 with terminal span 18. The resulting normalized interval endpoints must equal both rectangle search certificates exactly. The actual supplemental family comprises spans 19–30, range at most 22, crossing cap 5; its degree is at most 30×23 = 690.

## Mathematical assembly

Writing b_h for a finite bridge lower bound and U_h for a full bridge upper bound, the independent rational assembly uses

`alpha_h = max(0, b_h - sum_{j<h} beta_j U_{h-j})`

and, through span 17 only,

`beta_h = U_h - sum_{j<h} alpha_j b_{h-j}`.

The lower subtraction applies to the specified finite irreducible family because its reducible bridges inject into the full renewal products. It does not assert an exact renewal identity for width-truncated families. At span 18 only the lower formula is used. The packet supplies irreducible enclosures rather than raw bridge outputs; since all its alpha values are positive, its implied raw bridge bounds can be recovered uniquely and compared with the new enumeration without treating them as trusted numerical premises.

Let b=51081913/2^27, c=(51081913+314)/2^27, and let L17, L18 be the independently assembled lower values at b. U is the independently assembled full irreducible upper sum through span 17 at c. The rectangle evaluations give `e=max(0,(lo22-hi23)/2^96)`, a lower value of the genuine disjoint higher-span family. No signed difference of coefficient families is used.

For k=1353, r=(51081913-k)/51081913, the final exact expression is

`S(k) = (1+k/314)L17 - (k/314)U + r^1296 L18 + r^690 e`.

The secant inequality follows coefficientwise from the monotonicity of the divided differences of integer powers. The degree powers follow from r^n >= r^N for 0<r<1 and n<=N. Unique factorization at singly crossed cuts makes concatenations of the chosen irreducible bridges inject into self-avoiding walks. Thus S(k)>=1 forces divergence of the walk generating series at a=(51081913-k)/2^27; the submultiplicative growth limit gives mu>=1/a. The reciprocal reduces exactly to 8388608/3192535. Failure of this particular sufficient inequality at k+1 is not an upper bound on mu.

`check.py` uses Python integers and `fractions.Fraction` throughout. It checks all input hashes, family parameters, the intermediate span-degree/secant/disjoint seed arithmetic, both rectangle search values, the entire frozen rational S(1353), S(1353)>=1, and the reciprocal. PASS additionally requires every new native output, exact main-span enclosure matches, exact auxiliary upper-sum equality, and both normalized rectangle interval matches. Missing native output remains PARTIAL. The expanded coefficient vector is not materialized or claimed to have been compared.

## Controls and operational record

`literal.cpp` independently enumerates ordered vertex sequences by depth-first search and compares every coefficient with the transfer sweep for spans 1–12. There are 36 comparisons: one- and two-row frames at all lengths, and three-row frames through min(18,3h). These controls do not constitute exhaustive unrestricted enumeration of those spans. `literal_rectangle.cpp` independently counts irreducible walks in frames of one through five rows, spans 2–5, at all possible lengths. Their exact rational generating values must lie in the independently computed rectangle intervals.

The pod computations run at nice 10, with at most 28 enumeration threads. PID files, resource samples, native logs, a minute heartbeat, and 15-minute local pulls are retained in `../pod/`. The first large graph build retained every stage's hash table; it was replaced with a build that releases a destination table after processing the stage. A later allocation-only refinement reserves exact edge-vector capacities. The same numerical algorithm is retained, with explicit completion-sum capacity checks. The final checked builds are identified below. The initial span-17/18 construction attempts were stopped to reduce memory; both replacement computations completed. One duplicate range-22/span-18 job was stopped because the identical value was already computed by the range-22 sweep’s span-18 terminal fork. No final computation failed a mathematical or arithmetic guard.

## Reproduction

Audit the retained independent native outputs, from the job directory:

```sh
nice -n 10 python3 replay/check.py
```

For a completely fresh replay on Linux with GCC/OpenMP, preserving the job directory's `inputs/`, manifest, and `replay/` layout (one native job at a time, up to 28 threads per strip job):

```sh
nice -n 10 python3 replay/check.py --run --threads 28 --native-dir replay/fresh
```

The latter rebuilds the independent native programs and performs the full enumeration. It is computationally expensive. No producer executable or source is needed. The native programs read the family parameters and evaluation points, not certificate values. The latter enter only the independent Python comparison and assembly.


## Completed comparisons and runtime

All 18 main-point finite bridge lower bounds agree exactly with the values uniquely implied by `EXACT_ENCLOSURES.json`. Through span 17, all full bridge upper bounds and both renewal endpoints agree exactly. Span 18’s finite bridge upper bound also agrees exactly; no full-width upper claim is made for that span. All 17 auxiliary-point computations completed, and their independently assembled irreducible upper sum equals the frozen U exactly. The span-degree, linear secant, disjoint-extension, and exact-power seed arithmetic also agrees.

The two normalized rectangle intervals agree at **both** endpoints, at scale 2^96:

| Family | Lower numerator | Upper numerator |
|---|---:|---:|
| Range <=22, spans 18–30, cap 5 | 7451330849486838403732161 | 7451330849486838421757765 |
| Range <=23, span 18, cap 5 | 3415308433821208587293284 | 3415308433821208589119087 |

Consequently the independently recomputed supplement lower value is exactly
`2018011207832814907306537/39614081257132168796771975168`.
Combining it with the independently recomputed L17, L18, and U reproduces the **entire** frozen rational S(1353), not merely its decimal display. The exact tests S(1353)>=1, S(1354)<1, and 1/a=8388608/3192535 all pass.

All 36 bridge coefficient controls and all five literal irreducible rectangle controls passed. The final guarded build repeated all 32 span-point records through span 16; every field other than elapsed time equals the earlier independent run. No coefficient samples were substituted for the prescribed large evaluations.

Large-strip runtime includes graph construction, all prescribed forward columns, and upper-potential construction where applicable:

| Span | Width | Stage states | Transitions | Evaluated points | Wall seconds | Threads |
|---|---:|---:|---:|---:|---:|---:|
| 16 | 376 | 184210059 | 292146006 | 2 | 1687.10 | 4 |
| 17 | 401 | 545181552 | 865431549 | 2 | 3161.72 | 8 |
| 18 | 72 | 1613562216 | 2563523274 | 1 | 2875.58 | 12 |

The three rectangle sweeps took 4815.64 seconds (range-22 frame, spans 18–30), 3029.95 seconds (range-21 frame, spans 18–30), and 4452.26 seconds (range-23 frame, span 18). Each used one thread. The range-22/span-18 frame is the saved h=18 terminal fork of the first sweep; its exact integers are parsed from that independent native log, and the same extraction is implemented in `check.py --run`.

The run began at about 2026-11-04 15:30 UTC; all enumeration finished by 17:07 UTC, the final pull completed at about 17:09 UTC, and a final Mini process audit reconfirmed zero workers at 2026-11-04T17:12:49.044217+00:00. Sampled peak aggregate worker RSS was **86,997,323,776 bytes**, below the approximately 110 GB budget. At most 28 enumeration threads were allocated concurrently; all enumeration ran at nice 10. The compiler was GCC 13.3.0 on Ubuntu 24.04.

Spans 1–16 used `strip.cpp`; spans 17–18 used the retained `strip_v2.cpp`. Their only differences are vector reservation and capacity trimming during graph construction. Their component rules, graph closure, directed arithmetic, potential checks, and completion capacity checks are identical. `transfer.hpp` is shared. `ENUMERATION_SUMMARY.json`, `RECTANGLE_SUMMARY.json`, and `RESULTS.json` retain the complete results and comparisons; `../pod/BUILD_SHA256SUMS` records the executed binary and native-source hashes.

The model label `gpt-6` records the family identified by this session; no more specific deployment suffix was exposed.

## Cleanup and artifact binding

The final pod audit checked the recorded worker PIDs and scanned `ps -axo pid,ppid,pcpu,command` for remaining job processes. It found **zero**. The local supervisor was stopped; seven lingering SSH wrappers for completed jobs were terminated, and the Mini process audit likewise found **zero** remaining workers. The final rsync after shutdown retained the pod cleanup receipt. See `../pod/CLEANUP_POD.json` and `CLEANUP_MINI.json`. No job worker or supervisor was intentionally left running. `STATUS.md` is updated, and completion was well before the user’s hard deadline.

Source-manifest SHA256: `4d35f24141bbefd4aa64a79508fb474e6163145eceaa8f57bbcbe09a55d08cac`.

Exact-result manifest SHA256: `b6e94bba4f640c62cc8a7184b1a48b2e3872ddacbcb79983ba464ffebd6cccfd`.

No further computation is needed for this replay. Independent reviewers can rerun `check.py --run` using the supplied inputs and these sources; no producer code is required.
