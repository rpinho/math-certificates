import subprocess,json,pathlib,gzip,shutil
R=pathlib.Path(__file__).resolve().parent
rows=[]
for cmd in [['g++','-O3','-std=c++17','make_quintic13_nonhomogeneous_certificate.cpp','-o','make_quintic13_nonhomogeneous_certificate'],['./make_quintic13_nonhomogeneous_certificate']]:
 p=subprocess.Popen(cmd,cwd=R);rows.append({'pid':p.pid,'command':cmd})
 (R/'receipts/quintic13_certificate_pids.json').write_text(json.dumps(rows,indent=2)+'\n')
 try:code=p.wait(timeout=3600)
 finally:
  if p.poll() is None:p.terminate();p.wait()
 rows[-1]['code']=code;assert code==0
with (R/'quintic_minimum_templates.bin').open('rb') as src,gzip.open(R/'quintic_minimum_templates.bin.gz','wb') as dst:shutil.copyfileobj(src,dst)
# This is a temporary binary generated in this session; the frozen gzip remains.
(R/'quintic_minimum_templates.bin').unlink()
(R/'receipts/quintic13_certificate_pids.json').write_text(json.dumps(rows,indent=2)+'\n')
