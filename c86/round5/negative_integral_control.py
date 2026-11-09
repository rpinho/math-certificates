"""Corrupt one density node and rebind T/m, so both analytic E4 paths must reject."""
import argparse,copy,json,hashlib,subprocess,sys
from pathlib import Path
from fractions import Fraction as F
import independent_verify as V
from flint import acb
p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('tag');a=p.parse_args();raw=Path(a.certificate).read_bytes();c=json.loads(raw);assert [0,1] in c['A'];e=list(map(F,c['edges']));h=list(map(F,c['node_densities']));k=max((i for i in range(1,len(h)-1) if h[i]>0 and e[i]>1),key=lambda i:h[i]*(e[i+1]-e[i-1]));h[k]*=F(99,100);c['node_densities']=list(map(str,h));mass=sum((y-x)*(u+v)/2 for x,y,u,v in zip(e,e[1:],h,h[1:]));trace=sum((y-x)*((2*x+y)*u+(x+2*y)*v)/6 for x,y,u,v in zip(e,e[1:],h,h[1:]));c['bound']=str(trace/mass);c['bound_float']=float(trace/mass);Path('controls').mkdir(exist_ok=True);dst=Path('controls')/(a.tag+'-negative-integral.json');dst.write_text(json.dumps(c));data=V.load_certificate(dst);direct=V.cell_integral(data,acb(0));jump=V.potential(data,acb(0));assert (direct-jump).contains(0) and direct<0
rows=[]
for name,cmd in [('independent',[sys.executable,'-u','independent_verify.py',str(dst),'--integrals-only','--output','controls/'+a.tag+'-bad-integral-independent.json']),('linear',[sys.executable,'-u','verify_linear.py',str(dst),'--beat','1.81','--output','controls/'+a.tag+'-bad-integral-linear.json'])]:
 log=Path('logs')/(a.tag+'-control-integral-'+name+'.log')
 with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 text=log.read_text();assert r.returncode!=0,(name,'corruption accepted')
 assert ('negative/uncertain log integral' in text) if name=='independent' else ('E4' in text),text[-1200:]
 rows.append(dict(verifier=name,exit_code=r.returncode,rejected=True,log=str(log)))
out=dict(source_sha256=hashlib.sha256(raw).hexdigest(),corrupted_file=str(dst),corrupted_sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),modified_node=k,multiplier='99/100',bound_recomputed=True,exact_mass=str(mass),direct_log_x_integral=str(direct),jump_crosscheck=str(jump),results=rows);Path(a.tag+'-negative-integral-control.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
