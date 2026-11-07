# Independent referee report

The fifteen stated OPTW values pass a newly written exact finite-cover checker, plus independent raw-data primal checks under both stated distance conventions. This is a mathematical verification for the explicitly stated service-start/floor2 model. It is not an operational floating-point optimality proof. No claimant search or verifier source was imported, linked or run. See VERDICT.md for the final decision and SUMMARY.json for final counts.

The new C++ verifier checks the root, every retained state's feasible return and each permitted customer extension. It rebuilds all bounds from fresh public raw data. Its proof argument is in VALIDITY.md. The fifteen files contain 225,910 labels and require 11,439,464 successor checks. Python fractions independently verify the routes and unrounded Euclidean rational enclosures. The exact public input bytes and supplied proof bytes match the frozen cohort, selected from the SHA-verified immutable capsule. The locally retained evidence.tar.gz contains only this claim's data, not the capsule's other jobs.

Primary checks: Gama and Hugo L. Fernandes are the named authors of arXiv:2011.03647v2. The historical BKS and neural values match Tables B.7/B.1, pp. 27/22. They are raw single-day benchmark rewards, not generated-tourist averages. Eq. 2.1 and the released feasibility code use service-start deadlines; the introductory prose's wording about when a visit stops is less precise. Ten supplied witnesses would fail a service-completion-window interpretation. The released format explicitly specifies rounding down to two decimals. Exact truncation and the released floating computation nevertheless differ on 33 undirected edges; for example, t201 edge 117–81 is exactly 16.15 but floating flooring gives 16.14. All fifteen supplied witnesses pass a separate float32 scheduling simulation. That does not rule out a different route that floating rounding accepts.

There is no predictive holdout: these are retrospective exact solves of fixed public instances. The fifteen are selected from the full 33-case cohort by proof completion, not an estimate of generalization. Historical overwritten control-receipt bytes remain unrecovered; this referee's fresh checks establish present mathematical validity, not the authenticity of a lost historical seal. Original circuit solver flags and claimant PASS labels are not used as proof here.

Relative to the primary paper, eleven of the fifteen reward values already appear in its BKS or neural columns. Four exceed all those columns: t203=182, t204=179, t236=180, t243=204. The addition relative to that paper is a finite optimality/upper-bound reference, rather than a new training method. Later Kim/Barde MetaPNet-OPTW reports 20/33 improvements, but its per-case table was not obtained. Established ng-route/ESPPRC methods and public Pulse solvers predate this claim. No novelty, priority, speed, or author-interest judgment follows; PRIOR_ART.md records the source screen and access limits.

Reproduce on the authorized pod in /workspace/ref_hugo_HB01, using the included transport helpers to place the retained data/code there:

```sh
mkdir -p evidence
tar -xzf evidence.tar.gz -C evidence
nice -n 10 python3 fetch_sources.py
nice -n 10 python3 -m pip install --no-cache-dir --target deps pypdf
nice -n 10 g++ -std=c++17 -O3 -Wall -Wextra referee.cpp -o referee
nice -n 10 python3 controls.py
nice -n 10 python3 audit.py
nice -n 10 python3 run_covers.py
nice -n 10 python3 run_dfs.py
nice -n 10 g++ -std=c++17 -O3 greedy.cpp -o greedy
nice -n 10 python3 extra_audit.py
nice -n 10 python3 summarize.py
```

Use nohup/logs for long remote work and at most four concurrent single-thread workers. The DFS has a fixed 300-second cap per case; only COMPLETE outputs certify an upper. The cover checks are the upper proof for all fifteen regardless of the optional DFS cap. The fresh source fetch needs public network access; the live commit used was a21f70183b6a92bbfa71fa67b8cbb36b59888dcf. NumPy is already installed on this pod. Controls, audits, caps, source hashes and the heuristic control are retained as small JSON receipts.

The next evidence bar for extending the result to the released executable is an exact certificate over its float32 scheduling semantics and actual generated distance matrix. This would answer the remaining numerical-scope objection without a new heuristic search claim.

Final independent elementary pass: eleven COMPLETE proofs, 7,114,722,063 prefixes; t204/t223/t236/t250 hit the fixed 300-second cap and add no upper proof. The five elementary checks cited in the claim all completed again. The simple 24-variant insertion control reached four optima (t202/t208/t218/t227), with two scores above the paper's neural column (t218/t227). All fifteen benchmark false-upper and empty-cover mutations were rejected. NumPy scalar calculations independently confirmed the 33 floating-distance discrepancies and all fifteen float32 witness acceptances. The full official set of 33 single-day files matches the frozen cohort's instance set.

All started workers, including the first failed source-fetch/table-parser attempts, were checked exited. Temporary pod downloads, dependencies/caches and binaries were removed after copying back the small receipts. Final pod directory size: 9,833,749 bytes; WORKERS.json records termination and cleanup. No contact, publication, repository mutation, pod provisioning, or off-pod scientific computation was performed.
