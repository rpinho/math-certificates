"""Separately written (same agent) frozen directed rectangle packet check."""
import argparse,datetime,hashlib,json,pathlib,sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(200000)
class Reject(Exception):pass
def need(ok,code):
 if not ok:raise Reject(code)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p,code):
 try:d=json.loads(p.read_text())
 except (OSError,ValueError):raise Reject(code)
 need(type(d)is dict,code);return d
def check(root):
 root=pathlib.Path(root);mf=root/'input/MANIFEST.json';m=read(mf,'INPUT_JSON')
 need(m.get('schema')=='c38-point-rectangle-input-v1','SCHEMA')
 p=m.get('parameters',{});need(set(p)=={'W','span_min','span_max','crossing_cap','M','S'},'PARAMETER_KEYS')
 W,s,S,C,M,D=(p[k] for k in ['W','span_min','span_max','crossing_cap','M','S'])
 need(all(type(v)is int for v in [W,s,S,C,M,D]) and 1<=W<=28 and 2<=s<=S<=133 and 3<=C<=99 and M==51081913 and D==96,'PARAMETERS')
 files={'rectangle_point_pilot.cpp','verify_rectangle_point.cpp','PROOF_RECTANGLE_POINT.md','PROOF_RECTANGLE.md','BAR_PUBLIC.json','search.json'}
 need(set(m.get('sha256',{}))==files,'INPUT_COVERAGE')
 for name,pin in m['sha256'].items():
  q=root/'input'/name;need(q.is_file(),'INPUT_MISSING');need(sha(q)==pin,'INPUT_SHA256')
 r=read(root/'REPLAY_RECEIPT.json','RECEIPT_JSON');need(r.get('status')=='COMPLETE_FROZEN_POINT_REPLAY' and r.get('exit_code')==0,'REPLAY_INCOMPLETE')
 need(r.get('input_manifest_sha256')==sha(mf),'REPLAY_INPUT_BINDING')
 need(r.get('verifier_source_sha256')==m['sha256']['verify_rectangle_point.cpp'],'REPLAY_SOURCE_BINDING')
 need((root/'replay.json').is_file() and r.get('output_sha256')==sha(root/'replay.json'),'REPLAY_SHA256')
 try:
  t=[datetime.datetime.fromisoformat(x) for x in [m['frozen_utc'],r['started_utc'],r['completed_utc']]]
  need(all(x.tzinfo for x in t) and t==sorted(t),'FREEZE_REPLAY_ORDER')
 except (KeyError,TypeError,ValueError):raise Reject('FREEZE_REPLAY_TIME')
 a=read(root/'input/search.json','SEARCH_JSON');b=read(root/'replay.json','REPLAY_JSON')
 need(a.get('status')=='SEARCH_ONLY_UNVERIFIED_POINT_PILOT' and b.get('status')=='COMPLETE_SEPARATE_SAME_AGENT_POINT_REPLAY','STATUS')
 need(set(a)==set(b)==set(p)|{'status','num_lo','num_hi'},'OUTPUT_FIELDS')
 for key,v in p.items():need(a.get(key)==b.get(key)==v,'OUTPUT_PARAMETERS')
 for key in ['num_lo','num_hi']:
  need(type(a.get(key))is str and a[key].isdigit() and type(b.get(key))is str and b[key].isdigit(),'NUMERATOR_FORMAT')
  need(a[key]==b[key],'FULL_POINT_REPLAY_MISMATCH')
 lo,hi=int(b['num_lo']),int(b['num_hi']);need(0<=lo<=hi<(1<<128),'INVERTED_INTERVAL')
 x=Q(M,1<<27);target=Q(400,1051);degree=S*(W+1);need(x<=target,'TARGET_ORDER')
 lower=Q(lo,1<<D);upper=Q(hi,1<<D)*(target/x)**degree
 return {'status':'VERIFIED_CANDIDATE_UNREFEREED_FINITE_CLASS','verification':'complete frozen separately written (same agent) scalar replay and exact rational target correction','parameters':p,'maximum_degree':degree,'no_length_truncation':True,'target_lower_value':str(lower),'target_upper_value':str(upper),'target_lower_decimal_diagnostic':float(lower),'target_upper_decimal_diagnostic':float(upper),'input_manifest_sha256':sha(mf),'scope':'all normalized irreducible bridges in the stated finite geometry and crossing cap; no bound on mu claimed'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('receipt');a=p.parse_args()
 try:
  d=check(a.artifact);pathlib.Path(a.receipt).write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['target_lower_decimal_diagnostic'],d['target_upper_decimal_diagnostic'])
 except Reject as e:print('REJECT:'+str(e));sys.exit(2)
