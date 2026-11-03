"""Corrupt artifacts and require rejection by each exact verifier."""
import copy,json,pathlib,subprocess,sys,tempfile
F=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve();out.mkdir(exist_ok=True,parents=True)
caps=json.loads((F/'certificates/caps.json').read_text());lemma=json.loads((F/'certificates/near_equality.json').read_text())
variants=[]
def add(name,which,fn):
 c=copy.deepcopy(caps);l=copy.deepcopy(lemma);fn(c if which=='caps' else l);variants.append((name,c,l))
add('r7_too_small','caps',lambda c:c['rows'][2].update(R=228,first_excluded=229))
add('r7_too_large','caps',lambda c:c['rows'][2].update(R=230,first_excluded=231))
add('r5_unproved','caps',lambda c:c['rows'][0].update(R=49,first_excluded=50))
add('wrong_base_R4','caps',lambda c:c['base_counts'].update({'4':21}))
add('missing_first_row','caps',lambda c:c['rows'].pop(0))
add('wrong_bound','caps',lambda c:c.update(bound='2'))
add('wrong_tail','caps',lambda c:c.update(tail='0'))
add('false_strict_claim','caps',lambda c:c.update(strict_claim='2.0'))
add('wrong_baseline','caps',lambda c:c.update(previous_bound='3'))
add('omit_near_lemma','caps',lambda c:c.update(near_equality_artifact='absent.json'))
add('wrong_tensor_deficit','lemma',lambda l:l['degree6_tensor_rows'][0].update(deficit=0))
add('missing_tensor_type','lemma',lambda l:l['degree6_tensor_rows'].pop())
add('false_direct_constant','lemma',lambda l:l['direct_case'].update(constant_square='1'))
add('wrong_partial_gap','lemma',lambda l:l['direct_case'].update(partial_gap=8))
add('omit_lemma_hypothesis','lemma',lambda l:l.update(statement='all controls excluded'))
add('wrong_sign_rank','lemma',lambda l:l['sign_completion']['cube_face_ranks'][0].update(rank=0))
add('missing_sign_dimension','lemma',lambda l:l['sign_completion']['cube_face_ranks'].pop())
add('erase_dimension_exception','lemma',lambda l:l['sign_completion'].update(dimension_two_exception=False))
add('wrong_range_argument','lemma',lambda l:l['sign_completion'].update(range='two components allowed'))
add('omit_sign_completion','lemma',lambda l:l.pop('sign_completion'))
results=[]
with tempfile.TemporaryDirectory(prefix='c44-r10-rejection-',dir=out) as temp:
 root=pathlib.Path(temp);(root/'certificates').mkdir();(root/'receipts').mkdir()
 for name,c,l in variants:
  (root/'certificates/caps.json').write_text(json.dumps(c));(root/'certificates/near_equality.json').write_text(json.dumps(l))
  for impl in ('a','b'):
   run=subprocess.run([sys.executable,str(F/f'verify_{impl}.py'),str(root)],capture_output=True,text=True,timeout=60)
   assert run.returncode!=0,(name,impl)
   results.append(dict(control=name,verifier=impl,rejected=True,exit=run.returncode,error=run.stderr[-500:]))
receipt=dict(status='PASS',corrupted_artifacts=len(variants),rejections=len(results),results=results)
(out/'rejection_controls.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS',len(results),'rejections',flush=True)
