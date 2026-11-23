"""Construct and check a partial-preorder witness after omitting ASYM."""
from pathlib import Path

from encoder import Encoding
from run_case import dimacs

folder = Path("runs/n12-fan-no-ASYM")
n, k = 12, 5
encoder = Encoding(n,k)
clauses = dimacs(folder/"formula.cnf")
for lower in range(1,6):
    def rank(a,b):
        gap = min(abs(a-b),n-abs(a-b))
        return lower if gap == lower+1 else gap

    groups = [rank(a,b) for a,b in encoder.edges]
    minimum = groups[encoder.edge(0,1)]
    assignment = set()
    for left,group in enumerate(groups):
        for right,other in enumerate(groups):
            if left == right:
                continue
            literal = encoder.lt(left,right)
            # Declare all different nonminimum classes incomparable in the
            # non-strict preorder. The minimum class precedes every class.
            truth = group != other and other != minimum
            assignment.add(literal if truth else -literal)
    for a in range(n):
        seen = set()
        for b in range(n):
            if a != b:
                gap = rank(a,b)
                literal = encoder.rep(a,b)
                assignment.add(literal if gap not in seen else -literal)
                seen.add(gap)
    failed = [i for i,clause in enumerate(clauses,1)
              if all(literal not in assignment for literal in clause)]
    print(f"merged classes {lower},{lower+1}: {len(failed)} failed clauses")
    if not failed:
        assert len(assignment) == encoder.variables
        output = folder/"constructed_model.txt"
        output.write_text(" ".join(map(str,sorted(assignment,key=abs)))+"\n")
        print(f"SAT: full witness satisfies all {len(clauses)} clauses")
        break
else:
    raise RuntimeError("no constructed witness")
