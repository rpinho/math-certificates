"""Read-only progress and worker accounting for this job's pod directory."""
import datetime
import json
import pathlib
root=pathlib.Path(__file__).resolve().parent
progress={}
for name in ['b12','c12','b15_interval','c15_interval','rectangle22','rectangle23']:
    output=root/'results'/f'{name}.json';log=root/'results'/f'{name}.log'
    progress[name]='COMPLETE' if output.exists() else (log.read_text().splitlines()[-1] if log.exists() and log.stat().st_size else 'starting')
active=[]
for file in (root/'results').glob('*PIDS.jsonl'):
    for line in file.read_text().splitlines():
        entry=json.loads(line);pid=entry['pid'];p=pathlib.Path('/proc')/str(pid)
        try:
            if (p/'cwd').resolve()!=root:continue
            cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode()
            if 'independent_' in cmd:active.append({'pid':pid,'command':cmd})
        except (FileNotFoundError,PermissionError):pass
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'progress':progress,'active_workers':active}
with (root/'results/MONITOR.jsonl').open('a') as f:f.write(json.dumps(result)+'\n')
print(json.dumps(result))
