"""Separate integer comparison and closed orbit-count controls.
This checks arithmetic from a complete receipt; it does not replay its
billions of drift inequalities. Use verify_c31_lower.py for that replay.
"""
import argparse,json,pathlib
from fractions import Fraction as Q

def need(ok,msg):
 if not ok:raise ValueError(msg)
p=argparse.ArgumentParser();p.add_argument('--receipt');a=p.parse_args();root=pathlib.Path(__file__).resolve().parent;d=json.loads((root/'packet.json').read_text());h=d['history'];r=Q(d['r']);g=2*r/(1+r)
# S4 cycle types in the Burnside sum give this closed formula.
classes=(16**h+16*4**h+16)//48
need((16**h+16*4**h+16)%48==0 and classes==d['classes'],'orbit count')
need(r==Q(7670895684,17179869184),'exact drift fraction')
need(g==Q(3835447842,6212691217),'gamma fraction')
old=Q(14982218,24268325);need(g-old==Q(570425344,150771609578801525)>0,'positive source comparison')
need(3835447842*24268325-14982218*6212691217==570425344,'comparison cross product')
need(617356908308*6212691217<3835447842*10**12<617356908309*6212691217,'decimal floor')
if a.receipt:
 v=json.loads(pathlib.Path(a.receipt).read_text());need(v['status']=='VERIFIED_CANDIDATE_UNREFEREED','complete verdict');need(v['classes']==classes and Q(v['r'])==r and Q(v['gamma_exact'])==g,'receipt values');need(v['min_numerator']>=r*v['drift_denominator'],'minimum drift');need(v['decoded_sha256']==d['decoded_sha256'],'decoded hash')
print('VALUE_ARITHMETIC_AND_CLOSED_ORBIT_COUNT_PASS; FULL_DRIFT_REPLAY_IS_SEPARATE')
