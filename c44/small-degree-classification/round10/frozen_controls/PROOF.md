# Auxiliary controls — candidate, unrefereed

Start with the four signed minimum quadratic gates from the retained
46-variable degree-five seed. Their supports partition the eight-control
cube. Merge gates zero and two by addition. Their supports are disjoint,
so the sum is ternary, and it and the other two gates still partition the
cube. The merged gate has eight distinct quadratic Fourier masks and
uses six controls; all three gates have degree two. Attach a disjoint Xi3
on ten variables to each gate. The resulting Boolean function has degree
five, six relevant controls and thirty payload inputs, hence 36 variables
and lift 38/32=19/16. This is a positive control, not a lower improvement.

The ten-gate bank consists of the four old gates and all six pair merges.
In any partition using a merge, at most three gates can be selected, since
each covers the support of at least two of the original four. Each payload
has ten variables and there are at most six relevant controls, so count
and potential numerator are at most 36. The displayed seed attains 36.
The two graph programs must find a partition at threshold 36 and fail at
37 on this frozen bank. Two independent full-polynomial/structured seed
verifiers check the actual 36-variable seed.

Both cubic catalogue scans, their exact input hash, the half-support proof
using those properties and rejection controls are retained here as auxiliary
exploratory evidence. They supply no accepted R5 cap. Catalogue completeness
remains the published premise already stated in the inherited proof.
