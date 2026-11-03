import copy,gzip,hashlib,json,pathlib,tempfile
from verify_c57c_forest import verify_part,aggregate,structure,Rejected,PARAMS
root=pathlib.Path.cwd();source=root/'results/c57c_phase_control055_mixed.jsonl.gz'
with gzip.open(source,'rt')as stream:head=json.loads(next(stream));rows=[json.loads(v)for v in stream]
defs=[v for v in rows if isinstance(v,dict)];leaves=[v for v in rows if not isinstance(v,dict)]
with tempfile.TemporaryDirectory(prefix='forest-verifier-control-',dir=root)as temporary:
 work=pathlib.Path(temporary);parts=[];receipts=[]
 for i,group in enumerate([leaves[:len(leaves)//2],leaves[len(leaves)//2:]]):
  path=work/f'part{i}.gz'
  with gzip.GzipFile(str(path),'wb',mtime=0)as out:
   for v in [head,*defs,*group]:out.write((json.dumps(v,separators=(',',':'))+'\n').encode())
  parts.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});receipt=work/f'part{i}.json';verify_part(path,receipt=receipt);receipts.append(receipt)
 manifest=work/'manifest.json';manifest.write_text(json.dumps({'format':'c57c-forest-v1','parameters':{k:head[k]for k in PARAMS},'parts':parts}));full=aggregate(manifest,receipts);assert full['verified_leaves']==len(leaves);print('FULL_FOREST_ACTUAL_ARITHMETIC_CONTROL_PASS',flush=True)
 for label,selected in [('gap',receipts[:1]),('overlap',[receipts[0],*receipts])]:
  try:aggregate(manifest,selected)
  except Rejected:print('REJECTED_'+label.upper(),flush=True)
  else:raise AssertionError(label+' accepted')
 saved=json.loads(receipts[-1].read_text());bad=copy.deepcopy(saved);bad['verified_leaves']-=1;receipts[-1].write_text(json.dumps(bad))
 try:aggregate(manifest,receipts)
 except Rejected:print('REJECTED_INCOMPLETE_ARITHMETIC',flush=True)
 else:raise AssertionError('incomplete replay accepted')
 receipts[-1].write_text(json.dumps(saved));data=json.loads(manifest.read_text());data['parts']=parts[:1];manifest.write_text(json.dumps(data))
 try:structure(manifest)
 except Rejected:print('REJECTED_MISSING_GLOBAL_SUBTREE',flush=True)
 else:raise AssertionError('missing subtree accepted')
print('ALL_COMPOSITE_FOREST_VERIFIER_CONTROLS_PASS')
