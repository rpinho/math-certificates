"""Exact finite torus-knot witness; uses only the verification geometry."""
import pathlib,json,hashlib,sys
from fractions import Fraction as F
from verify import Checker,Reject,need,B

def standard_diagram(k):
 need(k>=3 and k%2==1,'E_FINITE_DIAGRAM_RANGE')
 # For sigma1^k, material0 is over at even-index crossings and under at odd.
 # Odd k sends it to material1 at closure; material1 has opposite visits.
 first=[(v,1 if v%2==0 else -1) for v in range(k)]
 walk=first+[(v,-over) for v,over in first]
 graph=[set() for _ in range(k)];counts=[0]*k
 for (v,over),(w,next_over) in zip(walk,walk[1:]+walk[:1]):
  need(over!=next_over,'E_FINITE_DIAGRAM_ALTERNATION');counts[v]+=1;graph[v].add(w);graph[w].add(v)
 need(all(x==2 for x in counts),'E_FINITE_DIAGRAM_VISITS')
 need(all(graph[v]=={(v-1)%k,(v+1)%k} for v in range(k)),'E_FINITE_DIAGRAM_CYCLE')
 return {'crossings':k,'components':1,'alternating':True,'projection_graph':'cycle with doubled edges','no_loops_or_cut_vertices':True}

def check(folder,certificate=None):
 P=pathlib.Path(folder);raw=(P/'CONSTRUCTION.json').read_bytes();D=json.loads(raw);d=certificate if certificate is not None else json.loads((P/'finite_witness.json').read_text())
 need(set(d)=={'kind','artifact_sha256','n','crossings','coefficient_upper','cap_length_upper','length_upper_exact','ratio_upper_exact','bar'},'E_FINITE_SCHEMA');need(d['kind']=='finite_torus_witness_v1','E_FINITE_KIND');need(d['artifact_sha256']==hashlib.sha256(raw).hexdigest(),'E_FINITE_HASH')
 n=d['n'];need(type(n) is int and n>=1,'E_FINITE_N');N=F(D['parameters']['N']).numerator;crossings=4*N*n+3;need(type(d['crossings']) is int and d['crossings']==crossings,'E_FINITE_CROSSINGS');need(F(d['bar'])==F(36,5),'E_FINITE_BAR')
 C=Checker(D);C.scalar();C.topology();coefficient=F(d['coefficient_upper']);caps=F(d['cap_length_upper'])
 need(C.body_coefficient<B(coefficient),'E_FINITE_COEFFICIENT');need(C.cap_length<B(caps),'E_FINITE_CAPS')
 length=coefficient*(4*N*n)+caps;ratio=length/crossings
 need(F(d['length_upper_exact'])==length,'E_FINITE_LENGTH');need(F(d['ratio_upper_exact'])==ratio,'E_FINITE_RATIO');need(ratio<F(36,5),'E_FINITE_NOT_BELOW_BAR')
 return {'verdict':'EXACT_FINITE_WITNESS_PASS_CANDIDATE_UNREFEREED','n':n,'knot':f'T(2,{crossings}) up to mirror','crossings':crossings,'length_upper_exact':str(length),'ropelength_per_crossing_upper_exact':str(ratio),'display_only':float(ratio),'target_exact':'36/5','standard_diagram':standard_diagram(crossings),'qualification':'finite closure and crossing number use the all-n topology/cap proof and certificate'}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1]),indent=2))
 except Reject as e:print(str(e));sys.exit(1)
