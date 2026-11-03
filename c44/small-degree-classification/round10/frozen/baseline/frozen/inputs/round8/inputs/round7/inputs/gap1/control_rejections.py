"""Tamper controls exercise arithmetic directly, beyond the input-hash gate."""
from pathlib import Path
import copy,hashlib,importlib.util,json,subprocess,resource
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent',R/'verify_packet.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
c=json.loads((R/'certificate.json').read_text())
results=[];child_pids=[]
def reject(label,fn):
    try:fn()
    except (AssertionError,subprocess.CalledProcessError):results.append({'control':label,'rejected':True})
    else:raise AssertionError('forgery accepted: '+label)
for field,value in [('point_pair_pair','1/3'),('pair_triple','1/2'),('three_pairs','3/4')]:
    bad=copy.deepcopy(c);bad['top_energy_caps'][field]=value
    reject('false energy cap '+field,lambda:v.verify_structure(bad))
bad=copy.deepcopy(c);bad['types'].pop();reject('missing structural type',lambda:v.verify_structure(bad))
bad=copy.deepcopy(c);bad['types'][0]['fixed']=2;reject('incorrect structural degree',lambda:v.verify_structure(bad))
bad=copy.deepcopy(c);bad['external_R3']=9;reject('false cubic ceiling',lambda:v.verify_structure(bad))
out=R/'red_controls';out.mkdir(exist_ok=True)
w=json.loads((R/'witness22.json').read_text())
for label,mutate in [('sign',lambda z:z['terms'][0].__setitem__(1,-z['terms'][0][1])),
                     ('denominator',lambda z:z.__setitem__('denominator',7)),
                     ('mask',lambda z:z['terms'][0].__setitem__(0,0)),
                     ('count',lambda z:z.__setitem__('variables',23))]:
    bad=copy.deepcopy(w);mutate(bad);p=out/('witness_'+label+'.json');p.write_text(json.dumps(bad))
    reject('witness '+label,lambda:v.verify_witness(p))
# Flip one catalogue bit: verify directly rather than rejecting only its source hash.
b=bytearray((R/'sources/F10T6.txt').read_bytes());b[0]=ord('1') if b[0]==ord('0') else ord('0')
p=out/'catalogue_bit_flip.txt';p.write_bytes(b)
def malformed_catalogue():
    child=subprocess.Popen([str(R/'verify_catalogue'),str(p)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    child_pids.append(child.pid);child.communicate()
    if child.returncode:raise subprocess.CalledProcessError(child.returncode,child.args)
reject('catalogue truth-table corruption',malformed_catalogue)
# Check mathematical caps directly so a stale hash cannot be the rejection reason.
for label,mutate in [('unjustified R4=21',lambda z:z.__setitem__('quartic_R',21)),
                     ('false R5=52 cap',lambda z:z['caps'].__setitem__('5','13/8')),
                     ('false cubic energy envelope',lambda z:z.__setitem__('envelope','D<=1+E3/8')),
                     ('false equality signature',lambda z:z['equality_signatures'][1].__setitem__(2,8))]:
    bad=copy.deepcopy(c);mutate(bad)
    reject(label,lambda:v.verify_caps(bad))
(R/'control_rejections.json').write_text(json.dumps({'status':'PASS','controls':results,'child_pids':child_pids},indent=2)+'\n')
print(json.dumps({'status':'PASS','rejected_controls':len(results)},indent=2))
