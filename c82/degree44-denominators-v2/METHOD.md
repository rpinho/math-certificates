# Method

This continues the search in `../degree44-denominators/METHOD.md` from its saved library and LP dual. Column generation ran at degree 44 with numerator regeneration against the moved dual, and a side lane at degrees 60 to 104.

The degree 44 lane tested 73,680 polynomials from 24,178 starts and found 4 distinct admissible denominator candidates. The higher-degree lane tested 9,176 polynomials and found none. That doesn't rule out higher degrees.

The search stopped after 3.4 hours under a rule set in advance, because its last two checkpoints together gained less than 2e-6. It says nothing about optimality.

Nonmonic denominators were checked and dropped. The upper-bound argument seems to survive them, but a leading coefficient a costs about 0.984 log|a| in reduced cost, 0.682 for a = 2, and the best matched lead-2 lattice result at degree 44 had reduced cost +0.689. The numbers are in `receipts/nonmonic-cost-check.json`.
