"""Read-only audit of own job workers; no other job is controlled."""
import os,json,time,subprocess
from pathlib import Path
here=Path.cwd().resolve();own=[]
for entry in Path('/proc').iterdir():
 if not entry.name.isdigit():continue
 pid=int(entry.name)
 try:
  if Path(os.readlink(entry/'cwd')).resolve()!=here:continue
  cmd=(entry/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
  stat=(entry/'stat').read_text().rsplit(')',1)[1].split();status=(entry/'status').read_text();rss=next((int(x.split()[1]) for x in status.splitlines() if x.startswith('VmRSS:')),0)
  own.append(dict(pid=pid,ppid=int(stat[1]),nice=int(stat[16]),rss_kib=rss,command=cmd))
 except (FileNotFoundError,ProcessLookupError,PermissionError):continue
out=dict(utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),own=own,total_rss_kib=sum(x['rss_kib'] for x in own));Path('process-audit-current.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
