"""Build a reviewable point certificate only after the complete frozen replay."""
import pathlib,json,hashlib,shutil,sys
from assemble_strip import assemble
jobroot=pathlib.Path(__file__).resolve().parent
root=pathlib.Path(sys.argv[1]);fr=root/'input';replay=root/'replay'
manifest=fr/'INPUT_MANIFEST.json';m=json.loads(manifest.read_text())
for rel,sha in m['sha256'].items():assert hashlib.sha256((fr/rel).read_bytes()).hexdigest()==sha
receipts=json.loads((replay/'RECEIPTS.json').read_text());assert len(receipts['spans'])==18
assert receipts['input_manifest_sha256']==hashlib.sha256(manifest.read_bytes()).hexdigest()
for l,rec in enumerate(receipts['spans'],1):
 assert rec['l']==l and rec['status']=='COMPLETE_FROZEN_REPLAY_MATCH'
 assert rec['input_sha256']==hashlib.sha256((fr/('production/span_%d.json'%l)).read_bytes()).hexdigest()
 assert rec['output_sha256']==hashlib.sha256((replay/('span_%d.json'%l)).read_bytes()).hexdigest()
result=assemble(replay,18,51081913,True)
(root/'SEARCH_ASSEMBLY.json').write_text(json.dumps(result,indent=2)+'\n')
if not result['P_ge_1']:raise SystemExit('full finite-family lower sum is below 1; no positive packet created')
for name in ['verify_strip.cpp','PROOF_FINITE_STRIP.md','BAR_PUBLIC.json','PRIOR_ART_PUBLIC.md']:
 dst=root/name;src=fr/name
 if dst.exists():assert dst.read_bytes()==src.read_bytes()
 else:shutil.copy2(src,dst)
finite_names=[]
if m.get('terminal_span_mode')=='FINITE_LAST_SPAN_LOWER_ONLY':
 fc=json.loads((fr/'finite/MANIFEST.json').read_text());finite_names=list(fc['sha256'])
 for name in finite_names:
  src=fr/'finite'/name;dst=root/name
  if dst.exists():assert dst.read_bytes()==src.read_bytes()
  else:shutil.copy2(src,dst)
extras=['verify_packet.py','test_point_packet_controls.py','test_span17_stop_controls.py','verify_span17_stop.py','build_point_packet.py','assemble_strip.py','LICENSE_PLANOCKA','CREDITS.md','ARITHMETIC_PROOF.md','STATE_PROOF_APPENDIX.md','PACKET_README.md']
for name in extras:
 src=jobroot/name;dst=root/name
 if dst.exists():assert dst.read_bytes()==src.read_bytes()
 else:shutil.copy2(src,dst)
source_names=['verify_strip.cpp','PROOF_FINITE_STRIP.md','BAR_PUBLIC.json','PRIOR_ART_PUBLIC.md']+extras+finite_names
packet={'schema':'c38-finite-strip-v1','candidate_unrefereed':True,'target':{'p':1051,'q':400},'L':18,'M':51081913,'terminal_span_mode':m.get('terminal_span_mode','FULL_WIDTH_CERTIFIED'),'coefficient_class':'all irreducible bridges with span-specific transverse caps','coefficient_encoding':'exact finite combinatorial specification; expanded integer vector not materialized','max_degree':result['max_degree'],'P_lower':result['P_lower'],'frozen_input_manifest':{'path':'input/INPUT_MANIFEST.json','sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()},'frozen_replay_receipts':{'path':'replay/RECEIPTS.json','sha256':hashlib.sha256((replay/'RECEIPTS.json').read_bytes()).hexdigest()},'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in source_names},'spans':[]}
for l in range(1,19):
 prod=fr/('production/span_%d.json'%l);d=json.loads(prod.read_text());sep=replay/('span_%d.json'%l)
 packet['spans'].append({'l':l,'w':d['w'],'production':{'path':str(prod.relative_to(root)),'sha256':hashlib.sha256(prod.read_bytes()).hexdigest()},'separate':{'path':str(sep.relative_to(root)),'sha256':hashlib.sha256(sep.read_bytes()).hexdigest()}})
(root/'packet.json').write_text(json.dumps(packet,indent=2)+'\n');print('PACKET_CREATED P_lower=',result['P_decimal_diagnostic'],'degree=',result['max_degree'])
