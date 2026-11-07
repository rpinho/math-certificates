# Independent mathematical referee of L064

The stated even-sphere argument survives this review, with the scope and
verification limits below. L064 and the common L063 proof were reviewed jointly.
No submitted implementation was imported or executed. The conclusion rests on
the mathematical argument, not on the number of passing certificates.

The journal's p.21 Proposition 4.1 includes integer Novikov coefficients in its
monotone split-generation statement; Remark 4.2 asks about ordinary generation.
Section 3.1 permits arbitrary real exponents. Section 5's field restriction
does not supply integral module formality. There is no published numerical cone
benchmark here. The journal and arXiv identify Mohammed Abouzaid and Luís Diogo.
[Primary journal PDF](https://www.diva-portal.org/smash/get/diva2:1783421/FULLTEXT01.pdf),
[arXiv](https://arxiv.org/abs/2011.13478).

The mathematical addition relative to that paper is ordinary fibre generation
for even n over K_Z, within finite unfiltered twisted complexes. Classical
algebra supplies the other inputs: [Farber–Schütz Lemma 1](https://arxiv.org/pdf/0807.3240)
and [Seshadri 1958, pp.456–458](https://pmc.ncbi.nlm.nih.gov/articles/PMC335443/).
I read the original Seshadri scans, not only the submitted attribution or
[Endo's p.339 account](https://www.jstage.jst.go.jp/article/jmath1948/15/3/15_3_339/_pdf).
No novelty or priority conclusion follows; bounded coverage is in PRIOR_ART.md.

An independent ring check is possible directly. Let R be the series ring with
integer coefficients, support bounded below and finite below every bound.
Its leading-term product makes it a domain. For a nonzero ideal I choose f
whose positive leading coefficient m is least possible among I's nonzero
elements; normalize its leading exponent to zero using an invertible monomial.
For any g in I, integer division of its leading coefficient by m and one
monomial subtraction would produce a smaller positive leading coefficient if
there were a nonzero remainder. Thus m divides that leading coefficient.
Repeat cancellation. Every finite residual remains in I, so every subsequent
division remains integral. The quotient is a permitted series: the positive
support of f has a positive minimum gap and is locally finite; its additive
semigroup, added to the locally finite support of g, is locally finite below
each bound. The cancellations therefore escape every finite exponent bound.
They yield g=fq in R. Hence I=(f). This also explains why the full exponent
ring matters. Reversing exponents identifies it with Farber–Schütz's Nov.
The nonnegative-valuation subring is a different ring.

For the parity step, take A=R[u], |u| odd, with unrestricted associative square,
and S=R[t], t=u². A graded projective P is a graded retract of finite graded
free A-modules. Each P_i is consequently finite projective over S and is
S-free by Seshadri. The odd action maps U_i are injective; after inverting t
they are isomorphisms, so their free ranks agree. The graded splitting descends
modulo u. Its parity-one component makes C=coker(U_0) a finite R-projective,
thus R-free; this is the crucial hypothesis missing from a generic assertion
about arbitrary matrix factorizations.

The quotient S^r -> C factors through evaluation at t=0. Its resulting
surjection R^r -> R^c can be put into [I_c 0] by constant invertible bases:
the kernel is free and the sequence splits over the PID. Thus its S-kernel
has basis t e_1,...,t e_c,e_(c+1),...,e_r. Pull these vectors back along U_0.
They are a basis of P_0, and the relation U_1 U_0=tI forces the complementary
diagonal entries of U_1. These pairs are precisely homogeneous copies of A
and A[1]. No ungraded basis is presumed homogeneous, and 2 is never inverted.

Here is the categorical check. A polynomial ring over a PID is Noetherian
and has global dimension at most two. For example, the injective relative
sequence with map u tensor m - 1 tensor um expresses any module as the
cokernel of two induced R-modules of projective dimension at most one.
For a graded module, the parity-preserving component of an ungraded section
is still A-linear and still a section; this does not require averaging by 2.

For an object X in the paper's split-generated category, H(F,X) is finite over
A: finite generation is closed under triangles by Noetherianity and under
retracts. Choose finitely many homogeneous generators and represent them by
closed maps from shifts of F. For the triangle K_1 -> P_0 -> X, surjectivity
in both parities makes H(F,K_1) the actual kernel. Repeat once. The second
kernel is graded projective, hence graded free by the preceding argument.
Represent its homogeneous basis by P_2 -> K_2. The cone Z has H(F,Z)=0.
Since Z is split-generated, closing Hom(-,Z)-vanishing under triangles and
retracts gives Hom(Z,Z)=0. Thus P_2 -> K_2 is an isomorphism. Reverse the
two triangles to put X in the ordinary envelope of F.

All K_i and cones can be taken in the original finite Tw category, because X
is an original object; passing to a split closure is needed only for the
detection argument. Its fully faithful inclusion reflects the resulting
isomorphisms. This avoids installing new geometric local-system fibres or
assuming integral module formality. Finitely many upper-triangular cone arrows
give finitely many insertions in each twisted operation. Existing object-level
bounding-cochain convergence is an input of the given category. This is not a
claim about infinite, filtered or curved completions, or a reconstruction of
the published geometric split-generation proof.

The independent computation was run only on the authorized ref pod:

```
python3 _codex/friends_podsh.py ref send_check.sh 90
python3 _codex/friends_podsh.py ref poll_check.sh 90
```

send_check.sh sends referee_check.py plus the submitted certificate as data,
then launches launch_check.sh under nohup and nice 10. The program uses only
standard-library sparse integer arithmetic in Z[T,T^-1,u], substituting t=u².
It checks both inverses, both action products, homogeneous normal forms,
quotient annihilation and an integral right inverse to each nonempty quotient
map. All 28 cases pass. Five own corruptions fail. No inference about arbitrary
infinite Novikov coefficients is drawn from Laurent-polynomial computation.

A separate exhaustive control enumerated all 65,536 pairs of 2x2 matrices
with entries of degree at most one in F_2[t]. Exactly 48 satisfy both products
equal to tI: 6,36,6 by cokernel dimension 0,1,2. Every one has the expected
Smith type. This tests inputs not constructed by starting with the normal form,
but remains only a small characteristic-two control. There were also 300
sampled integral Koszul relations for (2,u). The universal control is algebraic:
(2,u) is nonprincipal since a common divisor of 2 and u is a unit, while the
quotient modulo (2,u) is nonzero. Its second Koszul kernel is free. Over Q[u]
the quotient disappears; modulo 2 the specialized Koszul complex has nonzero
H_1. A field-only one-syzygy shortcut would therefore change the problem.
The code's fixed nonunit flag records that argument; it is not an algorithm
for deciding units in arbitrary infinite series.

There is no statistical hold-out. Every submitted matrix comes with an
explicit conjugacy to a desired canonical block; their passing is expected
and cannot validate the universal theorem. The author's strongest reply is
correct: those matrices were advertised as arithmetic controls, and the proof
above carries the claim. No additional numerical or geometric improvement is
certified by the count 28.

The result JSON was transcribed from captured stdout into
referee_results_stdout.json; no byte-identical retrieval is claimed.
The raw pod result is referee_results.json,
whose certificate hash matches the sealed manifest. Source bodies and logs
remain in /workspace/ref_luis_L064. Later the shared pod ran out of disk and
even helper temporary scripts failed, preventing raw-file retrieval and the
planned extra source collector. No one's files were removed and no pod state
was changed. Source PID 928222 and test PID 928454 had both already disappeared
in subsequent ps checks; no scientific worker was started after those checks.

NEXT BAR: combine the linked arguments into one self-contained even-sphere
theorem with the ring identification and the finite-Tw lifting written out.
