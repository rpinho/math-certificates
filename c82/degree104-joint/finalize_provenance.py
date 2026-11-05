"""Attribute final factors against actual source data, by full coefficients."""
import json
from pathlib import Path
from numerics import register, write_json

register('final_factor_provenance')
sources = []
for origin, filename in [
    ('ours from round 6', 'round6-certificate.json'),
    ('#280 v4', 'pr280-v4-certificate.json'),
    ('#280 v3', 'pr280-v3-certificate.json'),
    ('ours from round 5 or earlier', 'round5-certificate.json'),
    ("#280 bank", 'factor-bank.json'),
]:
    sources.append((origin, filename, json.loads((Path('prior_sources') / filename).read_text())))
historical = {'denominator': {}, 'numerator': {}}
for path in sorted(Path('../c82r6/rounds').glob('*.json')):
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        continue
    for kind in historical:
        records = list(data.get(kind, []))
        if kind == 'denominator':
            records += data.get('negative_candidates', [])
        for row in records:
            historical[kind].setdefault(tuple(row['coeffs']), []).append(
                {'origin': 'ours from round 6 earlier search states',
                 'name': row.get('name', ''), 'source': str(path)})
cert = json.loads(Path('certificate.json').read_text())
provenance = {}
for kind in historical:
    rows = []
    for row in cert[kind]:
        matches = [
            {'origin': origin, 'name': other['name'], 'source': filename}
            for origin, filename, data in sources
            for other in data[kind] if row['coeffs'] == other['coeffs']
        ]
        # The r7 union itself includes v4; it cannot establish r6 provenance.
        # Historical-only factors must occur in an actual r6 file.
        if not matches:
            matches = historical[kind].get(tuple(row['coeffs']), [])
        # Credit the public source when a factor also appeared in our seed.
        priority = {'#280 v3': 0, '#280 bank': 1, '#280 v4': 2,
                    'ours from round 5 or earlier': 3, 'ours from round 6': 4,
                    'ours from round 6 earlier search states': 5}
        origin = min(matches, key=lambda m: priority[m['origin']])['origin'] if matches else 'new here'
        rows.append({**row, 'origin': origin,
                     'all_full_coefficient_matches': matches})
    provenance[kind] = rows
write_json('FACTOR_PROVENANCE.json', provenance)
print(json.dumps({kind: len(rows) for kind, rows in provenance.items()}))
