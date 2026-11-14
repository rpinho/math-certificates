"""Independent membership/closure CNF with an exact prefix-count recurrence.

Usage: python encode.py COLOUR MINIMUM OUTPUT
Only the two JSON certificates are read from the producer (copied as data).
"""
import json
import sys
from pathlib import Path

colour, minimum, output = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
certificate = json.loads(Path('certificates/1183_n11_coloring.json').read_text())
colours = certificate['color_by_mask']
assert certificate['n'] == 11 and len(colours) == 2048
assert all(type(c) is int and c in (0, 1) for c in colours)
masks = [m for m, c in enumerate(colours) if c == colour]
member = {m: i + 1 for i, m in enumerate(masks)}
variables = len(masks)
clauses = 0
body = output.with_suffix('.body.tmp')
with body.open('w') as stream:
    def emit(*literals):
        global clauses
        if any(lit is True for lit in literals):
            return
        clause = {lit for lit in literals if lit is not False}
        if any(-lit in clause for lit in clause):
            return
        stream.write(' '.join(map(str, sorted(clause, key=lambda x: (abs(x), x)))) + ' 0\n')
        clauses += 1

    def neg(lit):
        return not lit if type(lit) is bool else -lit

    for i, a in enumerate(masks):
        for b in masks[i + 1:]:
            for result in (a & b, a | b):
                emit(-member[a], -member[b], member.get(result, False))
    closure_clauses = clauses

    # D(i,j) <=> D(i-1,j) OR (x_i AND D(i-1,j-1)).
    # D(i,0)=true; D(i,j)=false for j>i. All four implications
    # below enforce the equivalence, not just one direction.
    previous = [True] + [False] * minimum
    for i, m in enumerate(masks, 1):
        current = [True] + [False] * minimum
        x = member[m]
        for j in range(1, min(i, minimum) + 1):
            variables += 1
            q = current[j] = variables
            a, b = previous[j], previous[j - 1]
            emit(neg(a), q)
            emit(-x, neg(b), q)
            emit(-q, a, x)
            emit(-q, a, b)
        previous = current
    emit(previous[minimum])

with output.open('w') as dst, body.open() as src:
    dst.write(f'p cnf {variables} {clauses}\n')
    for line in src:
        dst.write(line)
# The body is a temporary file created by this run.
body.unlink()
metadata = dict(colour=colour, minimum=minimum, members=len(masks),
                masks=masks, variables=variables, clauses=clauses,
                closure_clauses=closure_clauses,
                counter_clauses=clauses-closure_clauses)
output.with_suffix('.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(json.dumps({k:v for k,v in metadata.items() if k != 'masks'}, sort_keys=True))
