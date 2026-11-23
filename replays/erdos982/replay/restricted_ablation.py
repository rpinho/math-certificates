"""Seek a SAT witness for the no-ASYM ablation with a simple preorder restriction."""
from pathlib import Path

from encoder import Encoding
from jobrun import run
from run_case import CADICAL, dimacs

folder = Path("runs/n12-fan-no-ASYM")
n = 12
enc = Encoding(n,5)
original = folder/"formula.cnf"
clauses = dimacs(original)
sides = {enc.edge(i,(i+1)%n) for i in range(n)}
restrictions = []
for left in range(enc.m):
    for right in range(left+1,enc.m):
        lt, gt = enc.lt(left,right),enc.lt(right,left)
        if left in sides and right in sides:
            restrictions.extend([(-lt,),(-gt,)])
        elif left in sides:
            restrictions.extend([(lt,),(-gt,)])
        elif right in sides:
            restrictions.extend([(-lt,),(gt,)])
        else:
            restrictions.extend([(-lt,gt),(-gt,lt)])
instance = folder/"restricted.cnf"
log = folder/"restricted.log"
with original.open() as source, instance.open("w") as target:
    next(source)
    print("p cnf",enc.variables,len(clauses)+len(restrictions),file=target)
    for line in source:
        target.write(line)
    for clause in restrictions:
        print(*clause,0,file=target)
rc,reason = run([CADICAL,instance],log,90,solve=True)
if rc == 10:
    model = {int(lit) for line in log.read_text().splitlines() if line.startswith("v ")
             for lit in line[2:].split() if lit != "0"}
    assert len(model) == enc.variables and all(-lit not in model for lit in model)
    assert all(any(lit in model for lit in clause) for clause in clauses)
    (folder/"restricted_model.txt").write_text(" ".join(map(str,sorted(model,key=abs)))+"\n")
print("Restricted no-ASYM",rc,reason)
