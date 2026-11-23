"""Run one command group with the job's absolute deadline and resource limits."""
import os
from pathlib import Path
import signal
import subprocess as sp
import sys
import time
from datetime import datetime, timezone

job = Path(__file__).resolve().parent
pinned_deadline = datetime(2026, 11, 23, 3, 3, 56, tzinfo=timezone.utc).timestamp()
replay_deadline = float(os.environ.get('LEANSHADOW_REPLAY_DEADLINE', pinned_deadline))
deadline = min(replay_deadline, time.time() + int(sys.argv[1]))
proc = sp.Popen(sys.argv[2:], start_new_session=True)
peak = 0
next_disk = 0
try:
    while proc.poll() is None:
        if time.time() >= deadline:
            raise RuntimeError('deadline')
        data = sp.check_output(['ps', '-axo', 'pgid=,rss='], text=True)
        rss = sum(int(row[1])*1024 for line in data.splitlines() if len(row := line.split()) == 2 and row[0] == str(proc.pid))
        peak = max(peak, rss)
        if rss > 6_800_000_000:
            raise RuntimeError(f'RSS guard at {rss} bytes')
        if time.monotonic() >= next_disk:
            used = int(sp.run(['du', '-sk', job], stdout=sp.PIPE, stderr=sp.DEVNULL).stdout.split()[0])*1024
            if used > 14_200_000_000:
                raise RuntimeError(f'disk guard at {used} bytes')
            next_disk = time.monotonic() + 3
        time.sleep(0.5)
    sys.exit(proc.returncode)
finally:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()
    print(f'peak sampled group RSS {peak} bytes', file=sys.stderr)
