"""Stop only this session's optional rectangle pilots after measured timing."""
import json
import os
import pathlib
import signal
import time
root=pathlib.Path(__file__).resolve().parent
stopped=[]
for line in (root/'results/FAST_RECT_PIDS.jsonl').read_text().splitlines():
    record=json.loads(line);pid=record['pid']
    cmdline=pathlib.Path('/proc')/str(pid)/'cmdline'
    if cmdline.exists() and b'independent_rectangle_fast' in cmdline.read_bytes():
        os.kill(pid,signal.SIGTERM);stopped.append(pid)
result={'utc_epoch':time.time(),'stopped_pids':stopped,
        'reason':'Pilot timings predict no earlier completion than the ongoing 160-bit runs. The small literal control passed; partial large runs are not numerical evidence.'}
(root/'results/FAST_RECT_STOP.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
