"""Separately written (same agent) exact upper comparison for span>=18 extensions."""
import argparse,json,pathlib,hashlib,sys
from fractions import Fraction as Q
from verify_span17_stop import check as stop_check,Reject as StopReject
from verify_rectangle_point_packet import check as point_check,Reject as PointReject
sys.set_int_max_str_digits(200000)
class Reject(Exception):pass
def need(t,c):
 if not t:raise Reject(c)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(stop,point):
 stop=pathlib.Path(stop);point=pathlib.Path(point)
 m=json.loads((point/'input/MANIFEST.json').read_text());need(m['parameters']['span_min']>=18,'DISJOINT_SPAN_SCOPE')
 try:s=stop_check(stop)
 except StopReject as e:raise Reject('STOP_'+str(e))
 try:p=point_check(point)
 except PointReject as e:raise Reject('POINT_'+str(e))
 f=stop/'FULL_ACCEPTANCE.json';need(f.is_file(),'STOP_FULL_MISSING');full=json.loads(f.read_text())
 need(full.get('fresh_full_replay') is True and full.get('input_manifest_sha256')==s['input_manifest_sha256'] and full.get('upper_sum')==s['upper_sum'],'STOP_FULL_INCOMPLETE')
 for root,label in [(stop,'STOP'),(point,'POINT')]:
  c=json.loads((root/'REJECTION_CONTROLS.json').read_text());need(c.get('status')=='PASS' and all(x.get('actual')==x.get('expected') and x['actual'].startswith('REJECT:') for x in c['controls']),label+'_CONTROLS_INCOMPLETE')
 upper=Q(s['upper_sum'])+Q(p['target_upper_value']);need(upper<1,'UPPER_NOT_BELOW_ONE')
 return {'status':'CANDIDATE_UNREFEREED_EXTENSION_TOO_SMALL','verification':'separately written (same agent) exact rational comparison of completed frozen native certificates','verifier_source_sha256':sha(pathlib.Path(__file__)),'proof_sha256':sha(pathlib.Path(__file__).with_name('PROOF_EXTENSION_GAP.md')),'span17_input_manifest_sha256':s['input_manifest_sha256'],'point_input_manifest_sha256':p['input_manifest_sha256'],'stop_full_receipt_sha256':sha(f),'point_full_receipt_sha256':sha(point/'REPLAY_RECEIPT.json'),'span17_upper':s['upper_sum'],'extension_target_upper':p['target_upper_value'],'combined_upper':str(upper),'combined_upper_decimal_diagnostic':float(upper),'gap_below_one':str(1-upper),'scope':'all irreducible bridges of spans<=17 plus the specified disjoint finite extension at spans>=18 fail the target renewal bar; no upper bound on mu','baseline_dependency':'none; Numaro original enumeration is not a premise'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('stop');a.add_argument('point');a.add_argument('output');p=a.parse_args()
 try:
  d=check(p.stop,p.point);pathlib.Path(p.output).write_text(json.dumps(d,indent=2)+'\n');print(d['status'],d['combined_upper_decimal_diagnostic'])
 except Reject as e:print('REJECT:'+str(e));sys.exit(2)
