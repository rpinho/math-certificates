# A finite final span, using full upper bounds only at smaller spans

Candidate and unrefereed. Verifier: separately written (same agent).
Credit Kesten, Jensen, Enting, Numaro and Vít Plánočka as detailed in
CREDITS.md. This appendix specifies the final-span mode used by this
packet. Apply sections5–6 of PROOF_FINITE_STRIP.md only through span17;
the following argument replaces the span18 full-width upper step.
The local graph rules, exact directed forward arithmetic, finite-family
coefficient definition and concatenation proof are unchanged.

For each h=1,...,17, the complete fresh frozen replay supplies

    b_h <= B_h <= U_h,   alpha_h <= A_h <= beta_h,

where B_h and A_h are the full all-transverse-range bridge and irreducible
sums at z0=51081913/2^27, respectively. These sums are finite by their
exact nonnegative upper potentials. The same proof also gives
alpha_h <= I_h^[w_h], the finite irreducible sum with range<=w_h-1.

Choose any finite positive width w18. Let B18^[w18] count all span18
bridges of transverse range<=w18-1, and I18^[w18] its irreducible subset.
Both are finite polynomials: there are at most18*w18+1 vertices, including
the unique starting vertex. The finite forward sweep gives exact rational
bounds b18<=B18^[w18]<=u18. No infinite-range tail bound at span18 is
assumed or needed. In this mode num_tail=0 is an explicit unused marker,
not a claim that an infinite omitted tail is zero.

Every reducible bridge counted by B18^[w18] has a unique first
irreducible factor of span j in{1,...,17}, followed by a bridge of
span18-j. Its length weight factors multiplicatively. This gives an
injection, preserving weights, into the disjoint union of pairs counted
by A_j*B_(18-j). All these factors have smaller spans and finite full
sums. Consequently its reducible sub-sum satisfies

    R18^[w18] <= sum_(j=1)^17 A_j*B_(18-j)
               <= sum_(j=1)^17 beta_j*U_(18-j) = C.

Subtracting this upper bound from the finite bridge lower bound gives

    alpha18=max(0,b18-C) <= I18^[w18].

This step uses only smaller-span upper bounds. It makes no assertion
that the full A18 or B18 exists as a finite numerical sum, and it does
not produce or use beta18 as a full irreducible upper bound. A finite
upper bound I18^[w18]<=u18 may be retained as a diagnostic.

For the finite family consisting of all the chosen span-specific classes,
its exact nonnegative coefficients a_n therefore satisfy

    sum_n a_n*z0^n >= sum_(h=1)^17 alpha_h + alpha18.

Acceptance requires the last exact rational expression to be at least1.
The finite-family concatenation and unique-factor argument of the main
proof then gives mu>=1/z0>=1051/400. The expanded integer coefficient
vector remains unmaterialized; the family and its coefficients are
specified exactly and its value is enclosed by exact rational arithmetic.

The producer may choose w18 adaptively. Using its already-certified
smaller-span search brackets, it forms C_search and P17_search, and
an exact integer threshold

    T=ceil(2^96*(C_search+1-P17_search+1/1000000)).

It stops only after a whole column when its finite lower numerator is
at least T. This is a search rule, not final acceptance. The complete
span18 input, chosen w18, finite verifier source and this proof are
frozen before its fresh native replay. Final verification separately
assembles the exact lower expression from the separately written
(same agent) replays at every span. If that expression is below1, the
candidate is rejected regardless of the search threshold. The extra
search margin protects against slightly different valid tail enclosures;
no decimal tolerance enters the final comparison.

The finite verifier is derived from the separately written component-rule
verifier by omitting its upper-potential call and marking the output mode
FINITE_LAST_SPAN_LOWER_ONLY. Its graph closure and both complete directed
finite forward planes are recomputed from scratch at every prescribed
column. The producer retains Plánočka's credited case-table graph with
its validated destination accumulation. Small fixed-column controls must
match the unmodified public finite numerators, and an adaptive first-crossing
control must match a complete finite verifier replay before the large run.
