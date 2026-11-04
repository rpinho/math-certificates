# Exact balanced-contact examples

Candidate/unrefereed diagnostic controls. The constructions use the retained
Fourier/contact setup of Pinho with Patankar's flux input, Wang's coefficient
approach and Wikström's moment integration. No additional C68 bound is claimed.

The frozen data specify domain unit vectors z_i, image unit directions v_i,
and positive probability weights lambda_i with sum lambda_i*v_i=0 exactly.
For each domain pair compute the rational Fourier profile

 F_ij=(1-Re(z_i*conj(z_j)))/2-(3/25)*(1-Re((z_i*conj(z_j))²)).

Set u=min_(i<j) 2F_ij/(1-v_i dot v_j)>0 and h²=1+D*u, D=100000.
Choose a hyperbolic circle about zero with cosh radius h, and put contacts
on it in the directions v_i. Its cosine-rule distances are exactly

 cosh d(p_i,p_j)=1+D*u*(1-v_i dot v_j)<=1+2D*F_ij.

Thus these are balanced geometric contacts obeying every retained Fourier
pair constraint. Their disk is minimal: for any other center x, the average
of cosh d(x,p_i) is h*cosh d(x,0)>=h. Any enclosing radius is consequently
at least arcosh h. This argument also proves each contact-row average is h².

The checker recomputes all those identities, the first/second moments,
the exact projected second moment q0, and the improved radius inequality.
It uses rational arithmetic for the geometry and Arb only for sqrt(|m1|²)
in J=a(q0+a)/(1+a). No search or acceptance code is imported.

The two-point case has equal masses at opposite domain/image points. Here
m1=0,m2=1,S=J=0,u=1; the enclosing bound is exactly saturated and the
singular scalar weight is (12/25)sin²theta. The three-point case uses image
directions 1,(-3+4i)/5,(-3-4i)/5 and weights 3/8,5/16,5/16. Its domain
points are 1,-1,(-399+40i)/401. The checker requires J>S in that case, so
it exhibits an actual strengthening of the geometric floor with positive
balanced weights, while checking all pair constraints.

These controls do not assert that a holomorphic annular map interpolates
the chosen contacts. They test the exact geometric hypotheses used in the
row reduction. certificates/contact-configurations.json and its verifier
are retained separately from the successful bound certificate.
