"""Record the referee job's environment and, on request, worker cleanup."""
import datetime
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

root=pathlib.Path(__file__).resolve().parent
def capture(args):
    p=subprocess.run(args,text=True,capture_output=True,check=True)
    return p.stdout.strip()
record={
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'platform':platform.platform(),
    'python':sys.version,
    'compiler':capture(['g++','--version']).splitlines()[0],
    'sha256':{},
}
for name in ['independent_tm.cpp','independent_interval.cpp','independent_rectangle.cpp',
             'independent_tm','independent_interval','independent_interval_large',
             'independent_rectangle','final_tm']:
    p=root/name
    if p.exists():record['sha256'][name]=hashlib.sha256(p.read_bytes()).hexdigest()
ps=capture(['ps','-axo','pid,ppid,pcpu,command'])
if sys.platform.startswith('linux'):
    own=[]
    for line in ps.splitlines()[1:]:
        fields=line.split(None,3)
        if len(fields)<4:continue
        pid=int(fields[0])
        try:belongs=(pathlib.Path('/proc')/str(pid)/'cwd').resolve()==root
        except OSError:belongs=False
        try:executable=(pathlib.Path('/proc')/str(pid)/'exe').resolve().name
        except OSError:executable=''
        if belongs and executable in {'independent_tm','independent_interval',
                                      'independent_interval_large','independent_rectangle',
                                      'independent_rectangle_fast','final_tm','final_rectangle'}:
            own.append(line.strip())
    record['native_workers']=own
    if '--final' in sys.argv:
        assert not own,own
        record['cleanup_status']='NO_NATIVE_WORKERS_RUNNING'
else:
    # Retain only this job's distinctive executable invocations, not unrelated
    # applications from the machine-wide process listing.
    own=[line.strip() for line in ps.splitlines()[1:]
         if any(token in line for token in ['./literal_walks ',str(root)+'/literal_walks '])]
    record['native_workers']=own
    if '--final' in sys.argv:
        assert not own,own
        record['cleanup_status']='NO_NATIVE_WORKERS_RUNNING'
name='COMPUTE_FINAL.json' if '--final' in sys.argv else 'COMPUTE_ENVIRONMENT.json'
(root/'results'/name).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'file':name,'native_workers':record['native_workers']}))
