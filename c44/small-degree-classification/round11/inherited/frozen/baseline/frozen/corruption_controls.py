"""Rejection controls on disposable session-created artifact copies.
Runs each exact checker as a subprocess; imports no verification maths.
"""
import copy, json, os, pathlib, shutil, subprocess, sys, tempfile, time
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
O=R.parent/'receipts' if R.name=='frozen' else R/'receipts';O.mkdir(exist_ok=True)
scratch=O/'temporary_corruptions';scratch.mkdir(exist_ok=True)
ledger={'pid':os.getpid(),'tests':[]};record=O/'corruptions.json'
def save():record.write_text(json.dumps(ledger,indent=2)+'\n')
third=json.loads((R/'certificates/third_weight.json').read_text())
caps=json.loads((R/'certificates/caps.json').read_text())
flat=json.loads((R/'certificates/flat_controls.json').read_text())
lower=json.loads((R/'certificates/lower_results.json').read_text())
mutations=[]
def add(label,kind,operation):mutations.append((label,kind,operation))
add('missing_h14_case','third',lambda x:x['cases'].pop())
add('duplicate_case','third',lambda x:x['cases'].__setitem__(-1,copy.deepcopy(x['cases'][-2])))
add('false_control_ceiling','third',lambda x:x.__setitem__('conclusion','controls <= 12'))
add('false_partial_minimum','third',lambda x:x.__setitem__('minimum_partial_energy',15))
add('false_norm','third',lambda x:x.__setitem__('numerator_norm',55))
add('false_template_count','third',lambda x:x['template_counts'].__setitem__('14',752751))
add('false_good_set','third',lambda x:x['cases'][-1].__setitem__('goodbits',x['cases'][-1]['goodbits']^2))
add('false_seed_block','third',lambda x:x['cases'][-1]['blocks'].__setitem__(0,x['cases'][-1]['blocks'][0]^2))
add('unresolved_leaf_hidden','third',lambda x:x['cases'][-1].__setitem__('unresolved',1))
def false_count(x):
    row=x['rows'][1];row['R']=106;row['first_excluded']=107;x['caps']['6']='53/32'
add('false_mathematical_R6_106','caps',false_count)
add('false_selector_envelope','caps',lambda x:x['rows'][1].__setitem__('b','1/2'))
add('false_tail','caps',lambda x:x.__setitem__('tail','0'))
add('false_final_rational','caps',lambda x:x.__setitem__('bound','2'))
add('false_strict_decimal','caps',lambda x:x.__setitem__('strict_claim','2'))
add('missing_recurrence_row','caps',lambda x:x['rows'].pop())
add('false_degree_horizon','caps',lambda x:x.__setitem__('horizon',95))
add('false_character_signing','flat',lambda x:x['character_sign_vectors'].__setitem__(0,x['nonaffine_sign_vector']))
add('missing_flat_point','flat',lambda x:x['masks'].pop())
add('false_flat_denominator','flat',lambda x:x.__setitem__('denominator',31))
add('false_lower_parity_coefficient','lower',lambda x:x['entries'][0]['result']['terms'][0].__setitem__(1,x['entries'][0]['result']['terms'][0][1]+1))
add('false_lower_variable_count','lower',lambda x:x['entries'][0]['result'].__setitem__('relevant_variables',47))
def false_outer(x):
    entry=next(e for e in x['entries'] if e['family']=='shared-selector')
    entry['result']['outer_terms'][0][1]+=1
add('false_lower_outer_function','lower',false_outer)
add('false_lower_lift','lower',lambda x:x.__setitem__('best_lift','49/32'))
for label,kind,operation in mutations:
    with tempfile.TemporaryDirectory(prefix='control_',dir=scratch) as directory:
        work=pathlib.Path(directory)
        shutil.copytree(R/'certificates',work/'certificates')
        data=copy.deepcopy({'third':third,'caps':caps,'flat':flat,'lower':lower}[kind]);operation(data)
        filename={'third':'third_weight.json','caps':'caps.json','flat':'flat_controls.json','lower':'lower_results.json'}[kind]
        (work/'certificates'/filename).write_text(json.dumps(data)+'\n')
        scripts=({'flat':['verify_flat_controls_a.py','verify_flat_controls_b.py'],
                  'lower':['verify_lower_a.py','verify_lower_b.py']}.get(kind,['verify_packet_a.py','verify_packet_b.py']))
        for script in scripts:
            command=[sys.executable,str(R/script),str(work)]
            if kind=='third':command.append('--structure-only')
            if script=='verify_lower_b.py':
                binary=O.parent/'build/frozen_lower_b'
                if not binary.exists():binary=O.parent/'build/lower_outer_b'
                assert binary.exists();command.append(str(binary))
            row={'label':label,'checker':script,'command':command}
            log=O/(label+'_'+script[:-3]+'.log')
            with log.open('w') as output:
                child=subprocess.Popen(command,stdout=output,stderr=subprocess.STDOUT)
                row['pid']=child.pid;ledger['tests'].append(row);save()
                try:code=child.wait(timeout=180)
                finally:
                    if child.poll() is None:child.kill();child.wait()
            row['code']=code;row['rejected']=code!=0
            nested=work/'receipts/lower_b.json'
            if script=='verify_lower_b.py' and nested.exists():row['nested_children']=json.loads(nested.read_text()).get('children',[])
            save()
            assert code!=0,(label,script)
    print('rejected',label,flush=True)
ledger['status']='PASS';ledger['rejections']=len(ledger['tests']);save()
print('PASS',ledger['rejections'],'separate checker rejections',flush=True)
