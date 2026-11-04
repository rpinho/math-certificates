# Packaging adaptations

The layout follows round 4's flat certificate/verifier/proof arrangement,
adding verification/, controls, regression fixtures and release-copy receipts.
Search code, optimizer graphs, remote execution/harvest utilities, caches,
and unrelated logs are omitted. The certificate and both mathematical
checker implementations are copied unchanged. Producer include files and
all three producer control/exponent implementations are also unchanged.

Regression tests change only the two paths required by this flat layout:
the fixture root and verify_orbit8.py. Historical fixture compiler paths
are redacted without changing checkpoints or diagnostics. Historical repair
documents are labeled archive records; their omitted receipt paths refer
to the producer archive. PROOF.md relocates certificate/control links and
labels the omitted historical invariant snapshot. The round-5 proof is
retained verbatim as the universal frontier/base-rule premise; historical
round-5 artifact/log references are context, not reproduction inputs.

The producer full-replay log predates the operational checkpoint repair;
its printed source hashes are historical. The repair changed diagnostics
and launcher behavior, preserving mathematical predicates, arithmetic and
certificate bytes (CHANGES_CONTROLS.md). The independent full replay hashes
the exact unchanged independent implementations supplied here.

PROVENANCE.md in verification/ documents correction of the generic checker
model label from the executor-selection sidecar and all relocated receipt
paths. The original receipt and level packet remain byte-identical archive
records. The strict body-level packet is separately normalized relative to
pr_body.md. These receipt transformations do not assert a new full replay.

Release-control raw captures can include local interpreter, compiler and
temporary directory paths. Their publication copies replace only those
paths, preserving statuses, checkpoints and diagnostic text; their receipt
log hashes are regenerated. Original local captures are kept outside this
publication tree. No private home-directory paths are publication inputs.
