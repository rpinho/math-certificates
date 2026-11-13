"""Replay and document the final candidate packet after search stops."""
import json,subprocess,sys
from pathlib import Path
from numerics import register
from supervise import run
from fractions import Fraction
register('finalize')
r=json.loads(Path('RESULT.json').read_text())
run(['verify_best.py','--certificate','certificate.json','--target',r['stated_decimal'],'--precision','256','--tol','1e-13','--out','evidence/final-replay.json'],'logs/final-replay.log')
run(['rejection_controls.py','--certificate','certificate.json','--verifier','verify_best.py'],'logs/rejection-controls.log')
cert=json.loads(Path('certificate.json').read_text())
with open('CERTIFICATE_ENCODING.md','a') as out:
 out.write('\n## Final packet\n\n| Factor | Stored q_rational | Equal doubled fraction |\n| --- | --- | --- |\n')
 for row in cert['numerator']:
  raw=row['q_rational'];q=Fraction(raw);a,b=map(int,raw.split('/')) if '/' in raw else (int(raw),1)
  if len(str(abs(a))) in [15,16] or len(str(abs(q.numerator))) in [15,16]:
   doubled=f'{2*a}/{2*b}';assert Fraction(doubled)==q
   out.write(f"| {row['name']} | {raw} | {doubled} |\n")
run(['plot_curve.py'],'logs/plot-curve.log')
run(['source_inventory.py'],'logs/source-inventory.log')
subprocess.run([sys.executable,'finish_report.py'],check=True)
# Run cleanup.py from the shell after this orchestrator exits.
