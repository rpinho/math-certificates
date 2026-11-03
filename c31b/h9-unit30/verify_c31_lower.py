"""Standalone exact lower certificate wrapper; no producer imports.

A raw decoded vector is checked by a separately implemented literal operator.
The small procedural packet contains a decoder and exact vector SHA256; the
checker can regenerate the vector, then treats it as untrusted input.
"""

def need(condition, message):
    if not condition:
        raise ValueError(message)
import argparse, hashlib, itertools, json, math, os, pathlib, re, subprocess, tempfile, time
from fractions import Fraction

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def burnside(k, h):
    total = 0
    for p in itertools.permutations(range(k)):
        fixed = sum((p[i] == i for i in range(k)))
        square = sum((p[p[i]] == i for i in range(k)))
        total += fixed ** (2 * h) + square ** h
    need(total % (2 * math.factorial(k)) == 0, 'certificate validation failed')
    return total // (2 * math.factorial(k))

def check(meta, vector, threads=1, receipt=None):
    start = time.monotonic()
    path = pathlib.Path(meta).resolve()
    data = json.loads(path.read_text())
    root = path.parent
    for label in ('generator', 'decoder'):
        need(sha(root / data[label]) == data[label + '_sha256'], label + ' source hash mismatch')
    need(data['format'] == 'c31-lower-procedural-v1', 'certificate validation failed')
    need(os.sys.byteorder == 'little', 'raw checker requires little-endian host')
    k, h, shift = (data['alphabet'], data['history'], data['shift'])
    r = Fraction(data['r'])
    need(2 <= k <= 4 and 2 <= h <= 9 and (1 <= shift <= 35) and (0 < r < 1), 'certificate validation failed')
    classes = burnside(k, h)
    need(classes == data['classes'], 'certificate validation failed')
    numerator = r * k * k * 2 ** shift
    need(numerator.denominator == 1, 'certificate validation failed')
    vector = pathlib.Path(vector)
    need(vector.stat().st_size == 8 * classes, 'certificate validation failed')
    vector_hash = sha(vector)
    need(vector_hash == data['decoded_sha256'], 'decoded vector hash mismatch')
    kernel = root / data['checker_kernel']
    need(sha(kernel) == data['checker_sha256'], 'checker source hash mismatch')
    need(1 <= threads <= 3, 'certificate validation failed')
    with tempfile.TemporaryDirectory(prefix='lower-exact-', dir=root) as scratch:
        exe = pathlib.Path(scratch) / 'checker'
        subprocess.run([os.environ.get('CC', 'cc'), '-O3', '-march=native', '-std=c11', '-pthread', str(kernel), '-o', str(exe)], check=True)
        done = subprocess.run([str(exe), str(k), str(h), str(shift), str(numerator.numerator), str(vector), str(threads), str(classes)], text=True, stdout=subprocess.PIPE, stderr=None, check=True)
    print(done.stdout, end='', flush=True)
    match = re.search('EXACT_LOWER_PASS .*?classes=(\\d+) min_numerator=(-?\\d+) max_numerator=(-?\\d+) denominator=(\\d+)', done.stdout)
    need(match, 'certificate validation failed')
    need(int(match[1]) == classes and int(match[2]) >= numerator and (int(match[4]) == k * k * 2 ** shift), 'certificate validation failed')
    gamma = 2 * r / (1 + r)
    result = {'status': 'VERIFIED_CANDIDATE_UNREFEREED', 'alphabet': k, 'history': h, 'classes': classes, 'r': str(r), 'gamma_exact': str(gamma), 'gamma_floor_12': f'{(gamma * 10**12).__floor__() // 10**12}.{(gamma * 10**12).__floor__() % 10**12:012d}', 'gamma_decimal_diagnostic': float(gamma), 'min_numerator': int(match[2]), 'max_numerator': int(match[3]), 'drift_denominator': int(match[4]), 'decoded_sha256': vector_hash, 'metadata_sha256': sha(path), 'checker_sha256': sha(kernel), 'wrapper_sha256': sha(__file__), 'seconds': time.monotonic() - start}
    if receipt:
        pathlib.Path(receipt).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)
    return result
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('metadata')
    p.add_argument('--vector')
    p.add_argument('--generate', action='store_true')
    p.add_argument('--work')
    p.add_argument('--threads', type=int, default=1)
    p.add_argument('--receipt')
    a = p.parse_args()
    meta = pathlib.Path(a.metadata).resolve()
    data = json.loads(meta.read_text())
    if a.generate:
        need(a.work, '--generate requires an explicit scratch directory')
        decoder = meta.parent / data['decoder']
        need(sha(decoder) == data['decoder_sha256'], 'certificate validation failed')
        subprocess.run([os.sys.executable, str(decoder), str(meta), '--work', a.work, '--threads', str(a.threads)], check=True)
        vector = pathlib.Path(a.work) / data['decoded_filename']
    else:
        need(a.vector, 'supply --vector or --generate --work')
        vector = a.vector
    check(meta, vector, a.threads, a.receipt)
