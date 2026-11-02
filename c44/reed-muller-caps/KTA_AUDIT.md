# KTA through 2.5: useful structure, and a table pitfall

Candidate, unrefereed research note. The accepted C44 bound uses the
below-two theorem and allows all energy-grid values at and above two.
It does not claim a full corrected transcription of the 1974/1976 KTA
classification. This distinction matters for the requested higher lever.

The primary articles are Kasami–Tokura (1970), DOI
10.1109/TIT.1970.1054545, and Kasami–Tokura–Azumi (1976),
DOI 10.1016/S0019-9958(76)90355-7. The latter classifies affine-equivalence
representatives below 2.5 times minimum weight. Its original PDF endpoint
and Elsevier API returned access denials during this job. OpenAlex confirms
the open-archive endpoint but supplies no alternative full-text location.
Attempts and their returned bodies are retained under sources/.

Carlet (2024), section 2, provides an explicit statement of the below-two
weights and two affine normal forms:
https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf .
Those normal forms are statements over F2, with arbitrary affine maps.
They do not preserve real degree or coordinate restriction cost. Formula
(1) in PROOF.md is the independently derived real-degree bridge used here.
It gives a safe h bound for every representative and every affine image
that actually admits the required ternary real polynomial.

Klein–Storme (2011), Lemma 1, explicitly recalls a KTA structural consequence:
for algebraic order r>=4 and weight strictly less than 2.5 times minimum,
the support is covered by two affine hyperplanes with independent linear
parts. Equivalently it misses their complementary codimension-two flat.
https://backoffice.biblio.ugent.be/download/2140143/2939938 .
This can guide a further structural attack. It does not itself provide
small coordinate controls: the affine forms may be long parities, and
restricting affine parity variables does not preserve the weighted
coordinate argument. No unsupported control reduction is inferred from it.

There is also a specific defect to avoid in a numerical use of the final
table. Denis Krotov's 2017 public discussion identifies a missing sequence
after equation (23), affecting codimension above seven:
https://www.researchgate.net/post/What_is_the_next_admissible_weight_of_codewords_of_the_Reed-Muller_code_RMm_r_after_2d_where_d2m-r_is_the_code_distance .
This is a primary author's technical report of a problem, not a theorem
premise in the accepted proof. We checked its mathematical example ourselves.
Let

    q=1+x1*x2+x3*x4+x5*x6+x7*x8+x9*x10  over F2.

For one pair, the sign (-1)^(xy) has expectation 1/2. Independence gives
E(-1)^q=-(1/2)^5=-1/32. Hence

    Pr[q=1]=(1-E(-1)^q)/2=33/64,
    wt(q)=528, min RM(2,10)=256, wt/min=33/16=2.0625.

The exact truth-table control also counts all 1024 values and gets 528.
Multiplying by two fresh bits gives an order-four word on twelve inputs
with the same weight and minimum weight 256. Thus simply restricting to
order at least four does not repair a proposed universal empty interval
(2,17/8). The example is not asserted to have real degree two/four or to
be a derivative witness. It suffices to refute that blanket coding gap.

The recent Lou–Wang arXiv:2610.36687 (27 Oct 2026), section 2, equation (5),
https://arxiv.org/html/2610.36687 , gives the codimension-seven specialization
below weight 320. Its first weight above twice minimum 128 is 272, i.e.
17/8 times minimum. That fixed-codimension statement is compatible with
the counterexample and cannot be silently extended to all n-r.
The 2026 paper's newer exclusions are not premises of this job's bound.

Consequence for this round: the full valid below-two spectrum improves
the new control method from 2.2108998048 (second gap alone) to
2.1974348818. The accepted arithmetic treats 2..2.5 conservatively, with
no weight exclusions there. A future corrected classification or a proof
of signed real-degree compatibility may improve it; the current packet
has not certified that further tightening. This explicitly records what
was and was not accomplished in the requested 2.5-range investigation.
