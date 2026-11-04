"""Exact one-slope producer for the finite-family secant extension."""
import pathlib,json,hashlib,datetime,shutil
from fractions import Fraction as Q
r=pathlib.Path(__file__).resolve().parent;base=r/'frozen/c38_finite_strip';stop=r/'frozen/span17_all_length_stop';span=r/'frozen/c38_span_degree'
v=json.loads((base/'FULL_ACCEPTANCE.json').read_text());u=json.loads((stop/'FULL_ACCEPTANCE.json').read_text());assert u['fresh_full_replay'] is True
controls=json.loads((stop/'REJECTION_CONTROLS.json').read_text());assert controls['status']=='PASS' and len(controls['controls'])==11
M=v['M'];L18=Q(v['spans'][-1]['finite_irreducible_lower']);L17=Q(v['P_lower'])-L18;U=Q(u['endpoint_upper_sums'][1]);degree=v['spans'][-1]['l']*v['spans'][-1]['w'];slope=(U-L17)/314+Q(degree,M)*L18;assert slope>0
margin=L17+L18-1;k=(margin.numerator*slope.denominator)//(margin.denominator*slope.numerator);S=L17+L18-k*slope;assert S>=1 and M-k*degree>=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
artifact=r/'frozen/c38_secant_rescale';fr=artifact/'input';fr.mkdir(parents=True,exist_ok=False)
seed={'schema':'c38-secant-seed-v1','candidate_unrefereed':True,'family':'unchanged exact finite main bridge family; expanded full coefficient vector unmaterialized','main_relative':'../c38_finite_strip','stop_relative':'../span17_all_length_stop','span_relative':'../c38_span_degree','main_packet_sha256':sha(base/'packet.json'),'span_manifest_sha256':sha(span/'input/MANIFEST.json'),'stop_manifest_sha256':sha(stop/'input/INPUT_MANIFEST.json'),'stop_full_sha256':sha(stop/'FULL_ACCEPTANCE.json'),'stop_controls_sha256':sha(stop/'REJECTION_CONTROLS.json'),'M':M,'upper_point_M':51082227,'L17':str(L17),'L18':str(L18),'U':str(U),'degree18':degree,'k':k,'new_M':M-k,'slope':str(slope),'S':str(S),'mu':str(Q(1<<27,M-k))}
(fr/'seed.json').write_text(json.dumps(seed,indent=2)+'\n')
for name in ['build_secant_rescale.py','verify_secant_rescale.py','test_secant_controls.py','PROOF_SECANT_RESCALE.md']:shutil.copy2(r/name,fr/name)
manifest={'schema':'c38-secant-input-v1','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':{p.name:sha(p) for p in fr.iterdir()}}
(fr/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for p in fr.iterdir():p.chmod(0o444)
print(seed['mu'],float(Q(seed['mu'])),k,float(S),sha(fr/'MANIFEST.json'))
