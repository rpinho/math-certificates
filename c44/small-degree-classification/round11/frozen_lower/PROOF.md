# Lower construction controls — candidate, unrefereed

No asymptotic lower bound above3/2 was found. This packet certifies three
known-count degree5/6 seeds and23 successful cofactor splittings; it makes
no claim that the resulting functions are outside previously known families.
The graph proposer and its group completeness do not enter the proof.

The Xi recursion starts at one sign variable. Given disjoint sign Boolean
functions g,h of degree d on n inputs each, set

    F=(s+t)g/2+(s-t)h/2.

For every sign choice s,t exactly one coefficient is zero and the other
is a sign, so F is Boolean. Its Fourier supports from the two payloads
are disjoint; degree is d+1 and all2n+2 inputs are relevant. Thus
L_1=1,L_(d+1)=2L_d+2, giving L_d=3*2^(d-1)-2. Iterating the same recursion
from a degree-d,n-input seed gives2^t(n+2)-2 inputs at degree d+t, so
C44>=(n+2)/2^d. The supplied46-input degree-five and94-input degree-six
controls both give3/2. Exact Booleanity, degrees, counts and lifts are
verified from their full sparse polynomials by both implementations.

For a general sign Boolean f=x_b U(X)+V(X), f^2=1 implies UV=0 and
U^2+V^2=1. Let U' be a signed coordinate permutation of U with (U')^2=U^2.
Then U'V=0 because their supports are disjoint: at V!=0, U^2=0.
Put G=(U+U')/2,H=(U-U')/2. We have GH=0,G^2+H^2=U^2 and VG=VH=0.
For a new independent z,

    f_new=V+x_b G+zH

has square1 exactly. Its degree is at most deg f since U,U' have degree
at most deg f-1. When U' is neither U nor -U, both selectors occur.
Every old X input is retained: U=G+H, and Fourier masks carrying different
selectors cannot cancel. Therefore the relevant count rises by one.

The frozen chain starts at Xi4 times one fresh sign, degree5,count23.
Every record gives an exact signed variable permutation fixing its split
coordinate. All23 companion-square identities and resulting Boolean
polynomials are checked in both implementations. The final count is46,
with asymptotic lift3/2. A uses ordered integer XOR products and full
Boolean squares at every step. B uses unordered autocorrelations,
polarization for cofactor products, and separately reconstructs all maps.
Neither imports the proposer or the other verifier. Corruption controls
must reject altered coefficients, denominator, degree, relevance, lift,
permutation and chain metadata before the packet is accepted.

The much larger failed symmetry searches remain exploratory finite-family
outcomes. No universal nonexistence conclusion or optimality of3/2 follows.
