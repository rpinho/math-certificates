"""Rejection controls derived from the actual final composite artifact."""
import argparse,copy,gzip,hashlib,json,pathlib,tempfile
from verify_c57c_forest import structure,Arithmetic,prepare,Rejected,code_hashes
p=argparse.ArgumentParser();p.add_argument('manifest',nargs='?',default='C57_FOREST.json');args=p.parse_args()
ROOT=pathlib.Path(__file__).resolve().parent;source=ROOT/args.manifest;data=json.loads(source.read_text());passed=[]
def reject(label,call):
 try:call()
 except (Rejected,ValueError,KeyError) as error:passed.append(label);print('REJECTED_'+label+': '+str(error),flush=True)
 else:raise AssertionError(label+' unexpectedly accepted')
with tempfile.TemporaryDirectory(prefix='actual-forest-controls-',dir=ROOT)as temporary:
 work=pathlib.Path(temporary);(work/'cert_parts').symlink_to(ROOT/'cert_parts',target_is_directory=True);target=work/'bad_manifest.json'
 for label in ['missing_part','duplicate_part','corrupt_sha','false_parameters']:
  bad=copy.deepcopy(data)
  if label=='missing_part':bad['parts'].pop()
  elif label=='duplicate_part':bad['parts'].append(bad['parts'][0])
  elif label=='corrupt_sha':bad['parts'][0]['sha256']='0'*64
  else:bad['parameters']['radius']='13/20'
  target.write_text(json.dumps(bad));reject(label,lambda:structure(target))
with gzip.open(ROOT/data['parts'][0]['file'],'rt')as f:head=json.loads(next(f))
false={'kind':'taylor4','phase_rule':'j*theta/2','forms':[{'mode':0,'z':[[1,0]]+[[0,0]for _ in range(6)],'weight':'1'}],'area_weight':'1'}
prepared_false=prepare(false) # Positive area weight must pass witness validation.
A=Arithmetic(head,192);reject('identically_positive_false_exclusion',lambda:A.leaf(((0,40),)*4,prepared_false))
bad=copy.deepcopy(false);bad['forms'][0]['weight']='-1';reject('negative_weight',lambda:prepare(bad))
bad=copy.deepcopy(false);bad['phase_rule']='j*theta';reject('unsupported_phase',lambda:prepare(bad))
bad=copy.deepcopy(head);bad['t']='1';reject('invalid_transform_t',lambda:Arithmetic(bad))
bad=copy.deepcopy(head);bad['coefficient_caps']=['0','0','0','0'];reject('false_coefficient_caps',lambda:Arithmetic(bad))
result={'status':'ALL_ACTUAL_FOREST_REJECTION_CONTROLS_PASSED','manifest':source.name,'manifest_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checker_files':code_hashes(),'controls':passed,'qualification':'rejection controls only, no substitute for exhaustive arithmetic'}
(ROOT/'results/c57c_actual_forest_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
