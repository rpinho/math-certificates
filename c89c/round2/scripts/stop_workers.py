"""Stop only processes whose cwd is inside this job, then retain a process audit."""
import os,signal,time,json,subprocess,sys
from pathlib import Path
root=Path.cwd();me=os.getpid();ancestors={me};p=me
while p>1:
 try:
  s=Path(f'/proc/{p}/stat').read_text();p=int(s[s.rfind(')')+2:].split()[1]);ancestors.add(p)
 except (OSError,ValueError):break
def own():
 rows=[]
 for path in Path('/proc').iterdir():
  if not path.name.isdigit() or int(path.name) in ancestors:continue
  try:
   cwd=os.readlink(path/'cwd')
   if cwd!=str(root) and not cwd.startswith(str(root)+'/'):continue
   cmd=(path/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
   if cmd:rows.append({'pid':int(path.name),'command':cmd})
  except OSError:pass
 return rows
before=own()
for row in before:
 try:os.kill(row['pid'],signal.SIGTERM)
 except ProcessLookupError:pass
for _ in range(10):
 if not own():break
 time.sleep(.5)
remaining=own()
for row in remaining:
 try:os.kill(row['pid'],signal.SIGKILL)
 except ProcessLookupError:pass
time.sleep(.5);after=own();assert not after,after
with open('receipts/pod_ps_final.txt','w') as f:subprocess.run(['ps','-axo','pid,ppid,pcpu,command'],stdout=f,check=True)
result={'PASS':True,'utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime()),'stopped':before,'force_stopped':remaining,'remaining_own_workers':after,'scope':'only this own-job cwd or descendants; audit process and ancestors excluded'}
Path('receipts/'+(sys.argv[1] if len(sys.argv)>1 else 'worker_cleanup.json')).write_text(json.dumps(result,indent=2));print('PASS: no own-job workers remain; stopped',len(before))
