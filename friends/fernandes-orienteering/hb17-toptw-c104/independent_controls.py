"""Independent exhaustive small-instance oracle + destructive certificate controls.
No claimant code used. All generated data live in this referee directory.
"""
import pathlib,random,math,subprocess,json,itertools,copy,time
base=pathlib.Path('controls');base.mkdir(exist_ok=True)
rng=random.Random(411703)
records=[]
def run(raw,dual,proof):
 p=subprocess.run(['./independent_upper',str(raw),str(dual),str(proof),str(base/'last_unresolved.tsv')],capture_output=True,text=True)
 return {'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
# Real proof must reject a removed root, insufficient bound, and illegal penalties.
raw=pathlib.Path('input/c104.txt');dual=pathlib.Path('input/BEST.dual');proof=pathlib.Path('input/BEST.proof')
p=proof.read_text().splitlines();n=int(p[1].split()[0]);countline=n+2
for name,lines in [('no_states',p[:countline]+['0']),('zero_upper',p[:1]+['101 0 0']+p[2:])]:
 dst=base/(name+'.proof');dst.write_text('\n'.join(lines)+'\n');r=run(raw,dual,dst);assert r['returncode']!=0;r['name']=name;records.append(r)
d=dual.read_text().split();d[5]='-1';dst=base/'negative.dual';dst.write_text(' '.join(d));r=run(raw,dst,proof);assert r['returncode']!=0;r['name']='negative_penalty';records.append(r)
d=dual.read_text().split();d[6]=str(int(d[6])+1000000);dst=base/'oversized.dual';dst.write_text(' '.join(d));r=run(raw,dst,proof);assert r['returncode']!=0;r['name']='oversized_penalty';records.append(r)
# A complete elementary-route enumeration is an independent oracle. The
# resulting full-memory proof is then aggressively thinned; rejection is
# acceptable, acceptance of a false bound is never acceptable.
for case in range(36):
 nc=6 if case<24 else 7;n=nc+1;xy=[(0,0)]+[(rng.randrange(10),rng.randrange(10)) for _ in range(nc)]
 service=[0]+[rng.randrange(1,6)*10 for _ in range(nc)]
 prize=[0]+[rng.randrange(1,6)*10 for _ in range(nc)]
 close=[rng.randrange(22,46)*10]+[rng.randrange(12,46)*10 for _ in range(nc)]
 opens=[0]+[rng.randrange(0,10)*10 for _ in range(nc)]
 travel=[[math.isqrt(100*((x-a)**2+(y-b)**2)) for a,b in xy]for x,y in xy]
 u=[0]+[rng.randrange(prize[j]*1000+1) for j in range(1,n)]
 q=[prize[j]*1000-u[j] for j in range(n)]
 labels=[(0,0,0,1)];terminal=[]
 def dfs(i,t,val,mask,pmask):
  if t+travel[i][0]<=close[0]:terminal.append((val,pmask))
  for j in range(1,n):
   if mask>>j&1:continue
   st=max(opens[j],t+travel[i][j])
   if st>close[j]:continue
   nt=st+service[j]
   if nt>close[0]:continue
   nm=mask|1<<j;labels.append((j,nt,val+q[j],nm));dfs(j,nt,val+q[j],nm,pmask|1<<(j-1))
 dfs(0,0,0,1,0)
 exact=max(v for v,m in terminal)
 rfile=base/'fixture.txt'
 rfile.write_text(f'4 10 {nc} 1\n0 200\n'+'\n'.join(f'{j} {xy[j][0]}.00 {xy[j][1]}.00 {service[j]/10:.2f} {prize[j]}.00 0 0 {opens[j]/10:.2f} {close[j]/10:.2f}'for j in range(n))+'\n')
 dfile=base/'fixture.dual';dfile.write_text(f'DUAL1 {n} 1000 4\n'+' '.join(map(str,u)))
 # The oracle uses tenths, whereas the certificate uses hundredths.
 head=['NGBOUND2',f'{n} 0 {exact}']+[str(n)+' '+' '.join(map(str,range(n))) for j in range(n)]
 pfile=base/'fixture.proof'
 rec={'case':case,'n':n,'routes_enumerated':len(terminal),'labels':len(labels),'exact_q':exact}
 for mode,subset in [('complete',labels),('thinned',labels[::3]),('empty',[])]:
  for false in [False,True]:
   if false and exact==0:continue
   h=head.copy();h[1]=f'{n} 0 {exact-int(false)}'
   pfile.write_text('\n'.join(h+[str(len(subset))]+[f'{i} {t*10} {v} {m}'for i,t,v,m in subset])+'\n')
   rr=run(rfile,dfile,pfile)
   if mode=='complete' and not false:assert rr['returncode']==0,(case,rr)
   if false:assert rr['returncode']!=0,(case,mode,'ACCEPTED FALSE BOUND',rr)
   rec[mode+('_false'if false else '_true')]=rr
 records.append(rec)
pathlib.Path('controls_receipt.json').write_text(json.dumps(records,indent=2))
print(json.dumps({'real_forgeries_rejected':4,'exhaustive_fixtures':36,'fixture_runs':216,'all_pass':True}))
