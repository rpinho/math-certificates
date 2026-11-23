"""Export the actual pinned statements and proof closure, then one corrupted copy."""
import json
import os
from pathlib import Path
import shutil
import subprocess as sp

repo = Path.cwd()
job = repo.parent.parent
scratch = job / 'tmp'
config = json.loads(Path('ComparatorChallenges/LeanShadow.json').read_text())
primitives = ('Nat.zero Nat.succ Nat.add Nat.sub Nat.mul Nat.div Nat.mod Nat.pow Nat.gcd Nat.beq '
              'Nat.ble Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight String.ofList Char.ofNat List eagerReduce').split()
targets = ['Nat', 'String', 'String.mk', 'Char', 'Quot', 'Quot.mk', 'Quot.lift', 'Quot.ind', *config['theorem_names'], *config['permitted_axioms'], *primitives]
exporter = repo / '.lake/packages/lean4export/.lake/build/bin/lean4export'
art = repo / '.lake/build/lib/lean'
copy = scratch / 'corrupt'
copy.mkdir(exist_ok=True)
shutil.copytree('LeanShadow', copy / 'LeanShadow', dirs_exist_ok=True)
for obj in (art / 'LeanShadow').glob('*.olean'):
    if obj.stem != 'ComparatorDefinitions':
        dest = copy / 'LeanShadow' / obj.name
        if not dest.exists():
            dest.symlink_to(obj)
defs = copy / 'LeanShadow/ComparatorDefinitions.lean'
old = 'def delta (m : ℕ) : ℝ := capMass m (Real.pi / 4)'
s = defs.read_text()
assert s.count(old) == 1
defs.write_text(s.replace(old, old.replace('/ 4', '/ 3')))
diff = sp.run(['diff', '-u', 'LeanShadow/ComparatorDefinitions.lean', defs], capture_output=True, text=True)
assert diff.returncode == 1
(job / 'logs/corruption.diff').write_text(diff.stdout)
env = dict(os.environ, LEAN_PATH=str(copy) + ':' + os.environ['LEAN_PATH'])
sp.run(['lean', '-j2', '-o', 'LeanShadow/ComparatorDefinitions.olean', 'LeanShadow/ComparatorDefinitions.lean'],
       cwd=copy, env=env, check=True)
for label, module, paths in [('challenge', config['challenge_module'], os.environ),
                             ('solution', config['solution_module'], os.environ),
                             ('corrupt', config['solution_module'], env)]:
    dest = scratch / (label + '.ndjson')
    print('export', label, module, flush=True)
    with dest.open('wb') as f:
        sp.run([exporter, module, '--', *targets], stdout=f, env=paths, check=True)
    print('bytes', dest.stat().st_size, flush=True)
