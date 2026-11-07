"""Summarize independent results; exact finite costs, no significance claims."""
from referee_costs import R,B,load_public,pq,tally
import json,hashlib,pickle,zipfile,sys,platform
from fractions import Fraction
import numpy as np
import pandas as pd
import scipy,sklearn,lightgbm,pyarrow

def main():
    result=json.loads((R/'POLICY_RESULT.json').read_text());assert len(result['results'])==25
    f,b=load_public();alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet');test=alerts.loc[alerts.month==7]
    source=pq(f,'FiFAR/synthetic_experts/expert_predictions.parquet').loc[test.index];h=np.load(R/'h_independent.npz')['q'];source['classifier_h']=(h>=.5).astype(int)
    rows=[];assignment_differences=0;coef=0.;validation=0.;heads=0
    for item in result['results']:
        heads+=item['logistic_heads_fitted'];coef=max(coef,item['max_coefficient_difference']);validation=max(validation,item['validation_max_abs_difference'])
        assignment_differences+=sum(x['independent_assignment_differences'] for x in item['assignment_checks'])
        tag=item['tag'];z=np.load(R/(tag+'_own_assignments.npz'));assert np.array_equal(z['case_ids'],test.index.to_numpy())
        dm=source[z['workers'].astype(str)].to_numpy()
        for name in z.files:
            if not name.startswith('testsize'):continue
            env,method=name.split('__');a=z[name];fp,fn,u=tally(test.fraud_bool.to_numpy(),dm[np.arange(len(dm)),a])
            rows.append(dict(seed=tag,team=tag.split('#')[1],env=env,method=method,fp=fp,fn=fn,units=u))
    d=pd.DataFrame(rows);d.to_csv(R/'own_policy_costs.csv',index=False)
    means=[]
    for (method,team),g in d.groupby(['method','team']):
        v=Fraction(int(g.units.sum()),1000*len(g));means.append(dict(method=method,team=team,n=len(g),exact=str(v),mean=float(v)))
    pd.DataFrame(means).to_csv(R/'own_policy_means.csv',index=False)
    original=pd.read_csv(R/'independent_costs.csv');claimed=original[(original.origin=='claim')&(original.method=='conditional')]
    own=d[d.method=='headline'];joined=own.merge(claimed,on=['seed','team','env'],suffixes=('_ours','_claim'))
    assert len(joined)==125
    changed=int(np.sum(joined.units_ours!=joined.units_claim))
    # Separate LP optima can choose different assignments if utilities tie.
    # Every saved assignment was independently certified exactly for rounded costs.
    output=dict(policies=25,validation_menu_models=25*14,logistic_heads_refitted=heads,max_coefficient_difference=coef,max_validation_score_difference=validation,headline_independent_optimum_checks=125,exact_integer_cycle_certificates=125,independent_different_case_assignments=assignment_differences,independent_scenarios_with_different_realized_cost=changed,means=means,original_source_cost_result=json.loads((R/'COST_RESULT.json').read_text()),environment=dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,lightgbm=lightgbm.__version__,pyarrow=pyarrow.__version__))
    (R/'REFEREE_RESULT.json').write_text(json.dumps(output,indent=2));print(json.dumps(output,indent=2))

if __name__=='__main__':main()
