"""Summarize current search phase and certified best for the active session."""
import json,time
from pathlib import Path
from numerics import register
register('progress')
r=json.loads(Path('RESULT.json').read_text())
s=Path('STATUS.md').read_text().splitlines()
phase=next((x for x in reversed(s) if 'new-column search' in x or x.startswith('{"round"')), 'baseline replay')
latest=max([p for folder in ['logs','rounds'] for p in Path(folder).glob('*.log') if not p.name.startswith(('cg','compact','resume')) and p.name!='source-inventory.log'],key=lambda p:p.stat().st_mtime,default=None)
print(json.dumps({'elapsed_minutes':round((time.time()-json.loads(Path('evidence/start.json').read_text())['start_epoch'])/60,1),'certified_upper':r['interval_upper'],'below_frozen_bar':r['below_frozen_bar'],'phase':phase,'latest_log':str(latest) if latest else None,'latest_line':latest.read_text(errors='replace').splitlines()[-1][:250] if latest and latest.stat().st_size else '', 'completed_round':json.loads(Path('rounds/progress.json').read_text())['history'][-1]['round'] if Path('rounds/progress.json').exists() else None, 'completed':Path('rounds/finished.json').exists()}))
