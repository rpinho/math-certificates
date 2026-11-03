"""Standalone small-state exact controls for the frozen checker.
These are controls, never a replacement for the complete h=9 receipt.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,json,os,pathlib,shutil,subprocess,tempfile
from verify_c31_lower import check,sha
root=pathlib.Path(__file__).resolve().parent;packet=json.loads((root/'packet.json').read_text());rejected=[]
with tempfile.TemporaryDirectory(prefix='controls-',dir=root)as temporary:
 work=pathlib.Path(temporary)
 for key in ['generator','decoder','checker_kernel']:shutil.copyfile(root/packet[key],work/packet[key])
 exe=work/'generator';subprocess.run([os.environ.get('CC','cc'),'-O3','-march=native','-std=c11','-pthread',str(work/packet['generator']),'-o',str(exe)],check=True)
 env={k:v for k,v in os.environ.items()if not k.startswith('KLOW_')};env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 with (work/'generation.log').open('w')as log:subprocess.run([str(exe),'4','5','120','1',str(work/'control')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 vector=work/'control_w.bin';expected=packet['recipe'][0]['sha256']
 if sha(vector)!=expected:raise ValueError('small procedural control hash mismatch')
 data=copy.deepcopy(packet);data.update(history=5,classes=(16**5+16*4**5+16)//48,r='459351854/1073741824',decoded_sha256=expected,decoded_filename=vector.name)
 meta=work/'packet.json';meta.write_text(json.dumps(data));positive=check(meta,vector,1)
 def reject(name,metadata,path=vector):
  meta.write_text(json.dumps(metadata))
  try:check(meta,path,1)
  except (ValueError,subprocess.CalledProcessError):rejected.append(name);print('REJECTED_AS_REQUIRED',name,flush=True)
  else:raise AssertionError('invalid control accepted: '+name)
 altered=copy.deepcopy(data);altered['r']='1/2';reject('inflated drift',altered)
 zeros=work/'zero.bin';zeros.write_bytes(b'\0'*vector.stat().st_size);altered=copy.deepcopy(data);altered['decoded_sha256']=sha(zeros);reject('rehashed zero potential',altered,zeros)
 bad=work/'one_bad_byte.bin';raw=bytearray(vector.read_bytes());raw[0]^=1;bad.write_bytes(raw);reject('corrupted vector bytes',data,bad)
 altered=copy.deepcopy(data);altered['decoder_sha256']='0'*64;reject('corrupted decoder hash',altered)
 altered=copy.deepcopy(data);altered['r']='1';reject('invalid drift domain',altered)
 kernel=work/data['checker_kernel'];kernel.write_text(kernel.read_text()+'\n/* deliberately corrupted copy */\n');reject('corrupted checker source',data)
result={'status':'ALL_LOWER_CONTROLS_PASS','positive_control_history':5,'positive_control_classes':positive['classes'],'positive_control_min_numerator':positive['min_numerator'],'rejected':rejected,'qualification':'small-state controls; use the complete h9 exact receipt for the headline bound'}
(root/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));print('ALL_LOWER_CONTROLS_PASS')
