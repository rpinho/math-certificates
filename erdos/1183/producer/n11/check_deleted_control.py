#!/usr/bin/env python3
"""Verify deletion of exactly the cardinality unit, and the returned SAT model."""
from pathlib import Path
original=Path('data/1183_n11_c0.cnf').read_text().splitlines();deleted=Path('data/1183_control_deleted.cnf').read_text().splitlines()
assert original[1:-1]==deleted[1:] and original[-1]=='10466 0'
assert int(deleted[0].split()[-1])+1==int(original[0].split()[-1])
model=Path('logs/1183_control_deleted.solve').read_text();assert 's SATISFIABLE' in model
values={abs(int(v)):int(v)>0 for line in model.splitlines() if line.startswith('v ') for v in line[2:].split() if int(v)}
for line in deleted[1:]:
 lits=list(map(int,line.split()[:-1]));assert any(values.get(abs(v),False)==(v>0) for v in lits)
print('VALID DELETION CONTROL: exactly one threshold unit removed; complete SAT assignment satisfies every remaining clause')
