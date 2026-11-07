Independent referee: exact optimum654 verified for classical TOPTW long-window Cordeau pr11 with three routes. The claim's numerical result passes. Its link to MontemanniTOPTW1 is incorrect; the authentic input is in MontemanniTOPTW2. This is a certificate for a known feasible score, not a higher score or a correction to Gama/Fernandes's single-route paper.

Fresh public-source downloads, independently written code, all certificate data, the public baseline source/configuration/output, and compact receipts are in `evidence/`, recovered from mscr in `referee_bundle.tgz`. `RECOVERY_RECEIPT.json` authenticates the copy-back. No claimant search or verifier source was read, imported or executed. The public Ševeček solver was separately compiled as the baseline. All scientific computation ran nice10 on mscr inside the authorized folder, within the12-core limit; solvers/checkers used one core each and builds used two. No model fitting or holdout was used.

The independent parser follows the official format. Raw coordinates are exact thousandths; travel in hundredths is `isqrt(dx*dx+dy*dy)//10`. Windows constrain service start. Routes may wait, start/end at the depot, and return by1000. D/Q/header fields are irrelevant under the official rules. All raw bytes independently match the claim's SHA256. Both submitted and fresh public routes score654, visit47 customers, and omit node19 of prize3.

The upper checker treats the saved proof as untrusted numerical state data. A state is a current node, departure time, reduced reward and remembered visited nodes. Serialization is converted to service-start time. An elementary route is contained in the relaxed state system that forgets visited nodes outside a chosen neighborhood. A label dominates another only at the same node, with no later time, no smaller reward and a subset of remembered nodes. These relations are preserved by every allowable extension. The checker requires the initial state to be dominated and every allowable successor of every saved state to be dominated. All saved rewards must be at most11082. Arbitrary unreachable saved states do not invalidate this inductive simulation argument.

It independently checks46749 states and1180957 transitions, with zero uncovered successors. It uses all-pairs shortest travel lower bounds to reject impossible returns, rather than assuming floored Euclidean distances obey the triangle inequality. No knapsack/suffix pruning or native optimizer status is needed in this independent check. With scaled reward `1000*p_i=y_i+w_i`, nonnegative penalties, and no repeated customer across routes, `1000*score <= sum(y_i)+3*11082 = 623716+33246 = 656962`. Hence score<=656. Exact raw subset-prize reachability tightens this to654: total657 and minimum positive prize3 exclude655/656. The feasible654 witness closes the bound.

Validation includes40 exhaustive small directed non-metric fixtures, plus rejection of false bounds and missing initial states in every fixture. The raw route checker rejects five malformed witnesses (fleet, duplicate, index, depot, time window). A deterministic prize/added-travel-and-service insertion control scores544; it does not match654. Fresh unmodified public SISR reaches654 and its new routes pass the independent raw checker. A separately written mandatory-all-customers CP-SAT feasibility control returned UNKNOWN after120seconds on one core; this is inconclusive and contributes nothing to the proof.

Reproduce on the authorized pod after restoring `evidence/` into its folder:

```sh
cd /workspace/ref_hugo_HB16
nice -n 10 python3 prepare.py
nice -n 10 g++ -O2 -std=c++17 closure.cpp -o closure
nice -n 10 ./closure
nice -n 10 python3 fixture_checks.py
nice -n 10 python3 finalize.py
```

`finalize.py` checks the closure, derives the exact subset-prize upper bound, and replays both654 witnesses from raw inputs. `controls.py` additionally runs the insertion and120-second inconclusive CP control. `baseline.sh` builds the public source and repeats its randomized run; stochastic outputs may differ. Python standard library and GCC suffice for the certificate; OR-Tools is used only for the inconclusive CP control and pypdf only for source extraction.

The source audit is in `PRIOR_ART.md`. Fresh2020 supplement Tables9/20 authenticate unstarred654 for m3 and starred657 for m4, with stars explicitly defined as proven optima. A fresh public-session thesis download matches its retained real PDF and TableC.5 confirms654. Gama/Hugo L. Fernandes's original paper is genuinely coauthored by Hugo and addresses one-route OPTW: pr11 BKS353, ILS330, model351. The mechanical addition here is an exact upper certificate for the already-known three-route score; no learned-model or generalization comparison has been tested. Benchmark reuse is open, with no untouched holdout asserted. Gedik2017's two extra optima are visible in its abstract, but its per-case table and the2026 Springer full table remain unauthenticated. No novelty/priority/interest judgment follows from these bounded checks.

Strongest author objection: three-route654 was already a published feasible score and differs from the one-route neural benchmark; this certificate does not establish an improvement to those reported learned-model results. The claim itself largely recognizes that boundary. The concrete next step is a corrected source-linked comparison row distinguishing those two tasks and linking the correct official archive.
