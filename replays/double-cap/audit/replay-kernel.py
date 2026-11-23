"""Check every pinned proof module, one leanchecker process at a time."""
from pathlib import Path
import subprocess

modules = ['LeanShadow.' + path.stem for path in sorted(Path('LeanShadow').glob('*.lean'))]
for module in modules:
    print('checking ' + module, flush=True)
    subprocess.run(['leanchecker', '--verbose', module], check=True)
print(f'PASS: replayed {len(modules)} modules. LeanShadow.lean is the imports-only umbrella.', flush=True)
