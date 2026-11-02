"""Remove only regenerable temporary files created in this own-job session.
Selected immutable artifacts and the proof bundle are retained and checked first.
"""
import os,json,gzip,hashlib
from pathlib import Path
root=Path.cwd();assert root.name=='math_c89cr2_1101'
facts=json.loads(Path('CERTIFICATES.json').read_text())
for name,info in facts.items():
 data=Path('certificates',name).read_bytes();raw=gzip.decompress(data) if name.endswith('.gz') else data;assert hashlib.sha256(raw).hexdigest()==info['sha256_certificate']
receipt=json.loads(Path('receipts/bundle_receipt.json').read_text());assert hashlib.sha256(Path(receipt['archive']).read_bytes()).hexdigest()==receipt['sha256']
removed=[]
def discard(p):
 if not (p.exists() or p.is_symlink()):return
 assert p.is_relative_to(root)
 size=p.lstat().st_size;removed.append({'path':str(p.relative_to(root)),'bytes':size});p.unlink()
# These working tables, solver states and intermediate candidates were all made
# during this session. The selected frozen bytes are retained in certificates/,
# proof_bundle/, and the verified archive before their working copies are removed.
for directory,dirs,files in os.walk(root/'artifacts',followlinks=False):
 for name in files:discard(Path(directory)/name)
 for name in dirs:
  p=Path(directory)/name
  if p.is_symlink():discard(p)
for base in ['openai_math_tree.json','plasma-ai_erdos_tree.json']:
 p=root/'sources'/base;z=Path(str(p)+'.gz')
 if p.exists():assert z.exists() and gzip.decompress(z.read_bytes())==p.read_bytes();discard(p)
for name in ['sources/published_certificates.zip','sources/published_c5.json','check_manifest.py','verify_legacy_gmp.cpp','verify_lift9.cpp']:
 discard(root/name)
for p in root.iterdir():
 if p.is_file() and (p.name=='core' or (p.name.startswith('core.') and p.name[5:].isdigit())):discard(p)
result={'PASS':True,'removed_temporary_files':len(removed),'removed_bytes':sum(x['bytes'] for x in removed),'selected_certificates_and_archive_rechecked':True,'files':removed}
Path('receipts/temporary_cleanup.json').write_text(json.dumps(result,indent=2));print('PASS temporary cleanup',len(removed),'files',result['removed_bytes'],'bytes')
