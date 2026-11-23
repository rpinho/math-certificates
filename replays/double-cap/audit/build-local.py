"""Elaborate only the pinned upstream sources against the existing dependency cache."""
import graphlib
from pathlib import Path
import subprocess

sources = [*sorted(Path('LeanShadow').glob('*.lean')), Path('LeanShadow.lean')]
modules = {str(p.with_suffix('')).replace('/', '.'): p for p in sources}
order = graphlib.TopologicalSorter()
for module, path in modules.items():
    imports = [s for line in path.read_text().splitlines() if line.startswith('import ')
               for s in line.split()[1:] if s in modules]
    order.add(module, *imports)
out = Path('.lake/build/lib/lean')
for i, module in enumerate(order.static_order(), 1):
    src = modules[module]
    obj = out / src.with_suffix('.olean')
    obj.parent.mkdir(parents=True, exist_ok=True)
    print(f'[{i}/{len(sources)}] {module}', flush=True)
    subprocess.run(['lean', '-j2', '-o', str(obj), str(src)], check=True)
print(f'Built {len(sources)} proof modules.', flush=True)
