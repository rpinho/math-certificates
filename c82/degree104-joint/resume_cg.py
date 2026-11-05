"""Consume saved round-one search checkpoints, then resume the inherited loop."""
import json
from pathlib import Path
import subprocess
import sys
import time
from numerics import register, write_json
from run_cg import run, verify, compact

register('resume_column_generation')
with open('STATUS.md', 'a') as f:
    f.write('\n2026-11-05 resume attempt 2: no numerical workers from attempt 1 remain. Union replay is complete and both round-one CVP checkpoints are usable; resume at their merge, without repeating saved searches. The original eight-hour clock in evidence/start.json is retained.\n')
searches = ['rounds/search-1-0.json', 'rounds/search-1-1.json']
data = [json.loads(Path(p).read_text()) for p in searches]
with open('evidence/compute.jsonl', 'a') as f:
    f.write(json.dumps({'kind': 'interrupted_cvp_pair_recovered', 'round': 1,
                        'cpu_seconds': sum(d['cpu_seconds'] for d in data),
                        'note': 'Recovered checkpoint process_time lower bounds from interrupted searches; old parent was interrupted before wait accounting.'}) + '\n')
state = 'rounds/restricted-1.json'
dual = 'rounds/union-dual.npz'
old = json.loads(Path(state).read_text())['lp']
negative = sum(len(d['negative_candidates']) for d in data)
if negative:
    prefix = 'rounds/den-1'
    run(['add_columns.py', '--state', state, '--prefix', prefix, *searches], 'logs/den-1.log')
    state, dual = prefix + '.json', prefix + '-dual.npz'
    verify(prefix)
for j in range(6):
    prefix = f'rounds/num-1-{j}'
    run(['numerator_search.py', '--state', state, '--dual', dual, '--prefix', prefix], f'logs/num-1-{j}.log')
    if not json.loads(Path(prefix + '-screen.json').read_text())['added']:
        break
    state, dual = prefix + '.json', prefix + '-dual.npz'
    verify(prefix)
new = json.loads(Path(state).read_text())['lp']
empty = int(old - new < 1e-10)
record = {'round': 1, 'old_lp': old, 'new_lp': new,
          'negative_candidates': negative, 'gain': old - new,
          'empty_rounds': empty, 'state': state, 'dual': dual}
write_json('rounds/resumed-round-1.json', record)
with open('STATUS.md', 'a') as f:
    f.write('\n' + json.dumps(record) + '\n')
state = compact(state, 'rounds/restricted-2.json')
run(['run_cg.py', '--state', state, '--dual', dual, '--first', '2',
     '--empty-start', str(empty), '--rounds', '100', '--seconds', '240', '--workers', '2'],
    'logs/cg-resumed.log')
finished = json.loads(Path('rounds/finished.json').read_text())
finished['history'].insert(0, record)
finished['resumed_from_round_one_search_checkpoints'] = True
write_json('rounds/finished.json', finished)
