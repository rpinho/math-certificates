"""Evaluate all port pairs of a fixed complete family; certify any improvement."""
import json,math,subprocess,sys,datetime
from pathlib import Path
import numpy as np
cert=json.loads(Path('certificates/current.json').read_text());m=np.array(cert['masks'],dtype=np.uint32);n=cert['n'];size=len(m)
bits=((m[:,None]>>np.arange(n,dtype=np.uint32))&1).astype(np.int32)
deg=bits.sum(axis=0);co=bits.T@bits
rows=[]
for p in range(n):
    for q in range(p+1,n):
        d=int(co[p,q]);b=int(deg[q])-d;c=int(deg[p])-d;a=size-b-c-d
        if min(a,b,c,d)<=0:continue
        rho=(b+c+math.sqrt((b-c)**2+4*a*d))/2
        rows.append({'ports':[p,q],'counts':[a,b,c,d],'rho':rho,'rate':rho**(1/(n-2))})
rows.sort(key=lambda x:x['rate'],reverse=True);Path('logs/port_search.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows[:10],indent=2))
# Every change to a claimed rate goes through the separate exact checker.
if rows[0]['ports']!=cert['ports'] and rows[0]['rate']>float(cert['claimed_rate_lower'])+1e-14:
    cert['ports']=rows[0]['ports'];cert.pop('claimed_rate_lower',None)
    Path('certificates/port_proposal.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
    output=Path('logs/port_proposal_check.json');check=subprocess.run([sys.executable,'checker.py','certificates/port_proposal.json','--output',str(output)],capture_output=True,text=True)
    result=json.loads(output.read_text());assert check.returncode==0 and result['bar_comparison']=='above'
    cert['claimed_rate_lower']=result['rate_interval_decimal'][0];name='best_'+cert['claimed_rate_lower'][:24]+'.json'
    Path('certificates',name).write_text(json.dumps(cert,separators=(',',':'))+'\n');Path('certificates/current.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();Path('logs/last_improvement_utc.txt').write_text(stamp+'\n')
    print('CERTIFIED_BEST',name)
