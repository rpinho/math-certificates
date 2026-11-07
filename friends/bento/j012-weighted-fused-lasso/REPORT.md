# Independent referee of bento_J012

The mathematical claim survived this audit. See VERDICT.md for the requested concise verdict and PROOF_AUDIT.md for the independent all-n argument. I found no change of quantity, invalid control substitution, or correctness gap.

All scientific computation ran on the permitted phys pod, under /workspace/ref_bento_J012, with nice 10 and at most twelve single-threaded solver workers. The Mini only read/edited files and packaged, transported, checksummed, and extracted small artifacts. No claimant search/verifier code was read or imported. No one was contacted, no credentials were placed on the pod, and no Mini data beyond the authorized derived files were transported.

The independent solver enumerates signed primal jump patterns, solves fused block levels from stationarity, and intersects exact rational KKT inequalities. It reconstructs the entire lambda path, not samples of it. The second checker imports no solver and verifies cumulative stationarity, interval-wide dual feasibility and subgradient signs, continuity, coverage, maximal pieces, and the constant infinite tail.

Results: 570/570 complete paths passed both independent programs. These comprise two baselines, the 73 supplied panel paths (all agree exactly with the claimant's coefficients and knots), 252 fresh cases across n=2,...,8 with multiple weight and tie patterns, and 243 exhaustive n=3 cases with weights in {1,2,3} and data in {-1,0,1}. The 73 supplied panel paths include 27 with unfusions; 22 fresh cases also have unfusions. No good contact returned, no bound was violated, and no pair exceeded the eight-event bound. The maximum observed charge count was two. This is finite diagnostic evidence, not the proof of the all-n theorem.

The primary Fig.1 has T=5 and knots 25/27,25/23,100/73,25/4; its equal-weight control has T=3. Independently reconstructed printed Theorem 4 inputs for n=3,...,10 yield T=3,4,5,8,9,10,13,16. These small values are not an asymptotic lower-bound proof. The independent one-defect n=10 reproduction gives T=12 and one unfusion. The second checker rejects a wrong slope, missing interval, missing tail, changed objective weight, and the independently solved zero-edge component control when tested under the original positive-weight objective.

PROOF_AUDIT.md checks the least-concave-majorant criterion, nonreturn of good contacts, signed-pattern count, amortized pair count, and simultaneous-event charging. The latter can be justified directly on the side where a changing coordinate is strictly free; no genericity assumption is needed. The claimant's perturbation identity is consistent as well. PRIOR_ART.md records primary references, author identity, the known concave-profile control, the 2026 signed-state count, and search limitations. No novelty or taste verdict is supplied.

Reproduce from this directory (these commands only transport and invoke work on phys):

```sh
python3 _codex/friends_podsh.py phys pod_start.sh 60
python3 _codex/friends_podsh.py phys pod_run.sh 60
python3 _codex/friends_podsh.py phys pod_poll.sh 60
# Poll until run.log ends with DONE 570 0, then:
python3 _codex/friends_podsh.py phys pod_checks_transport.sh 90
python3 _codex/friends_podsh.py phys pod_sources.sh 480
```

pod_run.sh contains the frozen input and independent solver payload; it does not depend on the claimant's current files. pod_checks_transport.sh contains the separate checker and zero-edge control. The source sweep's GitHub 403 responses are recorded, not replaced with successful-looking results.

All verdict evidence is now local in evidence/ and referee_evidence.tar.gz. BACKUP_RECEIPT.json records the matching pod/local SHA-256. The archived results include complete rational paths, exact inputs, code, logs, source snapshots and source receipts. finalize_transport.txt records aggregate diagnostics, absent worker processes, and cleanup: the pod directory ends at 1,223,884 bytes, below 1 GB; temporary downloads and export archive were removed only after their verified local copy existed.

Next bar: formalize the simultaneous-event endpoint-pair charging lemma in a proof assistant. That would address the strongest remaining objection to an informal universal proof; finite test expansion cannot substitute for it.
