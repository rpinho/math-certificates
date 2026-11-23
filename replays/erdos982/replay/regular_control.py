"""Construct and check the exact regular-polygon SAT witness at the bound."""
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

from run_case import dimacs

n = int(sys.argv[1])
folder = Path(sys.argv[2])
edges = list(combinations(range(n),2))
rank = {(a,b):min(b-a,n-b+a) for a,b in edges}
values = [rank[e] < rank[f] for e,f in permutations(edges,2)]
seen = [set() for _ in range(n)]
for a,b in permutations(range(n),2):
    length = rank[min(a,b),max(a,b)]
    values.append(length not in seen[a])
    seen[a].add(length)
assert all(len(row) == n//2 for row in seen)
assignment = {index if value else -index for index,value in enumerate(values,1)}
clauses = dimacs(folder/"formula.cnf")
assert all(any(lit in assignment for lit in clause) for clause in clauses)
(folder/"regular_model.txt").write_text(" ".join(map(str, sorted(assignment,key=abs)))+"\n")
result_path = folder/"result.json"
result = json.loads(result_path.read_text())
result["solver_probe"] = result["verification"]
result["verification"] = "Exact regular polygon SAT witness checked against every canonical clause"
result_path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(f"n={n}, regular SAT witness: {len(assignment)} variables, {len(clauses)} clauses, K={n//2}")
