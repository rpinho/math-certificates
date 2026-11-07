"""Reproduce the existing public transportation-LP baseline from official scores."""
from referee_policy import no_negative_cycle
from integer_transport import transport
from referee_costs import R,B,load_public,pq,caps_for,official_classifier,tally
import io,pickle,json,concurrent.futures,time
import numpy as np
import pandas as pd

def job(args):
    tag,method=args;f,b=load_public();alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet');test=alerts.loc[alerts.month==7]
    # Pandas supplies compatibility for old public pandas-pickle internals.
    d=pd.read_pickle(io.BytesIO(b.read(f'l2d_benchmarking/deferral/l2d_predictions/{method.lower()}.pkl')))[tag]
    ids=test.index.to_numpy();d=d.loc[ids];workers=list(d.columns);q=official_classifier(b,test)
    decisions=pq(f,'FiFAR/synthetic_experts/expert_predictions.parquet').loc[ids];decisions['classifier_h']=(q>=.5).astype(int);dm=decisions[workers].to_numpy()
    rows=[];team=tag.split('#')[1]
    for variant in ['hom','var_1','var_2','var_3','var_4']:
        env='testsize#'+team+'-'+variant;c,_=caps_for(f,env,len(ids));cap=np.asarray([c[w] for w in workers])
        cost=np.rint(-d.to_numpy()*1e12).astype(np.int64)
        a,obj,steps=transport(cost,cap);no_negative_cycle(cost,a)
        pred=dm[np.arange(len(ids)),a];fp,fn,units=tally(test.fraud_bool,pred)
        rows.append(dict(method=method,tag=tag,team=team,env=env,fp=fp,fn=fn,units=units,exchange_steps=steps))
    print('PRIOR DONE',method,tag,flush=True);return rows

def main():
    args=[(f'shuffle_{i}#team_{j}',m) for m in ['DeCCaF','OvA'] for i in range(1,6) for j in range(1,6)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:chunks=list(ex.map(job,args))
    d=pd.DataFrame([r for chunk in chunks for r in chunk]);d.to_csv(R/'prior_lp_costs.csv',index=False)
    mean=d.groupby(['method','team']).units.mean()/1000;mean.to_csv(R/'prior_lp_means.csv');print(mean,flush=True)
    (R/'PRIOR_LP_RESULT.json').write_text(json.dumps(dict(n=len(d),means={str(k):v for k,v in mean.items()}),indent=2))
if __name__=='__main__':main()
