"""Replay both seeds, then solve and certify the standard full union master."""
import resource,time,json
from pathlib import Path
from run_cg import run,verify
from numerics import register,write_json
from checkpoint import checkpoint
register('bootstrap');start=time.monotonic()
run(['prepare_union.py'],'logs/prepare.log')
for tag,target in [('round6','0.2519964890'),('pr280-v4','0.2520079724')]:
    verifier='verify_'+tag.replace('-','_')+'.py';cert='prior_sources/'+tag+'-certificate.json';replay='evidence/'+tag+'-replay.json'
    run([verifier,'--certificate',cert,'--target',target,'--precision','256','--tol','1e-13','--out',replay],'logs/replay-'+tag+'.log')
    checkpoint(cert,verifier,replay)
run(['joint_lp.py','--input','union-input.json','--prefix','rounds/union'],'logs/union.log')
verify('rounds/union')
write_json('evidence/bootstrap-finished.json',{'wall_seconds':time.monotonic()-start})
