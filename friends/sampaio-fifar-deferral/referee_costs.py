"""Independent FiFAR referee: paper cost definition; no claimant code imports."""
import os
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:4])
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']: os.environ[k]='1'
import io,json,zipfile,hashlib,pickle
from pathlib import Path
from fractions import Fraction
import numpy as np
import pandas as pd
import pyarrow as pa
from scipy.special import expit,logit
from sklearn.linear_model import LogisticRegression
import yaml
pa.set_cpu_count(4);pa.set_io_thread_count(2)
R=Path(os.environ.get('SAMPAIO_REF_ROOT','/workspace/ref_sampaio_YB01'))
B=Path(os.environ.get('SAMPAIO_CLAIM_INPUTS','/workspace/board_sampaio'))

def load_public():
    f=zipfile.ZipFile(R/'sources/fifar.zip'); b=zipfile.ZipFile(R/'sources/benchmark.zip')
    return f,b

def pq(z,n): return pd.read_parquet(io.BytesIO(z.read(n)))
def csv(z,n): return pd.read_csv(io.BytesIO(z.read(n)))

def tally(y,p):
    y=np.asarray(y);p=np.asarray(p)
    assert np.isin(y,[0,1]).all() and np.isin(p,[0,1]).all()
    fp=int(np.sum((y==0)&(p==1))); fn=int(np.sum((y==1)&(p==0)))
    return fp,fn,1000*fn+57*fp

def official_classifier(b,test):
    prefix='l2d_benchmarking/classifier_h/selected_model/'
    m=pickle.loads(b.read(prefix+'best_model.pickle')); m.set_params(n_jobs=1)
    cfg=yaml.safe_load(b.read(prefix+'model_properties.yaml'))
    booster=m.booster_;X=test[booster.feature_name()].copy()
    cats=[c for c in X if isinstance(X[c].dtype,pd.CategoricalDtype)]
    for c,levels in zip(cats,booster.pandas_categorical):X[c]=pd.Categorical(X[c],categories=levels)
    return expit(booster.predict(X,raw_score=True,num_threads=1)+cfg['init_score'])

def caps_for(f,env,n):
    c=csv(f,f'FiFAR/testbed/test/{env}/capacity.csv').iloc[0]
    assert c.batch_id==1 and c.batch_size==n
    d={str(k):int(v) for k,v in c.items() if k.startswith('standard#') and v>0}
    assert len(d)==10
    d['classifier_h']=n-sum(d.values())
    batch=csv(f,f'FiFAR/testbed/test/{env}/batches.csv')
    assert len(batch)==n and batch.case_id.is_unique and (batch.batch==1).all()
    return d,batch.case_id.to_numpy()

def main():
    f,b=load_public();alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet')
    test=alerts.loc[alerts.month==7];assert len(test)==4457 and test.index.is_unique
    ids=test.index.to_numpy();y=test.fraud_bool.to_numpy();q=official_classifier(b,test)
    decisions=pq(f,'FiFAR/synthetic_experts/expert_predictions.parquet').loc[ids].copy()
    decisions['classifier_h']=(q>=.5).astype(int)
    rows=[];capacity_checks=0;prediction_checks=0
    for n in b.namelist():
        if not n.endswith('/results.parquet') or '/deferral/results/' not in n:continue
        parts=n.split('/');method=parts[3]
        if method not in ['DeCCaF','OvA']:continue
        seed,env=parts[4:6];d=pq(b,n);a=pq(b,n.replace('results.parquet','assignments.parquet'))
        assert len(d)==len(a)==len(ids) and d.index.is_unique and a.index.is_unique
        assert set(d.index)==set(a.index)==set(ids)
        c,batchids=caps_for(f,env,len(ids));assert set(batchids)==set(ids)
        a=a.loc[ids].iloc[:,0];p=d.loc[ids].iloc[:,0].astype(int).to_numpy()
        assert a.value_counts().to_dict()==c
        expected=np.array([decisions.loc[i,w] for i,w in zip(ids,a)],dtype=int)
        assert np.array_equal(p,expected)
        fp,fn,u=tally(y,p);rows.append(dict(origin='paper',method=method,seed=seed,team=seed.split('#')[1],env=env,fp=fp,fn=fn,units=u))
        capacity_checks+=1;prediction_checks+=1
    # Independently rebuild the validation sigmoid used by the new classifier.
    val=alerts.loc[alerts.month==6];vh=official_classifier(b,val);even=val.index.to_numpy()%2==0
    sigmoid=LogisticRegression(C=1e4,max_iter=500,solver='lbfgs')
    sigmoid.fit(logit(np.clip(vh[even],1e-6,1-1e-6)).reshape(-1,1),val.fraud_bool.to_numpy()[even],sample_weight=np.where(val.fraud_bool.to_numpy()[even]==1,1.,.057))
    newq=sigmoid.predict_proba(logit(np.clip(q,1e-6,1-1e-6)).reshape(-1,1))[:,1]
    np.savez_compressed(R/'h_independent.npz',case_ids=ids,q=newq,coef=sigmoid.coef_,intercept=sigmoid.intercept_)
    z=np.load(B/'evidence/assignments2025.npz',allow_pickle=False)
    assert np.array_equal(z['case_ids'],ids)
    for name,a,workers,savedcaps,hd in zip(z['names'],z['assignments'],z['worker_names'],z['capacities'],z['h_decisions']):
        seed,env,method=str(name).split('|');c,batchids=caps_for(f,env,len(ids));assert set(batchids)==set(ids)
        workers=workers.astype(str);assert set(workers)==set(c)
        actual=np.bincount(a,minlength=len(workers))
        assert np.array_equal(actual,np.array([c[w] for w in workers])) and np.array_equal(actual,savedcaps)
        expected_h=(q>=.5) if method=='authors_flow' else (newq>=.5)
        assert np.array_equal(expected_h,hd)
        dm=decisions[workers].to_numpy().copy();dm[:,list(workers).index('classifier_h')]=expected_h
        p=dm[np.arange(len(ids)),a]
        fp,fn,u=tally(y,p);rows.append(dict(origin='claim',method=method,seed=seed,team=seed.split('#')[1],env=env,fp=fp,fn=fn,units=u))
        capacity_checks+=1
    d=pd.DataFrame(rows);d.to_csv(R/'independent_costs.csv',index=False)
    means=[]
    for keys,g in d.groupby(['origin','method','team']):
        value=Fraction(int(g.units.sum()),1000*len(g))
        means.append(dict(zip(['origin','method','team'],keys),n=len(g),exact=str(value),mean=float(value)))
    pd.DataFrame(means).to_csv(R/'independent_means.csv',index=False)
    result=dict(test_n=len(ids),test_fraud=int(y.sum()),test_nonfraud=int((1-y).sum()),original_cases=len(d[d.origin=='paper']),candidate_cases=len(d[d.origin=='claim']),capacity_checks=capacity_checks,original_decision_checks=prediction_checks,classifier=tally(y,decisions.classifier_h),full_rejection=tally(y,np.ones(len(y),dtype=int)),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'sources/fifar.zip',R/'sources/benchmark.zip']})
    (R/'COST_RESULT.json').write_text(json.dumps(result,indent=2))
    np.savez_compressed(R/'test_evidence.npz',case_ids=ids,y=y,official_h=q,decisions=decisions.to_numpy(),worker_names=np.asarray(decisions.columns,dtype=str))
    print(json.dumps(result,indent=2),flush=True);print(pd.DataFrame(means).to_string(index=False),flush=True)
if __name__=='__main__':main()
