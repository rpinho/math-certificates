"""Resume after the standard union matrix-copy resource failure."""
from run_cg import run,verify
from numerics import register,write_json
import time
register('resume_union');start=time.monotonic()
run(['joint_lp.py','--input','union-input.json','--prefix','rounds/union'],'logs/union.log')
verify('rounds/union')
write_json('evidence/bootstrap-finished.json',{'resumed_union_wall_seconds':time.monotonic()-start})
