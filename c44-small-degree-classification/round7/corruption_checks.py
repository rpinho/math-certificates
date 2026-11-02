"""Mathematical tamper checks on temporary copies, beyond manifest hash checks."""
import copy,gzip,json,pathlib,subprocess,sys,tempfile,shutil
R=pathlib.Path(__file__).resolve().parent
if R.name=='frozen':R=R.parent
F=R/'frozen';O=R/'receipts';O.mkdir(exist_ok=True)
ledger=[];results=[]
def reject(label,script,files,mutator):
 with tempfile.TemporaryDirectory(prefix='corruption_',dir=R) as name:
  T=pathlib.Path(name)
  for file in files:shutil.copyfile(F/file,T/file)
  mutator(T)
  with (O/('corruption_'+label+'.log')).open('w') as out:
   p=subprocess.Popen([sys.executable,str(F/script),str(T)],stdout=out,stderr=subprocess.STDOUT)
   ledger.append({'pid':p.pid,'label':label,'script':script})
   (O/'corruption_pids.json').write_text(json.dumps(ledger,indent=2)+'\n')
   try:code=p.wait(timeout=240)
   finally:
    if p.poll() is None:p.terminate();p.wait()
  assert code!=0,'tampering accepted: '+label
  results.append({'label':label,'verifier':script,'returncode':code,'rejected':True})
  print('REJECT',label,script,code,flush=True)

def scalar_mutate(t,what):
 p=t/'certificate.json';c=json.loads(p.read_text());m=c['modes']['classified']
 if what=='count':
  row=m['rows'][0];row['R']=50;row['first_excluded']=51;m['caps']['5']='25/16'
 elif what=='tail':
  m['tail']='0';m['bound']=m['caps']['96']
 elif what=='cell':m['rows'][3]['case_count']-=1
 p.write_text(json.dumps(c))
for typ in ['count','tail']:
 for impl in ['a','b']:reject(typ+'_'+impl,'verify_scalar_'+impl+'.py',['certificate.json'],lambda t,typ=typ:scalar_mutate(t,typ))
reject('omitted_cell','verify_scalar_a.py',['certificate.json'],lambda t:scalar_mutate(t,'cell'))

def quartic_mutate(t,what):
 p=t/'quartic_certificate.json.gz'
 with gzip.open(p,'rt') as f:c=json.load(f)
 if what=='branch':
  node=c['cases'][0]['tree'];assert node[0]==5;node[2].pop()
 else:c['patterns0'].pop()
 with gzip.open(p,'wt') as f:json.dump(c,f)
reject('quartic_branch','verify_quartic_a.py',['quartic_certificate.json.gz'],lambda t:quartic_mutate(t,'branch'))
for impl in ['a','b']:reject('quartic_template_'+impl,'verify_quartic_'+impl+'.py',['quartic_certificate.json.gz'],lambda t:quartic_mutate(t,'template'))
files=['quintic_minimum_templates.bin.gz','quintic13_homogeneous_certificate.json.gz','quintic13_nonhomogeneous_certificate.json']
def broken_template(t):
 p=t/'quintic_minimum_templates.bin.gz'
 with gzip.open(p,'rb') as f:b=bytearray(f.read())
 b[0]^=1
 with gzip.open(p,'wb') as f:f.write(b)
for impl in ['a','b']:reject('quintic_template_'+impl,'verify_quintic13_'+impl+'.py',files,broken_template)
(O/'corruption_results.json').write_text(json.dumps({'status':'PASS','controls':results,'pids':ledger},indent=2)+'\n')
