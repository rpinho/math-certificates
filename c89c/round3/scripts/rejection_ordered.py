"""Certificate-specific negative tests for the selected coloured ordered C6 proof."""
import hashlib, json, pathlib, subprocess

src = pathlib.Path('certificates/c6_ordered_type8.cert')
lines = src.read_text().splitlines()
assert lines[0].split()[-1] == '-2'
out = pathlib.Path('artifacts/ordered_controls')
out.mkdir(exist_ok=True)
cases = {}
a = lines.copy()
h = a[0].split(); h[4:6] = ['1', '1']; a[0] = ' '.join(h)
cases['false_bound_one'] = a
a = lines.copy()
h = a[0].split(); h[2] = '0'; a[0] = ' '.join(h)
cases['zero_denominator'] = a
a = lines.copy()
f = a[2].split(); f[1] = f[0]; a[2] = ' '.join(f)
cases['duplicate_flag'] = a
a = lines.copy()
h = a[1].split(); h[-1] = '2'; a[1] = ' '.join(h)
cases['invalid_colour'] = a
cases['truncated_factor'] = lines[:-1]
results = []
for name, content in cases.items():
    path = out / (name + '.cert')
    path.write_text('\n'.join(content) + '\n')
    for exe in ['./check_certificate_v3', './check_coloured_predecessor']:
        r = subprocess.run([exe, str(path), 'sources/graph8.g6'], capture_output=True, text=True)
        assert r.returncode != 0, (name, exe, r.stdout)
        results.append(dict(control=name, checker=exe, rejected=True,
                            diagnostic=(r.stderr + r.stdout).strip()[-500:]))
        print(results[-1], flush=True)
graphs=pathlib.Path('sources/graph8.g6').read_text().splitlines()
for name, rows in [('incomplete_graph_list',graphs[:10]),
                   ('duplicate_graph_list',[graphs[0],graphs[0]])]:
    path=out/(name+'.g6');path.write_text('\n'.join(rows)+'\n')
    r=subprocess.run(['./check_coloured_predecessor',str(src),str(path)],capture_output=True,text=True)
    assert r.returncode!=0,(name,r.stdout)
    results.append(dict(control=name,checker='./check_coloured_predecessor',rejected=True,
                        diagnostic=(r.stderr+r.stdout).strip()[-500:]))
    print(results[-1],flush=True)
pathlib.Path('receipts/c6_ordered_rejection_controls.json').write_text(json.dumps(
    dict(PASS=True, certificate_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
         controls=results), indent=2))
print('PASS all selected-certificate rejection controls', flush=True)
