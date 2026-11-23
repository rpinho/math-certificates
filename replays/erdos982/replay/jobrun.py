"""Run one local worker with the job's wall, disk and RSS limits."""
import os
from pathlib import Path
import resource
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent
def run(argv, logfile, budget, *, solve=False):
    deadline = time.time() + budget
    limits_path = ROOT / "job.env"
    if limits_path.is_file():
        limits = dict(line.split("=") for line in limits_path.read_text().splitlines())
        deadline = min(deadline, int(limits["SOLVE_STOP" if solve else "JOB_STOP"]))
    if time.time() >= deadline:
        raise TimeoutError("worker window closed")
    logfile = Path(logfile)
    logfile.parent.mkdir(parents=True, exist_ok=True)
    with logfile.open("w") as output:
        print("command:", *argv, flush=True, file=output)
        increment = max(0, 10 - os.getpriority(os.PRIO_PROCESS, 0))
        child = subprocess.Popen(["nice", "-n", str(increment), *map(str, argv)], cwd=ROOT,
                                 stdout=output, stderr=subprocess.STDOUT,
                                 start_new_session=True)
        with logfile.with_suffix(logfile.suffix+".pid").open("w") as receipt:
            print(child.pid, file=receipt)
        start = time.monotonic()
        last_disk = start - 5
        reason = ""
        max_rss = 0
        try:
            while child.poll() is None:
                now = time.monotonic()
                if time.time() >= deadline:
                    reason = "deadline"
                    break
                rss = subprocess.run(["ps", "-o", "rss=", "-p", str(child.pid)],
                                     capture_output=True, text=True, check=False).stdout.strip()
                if rss:
                    max_rss = max(max_rss, int(rss)*1024)
                    if max_rss >= 5_800_000_000:
                        reason = "RSS guard"
                        break
                if now-last_disk >= 5:
                    disk = subprocess.check_output(["du", "-sk", str(ROOT)], text=True)
                    if int(disk.split()[0])*1024 >= 4_500_000_000:
                        reason = "disk guard"
                        break
                    last_disk = now
                try:
                    child.wait(timeout=0.25)
                except subprocess.TimeoutExpired:
                    pass
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            print(f"worker exit={child.returncode} elapsed={time.monotonic()-start:.3f}s "
                  f"sampled_peak_rss={max_rss} cumulative_child_peak_rss="
                  f"{resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss} {reason}", file=output)
    return child.returncode, reason
