"""Rebuild the claimed 2025 policy from permitted annotations, independently.

Only this referee's cost module and standard libraries are imported. The
claimant's pickles are used as data for weight comparison, never for routing.
"""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
from referee_costs import R,B,pq,csv,load_public,official_classifier,caps_for,tally
from pathlib import Path
import json,pickle,hashlib,concurrent.futures,time
import numpy as np
import pandas as pd
from scipy.special import expit,logit
from integer_transport import transport,frequency_assignment
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import log_loss
import pyarrow as pa
pa.set_cpu_count(1);pa.set_io_thread_count(1)
CATS=['payment_type','employment_status','housing_status','source','device_os']

def features(d):
    x=d.drop(columns=[k for k in ['fraud_bool','month','batch','decision'] if k in d]).copy()
    for k in x:
        if k in CATS+['assignment']:x[k]=x[k].astype(str).fillna('NA')
        else:x[k]=pd.to_numeric(x[k],errors='coerce').fillna(-999)
    return x

def official_expert(b,tag,x):
    model=pickle.loads(b.read(f'l2d_benchmarking/expert_models/deccaf/{tag}/best_model.pickle'))
    booster=model.booster_;xx=x[booster.feature_name()].copy()
    cats=[k for k in xx if k in CATS+['assignment']]
    for k,levels in zip(cats,booster.pandas_categorical):xx[k]=pd.Categorical(xx[k],categories=levels)
    return expit(booster.predict(xx,raw_score=True,num_threads=1))

def new_h(b,d):
    z=np.load(R/'h_independent.npz');coef=z['coef'].item();intercept=z['intercept'].item()
    old=official_classifier(b,d)
    return expit(coef*logit(np.clip(old,1e-6,1-1e-6))+intercept)

def no_negative_cycle(integer_cost,a):
    # Moving a case from its current worker to another defines an exchange
    # edge. Any feasible improvement decomposes into cycles of workers.
    n,k=integer_cost.shape; D=np.zeros((k,k),dtype=np.int64)
    for j in range(k):
        ix=np.flatnonzero(a==j);assert len(ix)>0
        D[j]=np.min(integer_cost[ix]-integer_cost[ix,j,None],axis=0)
    for m in range(k):D=np.minimum(D,D[:,m,None]+D[None,m,:])
    assert np.min(np.diag(D))>=0,('negative cycle',np.diag(D))

def run_team(tag):
    f,b=load_public();d=pq(f,f'FiFAR/testbed/train_alert/{tag}/train.parquet')
    assert d.index.is_unique and set(d.month.unique())=={3,4,5,6}
    assert not d.assignment.isin(['classifier_h','model#0']).any()
    tr=d.loc[d.month<6];v=d.loc[d.month==6]
    assert set(tr.index).isdisjoint(v.index)
    xt=features(tr);xv=features(v);yt=(tr.decision==tr.fraud_bool).to_numpy().astype(int);yv=(v.decision==v.fraud_bool).to_numpy().astype(int)
    cats=[c for c in xt if c in CATS];nums=[c for c in xt if c not in CATS+['assignment']]
    pre=ColumnTransformer([('numeric',StandardScaler(),nums),('categorical',OneHotEncoder(handle_unknown='ignore'),cats)],sparse_threshold=1)
    zt=pre.fit_transform(xt);zv=pre.transform(xv)
    qv=new_h(b,v);weight=np.where(v.fraud_bool.to_numpy()==1,1.,.057);even=v.index.to_numpy()%2==0;odd=~even
    te=xt.assignment.to_numpy();ve=xv.assignment.to_numpy();fraud=tr.fraud_bool.to_numpy()
    auth=official_expert(b,tag,xv);heads_by_C={};scores=[];head_count=0
    def score(name,p):
        p=np.clip(p,1e-7,1-1e-7)
        value=float(log_loss(yv[odd],p[odd],sample_weight=weight[odd],labels=[0,1]))
        scores.append(dict(name=name,selection_weighted_logloss=value))
        return p
    score('authors',auth)
    counts={}
    for e in np.unique(te):
        counts[e]=[]
        for y in [0,1]:
            ix=(te==e)&(fraud==y);counts[e].append(float((yt[ix].sum()+1)/(ix.sum()+2)))
    def conditional(heads,z,experts,q):
        out=np.zeros(len(q))
        for e in np.unique(experts):
            ix=np.flatnonzero(experts==e)
            for y in [0,1]:
                h=heads[e][y];p=np.full(len(ix),h) if isinstance(h,float) else h.predict_proba(z[ix])[:,1]
                out[ix]+=p*(q[ix] if y else 1-q[ix])
        return out
    score('conditional_frequency',conditional(counts,zv,ve,qv))
    for reg in [.01,.1,1.,10.]:
        heads={}
        for e in np.unique(te):
            heads[e]=[]
            for y in [0,1]:
                ix=np.flatnonzero((te==e)&(fraud==y))
                if len(ix)<20 or len(np.unique(yt[ix]))<2:m=counts[e][y]
                else:
                    m=LogisticRegression(C=reg,max_iter=1000,solver='lbfgs');m.fit(zt[ix],yt[ix]);head_count+=1
                heads[e].append(m)
        heads_by_C[reg]=heads
        name='conditional_c'+str(reg);pp=score(name,conditional(heads,zv,ve,qv))
        cal=LogisticRegression(C=1e4,max_iter=500,solver='lbfgs')
        cal.fit(logit(np.clip(pp[even],1e-6,1-1e-6)).reshape(-1,1),yv[even],sample_weight=weight[even])
        score(name+'_sigmoid',cal.predict_proba(logit(np.clip(pp,1e-6,1-1e-6)).reshape(-1,1))[:,1])
        score('blend_authors__'+name,(auth+pp)/2)
    frozen=json.loads((B/'fit_conditional/2025'/tag/'selection.json').read_text())
    winner=min(scores,key=lambda r:r['selection_weighted_logloss'])['name'];assert winner==frozen['winner']
    delta=max(abs(a['selection_weighted_logloss']-c['selection_weighted_logloss']) for a,c in zip(scores,frozen['scores']))
    assert [r['name'] for r in scores]==[r['name'] for r in frozen['scores']] and delta<1e-8,(tag,delta)
    ordered=sorted(scores,key=lambda r:r['selection_weighted_logloss'])
    margin=ordered[1]['selection_weighted_logloss']-ordered[0]['selection_weighted_logloss']
    assert margin>2*delta,(tag,'validation winner numerically ambiguous',margin,delta)
    assert winner.startswith('blend_authors__conditional_c')
    chosen=float(winner.split('conditional_c')[1]);heads=heads_by_C[chosen]
    saved=pickle.loads((B/'fit_conditional/2025'/tag/(winner+'.pkl')).read_bytes())['right']
    maxcoef=0.
    assert list(pre.feature_names_in_)==list(saved['pre'].feature_names_in_)
    for e in heads:
        for y in [0,1]:
            h=heads[e][y];old=saved['by_expert'][e][y]
            if isinstance(h,float):assert h==old['constant']
            else:maxcoef=max(maxcoef,float(np.max(abs(h.coef_-old.coef_))),float(np.max(abs(h.intercept_-old.intercept_))))
    assert maxcoef<1e-10,(tag,maxcoef)
    # Only after independent validation selection do we read test features.
    alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet');test=alerts.loc[alerts.month==7].drop(columns='fraud_bool')
    ids=test.index.to_numpy();assert set(ids).isdisjoint(d.index)
    z=np.load(B/'evidence/assignments2025.npz');q=new_h(b,test)
    eligible=[i for i,n in enumerate(z['names']) if str(n).startswith(tag+'|') and str(n).endswith('|conditional')]
    workers=z['worker_names'][eligible[0]].astype(str);human=[w for w in workers if w!='classifier_h'];pcols=[];fcols=[]
    for e in human:
        xx=test.copy();xx['assignment']=e;xx=features(xx);ztst=pre.transform(xx);es=np.full(len(xx),e,dtype=object)
        pcols.append((official_expert(b,tag,xx)+conditional(heads,ztst,es,q))/2)
        fcols.append(conditional(counts,ztst,es,q))
    mass=.057/(1-q+.057*q)
    ps=np.column_stack(pcols+[np.maximum(q,1-q)]);fs=np.column_stack(fcols+[np.maximum(q,1-q)])
    worker_order=human+['classifier_h']; assert list(workers)==worker_order
    costs=mass[:,None]*(1-ps)
    frequency_rates=np.asarray([counts[e] for e in human])
    report=[];output={}
    for i in eligible:
        name=str(z['names'][i]);env=name.split('|')[1];capdict,_=caps_for(f,env,len(ids));cap=np.asarray([capdict[w] for w in workers])
        saved_a=z['assignments'][i];integer_cost=np.rint(costs*1e9).astype(np.int64)
        no_negative_cycle(integer_cost,saved_a)
        # Construct assignments without reading the saved assignment as a start.
        a,obj,steps=transport(integer_cost,cap)
        no_negative_cycle(integer_cost,a)
        achieved=int(integer_cost[np.arange(len(ids)),saved_a].sum());ours=int(integer_cost[np.arange(len(ids)),a].sum())
        assert achieved==ours and achieved==int(z['objectives'][i])
        control,control_obj=frequency_assignment(q,frequency_rates,cap)
        report.append(dict(name=name,objective_units=achieved,independent_assignment_differences=int(np.sum(a!=saved_a)),independent_objective=obj,integer_exchange_steps=steps,frequency_expected_cost=control_obj))
        output[env+'__headline']=a.astype(np.uint8);output[env+'__frequency']=control.astype(np.uint8)
    np.savez_compressed(R/(tag+'_own_assignments.npz'),case_ids=ids,workers=workers,**output)
    result=dict(tag=tag,n_train=len(tr),n_validation=len(v),winner=winner,validation_max_abs_difference=delta,validation_winner_margin=margin,max_coefficient_difference=maxcoef,logistic_heads_fitted=head_count,assignment_checks=report)
    (R/(tag+'_policy.json')).write_text(json.dumps(result,indent=2))
    print('DONE',tag,'heads',head_count,'validation_delta',delta,'coef_delta',maxcoef,flush=True)
    return result

def main():
    started=time.time();tags=[f'shuffle_{i}#team_{j}' for i in range(1,6) for j in range(1,6)]
    existing={tag:json.loads((R/(tag+'_policy.json')).read_text()) for tag in tags if (R/(tag+'_policy.json')).exists() and (R/(tag+'_own_assignments.npz')).exists()}
    missing=[tag for tag in tags if tag not in existing]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:added=list(ex.map(run_team,missing))
    existing.update({r['tag']:r for r in added});results=[existing[tag] for tag in tags]
    (R/'POLICY_RESULT.json').write_text(json.dumps(dict(elapsed=time.time()-started,results=results),indent=2))
    print('ALL POLICIES VERIFIED',time.time()-started,flush=True)
if __name__=='__main__':main()
