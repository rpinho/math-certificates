# Manuscript source and scope

`c30.tex` is the amsart source; `c30.pdf` is the 10-page built manuscript. Build from the packet root:

```sh
nice -n 10 tectonic -k --keep-logs manuscript/c30.tex
```

The final build has no TeX warnings, undefined references or overfull/underfull boxes. PDF pages were inspected as rendered thumbnails; all ten pages have readable, unclipped layouts. Build output and the contact sheet were inspected in the input job and are omitted from this release. The final input authority and manuscript are retained byte for byte; their input hashes are in `evidence/release_provenance.json`.

Proof correspondence:

| Final authority | Manuscript |
|---|---|
| §1, published inputs | §§1–2, definitions and cited inherited lemmas |
| §2, Lemma 2.1 and four-series derivation | §3, Lemma 3.1 and Proposition 3.2 |
| §3, kernels, Rouché and local mean | §4, including Lemma 4.1 |
| §4, first-moment selection and balancing | §5, Proposition 5.1 |
| §5, common integer envelope | §6, Lemma 6.1 |
| §6, staircase and rational point | §7 |
| Verification and caveats throughout | §8 and VERIFIED.md |

The added clause is: “noncrossing also excludes an arc from B0 into a gap, since it would cross the chain arc over that gap.” It is CS2's requested clarification of the existing concatenation-factor argument. All mathematical constants, hypotheses, conclusions and proof strategy are preserved. The paper adds definitions, history, attribution, explicit inherited lemma statements and verification limits; it asserts no stronger bound.

The first-moment density mu2, selection threshold s2 and synthetic envelope coordinate c2 remain distinct. Break-even ≈10.4207 is a reviewer diagnostic, not a certified result. The paper is conditional on unrefereed Norton v3, AI-written and AI-checked, with no human referee and no Lean proof.
