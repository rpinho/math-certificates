"""Mathematical corruption checks on session-created temporary copies."""
import copy,json,pathlib,shutil,subprocess,sys,tempfile,time
F=pathlib.Path(sys.argv[1]).resolve();R=F.parent;O=R/'receipts';O.mkdir(exist_ok=True)
base=json.loads((F/'completion_certificate.json').read_text());results=[];pids=[]
def run(label,script,packet):
 with tempfile.TemporaryDirectory(prefix='r8_corrupt_',dir=R) as temp:
  T=pathlib.Path(temp);(T/'completion_certificate.json').write_text(json.dumps(packet))
  with (O/('corruption_'+label+'.log')).open('w') as out:
   p=subprocess.Popen([sys.executable,str(F/script),str(T)],stdout=out,stderr=subprocess.STDOUT)
   pids.append({'label':label,'pid':p.pid,'script':script});(O/'corruption_pids.json').write_text(json.dumps(pids,indent=2)+'\n')
   try:code=p.wait(timeout=300)
   finally:
    if p.poll() is None:p.terminate();p.wait()
  assert code!=0,'corruption accepted: '+label
  results.append({'label':label,'checker':script,'rejected':True,'code':code})
  print('REJECT',label,script,flush=True)
for kind in ('R5','R6','tail','b'):
 packet=copy.deepcopy(base)
 for mode in ('simple','sharp'):
  m=packet['modes'][mode]
  if kind in ('R5','R6'):
   d=5 if kind=='R5' else 6;r=m['rows'][d-5];r['R']-=1;r['first_excluded']-=1
   from fractions import Fraction
   m['caps'][str(d)]=str(Fraction(r['R'],1<<d))
  if kind=='tail':m['tail']='0';m['bound']=m['caps']['96']
  if kind=='b':m['rows'][0]['b']='7/8'
 for impl in ('a','b'):run(kind+'_'+impl,'verify_completion_'+impl+'.py',packet)
packet=copy.deepcopy(base);packet['modes']['simple']['rows'][3]['representatives']-=1
run('omitted_cell','verify_completion_a.py',packet)
packet=copy.deepcopy(base);packet['modes']['simple']['rows'][0]['feasible']['lambda']='1/2'
run('false_feasible_point','verify_completion_a.py',packet)
(O/'corruptions.json').write_text(json.dumps({'status':'PASS','controls':results,'pids':pids},indent=2)+'\n')
