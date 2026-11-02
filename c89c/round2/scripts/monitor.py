"""Record this job's processes and aggregate memory; read-only outside own job."""
import os,time,json
from pathlib import Path
root=Path('/root/os/math_c89cr2_1101');seen=set()
while True:
 rows=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   if os.readlink(p/'cwd')!=str(root):continue
   stat=(p/'stat').read_text();right=stat.rfind(')');s=stat[right+2:].split();cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
   pid=int(p.name);seen.add(pid);rows.append({'pid':pid,'ppid':int(s[1]),'nice':int(s[16]),'threads':int(s[17]),'rss_kb':int(s[21])*os.sysconf('SC_PAGE_SIZE')//1024,'command':cmd})
  except (OSError,ValueError):pass
 rec={'utc':time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()),'rss_kb':sum(r['rss_kb'] for r in rows),'processes':rows}
 with (root/'receipts/resources.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 (root/'receipts/observed_pids.json').write_text(json.dumps(sorted(seen)))
 time.sleep(30)
