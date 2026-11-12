"""Final ps check and cleanup of this job's tracked numerical workers only."""
import json,os,subprocess,time
from pathlib import Path
tracked=set()
for line in Path('evidence/pids.jsonl').read_text().splitlines():
    d=json.loads(line)
    if 'pid' in d:tracked.add(int(d['pid']))
for p in Path('.').rglob('*.log'):
    for line in p.read_text(errors='replace').splitlines()[:8]:
        try:d=json.loads(line)
        except (ValueError,TypeError):continue
        if isinstance(d,dict) and d.get('event')=='start' and 'pid' in d:tracked.add(int(d['pid']))

def owned_live():
    raw=subprocess.check_output(['ps','-axo','pid,ppid,pcpu,command'],text=True);found=[]
    for line in raw.splitlines()[1:]:
        parts=line.strip().split(None,3)
        if len(parts)<4:continue
        pid=int(parts[0])
        if pid==os.getpid():continue
        executable=Path(parts[3].split()[0]).name
        if not (executable.startswith('python') or executable=='time'):continue
        p=subprocess.run(['/usr/sbin/lsof','-a','-p',str(pid),'-d','cwd','-Fn'],capture_output=True,text=True)
        cwd=[s[1:] for s in p.stdout.splitlines() if s.startswith('n')]
        if str(Path.cwd()) in cwd:found.append({'pid':pid,'ppid':int(parts[1]),'pcpu':parts[2],'command':parts[3]})
    return found
before=owned_live()
for row in before:
    try:os.kill(row['pid'],15)
    except ProcessLookupError:pass
if before:time.sleep(2)
after=owned_live()
result={'ps_command':'ps -axo pid,ppid,pcpu,command','tracked_ids':sorted(tracked),'alive_before_cleanup':before,'alive_after_cleanup':after,'none_of_our_workers_running':not after,'checked_epoch':time.time()}
Path('evidence/process-cleanup.json').write_text(json.dumps(result,indent=2)+'\n')
assert not after,after
print(json.dumps({'none_of_our_workers_running':True,'terminated_stale_workers':len(before)}))
