"""Separate realized-cost differences from near ties in prior forecast objectives."""
from referee_costs import R,B,load_public,pq,caps_for,official_classifier,tally
from integer_transport import transport
import io,json,concurrent.futures
import numpy as np,pandas as pd

def job(arg):
    tag,method=arg;f,b=load_public();alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet');test=alerts.loc[alerts.month==7];ids=test.index.to_numpy()
    d=pd.read_pickle(io.BytesIO(b.read(f'l2d_benchmarking/deferral/l2d_predictions/{method.lower()}.pkl')))[tag].loc[ids]
    z=np.load(B/'evidence/public_lp_assignments2025.npz');assert np.array_equal(z['case_ids'],ids)
    q=official_classifier(b,test);assert np.array_equal(q>=.5,z['h_decisions'])
    decision=pq(f,'FiFAR/synthetic_experts/expert_predictions.parquet').loc[ids];decision['classifier_h']=(q>=.5).astype(int)
    own=pd.read_csv(R/'prior_lp_costs.csv');out=[]
    for i,name in enumerate(z['names']):
        seed,env,methodname=str(name).split('|')
        if seed!=tag or methodname!=method+'_LP':continue
        workers=z['worker_names'][i].astype(str);a=z['assignments'][i];c,_=caps_for(f,env,len(ids));cap=np.asarray([c[w] for w in workers])
        cost=np.rint(-d[workers].to_numpy()*1e12).astype(np.int64);old=int(cost[np.arange(len(ids)),a].sum())
        new,obj,steps=transport(cost,cap,initial=a)
        fp,fn,u=tally(test.fraud_bool.to_numpy(),decision[workers].to_numpy()[np.arange(len(ids)),a])
        ownrow=own.loc[(own.tag==tag)&(own.method==method)&(own.env==env)].iloc[0]
        out.append(dict(tag=tag,method=method,team=tag.split('#')[1],env=env,fp=fp,fn=fn,units=u,own_units=int(ownrow.units),forecast_objective_gain=(old-obj)/1e12,warm_exchange_steps=steps))
    return out

def main():
    args=[(f'shuffle_{i}#team_{j}',m) for m in ['DeCCaF','OvA'] for i in range(1,6) for j in range(1,6)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:chunks=list(ex.map(job,args))
    d=pd.DataFrame([x for c in chunks for x in c]);assert len(d)==250;d.to_csv(R/'prior_saved_audit.csv',index=False)
    means=d.groupby(['method','team']).units.mean()/1000
    out=dict(scenarios=len(d),different_realized_cost_scenarios=int((d.units!=d.own_units).sum()),max_forecast_objective_gain=float(d.forecast_objective_gain.max()),total_forecast_objective_gain=float(d.forecast_objective_gain.sum()),saved_means={str(k):v for k,v in means.items()},interpretation='Saved prior-LP assignments and a new optimizer can produce different realized costs under near-tied forecast objectives; this is not a discrepancy in the realized FP/FN metric. Headline conditional assignments were separately replayed exactly.')
    (R/'PRIOR_TIE_AUDIT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
