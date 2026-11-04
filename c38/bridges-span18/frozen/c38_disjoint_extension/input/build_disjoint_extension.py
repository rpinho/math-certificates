"""Single-slope exact producer for a disjoint higher-span finite supplement."""
import pathlib,json,hashlib,datetime,shutil
from fractions import Fraction as Q
r=pathlib.Path(__file__).resolve().parent;base=r/'frozen/c38_secant_rescale';p22=r/'frozen/rectangle_point/w22_h18_30_c5';p23=r/'frozen/rectangle_point/w23_h18_18_c5_parallel'
s=json.loads((base/'input/seed.json').read_text());a=json.loads((p22/'replay.json').read_text());b=json.loads((p23/'replay.json').read_text())
for p in [p22,p23]:
 assert json.loads((p/'REJECTION_CONTROLS.json').read_text())['status']=='PASS';assert json.loads((p/'VERIFIED.json').read_text())['status']=='VERIFIED_CANDIDATE_UNREFEREED_FINITE_CLASS'
M=s['M'];e=max(Q(0),Q(int(a['num_lo'])-int(b['num_hi']),1<<96));assert e>0
L=Q(s['L17'])+Q(s['L18'])+e;slope=Q(s['slope'])+Q(690,M)*e;margin=L-1;k=(margin.numerator*slope.denominator)//(margin.denominator*slope.numerator);S=L-k*slope;assert S>=1 and min(M-k*1296,M-k*690)>=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
artifact=r/'frozen/c38_disjoint_extension';fr=artifact/'input';fr.mkdir(parents=True,exist_ok=False)
seed={'schema':'c38-disjoint-seed-v1','candidate_unrefereed':True,'family':'main spans1-18 union normalized span19-30 range22 cap5 irreducibles; expanded full coefficient vector unmaterialized','secant_relative':'../c38_secant_rescale','point22_relative':'../rectangle_point/w22_h18_30_c5','point23_relative':'../rectangle_point/w23_h18_18_c5_parallel','secant_manifest_sha256':sha(base/'input/MANIFEST.json'),'secant_seed_sha256':sha(base/'input/seed.json'),'point22_manifest_sha256':sha(p22/'input/MANIFEST.json'),'point23_manifest_sha256':sha(p23/'input/MANIFEST.json'),'point22_controls_sha256':sha(p22/'REJECTION_CONTROLS.json'),'point23_controls_sha256':sha(p23/'REJECTION_CONTROLS.json'),'M':M,'lower22':str(Q(int(a['num_lo']),1<<96)),'upper23':str(Q(int(b['num_hi']),1<<96)),'extra_lower':str(e),'extra_span_min':19,'extra_span_max':30,'extra_range':22,'extra_crossing_cap':5,'extra_degree':690,'k':k,'new_M':M-k,'S':str(S),'mu':str(Q(1<<27,M-k))}
(fr/'seed.json').write_text(json.dumps(seed,indent=2)+'\n')
for name in ['build_disjoint_extension.py','verify_disjoint_extension.py','test_disjoint_controls.py','PROOF_DISJOINT_EXTENSION.md','verify_rectangle_point_packet.py']:shutil.copy2(r/name,fr/name)
manifest={'schema':'c38-disjoint-input-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in fr.iterdir()}}
(fr/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for p in fr.iterdir():p.chmod(0o444)
print(seed['mu'],float(Q(seed['mu'])),k,float(S),sha(fr/'MANIFEST.json'))
