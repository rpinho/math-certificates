import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('word');a=p.parse_args();n=len(a.word)-1
chain=[(1<<r)-1 for r in range(n+1) if a.word[r]=='1']
w=[]
screen=pathlib.Path(f'data/screen_n{n}_t{8 if n==13 else 9}_witnesses.jsonl')
if n==13:
 for line in screen.read_text().splitlines():
  d=json.loads(line)
  if d['word']==a.word:w=d['family'];break
out={'n':n,'rank_word':a.word,'mask_convention':'bit i represents element i+1','colors':[int(a.word[s.bit_count()]) for s in range(1<<n)],'monochromatic_chain':chain,'explicit_optimal_family':w if w else chain}
pathlib.Path(f'certificates/n{n}_coloring.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='colors'}))
