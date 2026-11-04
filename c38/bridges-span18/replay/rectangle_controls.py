from fractions import Fraction as Q
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
x=Q(51081913,1<<27);D=1<<96
rows=[json.loads(s) for s in (root/'literal_rectangle.jsonl').read_text().splitlines()]
for r in rows:
 W=r['frame_range'];v=sum(int(c)*x**n for n,c in enumerate(r['coefficients']))
 p=subprocess.run([str(root/'rectangle'),str(W),'2','5','5'],capture_output=True,text=True,check=True)
 a=json.loads(p.stdout)
 (root/f'control_frame{W}.json').write_text(p.stdout)
 assert Q(int(a['num_lo']),D)<=v<=Q(int(a['num_hi']),D)
 print(json.dumps({'frame_range':W,'all_lengths':True,'exact_literal_enclosed':True}))
