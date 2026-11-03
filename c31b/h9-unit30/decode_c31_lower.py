"""Finite procedural decompression, using exact integer iterations.

The generator is not trusted by the checker. Intermediate and final bytes
must match packet hashes before exact direct-sum verification is attempted.
Use an empty scratch directory; this decoder never overwrites existing data.
"""

def need(condition, message):
    if not condition:
        raise ValueError(message)
import argparse, hashlib, json, os, pathlib, subprocess

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('metadata')
    p.add_argument('--work', required=True)
    p.add_argument('--threads', type=int, default=1)
    a = p.parse_args()
    need(1 <= a.threads <= 3, 'certificate validation failed')
    need(os.sys.byteorder == 'little', 'decoder requires little-endian host')
    meta = pathlib.Path(a.metadata).resolve()
    d = json.loads(meta.read_text())
    root = meta.parent
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    need(not any(work.iterdir()), 'use an empty scratch directory')
    src = root / d['generator']
    need(sha(src) == d['generator_sha256'], 'certificate validation failed')
    exe = work / 'decoder'
    subprocess.run([os.environ.get('CC', 'cc'), '-O3', '-march=native', '-std=c11', '-pthread', str(src), '-o', str(exe)], check=True)
    previous = None
    for step in d['recipe']:
        h = step['history']
        prefix = work / f'lower_h{h}'
        env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        for key in ['KLOW_INIT', 'KLOW_RESUME', 'KLOW_SECONDS', 'KLOW_THREADS_FILE', 'KLOW_TARGET_R', 'KLOW_CHECKPOINT_PREFIX']:
            env.pop(key, None)
        if previous is not None:
            env['KLOW_INIT'] = str(previous)
        with (work / f'h{h}.log').open('w') as log:
            subprocess.run([str(exe), str(d['alphabet']), str(h), str(step['iteration_limit']), str(a.threads), str(prefix)], env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        previous = pathlib.Path(str(prefix) + '_w.bin')
        need(sha(previous) == step['sha256'], 'procedural decoding hash mismatch')
    need(previous.name == d['decoded_filename'] and sha(previous) == d['decoded_sha256'], 'certificate validation failed')
    print('DECODED_AND_HASH_MATCHED', previous)
if __name__ == '__main__':
    main()
