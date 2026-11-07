"""Verify all headline/source costs using only compact retained source witnesses."""
from referee_costs import R,B,pq,official_classifier,caps_for,tally
from pathlib import Path
import zipfile,json
import numpy as np,pandas as pd
from scipy.special import logit
from sklearn.linear_model import LogisticRegression

def main():
    w=zipfile.ZipFile(R/'public_source_witness.zip');alerts=pq(w,'FiFAR/alert_data/processed_data/alerts.parquet');test=alerts.loc[alerts.month==7];ids=test.index.to_numpy();y=test.fraud_bool.to_numpy()
    experts=pq(w,'FiFAR/synthetic_experts/expert_predictions.parquet').loc[ids];oldq=official_classifier(w,test);experts['classifier_h']=(oldq>=.5).astype(int)
    val=alerts.loc[alerts.month==6];even=val.index.to_numpy()%2==0;vh=official_classifier(w,val)
    m=LogisticRegression(C=1e4,max_iter=500,solver='lbfgs');m.fit(logit(np.clip(vh[even],1e-6,1-1e-6)).reshape(-1,1),val.fraud_bool.to_numpy()[even],sample_weight=np.where(val.fraud_bool.to_numpy()[even]==1,1.,.057))
    newq=m.predict_proba(logit(np.clip(oldq,1e-6,1-1e-6)).reshape(-1,1))[:,1]
    expected=pd.read_csv(R/'independent_costs.csv');checks=0
    z=np.load(R/'public_original_results.npz');assert np.array_equal(z['case_ids'],ids)
    allsource=experts[[f'standard#{i}' for i in range(50)]+['classifier_h']].to_numpy()
    for name,a,pred in zip(z['names'],z['assignment'],z['decision']):
        method,tag,env=str(name).split('|');assert np.array_equal(pred,allsource[np.arange(len(ids)),a])
        fp,fn,u=tally(y,pred);row=expected.loc[(expected.origin=='paper')&(expected.method==method)&(expected.seed==tag)&(expected.env==env)].iloc[0]
        assert (fp,fn,u)==(row.fp,row.fn,row.units);checks+=1
    z=np.load(B/'evidence/assignments2025.npz');assert np.array_equal(z['case_ids'],ids)
    for name,a,workers,hd in zip(z['names'],z['assignments'],z['worker_names'],z['h_decisions']):
        tag,env,method=str(name).split('|');workers=workers.astype(str);c,_=caps_for(w,env,len(ids));assert np.array_equal(np.bincount(a,minlength=11),[c[e] for e in workers])
        h=(oldq>=.5) if method=='authors_flow' else (newq>=.5);assert np.array_equal(h,hd)
        p=experts[workers].to_numpy().copy();p[:,list(workers).index('classifier_h')]=h
        fp,fn,u=tally(y,p[np.arange(len(ids)),a]);row=expected.loc[(expected.origin=='claim')&(expected.method==method)&(expected.seed==tag)&(expected.env==env)].iloc[0]
        assert (fp,fn,u)==(row.fp,row.fn,row.units);checks+=1
    z=np.load(R/'public_masked_annotations.npz');obsids=z['case_ids'];assert len(np.unique(obsids))==len(obsids) and set(obsids).isdisjoint(ids) and set(alerts.loc[obsids].month.unique())=={3,4,5,6}
    assert z['expert_number'].shape==z['decision'].shape==(25,len(obsids))
    assert checks==1250
    result=dict(original_and_candidate_costs_checked=checks,source_cases=len(alerts),masked_annotation_tables=25,full_bulk_downloads_needed_for_this_check=False,source='Only public_source_witness.zip, public_original_results.npz, public_masked_annotations.npz and retained claim assignments; no original bulk archives opened.')
    (R/'RETAINED_WITNESS_VERIFICATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
