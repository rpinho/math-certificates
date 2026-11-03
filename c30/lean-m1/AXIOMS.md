# Axiom audit

Non-standard axiom list: **empty**. No paper, numerical-certificate, analytic
or combinatorial premise is declared as an axiom in this project. All
feasibility hypotheses are visible arguments of the theorems and are discharged
in the exact-parameter corollary.

`Audit.lean` (milestone 1) and `AuditM2.lean` (milestone 2) request
`#print axioms` for **every theorem in the project**,
including the auxiliary lemmas. The main results are `strip_envelope`,
`strip_envelope_application`, `finite_weighted_markov` and
`finite_family_selection`; `integer_strip_envelope` and `parity_envelope`
expose the integer-only results separately.

The milestone-1 output is:

```text
'C30Lean.excess_nonneg' depends on axioms: [propext, Quot.sound]
'C30Lean.strip_count_identities' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.StripEnvelope.vector_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.StripEnvelope.vector_length' depends on axioms: [propext]
'C30Lean.StripEnvelope.vector_sum' depends on axioms: [propext]
'C30Lean.StripEnvelope.excess_values' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.parity_envelope' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.integer_strip_envelope' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.realExcess_int' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.realExcess_interpolate' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.integer_thresholds_suffice' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.strip_envelope' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.application_feasibility' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.strip_envelope_application' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.finite_weighted_markov' depends on axioms: [propext, Classical.choice, Quot.sound]
'C30Lean.finite_family_selection' depends on axioms: [propext, Classical.choice, Quot.sound]
```

These are exclusively Lean's standard axioms. The raw replay output is retained
in `receipts/axioms.txt`, with complete checked theorem signatures in
`receipts/axioms-and-statements.txt`. `lake build` also compiles `Audit.lean`
as a default target, so its output appears in the clean build log.

No project source uses `sorry`, `sorryAx`, `admit`, `native_decide` or
`Lean.ofReduceBool`. `receipts/grep.txt` scans every project `.lean` file;
`receipts/lean.sha256` enumerates the scope. Keywords in the frozen pass bar,
documentation and audit scripts are not proof uses. Dependency implementations
are supplied by the pinned Mathlib cache; no assumption is made that Mathlib's
entire source tree is free of tactic definitions bearing these names. The
reported axiom closures are for the actual resulting proof terms.

Proof tactics used here include `omega`, `linarith`, `nlinarith`, `ring`,
`norm_num`, simplification and casts. They produce proof terms checked by the
Lean kernel; no native reduction trust shortcut or external numeric verifier is
used. No non-standard axiom citation is applicable.

