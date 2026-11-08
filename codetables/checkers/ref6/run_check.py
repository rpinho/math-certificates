"""Reproduce the exact check, with four CPU threads and measured runtimes."""
import datetime,json,platform,subprocess,sys,time
from pathlib import Path
start=time.perf_counter();stages=[];pids=[]
def run(name,args,output):
    begin=time.perf_counter()
    with open(output,'w') as f:
        p=subprocess.Popen(args,stdout=f);pids.append(p.pid)
        Path('worker_pids.json').write_text(json.dumps(pids)+'\n')
        try:code=p.wait()
        except BaseException:
            p.terminate();p.wait();raise
    if code:raise RuntimeError(f'{name} failed with {code}; inspect {output}')
    stages.append({'stage':name,'seconds':time.perf_counter()-begin})
run('compile',['clang++','-O3','-std=c++17','-pthread','enumerate.cpp','-o','enumerate'],'compile.log')
run('field_rank_BCH',[sys.executable,'checker.py'],'initial_check.log')
run('subcode_information_sets_RS_control',[sys.executable,'prepare.py'],'prepare.log')
run('RS_BZ',['./enumerate','rs_input.txt','1'],'rs_bz.jsonl')
run('candidate_BZ',['./enumerate','bz_input.txt','4'],'bz_result.jsonl')
run('BCH_cases_and_assemble',[sys.executable,'finish_distance.py'],'finish_distance.log')
result={'utc_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'python':platform.python_version(),'max_threads':4,'stages':stages,'total_seconds':time.perf_counter()-start,'all_children_exited':True,'pids':pids}
Path('run_metadata.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
