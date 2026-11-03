# R5 route: precise remaining completion obstruction

Candidate, unrefereed analysis. This is not a proof that R5<=49.

In the sharp accepted round-eight scalar system, N=50 forces normalized
minimum influence lambda=1 and eight derivative controls: for h<=7 the
ordinary budget is at most 197/4<50. The minimum-support theorem forces
four disjoint pair factors. With N=50 there would be 41 outside Y
coordinates, originally of local degree five. Restricting all eight
controls gives 16 active and 240 inactive assignments among 256.

The coordinatewise restriction inequality on Y requires summed section
potential at least 256*(41/32)=328. Each inactive Boolean quartic has
potential at most 22/16, for a total at most 240*(22/16)=330. Total deficit
from that maximum is at most two. Every quartic potential is a multiple
of 1/16, so at most 32 inactive sections can have smaller potential;
at least 208 must attain 22/16.

Let Q(H) be the vector of homogeneous quartic Y coefficients in a section.
Each coefficient is affine in H, since the original function has degree
five, and vanishes whenever all four pairs are equal. Consequently

    Q = sum_(j=1)^4 (s_j-t_j) P_j / 2.

On the fully mismatched assignments, Q=sum epsilon_j P_j. Each section
is Boolean, hence ||Q||^2<=1. Averaging over the independent mismatch
signs gives sum ||P_j||^2<=1. Averaging over all controls therefore gives
E_H ||Q||^2<=1/2, or summed top Fourier energy at most 128.

If every potential-maximizing quartic were known to have top energy at
least 5/8, the 208 maximizing sections would contribute at least 130,
a contradiction. Thus a proved quartic statement of that strength would
exclude N=50 and give R5<=49. A potential maximizer cannot have a coordinate of local degree below four:
the CHS simultaneous-duplication argument would add positive selector
potential while preserving all old weights and degree at most four. Hence
such a maximizer has exactly 22 coordinates, all of local degree four.
Proving the stated energy envelope for 22-variable quartics is sufficient.
No unrestricted quartic classification or such energy theorem is supplied
by the input. The cubic catalogue's
energy envelope does not imply it. Assuming it would be an unsupported
step. This route ends at a sharply specified structural question; the
successful bound in this job instead comes from R6.
