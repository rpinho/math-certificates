"""Frozen packet entrypoint. Every mathematical checker is same-agent."""
import pathlib,json,sys
import verify_ropelength,verify_contact,verify,verify_projection,verify_length_identity,verify_margin,verify_finite,verify_diagram,verify_manifest

def diagram_binding(D,packet):
 N=verify.frac(D['parameters']['N']).numerator;expected={'kind':'finite_alternating_braid_diagrams_v1','cases':[{'m':2,'word':[1],'repeat':4*N*n+3,'crossings':4*N*n+3} for n in [1,2,3]]}
 verify.need(packet==expected,'E_DIAGRAM_BINDING')
def check(folder,integrity=True):
 P=pathlib.Path(folder);receipt={'integrity':verify_manifest.check(P)} if integrity else {}
 D=json.loads((P/'CONSTRUCTION.json').read_text());diagrams=json.loads((P/'diagrams.json').read_text());diagram_binding(D,diagrams)
 receipt['geometry']=verify.check_folder(P);receipt['physical_braid']=verify_projection.check(P);receipt['length_identity']=verify_length_identity.check(P);receipt['margin']=verify_margin.check(P);receipt['finite_witness']=verify_finite.check(P);receipt['standard_diagrams']=verify_diagram.check(diagrams);receipt['ropelength']=verify_ropelength.check(P);receipt['contact']=verify_contact.check(P)
 verify.need(receipt['geometry']['topology']['body_matrix']==receipt['physical_braid']['body_matrix'],'E_TOPOLOGY_ACTION_BINDING')
 c=D['claim'];rop=receipt['ropelength'];contact=receipt['contact'];margin=receipt['margin']
 return {'verdict':('ALL_FROZEN_C22B_CHECKS_PASS_CANDIDATE_UNREFEREED' if integrity else 'ALL_SEMANTIC_C22B_CHECKS_PASS_CANDIDATE_UNREFEREED'),'verifiers':'separately written (same agent)','claim':'C22b <='+rop['upper_exact'],'upper_exact':rop['upper_exact'],'upper_display_only':rop['upper_display_only'],'family':f"T(2,{c['crossings_slope']}n+{c['crossings_intercept']}), n>={c['n_min']}, up to mirror",'thickness_lower_exact':margin['original_thickness_lower'],'thickness_upper_exact':contact['closed_family_thickness_upper_exact'],'length_inequality':f"L_n<=({c['coefficient']})({c['crossings_slope']}n+{c['crossings_intercept']})+{c['additive']}",'ropelength_limit_upper_exact':rop['exact_limit_upper'],'qualification':'explicit proof in PROOF.md uses stated classical theorems; not referee review or a formal proof assistant','checks':receipt}

if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1],'--semantic-only' not in sys.argv),indent=2))
 except (verify.Reject,verify_length_identity.Reject,verify_diagram.Reject,verify_manifest.Reject) as e:print(str(e));sys.exit(1)
