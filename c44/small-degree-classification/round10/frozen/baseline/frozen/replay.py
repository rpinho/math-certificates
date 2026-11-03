"""Self-contained frozen replay; standard Python and C++17 only.
Copied as frozen/replay.py. All mutable output stays beside the packet.
"""
import argparse,datetime,hashlib,json,os,pathlib,shutil,signal,subprocess,sys,time
parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=8);parser.add_argument('--replay',action='store_true');args=parser.parse_args()
here=pathlib.Path(__file__).resolve().parent
F=here if here.name=='frozen' else here.parent/'frozen';R=F.parent
assert 1<=args.workers<=10 and os.getpriority(os.PRIO_PROCESS,0)>=10
os.chdir(R)
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
O=R/'receipts';O.mkdir(exist_ok=True);(R/'build').mkdir(exist_ok=True)
plans=R/'replay_plans';plans.mkdir(exist_ok=True)
M=json.loads((F/'MANIFEST.json').read_text());manifest_hash=hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest()
def hashes():
    assert {str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(M['sha256'])|{'MANIFEST.json'}
    for name,digest in M['sha256'].items():assert hashlib.sha256((F/name).read_bytes()).hexdigest()==digest,name
hashes()
S=json.loads((F/'certificates/third_weight.json').read_text())
ledger={'pid':os.getpid(),'manifest_sha256':manifest_hash,'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stages':[]}
record=O/'frozen_replay_ledger.json'
def save():record.write_text(json.dumps(ledger,indent=2)+'\n')
active=None
def stop(signum=None,frame=None):
    if active is not None and active.poll() is None:
        active.terminate()
        try:active.wait(timeout=10)
        except subprocess.TimeoutExpired:active.kill();active.wait()
    if signum is not None:raise KeyboardInterrupt
for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(sig,stop)
def stage(label,tasks,workers):
    global active
    plan=plans/(label+'.json');plan.write_text(json.dumps({'label':label,'workers':workers,'tasks':tasks},indent=2)+'\n')
    command=[sys.executable,str(F/'run_batch.py'),str(plan)]
    if args.replay:command.append('--replay')
    active=subprocess.Popen(command)
    row={'label':label,'pid':active.pid};ledger['stages'].append(row);save()
    code=active.wait();row['code']=code;active=None;save()
    assert code==0,label
    result=json.loads((O/(label+'_ledger.json')).read_text());assert result['status']=='PASS',label
def task(label,command,timeout=1800):return dict(label=label,command=list(map(str,command)),timeout=timeout,memory_mb=6000)
try:
    compile_tasks=[]
    for impl in ('a','b'):
        compile_tasks.append(task('third_'+impl,['g++','-O3','-std=c++17',F/('verify_third_'+impl+'.cpp'),'-o',R/('build/frozen_third_'+impl)]))
    compile_tasks.extend([
      task('lower_b',['g++','-O3','-std=c++17',F/'verify_lower_outer_b.cpp','-o',R/'build/frozen_lower_b']),
      task('completion_control',['g++','-O2','-std=c++17',F/'inputs/round8/control_completion.cpp','-o',R/'build/frozen_completion_control']),
      task('integer_gap',['g++','-O2','-std=c++17',F/'inputs/round8/inputs/round7/control_integer_gap.cpp','-o',R/'build/frozen_integer_gap'])])
    stage('frozen_compile',compile_tasks,2)
    stage('frozen_structure',[task('a',[sys.executable,F/'verify_packet_a.py',F,'--structure-only']),task('b',[sys.executable,F/'verify_packet_b.py',F,'--structure-only'])],2)
    inherited=R/('replay_inherited_'+str(os.getpid()))
    shutil.copytree(F/'inputs/round8',inherited)
    # Every copied file is checked against the frozen original before use.
    for original in (F/'inputs/round8').rglob('*'):
        if original.is_file():assert (inherited/original.relative_to(F/'inputs/round8')).read_bytes()==original.read_bytes()
    premise_tasks=[]
    for name in ('completion_a','completion_b'):
        premise_tasks.append(task(name,[sys.executable,inherited/('verify_'+name+'.py'),inherited]))
    seventh=inherited/'inputs/round7'
    for name in ('quartic_a','quartic_b','quintic_a','quintic_b','quintic13_a','quintic13_b'):
        premise_tasks.append(task(name,[sys.executable,seventh/('verify_'+name+'.py'),seventh]))
    fourth=seventh/'inputs/gap1'
    resource_wrapper=fourth/'run_checks_job.py'
    original_script=(fourth/'run_checks.py').read_text()
    assert '40*1024**3' in original_script
    resource_wrapper.write_text(original_script.replace('40*1024**3','6_000_000_000'))
    premise_tasks.append(task('R4_full',[sys.executable,resource_wrapper],1800))
    stage('frozen_inherited',premise_tasks,min(args.workers,3))

    (O/'frozen_classification').mkdir(exist_ok=True)
    classification=[]
    # Start the largest A orbit first to avoid a needless late straggler.
    cases=sorted(S['cases'],key=lambda c:(0 if (c['n'],c['kind'],c['case_index'])==(14,'hom',0) else 1,-c['n'],c['kind'],c['case_index']))
    for c in cases:
        name=f"n{c['n']}_{c['kind']}_{c['case_index']}";file=F/'certificates/third_cases'/c['file']
        for impl in ('a','b'):
            output=O/'frozen_classification'/(impl+'_'+name+'.json')
            command=[R/('build/frozen_third_'+impl)]
            if impl=='a':command.append('--case-file')
            command.extend([file,output])
            classification.append(task(impl+'_'+name,command,3600))
    extras=[task('packet_a',[sys.executable,F/'verify_packet_a.py',F]),task('packet_b',[sys.executable,F/'verify_packet_b.py',F]),
            task('signed_flat_a',[sys.executable,F/'verify_flat_controls_a.py',F]),task('signed_flat_b',[sys.executable,F/'verify_flat_controls_b.py',F]),
            task('lower_a',[sys.executable,F/'verify_lower_a.py',F]),task('lower_b',[sys.executable,F/'verify_lower_b.py',F,R/'build/frozen_lower_b']),
            task('completion_control',[R/'build/frozen_completion_control']),task('integer_gap',[R/'build/frozen_integer_gap']),
            task('corruptions',[sys.executable,F/'corruption_controls.py',F])]
    controls=json.loads((F/'certificates/flat_controls.json').read_text())
    for c in controls['cases']:
        for impl in ('a','b'):
            extras.append(task('flat_'+impl+'_'+c['file'][:-4],[R/('build/frozen_third_'+impl),'--flat-control',F/'certificates/flat_cases'/c['file'],str(int(c['expected']))]))
    # Classification and arithmetic read independent immutable files.
    stage('frozen_mathematics',classification[:2]+extras+classification[2:],args.workers)
    totals={impl:{'cases':0,'nodes':0,'unresolved':0,'flat_residual_rejections':0} for impl in ('a','b')}
    for c in S['cases']:
        name=f"n{c['n']}_{c['kind']}_{c['case_index']}"
        for impl in ('a','b'):
            data=json.loads((O/'frozen_classification'/(impl+'_'+name+'.json')).read_text())
            assert (data['n'],data['norm'],data['goodbits'],data['unresolved'])==(c['n'],56,c['goodbits'],0)
            if impl=='a':assert data['templates']==S['template_counts'][str(c['n'])]
            totals[impl]['cases']+=1
            for key in ('nodes','unresolved','flat_residual_rejections'):totals[impl][key]+=data.get(key,0)
    assert all(x['cases']==189 and x['unresolved']==0 for x in totals.values())
    P=json.loads((F/'certificates/caps.json').read_text())
    assert json.loads((O/'packet_a.json').read_text())['bound']==P['bound']==json.loads((O/'packet_b.json').read_text())['bound']
    assert json.loads((O/'lower_a.json').read_text())['best_lift']==json.loads((O/'lower_b.json').read_text())['best_lift']=='3/2'
    assert json.loads((O/'corruptions.json').read_text())['status']=='PASS'
    hashes()
    receipt={'status':'PASS','qualification':'candidate, unrefereed; external completeness premises explicit',
             'manifest_sha256':manifest_hash,'bound':P['bound'],'strict_claim':P['strict_claim'],
             'R5_upper':50,'R6_upper':107,'lower_bound':'3/2','classification':totals,
             'artifact_rejections':json.loads((O/'corruptions.json').read_text())['rejections'],
             'ended':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (O/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    ledger['status']='PASS';ledger['ended']=receipt['ended'];save();print(json.dumps(receipt),flush=True)
finally:
    stop();save()
