# Exact controls and the next obstruction

Candidate, unrefereed. verify_controls.py independently uses rational XOR
convolution of sparse Fourier polynomials. f²=1 certifies sign Booleanity;
A³=A certifies ternary values. It checks real degree, relevant-variable
count, Parseval energy and every relevant partial energy on each witness.

The CHS/Shinkar–Tal family Xi1=x,
Xi_d=(s+t)Xi_(d-1)(X)/2+(s-t)Xi_(d-1)(Y)/2 with disjoint copies is checked
through degree six: 1,4,10,22,46,94 variables. The written induction in
PROOF.md proves its full infinite family and C44>=3/2.

For the sharp second-weight control examples, take coordinates a,b,c,d,e,f
and the ternary quadratic

    A2=(bc+ad-bd-ec-af+ef)/4.

It is the half-difference of the two Boolean quadratics
(ac+bc+ad-bd)/2 and (ac+ec+af-ef)/2. Direct rational convolution checks
A2³=A2, degree two, six controls and E A2²=3/8. For k>=2 multiply by k-2
fresh pair factors (s+t)/2. This preserves ternary values, increases degree
by k-2 and control count by 2(k-2), and multiplies energy by 2^{-(k-2)}.
Thus degree-k examples have lambda=2^k E A_k²=3/2 and exactly 2k+2
controls. The verifier checks k=2,3,4,5 explicitly. In particular the
quartic ceiling ten and quintic ceiling twelve are attained by actual
ternary polynomials. They are not Boolean functions with R5=51 or R6=110.

At d=5, c4=11/8, the scalar point (N,lambda,h)=(51,3/2,10) satisfies
both count budgets: the control budget is 411/8=51.375, and the influence
budget is 160/3>51. At d=6, c5=51/32, the scalar point (110,3/2,12)
has control budget 3543/32=110.71875 and influence budget 128>110.
Their budgets are exact. Thus neither improving the control count below
ten/twelve nor merely optimizing the present scalar constraints can
establish the desired exact counts 46/94. The missing condition is that
an extremal signed derivative must admit a degree-five/six Boolean
completion with many relevant variables, and that all its other
partials must be simultaneously compatible.

A promising next input is a universal quartic energy envelope refining
D(g)<=11/8 as a function of its top Fourier energy. The cubic catalogue
supplies such an envelope at degree three; the unrestricted quartic
catalogue is missing. Assuming an unproved quartic envelope is not part
of this certificate. Likewise no binary affine normal form is used to
infer short real-coordinate controls.

control_integer_gap.cpp checks every truth table with values
{-2,-1,0,1,2} on one through three inputs, using integer bit interpolation
for actual degree. It checks the minimum L2 energy and absence of energy
strictly between that minimum and 3/2 times it. The 391,275 tables are
finite corroboration of BW_GAP_PROOF.md, not a proof of its universal
lattice/group premises.
