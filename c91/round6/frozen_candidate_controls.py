"""Fail-closed controls of the frozen bytes, run serially at nice 10.

Every negative control requires its exact verifier diagnostic AND exit status.
A bounded positive replay must reach C++ and its canonical-word validation.
This is not a full replay of the certificate. Run from the job directory.
"""
import argparse
import copy
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time


EXPECTED = {
    'schema': (41, 'VERIFY_REJECT schema'),
    'exponent': (42, 'VERIFY_REJECT exponent'),
    'canonical_word': (1, 'REJECT: listed word is canonical'),
    'zero_initial': (44, 'VERIFY_REJECT initial potential (requires 0 < initial <= 2^60)'),
    'constant_positive_potential': (1, 'REJECT: exact row inequality failed at 0 (positive-minimum lower bound)'),
}
SCHEMA = 'VERIFY_CHECKPOINT schema PASS'
EXPONENT = 'VERIFY_CHECKPOINT exponent PASS'
CPP = 'VERIFY_CHECKPOINT cpp START'
CANONICAL = 'VERIFY_CHECKPOINT canonical word PASS'
RECIPE = 'VERIFY_CHECKPOINT integer power recipe PASS'

# Exact ordered evidence before each rejection (or positive outcome).
# The first three Python checks intentionally run before C++ is launched.
REQUIRED_CHECKPOINTS = {
    'schema': (),
    'exponent': (SCHEMA,),
    'zero_initial': (SCHEMA, EXPONENT),
    'canonical_word': (SCHEMA, EXPONENT, RECIPE, CPP),
    'constant_positive_potential': (SCHEMA, EXPONENT, RECIPE, CPP, CANONICAL),
    'positive_frozen': (SCHEMA, EXPONENT, RECIPE, CPP, CANONICAL),
}


def evaluate(name, code, output, stopped=False):
    """Pure classifier: unexpected exits, reasons and tracebacks are ERRORs."""
    lines = output.splitlines()
    # Count every rejection line, including indented or unexpected formats.
    diagnostics = [s for s in lines if re.search(r'\bREJECT\b|VERIFY_REJECT\b', s)]
    ordinary_output = '\n'.join(s for s in lines if not re.fullmatch(
        r'RESOURCE_LIMIT RLIMIT_AS (?:APPLIED [0-9]+|SKIPPED (?:AttributeError|OSError|ValueError) .+)', s))
    if re.search(r'\b\w*(?:Error|Exception)\b|Traceback|terminate called|HARNESS_ERROR|VERIFY_EXECUTION_ERROR|(?:^|\s)(?:fatal )?error:', ordinary_output):
        return False, 'exception or execution failure in verifier output'
    required = REQUIRED_CHECKPOINTS[name]
    positions = [lines.index(s) if s in lines else -1 for s in required]
    observed = tuple(s for s in lines if s.startswith('VERIFY_CHECKPOINT '))
    if observed != required or -1 in positions or positions != sorted(positions):
        return False, 'missing or out-of-order verifier checkpoint'
    if name == 'positive_frozen':
        ok = not diagnostics and ((stopped and code in (-15, 143)) or
              (code == 0 and any(s.startswith('SEPARATELY_WRITTEN_SAME_AGENT_EXACT_ARB_PASS') for s in lines)))
    else:
        expected = EXPECTED[name]
        if diagnostics == [expected[1]] and positions and lines.index(expected[1]) <= positions[-1]:
            return False, 'rejection diagnostic precedes required verifier checkpoints'
        ok = code == expected[0] and diagnostics == [expected[1]] and not stopped
    return ok, 'expected evidence observed' if ok else 'wrong exit status, diagnostic, or stop condition'


def terminate_group(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
    # A child can outlive an exited group leader, including after SIGTERM.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_case(name, artifact, verifier, label, timeout):
    logpath = Path('logs') / f'{label}_control_{name}.log'
    start = time.monotonic()
    stopped = False
    timed_out = False
    seen = {}
    max_processes = 0
    max_rss = 0
    last_sample = -1.0
    command = [sys.executable, '-u', str(verifier), str(artifact)]
    process = None
    # Each run owns a new process group. No unrelated job is signalled.
    with logpath.open('w') as log:
        try:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            print('CONTROL_START', name, 'pid', process.pid, flush=True)
            while process.poll() is None:
                if time.monotonic() - last_sample >= 0.5:
                    listing = subprocess.check_output(['ps', '-axo', 'pid,ppid,pgid,ni,rss,command'], text=True)
                    own = []
                    for line in listing.splitlines()[1:]:
                        fields = line.split(None, 5)
                        if len(fields) == 6 and int(fields[2]) == process.pid:
                            row = dict(pid=int(fields[0]), ppid=int(fields[1]), pgid=int(fields[2]),
                                       nice=int(fields[3]), rss_kib=int(fields[4]), command=fields[5])
                            seen[row['pid']] = row
                            own.append(row)
                    max_processes = max(max_processes, len(own))
                    max_rss = max(max_rss, sum(row['rss_kib'] for row in own)*1024)
                    if len(own) > 4 or any(row['nice'] < 10 for row in own):
                        raise RuntimeError('worker count or nice limit violated')
                    last_sample = time.monotonic()
                output = logpath.read_text()
                if name == 'positive_frozen' and all(s in output.splitlines() for s in
                                                    (SCHEMA, EXPONENT, RECIPE, CPP, CANONICAL)):
                    stopped = True
                    terminate_group(process)
                    break
                if time.monotonic() - start >= timeout:
                    timed_out = True
                    terminate_group(process)
                    break
                time.sleep(0.05)
        except Exception as error:
            print('HARNESS_ERROR',type(error).__name__,str(error),file=log,flush=True)
        finally:
            # Also cleans up compilers/checkers on interruption or reader failure.
            if process is not None:
                terminate_group(process)
    output = logpath.read_text()
    passed, reason = evaluate(name, process.returncode if process else None, output, stopped)
    if timed_out:
        passed, reason = False, 'deadline reached before the required outcome'
    result = dict(name=name, status='passed' if passed else 'ERROR', passed=passed,
                  reason=reason, exit_code=process.returncode if process else None,
                  seconds=time.monotonic()-start, command=command, pid=process.pid if process else None,
                  intentional_checkpoint_stop=stopped, timed_out=timed_out,
                  log=str(logpath), log_sha256=sha(logpath),
                  resource_notices=[s for s in output.splitlines() if s.startswith('RESOURCE_LIMIT ')],
                  seen_processes=list(seen.values()), max_sampled_worker_processes=max_processes,
                  peak_sampled_group_rss_bytes=max_rss)
    print('FROZEN_CONTROL', json.dumps(result), flush=True)
    return result


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact', type=Path)
    parser.add_argument('verifier', type=Path)
    parser.add_argument('label')
    parser.add_argument('--timeout', type=float, default=600)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.label) or not 0 < args.timeout <= 600:
        parser.error('safe label and 0 < timeout <= 600 required')
    if os.getpriority(os.PRIO_PROCESS, 0) < 10:
        os.setpriority(os.PRIO_PROCESS, 0, 10)
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_THREAD_LIMIT'):
        os.environ[key] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    Path('logs').mkdir(exist_ok=True)
    Path('work').mkdir(exist_ok=True)
    receipt = dict(status='running', started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   source_sha256=sha(args.artifact), verifier_sha256=sha(args.verifier),
                   harness_sha256=sha(__file__),
                   nice=os.getpriority(os.PRIO_PROCESS, 0),
                   max_concurrent_workers=1, timeout_seconds=args.timeout, results=[])
    receipt_path = Path('logs') / f'{args.label}_frozen_controls.json'
    def save():
        receipt_path.write_text(json.dumps(receipt, indent=2)+'\n')
    save()
    try:
        # Positive frozen bytes use exactly the same wrapper/launcher as negatives.
        receipt['results'].append(run_case('positive_frozen', args.artifact, args.verifier,
                                          args.label, args.timeout))
        save()
        source = json.loads(gzip.decompress(args.artifact.read_bytes()))
        # Temporary copies created by this invocation only. Never alter the source.
        with tempfile.TemporaryDirectory(prefix=f'{args.label}-controls-', dir='work') as folder:
            for name in EXPECTED:
                changed = copy.deepcopy(source)
                if name == 'schema':
                    changed['schema'] = 'corrupted'
                elif name == 'exponent':
                    changed['bound'] = [9, 10]
                elif name == 'canonical_word':
                    changed['forbidden_patterns'].extend([[1, 0], [1, 1]])
                elif name == 'zero_initial':
                    changed['potential']['initial'] = 0
                else:
                    changed['potential']['steps'] = 0
                path = Path(folder)/f'{name}.json.gz'
                with gzip.open(path, 'wt', compresslevel=1) as stream:
                    json.dump(changed, stream, separators=(',', ':'))
                del changed
                result = run_case(name, path, args.verifier, args.label, args.timeout)
                result.update(corrupted_sha256=sha(path), expected_exit_code=EXPECTED[name][0],
                              expected_diagnostic=EXPECTED[name][1])
                receipt['results'].append(result)
                save()
                path.unlink()  # session-created temporary corruption only
        receipt['status'] = 'passed' if all(r['passed'] for r in receipt['results']) else 'ERROR'
    except Exception as error:
        receipt.update(status='ERROR', error=f'{type(error).__name__}: {error}')
        print('HARNESS_ERROR', receipt['error'], flush=True)
    finally:
        receipt['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        receipt['source_unchanged'] = sha(args.artifact) == receipt['source_sha256']
        if not receipt['source_unchanged']:
            receipt['status'] = 'ERROR'
        save()
    return 0 if receipt['status'] == 'passed' else 2


if __name__ == '__main__':
    raise SystemExit(main())
