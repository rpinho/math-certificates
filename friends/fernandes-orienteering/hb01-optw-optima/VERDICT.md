HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

All fifteen stated rewards are exact optima for the explicitly claimed service-start, exact floor-to-two-decimals model. Each has a verified same-score unrounded-Euclidean witness. I found no mathematical counterexample.

The [primary paper](https://arxiv.org/pdf/2011.03647v2) is by Ricardo Gama and Hugo L. Fernandes. Every historical BKS/neural number matches Tables B.7/B.1, pp. 27/22. These are single-day benchmark rewards, not generated-tourist averages. Fresh public inputs match the frozen bytes and official commit a21f70183b6a92bbfa71fa67b8cbb36b59888dcf.

What I ran: newly written C++ raw parser/upper-certificate checker, importing no claimant search or verifier code; 225,910 states and 11,439,464 successor checks passed. Independent rational route checks passed for all fifteen under both travel conventions. Eighty brute-force fixtures passed; forged false uppers and empty covers were rejected on every claimed benchmark.

A separate full-visited-set exhaustion completed eleven cases, checking 7,114,722,063 prefixes, including all five elementary checks cited in the claim. t204/t223/t236/t250 hit my 300-second cap and provide no additional proof; their independently checked upper certificates still pass.

The convention matters: Eq. 2.1 and released code constrain service start; ten supplied witnesses finish service after a customer closes. Released floating flooring differs from exact truncation on 33 undirected edges. All fifteen witnesses pass my NumPy float32 simulation, but operational float32 optimality is unproved and explicitly excluded by the claim.

There was no predictive holdout: these are retrospective solves of public instances. The frozen cohort reports all 33; fifteen were selected by completed-proof criteria. This supplies no generalization estimate. Overwritten historical control-receipt bytes remain unrecovered; fresh verification does not restore that historical seal.

Trivial control: 24 simple greedy-insertion variants recover four optima (t202/t208/t218/t227); two also exceed the paper neural scores (t218/t227). The remaining gains are not explained by this control. No learned improvement is established or claimed.

Relative to the paper, the addition is fifteen certified upper/optimum values. Eleven rewards already appear in its BKS/neural columns; four exceed all those columns: t203=182, t204=179, t236=180, t243=204. Established ng-route/Pulse methods predate this work. Later [Kim/Barde MetaPNet](https://www.sciencedirect.com/science/article/pii/S0968090X25004541) reports 20/33 BKS improvements; its per-case table remains inaccessible. See PRIOR_ART.md.

Strongest author objection: these certificates do not establish the optimum of the released floating-point executable, so comparisons must retain the stated mathematical scope.

Evidence/code: REPORT.md, VALIDITY.md, SUMMARY.json, audit.json, covers.json, dfs.json, controls.json, extra_audit.json and evidence.tar.gz. All scientific computation ran on the authorized pod. All workers exited; temporary downloads/caches were removed; the pod directory ends at 9,833,749 bytes.

NEXT BAR: certify these fifteen values against the released executable's actual distance matrix and float32 scheduling transitions.
