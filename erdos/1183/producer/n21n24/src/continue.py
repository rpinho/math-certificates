"""Run the requested dimensions in order, with n=24's measured-cost decision."""
import pathlib,subprocess,sys,json,time,os,re
PY=sys.executable
timings=pathlib.Path('logs/stages.jsonl')

def launch(label,args,cwd=None):
 out=open('logs/'+label+'.log','w');err=open('logs/'+label+'.time','w')
 p=subprocess.Popen(['/usr/bin/time','-l',PY,'src/guard.py',*args],stdout=out,stderr=err,cwd=cwd)
 pathlib.Path('logs/worker_pids.txt').open('a').write(str(p.pid)+'\n')
 return label,p,out,err,time.time()
def finish(job):
 label,p,out,err,start=job;rc=p.wait();out.close();err.close()
 row=dict(label=label,wall_seconds=time.time()-start,returncode=rc)
 timings.open('a').write(json.dumps(row)+'\n');print('FINISHED',json.dumps(row),flush=True)
 assert rc==0,('stage failed',label,rc)
def completed(label):
 return timings.exists() and any(x['label']==label and x['returncode']==0 for x in map(json.loads,timings.read_text().splitlines()))
def run(label,args):
 if not completed(label):finish(launch(label,args))
def batch(jobs):
 running=[launch(label,args) for label,args in jobs if not completed(label)]
 for job in running:finish(job)
def status(text):
 pathlib.Path('STATUS.md').open('a').write('\n'+time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+': '+text+'\n')

profile_replay=None
def profile_if_ready():
 global profile_replay
 cp=pathlib.Path('logs/cost20/certificates/n20_T12/checkpoint.json')
 done=pathlib.Path('logs/cost20/logs/n20_T12_coverage.json')
 if profile_replay is None and cp.exists() and not json.loads(cp.read_text())['stack'] and not done.exists():
  profile_replay=launch('cost20_replay',[PY,'src/coverage.py','20','12'],cwd='logs/cost20')

# Existing n=21 producer stays owned by the interactive session.
while True:
 profile_if_ready()
 cp=pathlib.Path('certificates/n21_T12/checkpoint.json')
 if cp.exists() and not json.loads(cp.read_text())['stack']:break
 time.sleep(10)
run('coverage21_12',[PY,'src/coverage.py','21','12'])
for n,lb in [(22,13),(23,13),(24,14)]:
 target={22:13,23:14,24:14}[n]
 profile_if_ready()
 if n==24:
  if profile_replay is not None:finish(profile_replay)
  # Include measured prefix/tree-check costs; no orbit-only forecast.
  rows=[json.loads(s) for s in timings.read_text().splitlines()]
  # Compare attained-bound G-list production at both dimensions, including
  # all shorter lists. The isolated n=20 run uses exactly this producer.
  def cpu(path):
   s=pathlib.Path(path).read_text();m=re.search(r'([0-9.]+) real\s+([0-9.]+) user\s+([0-9.]+) sys',s)
   assert m,path
   return float(m[2])+float(m[3])
  t20=cpu('logs/cost20/logs/prefix20_12.time')
  t22=cpu('logs/prefix22_13.time')+cpu('logs/prefix22_13.serial.time')
  wall22=json.load(open('logs/n22_T13_prefix.json'))['seconds']
  check20=json.load(open('logs/cost20/logs/n20_T12_coverage.json'))['seconds']
  check22=json.load(open('logs/n22_T13_coverage.json'))['seconds']
  ratio=t22/t20;g=(ratio/4)**0.5
  check_ratio=check22/check20
  # Extrapolate the same +2 dimensions / +1 threshold again. Include a
  # complete lower-threshold replay, 15% margin and 120 seconds for uppers.
  forecast=1.15*(ratio*wall22+check_ratio*check22+check22)+120
  elapsed=time.time()-json.load(open('logs/start.json'))['epoch'];remaining=7.8*3600-elapsed
  decision=dict(n20_prefix_core_seconds=t20,n22_prefix_core_seconds=t22,n22_prefix_wall_seconds=wall22,parallel_workers=5,g_per_orbit_per_dimension=g,
                n20_check_seconds=check20,n22_check_seconds=check22,
                prefix_ratio=ratio,checker_ratio=check_ratio,forecast_n24_seconds=forecast,
                remaining_seconds=remaining,run=forecast<remaining)
  pathlib.Path('logs/n24_cost_decision.json').write_text(json.dumps(decision,indent=2)+'\n')
  status('n=24 measured-cost decision: '+json.dumps(decision));print('COST',decision,flush=True)
  if not decision['run']:break
 status(f'Start n={n}: upper bound first at target {target}; manuscript lower bound {lb}.')
 upperlabel=f'upper{n}' if target==lb else f'upper{n}_T{target}'
 run(upperlabel,[PY,'src/upper.py',str(n),str(target)])
 if not pathlib.Path(f'certificates/upper_n{n}.json').exists():
  findlabel=f'n{n}_upper_T{target}_find'
  code=f'import sys;sys.path.insert(0,"src");from screen import full;from run import Runner;r=Runner();full({n},{target},r,True,"{findlabel}");r.close()'
  run(findlabel,[PY,'-c',code])
  found=json.load(open(f'logs/{findlabel}.json'))
  assert found['survivors'],'No lower-bound word found; investigate before advancing'
  run(f'finish{n}',[PY,'src/finish_upper.py',f'logs/{findlabel}.json'])
 # Below-minimum screen first and at-minimum G-list screen, both resumable.
 for T in (target-1,target):run(f'prefix{n}_{T}',[PY,'src/parallel_prefix.py',str(n),str(T),'5'])
 batch([(f'coverage{n}_{T}',[PY,'src/coverage.py',str(n),str(T)]) for T in (target-1,target)])
 if n%2:
  # C producer prints the explicit witnesses; checker uses a separate code path.
  run(f'balanced{n}',['src/balanced_referee','bal',str(n)])
  # The stage log is the streamed witness list (no extra in-memory copy).
  run(f'balanced{n}_check',[PY,'src/check_balanced.py',str(n),f'logs/balanced{n}.log'])
 status(f'Completed n={n}: headline upper certificate, full rank minimum and G lists checked.' )
print('REQUESTED SCIENTIFIC STAGES COMPLETE',flush=True)
