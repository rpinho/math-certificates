"""Enforce the job's 8 GB aggregate RSS and wall deadline for descendants."""
import subprocess,sys,time,os,signal,json,pathlib,datetime
start=time.time();job_start=json.loads(pathlib.Path('logs/start.json').read_text())['epoch']
# The Codex process owns this session's commands. Include simultaneous stages,
# rather than applying an 8 GB limit separately to each stage.
parents={};commands={}
for line in subprocess.check_output(['ps','-axo','pid=,ppid=,command='],text=True).splitlines():
 fields=line.split(None,2)
 if len(fields)==3:parents[int(fields[0])]=int(fields[1]);commands[int(fields[0])]=fields[2]
owner=os.getpid()
while owner in parents and 'codex exec ' not in commands.get(owner,'') and parents[owner]>1:owner=parents[owner]
p=subprocess.Popen(sys.argv[1:]);pathlib.Path('logs/worker_pids.txt').open('a').write(str(p.pid)+'\n')
peak=0;last=0;stop=None
while p.poll() is None:
 rows=[]
 for line in subprocess.check_output(['ps','-axo','pid=,ppid=,rss='],text=True).splitlines():
  try:rows.append(tuple(map(int,line.split())))
  except ValueError:pass
 ids={owner};changed=True
 while changed:
  old=len(ids);ids.update(pid for pid,ppid,rss in rows if ppid in ids);changed=len(ids)>old
 rss=sum(rss for pid,ppid,rss in rows if pid in ids)*1024;peak=max(peak,rss)
 if rss>7_800_000_000 or time.time()-job_start>7.8*3600:
  stop='8 GB RSS' if rss>8_000_000_000 else 'wall limit'
  # Stop this newest launched stage and its children; do not kill the session.
  newest={p.pid}
  for _ in range(8):newest.update(pid for pid,ppid,_ in rows if ppid in newest)
  for pid in sorted(newest,reverse=True):
   try:os.kill(pid,signal.SIGTERM)
   except ProcessLookupError:pass
  break
 if time.time()-last>3600:
  pathlib.Path('STATUS.md').open('a').write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+f': running {sys.argv[1:]}; sampled aggregate peak RSS {peak} bytes. Search logs contain current results.\n');last=time.time()
 time.sleep(2)
code=p.wait();pathlib.Path('logs/guard_'+str(p.pid)+'.json').write_text(json.dumps(dict(command=sys.argv[1:],seconds=time.time()-start,peak_rss_bytes=peak,exit=code,stop=stop))+'\n');sys.exit(code)
