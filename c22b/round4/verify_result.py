"""Complete result replay, reusing our geometry, braid, and diagram checks."""
import json,pathlib,sys,hashlib,time
from fractions import Fraction as F
from verify import Checker,B,need,check_folder
import verify_projection
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent/'original'))
import verify_diagram

def check(folder):
    P=pathlib.Path(folder);start=time.time();raw=(P/'CONSTRUCTION.json').read_bytes();d=json.loads(raw);bound=json.loads((P/'BOUND.json').read_text())
    need(bound['construction_sha256']==hashlib.sha256(raw).hexdigest(),'E_RESULT_HASH')
    target=F('7.087580303');claim=F(bound['upper_bound']);need(claim<target,'E_RESULT_BAR')
    geometry=check_folder(P);braid=verify_projection.check(P)
    need(geometry['topology']['body_matrix']==braid['body_matrix'],'E_ACTION_BINDING')
    C=Checker(d);length,error=C.length_bound();need(length<B(claim),'E_FINAL_LENGTH')
    diagrams=verify_diagram.check({'kind':'finite_alternating_braid_diagrams_v1','cases':[{'m':2,'word':[1],'repeat':4*C.turns*n+3,'crossings':4*C.turns*n+3} for n in [1,2,3]]})
    return {'verdict':'CERTIFIED_CANDIDATE_C22B_UPPER_BOUND','qualification':'candidate, unverified by a third party; new modulated-radius proof steps are prose with no outside review','verifier':'separately written (same agent)','construction_sha256':hashlib.sha256(raw).hexdigest(),'upper_bound_exact':str(claim),'upper_bound_decimal':bound['upper_bound'],'target_exact':str(target),'margin_exact':str(target-claim),'family':f'T(2,{4*C.turns}n+3), n>=1, up to mirror','thickness_lower_exact':'1','length_per_crossing_interval':length.str(45),'length_taylor_remainder_interval':error.str(20),'cap_length_upper_exact':d['claim']['additive'],'geometry':geometry,'physical_braid':braid,'example_alternating_diagrams':diagrams,'seconds':time.time()-start}

if __name__=='__main__':print(json.dumps(check(sys.argv[1]),indent=2))
