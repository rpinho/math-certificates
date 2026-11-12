"""Plot the actual certified checkpoints, without fitting or extrapolation."""
import json,os,time
from pathlib import Path
os.environ['MPLCONFIGDIR']=str(Path('evidence/matplotlib-cache').resolve())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from numerics import register
register('plot_certified_curve')
start=json.loads(Path('evidence/start.json').read_text())['start_epoch']
rows=[json.loads(x) for x in Path('evidence/improvement-curve.jsonl').read_text().splitlines()]
x=[(r['epoch']-start)/3600 for r in rows];y=[float(r['upper']) for r in rows]
x.append((time.time()-start)/3600);y.append(y[-1])
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
ax.step(x,y,where='post',color='#164b78',linewidth=1.6,label='Certified upper endpoint')
ax.scatter(x[:-1],y[:-1],s=10,color='#164b78',zorder=3)
ax.axhline(.2519758216,color='#9c5940',linestyle='--',linewidth=1,label='Frozen bar 0.2519758216')
ax.set(xlabel='Elapsed job time (hours)',ylabel='Certified upper endpoint B',title='C82 round 9: warm continuation (candidate, unrefereed)')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.9f'))
ax.grid(alpha=.2);ax.legend(loc='lower left',frameon=False)
fig.savefig('IMPROVEMENT_CURVE.png',dpi=180)
fig.savefig('IMPROVEMENT_CURVE.pdf')
plt.close(fig)
print(json.dumps({'certified_checkpoints':len(rows),'latest_upper':rows[-1]['upper']}))
