# Claim-to-checker map for the frozen candidate

Packet: [frozen/c22b_7090412_rational](README.md).
Candidate and unrefereed. All verification code is separately written
(same agent). This map distinguishes finite arithmetic checks from the
analytic reductions and classical theorems in the written proof.
No novelty judgment is made. Read [ERRATA.md](ERRATA.md) for two prose
corrections; the original packet bytes and certificate inputs are unchanged.

| Claim | Frozen input and checker | Written justification |
| --- | --- | --- |
| Exact spatial realization | CONSTRUCTION.json; verify.py | PROOF.md Sections 1 and 4 give every body, connector, vertical segment, and semicircle formula, parameter domain, join, and orientation. |
| Complete body distance and curvature checks | covers/body_*.json.gz, covers/curvature_*.json.gz; verify.py | Section 2 reduces the infinite extension to the complete phase rectangles, short-arc cases, and vertical tails. A common screw isometry treats both bundles; a separate axis-distance inequality treats opposite bundles. |
| Complete cap and interface checks | 16 interface covers and two lower_cap_pair covers; verify.py | Section 4 supplies the analytical cap cases and tail reductions. Appendix E counts all 210 unordered piece-pair types. No numerical minimum or omitted local-search basin is an input. |
| Embeddedness and global thickness | The preceding cover/scalar checks | The short-arc chord projection excludes coincident distinct curve parameters and short doubly critical chords. CKS Lemmas 1 and 2 then give the stated thickness/reach conclusion for the embedded C1,1 closed curve. Shared analytic representations of an identified piece endpoint are one domain point, not a self-intersection. |
| Physical braid action | projection.json.gz; verify_projection.py | Section 5 and Appendix A explain inverse-height monotonicity, four zero functions covering all six strand pairs, certified root ordering, signs, and lane exchanges. Appendix H aligns cap and body frames by a fixed-endpoint braid isotopy. |
| Exact rational closing period | N=276/5 and core_periods=5; verify.py, verify_projection.py, verify_finite.py | Section 1 and Appendix I prove phase return after Q=5 axis turns and P=276 minor periods; P supplies the full-block inverse-height right-hand side, length-period count, and crossing slope. The wrong-period control requires E_PERIODS. |
| Exact speed and body coefficient | length_identity.json; verify_length_identity.py | Section 3 and Appendix B derive the velocity components, compare coefficients in Q(eta), and integrate over exactly276 complete minor periods per block using Cauchy–Schwarz. No quadrature estimate is assumed. |
| Global thickness margin for every n | margin.json; verify_margin.py and verify.py | Appendix C proves the transform is a homothety of every finite closed curve, including H_n and all cap translations. All 22 covers are recomputed on the transformed artifact. |
| Knot type and exact crossing number for all n | Actual body action plus checked cap algebra; diagrams.json | The nilpotent identity gives M^n exactly. Rationality follows from starting with a trivial two-arc tangle and adjoining boundary half twists. Kauffman–Lambropoulou classification identifies T(2,1104n+3), up to mirror. The reduced-alternating crossing-minimality theorem supplies C=1104n+3. |
| Finite n=1 witness | finite_witness.json; verify_finite.py | Appendix D uses the all-n geometry/topology proof and checks the standard alternating diagram of T(2,1107). The three auxiliary diagrams do not substitute for an all-n argument. |
| Final upper bound | ROP_BOUND.json; verify_ropelength.py | Appendix F applies Rop_min(type)<=L/tau, divides by the positive certified margin, and takes n to infinity. This yields 1772602767903/250000000000<1772603/250000. |
| Thickness upper bound of this specified family | CONTACT.json; verify_contact.py | Appendix G places the selected point pair on the last body period of every n>=1 curve. The tangent-circle limit gives an upper bound on thickness, not a knot-type optimality statement. |
| Frozen bytes and cross-component bindings | MANIFEST.json, SHA256SUMS; verify_manifest.py and verify_all.py | The reported manifest SHA256 anchors the byte set. The global entrypoint checks every mathematical component and binds the checked physical body action and the standard finite diagrams to the construction. |

The first frozen replay recomputes 146198 original-geometry leaves and
146198 transformed-geometry leaves, plus all 33800 projection leaves and
24849 inverse brackets. Construction parameters and certificate interval endpoints are exact rationals;
all required transcendental operations are enclosed by 220-bit Arb.
Only display fields are floating point.

The 108 corruption controls are grouped as follows:

| Component | Controls |
| --- | ---: |
| Geometry, period binding and coverage | 31 |
| Physical projection | 15 |
| Exact speed identity | 8 |
| Standard diagram combinatorics | 7 |
| Global margin | 6 |
| Finite witness | 8 |
| Split-radius cap pairs | 8 |
| Exact ropelength corollary | 12 |
| Selected contact | 8 |
| File-set and byte integrity | 4 |
| Binding to the correct finite knot diagrams | 1 |
| Total | 108 |

Every control reports both its expected and actual rejection code. The
consistently rebound false-margin control must fail E_DISTANCE_LEAF;
it does not rely on a stale construction digest. The nested reserved-name
extra-file control must fail E_FILE_SET. Both complete environment replays
and all these controls pass; this is same-agent arithmetic verification,
not external referee review or machine-formalized mathematics.

The [cap illustration](figures/caps.png) and
[selected contact illustration](figures/selected_contact.png) are floating
point drawings for reading the proof. Neither is a certificate.
