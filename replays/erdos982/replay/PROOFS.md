# Distance-order encoding

Let vertices be indexed in cyclic boundary order. An edge is an unordered pair of indices, including chords. Write \(xy\) for its length. Each ordered pair of different edges \(e,f\) has one Boolean \(L(e,f)\) with intended meaning \(e<f\). Define \(e\le f\) as \(\neg L(f,e)\) for different edges and define equality by two false strict comparisons. Squared distances give the same comparisons as distances. Every occurrence of an edge uses the same variables.

## Domain and deletion

A strictly convex polygon is a convex polygon with all internal angles strictly less than \(\pi\). Its vertices are extreme points of the hull. A boundary vertex that is not extreme lies in the relative interior of a hull edge and has straight angle. Conversely, if all the given points are extreme, the hull boundary in cyclic order is a convex polygon with a strict turn at each vertex. Three distinct collinear points would put the middle one on a segment of the other two. Thus the vertices of a strictly convex polygon are exactly points in convex position with no three collinear, ordered along their hull. Here convex position means each point is extreme.

Any subset of at least three vertices remains in strict convex position. If a point were in the convex hull of a subset of the other points, it would also be in the convex hull of all the other points. If \(n=2k+1\), delete one vertex, apply the bound for \(2k\), and restore the vertex. Restoring it cannot decrease a surviving vertex's distinct-distance count.

## Clause families

### ASYM and TRANS

ASYM forbids both strict comparisons between two edges from holding, making the induced non-strict comparison total. TRANS requires \((e\le f\ \land\ f\le g)\Rightarrow e\le g\) for each ordered triple of distinct edges. In literals this is \(L(f,e)\lor L(g,f)\lor \neg L(g,e)\). Reflexivity and ASYM cover triples with repeats. The resulting relation is a total preorder and its tie classes are equivalence classes. Every true distance list gives such a preorder.

### FIRST and BOUND

At a center \(v\), sort its other vertices by label. For each row edge \(e\), introduce \(R(e,v)\) for the assertion that no earlier edge \(f\) ties \(e\). For every earlier \(f\) add \(\neg R\lor L(e,f)\lor L(f,e)\). In reverse, for each choice of one comparison direction per earlier edge, add a clause with \(R\) and the negation of every chosen comparison. When every earlier edge differs, choose the true direction for each to see that the corresponding clause forces \(R\). When there is a tie, the corresponding forward clause forces \(\neg R\) and every reverse clause has a true negated comparison for the tie. In the empty prefix this produces a unit \(R\).

BOUND adds a disjunction of the negated representative variables for each choice of \(K+1\) row entries. FIRST marks exactly one representative per distance class. Thus BOUND is equivalent to at most \(K\) distinct incident distances.

### BISECTOR

For four distinct vertices \(a,b,c,d\) in cyclic order, require \(ab<bd\) or \(cd<ac\). In the quadrilateral, the perpendicular bisector of \(ad\) separates \(a,d\), so it crosses the relative interior of \(ad\). It intersects the convex quadrilateral in a segment. The segment endpoints are that crossing and exactly one crossing of the chain \(a,b,c,d\). The line cannot contain a hull edge because a supporting line cannot separate \(a,d\). On the chain the distance comparison therefore goes from strictly closer to \(a\), through at most one equality vertex, to strictly closer to \(d\). If \(b\) is at or past that crossing, \(c\) is strictly closer to \(d\).

### CROSS

In a convex quadrilateral \(a,b,c,d\), let \(q\) be the intersection of \(ac,bd\). The strict triangle inequalities in \(aqb,cqd\) give \(ac+bd>ab+cd\), and those in \(aqd,bqc\) give \(ac+bd>ad+bc\). The triangles are nondegenerate by strict convexity and the interior crossing. For each opposite side pair and each assignment of its two members to the two diagonals, one diagonal is strictly greater than its assigned side. Otherwise summing the two non-strict comparisons contradicts the sum inequality. These four clauses equal the four cyclic BISECTOR clauses over the same vertices.

### CAP

For cyclic \(a,b,c,d\), if \(ab=ad\) and \(ac\le ab\), require both \(bc<bd\) and \(cd<bd\). After a similarity and possibly reflection, use \(b=(-1,0)\), \(d=(1,0)\), \(a=(0,-h)\), \(c=(u,v)\) with \(h,v>0\). The diagonals place \(a,c\) on opposite sides of \(bd\). The radius comparison gives \(u^2+v^2+2hv\le1\), so \(u^2+v^2<1\). The triangle inequality gives distances from \(c\) to \(b,d\) strictly less than 2. Encode each implication as the disjunction of \(L(ab,ad),L(ad,ab),L(ab,ac)\) and the appropriate conclusion literal.

### SYM

Require \(01\le i(i+1\bmod n)\) for each other boundary edge. The unbroken constraints are invariant on the edge-order projection under rotations. They are also invariant under reversal, which exchanges the two directions of each chain and the two outer FAN sectors. FIRST can choose different representatives after relabeling, so recompute its unique auxiliary lift. BOUND is unchanged because it depends only on the number of representatives. Rotate a minimum boundary edge to \(01\). This gives a model of the broken formula from every model of the unbroken formula. The brute-force check enumerates all projected boundary total preorders through \(n=8\), which include the boundary restriction of every unbroken model at any \(K\).

### FAN extension

At vertex \(v\), choose four distinct other vertices \(a,b,c,d\) in their order along the cyclic chain after \(v\). The rays occur in the same order within the angle at \(v\). For example, orient the polygon counterclockwise and fix the direction of the first boundary edge. The signed areas of cyclic triples \((v,x,y)\) are positive, so the ray angles are strictly ordered within the wedge of width less than \(\pi\). The sum of \(\angle avb,\angle bvc,\angle cvd\) is \(\angle avd<\pi\).

In a nondegenerate triangle, if an angle has a weakly largest opposite side, that angle is weakly largest and at least \(\pi/3\). Hence at least one of the three angles at \(v\) has an opposite side strictly shorter than one of the two radii bounding the angle. The FAN clause is the six-literal disjunction of \(L(xy,vx),L(xy,vy)\) for \((x,y)=(a,b),(b,c),(c,d)\). Its test premise is that both outer sectors have weakly largest opposite sides. Its conclusion is that the middle sector does not.

## DIMACS convention

Number edges from zero in lexicographic order on endpoint pairs \(i<j\). For two different edge numbers \(e,f\) in an \(M\)-edge instance, set \(L(e,f)=1+e(M-1)+f-[f>e]\). For the row at \(v\) and other endpoint \(w\), set \(R(vw,v)=1+M(M-1)+v(n-1)+w-[w>v]\).

Generate ASYM for unordered edge pairs, TRANS for ordered edge triples, and FIRST and BOUND for each row. Iterate increasing quadruples and all four cyclic rotations for BISECTOR and CAP. Apply CROSS once per increasing quadruple. With FAN enabled, generate it for every increasing quintuple and each choice of center, starting the other vertices' cyclic list just after the center. Include SYM by default. Sort literals within each clause, deduplicate clauses, then sort clauses lexicographically by integer tuples. Emit the DIMACS header and each clause terminated by space and 0, using LF line endings. An ablation removes only the omitted family's contribution before deduplication.

A counterexample at order \(n\) supplies a model at \(K=\lfloor n/2\rfloor-1\), after symmetry normalization. A checked UNSAT proof at that setting proves the desired bound. A SAT assignment at that setting is an abstract candidate, whose geometric feasibility needs a separate proof. The regular \(n\)-gon supplies a geometric SAT control at \(K=\lfloor n/2\rfloor\), since distance classes correspond to minor step counts \(1,\ldots,\lfloor n/2\rfloor\). This is an exhaustive certificate problem, so a statistical holdout does not apply.

## Exact regular and concentric controls

For a regular \(m\)-gon the increasing chord-order key is the minor step \(s\). Indeed the squared distance is \(C_s=2-2\cos(2\pi s/m)\), and cosine is strictly decreasing on \([0,\pi]\). Restricting to a subset of vertices preserves the key and the extreme-point property.

For the concentric construction, use an even \(m\le28\) and alternate radii \(1,1+\epsilon\) over equally spaced directions, with \(\epsilon=1/10000\). In each vertex's radial direction, that vertex projects to at least 1, while any other vertex has projection less than 1. If \(\cos(2\pi/m)>0\), use the upper bound \((1+\epsilon)\cos(2\pi/m)<1\), since \(1-\cos(2\pi/m)=2\sin^2(\pi/m)\ge8/m^2\). If cosine is nonpositive, each other vertex projects to at most zero. Thus every vertex is exposed.

Squared distance is \(C_s r_i r_j+(r_i-r_j)^2\). The perturbation is at most \(4(2\epsilon+\epsilon^2)+\epsilon^2<16/m^2\). The sine difference formula gives consecutive \(C_s\) gaps of at least \(4\sin^2(\pi/m)\ge16/m^2\) over the allowed minor steps. At fixed \(s>0\), the three radius types are strictly ordered as inner, mixed and outer, since \(C_s\ge16/m^2>\epsilon\). Consequently the distance key is exactly \((s,\text{number of outer endpoints})\). The test uses subsets of these algebraic polygons.

For equilateral controls, a stored pair \((x,y)\) represents the Euclidean point \((x,\sqrt 3 y)\). The determinant signs are unchanged by this positive scaling, and squared distances are rational. The unit-circle parametrization in the stored coordinates is rational and the three fixed points form an equilateral triangle. Rational circle-fan, parabolic and perturbed parabolic cases use exact integer or rational orientation and distance comparisons. For the thin parabolas, the \(y\)-range divided by the \(x\)-range is at most \(2\cdot10^{-6}\).
