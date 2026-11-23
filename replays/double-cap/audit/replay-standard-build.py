"""Build the ordinary Lake targets sequentially after checking cached dependencies."""
import graphlib
from pathlib import Path
import subprocess as sp

sp.run(['lake', '--no-build', 'build', 'Mathlib'], check=True)
paths = sorted(Path('LeanShadow').glob('*.lean')) + [Path('LeanShadow.lean')]
modules = {str(p.with_suffix('')).replace('/', '.'): p for p in paths}
order = graphlib.TopologicalSorter()
for mod, p in modules.items():
    order.add(mod, *(tok for line in p.read_text().splitlines() if line.startswith('import ')
                     for tok in line.split()[1:] if tok in modules))
for mod in order.static_order():
    print('lake build ' + mod, flush=True)
    sp.run(['lake', 'build', '+' + mod], check=True)
sp.run(['lake', 'build'], check=True)
