"""Build and independently hash-check the selected frozen proof bundle."""
import json,hashlib,tarfile,gzip,io,shutil
from pathlib import Path
root=Path.cwd();dest=root/'proof_bundle';dest.mkdir(exist_ok=True)
files=['CERTIFICATE_README.md','PROOF.md','REPRODUCE.md','PRIOR_ART.md','CERTIFICATES.json']
files += [str(p) for p in sorted(Path('certificates').glob('*')) if p.is_file()]
files += ['sources/graph8.g6','sources/graph9.g6','sources/initial_inventory_summary.json','sources/param_csdp_unordered.txt']
files += [str(p) for p in sorted(Path('sources/final').glob('*')) if p.is_file()]
skip={'monitor.py','stop_workers.py','materialize_final.py','build_bundle.py','refresh_sources.py','cleanup_temporaries.py'}
files += [str(p) for p in sorted(Path('scripts').glob('*')) if p.is_file() and p.name not in skip and p.suffix in {'.py','.cpp','.hpp','.sh','.dat-s'}]
logs=['environment.json','public_input_hashes.json','resource_summary.json','worker_cleanup.json','exact_slacks.json','graph9_completeness.json','graph9_completeness.log','csdp_exact.log','csdp_legacy.log','csdp_lift9_exact.log','csdp_lift9_independent.log','k5_column_exact.log','k5_column_legacy.log','ppss_baseline.log','published_summary.log','negative_controls.json','negative_controls.log','negative_graph9.log','csdp_pipeline.json','csdp_lift9_pipeline.json','csdp_original8_warm.log','csdp_export_factors.log','csdp_polish.log','goodman_csdp.log','goodman_parallel.log','final_sources.log','closeout_sources.log','closeout_source_comparison.json']
files += ['receipts/'+name for name in logs]
for name in files:
 p=Path(name);assert p.is_file(),name;out=dest/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out)
manifest={'status':'candidate and unrefereed','hash_algorithm':'SHA256','files':{}}
for name in sorted(set(files)):
 data=(dest/name).read_bytes();manifest['files'][name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(dest/'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest,indent=2));shutil.copyfile(dest/'ARTIFACT_MANIFEST.json',root/'ARTIFACT_MANIFEST.json')
# Check certificate contents against the separately recorded exact-claim map.
facts=json.loads((dest/'CERTIFICATES.json').read_text())
for name,info in facts.items():
 data=(dest/'certificates'/name).read_bytes();raw=gzip.decompress(data) if name.endswith('.gz') else data
 assert hashlib.sha256(raw).hexdigest()==info['sha256_certificate'];h=raw.splitlines()[0].split();assert str(__import__('fractions').Fraction(int(h[4]),int(h[5])))==info['bound']
initial=json.loads((dest/'sources/initial_inventory_summary.json').read_text())['root_hashes'];final=json.loads((dest/'sources/final/root_hashes.json').read_text());assert initial==final
archive=root/'ramsey_multiplicity_candidates.tar.gz'
with archive.open('wb') as output:
 with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0) as zipped:
  with tarfile.open(fileobj=zipped,mode='w',format=tarfile.PAX_FORMAT) as tar:
   for p in sorted(dest.rglob('*')):
    if not p.is_file():continue
    data=p.read_bytes();rel=p.relative_to(dest).as_posix();entry=tarfile.TarInfo('ramsey_candidates/'+rel);entry.size=len(data);entry.mtime=0;entry.mode=0o644;entry.uid=entry.gid=0;entry.uname=entry.gname='';tar.addfile(entry,io.BytesIO(data))
with tarfile.open(archive,'r:gz') as tar:
 members={m.name:tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()}
 assert len(members)==len(manifest['files'])+1
 for name,info in manifest['files'].items():
  data=members['ramsey_candidates/'+name];assert len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256'],name
receipt={'PASS':True,'archive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'manifest_files':len(manifest['files']),'archive_replay':'every archive member independently matched its manifest hash and byte count','root_inventory_recheck':'all seven initial/final root hashes equal'}
Path('receipts/bundle_receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
