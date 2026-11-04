# Directed point evaluation of the finite rectangle family

Candidate and unrefereed; verifier separately written (same agent).
Credit Kesten, Jensen, Enting and Vít Plánočka for the bridge, finite-lattice
and credited production constructions. This appendix uses the component
rules and normalization proof in PROOF_RECTANGLE.md.

Fix transverse range W, spans s through S, and interior crossing cap C.
At each completed interior column retain only an odd number of crossing
edges between 3 and C. The lower condition enforces irreducibility. During
a column, already fixed right edges cannot disappear; rejecting a partial
column with more than C such edges loses no eventual accepted bridge.
The terminal column prohibits right edges and introduces the other endpoint.
Consequently the finite-state histories count exactly the specified family.
Subtracting the count in rows 1 through W from that in rows 0 through W
retains exactly those bridges with minimum transverse coordinate zero.
Translation gives a bijection with normalized bridges of range at most W.
No length truncation occurs. A bridge of span h has at most h(W+1)+1
vertices, including its start, so its length is at most N=S(W+1).

Evaluate at x=51081913/2^27 and scale D=2^96. Each state carries a lower and
upper integer numerator. Initially each possible starting edge has exact
numerator 51081913*2^69. For a transition adding k edges, k in {0,1,2},
multiply by x^k and round down or up respectively. Add all contributions
with checked integer addition. Induction over the finite stage sequence
encloses every state and completion sum. With A counting the full frame
and B the frame without its bottom row, the normalized lower numerator is
max(0,A_lower-B_upper), and its upper numerator is A_upper-B_lower.

The separately written scalar arithmetic avoids the producer's three-limb
product. For k>0 set q=51081913^k, r=27k, and write a=2^r u+v with
0<=v<2^r. Then

    floor(a*q/2^r) = u*q + floor(v*q/2^r).

The remainder is (v*q) mod 2^r. Adding one precisely when it is nonzero
gives the ceiling. The executable checks a<2^107. Since q<2^r, u*q<2^107;
also v*q<2^(2r)<=2^108. Both products and their sum fit unsigned128 bits.
Every accumulation separately rejects overflow. Thus an accepted execution
uses exact integers and valid directed rounding throughout.

The requested evaluation point t=400/1051 is slightly larger than x.
Coefficient nonnegativity gives F(t)>=F(x). For an upper failure test,
each length n<=N obeys t^n=x^n(t/x)^n<=x^n(t/x)^N, whence

    F(t) <= F_upper(x)*(t/x)^N.

This correction is computed as an exact rational. If an attributed baseline
polynomial plus this corrected upper value is below one, no supplement
from this specified finite family can fill that baseline deficit. This
conclusion is limited to the stated family and baseline premise and gives
no upper bound on the connective constant. It does not verify the baseline's
original enumeration. A producer point diagnostic alone is never accepted:
freeze its full output and sources before a complete fresh native replay,
bind the result hashes, and require the exact expected corruption rejections.
