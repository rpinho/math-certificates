"""Independently reconstruct the fraud-classifier validation menu."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
from referee_costs import R,B,load_public,pq,official_classifier
import numpy as np,pandas as pd,json
from scipy.special import logit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import log_loss
import lightgbm as lgb

def main():
    f,b=load_public();d=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet');d=d.loc[d.month<7]
    tr=d.month<6;v=d.month==6;cols=[c for c in d if c not in ['fraud_bool','month','model_score']]
    X=d[cols].copy();cats=[c for c in X if isinstance(X[c].dtype,pd.CategoricalDtype)];num=[c for c in X if c not in cats]
    for c in cats:X[c]=X[c].astype(str).fillna('NA')
    for c in num:X[c]=pd.to_numeric(X[c],errors='coerce').fillna(-999)
    xt=X.loc[tr];xv=X.loc[v];yt=d.loc[tr].fraud_bool.to_numpy();yv=d.loc[v].fraud_bool.to_numpy();wt=np.where(yt==1,1.,.057);wv=np.where(yv==1,1.,.057);even=xv.index.to_numpy()%2==0;odd=~even
    scores=[];pred={}
    def add(name,p):
        pp=np.clip(p,1e-7,1-1e-7);pred[name]=pp;value=float(log_loss(yv[odd],pp[odd],sample_weight=wv[odd],labels=[0,1]));scores.append(dict(name=name,selection_weighted_logloss=value));print(name,value,flush=True)
    base=official_classifier(b,d.loc[v]);add('authors',base)
    c=LogisticRegression(C=1e4,max_iter=500,solver='lbfgs');c.fit(logit(np.clip(base[even],1e-6,1-1e-6)).reshape(-1,1),yv[even],sample_weight=wv[even]);add('authors_sigmoid',c.predict_proba(logit(np.clip(base,1e-6,1-1e-6)).reshape(-1,1))[:,1])
    iso=IsotonicRegression(out_of_bounds='clip');iso.fit(base[even],yv[even],sample_weight=wv[even]);add('authors_isotonic',iso.predict(base))
    add('constant',np.full(len(xv),np.dot(yt,wt)/wt.sum()))
    for reg in [.1,1.,10.]:
        prep=ColumnTransformer([('numeric',StandardScaler(),num),('categorical',OneHotEncoder(handle_unknown='ignore'),cats)])
        model=make_pipeline(prep,LogisticRegression(C=reg,max_iter=1000,solver='lbfgs'));model.fit(xt,yt,logisticregression__sample_weight=wt);add('logistic_c'+str(reg),model.predict_proba(xv)[:,1])
    tt=xt.copy();vv=xv.copy()
    for c in cats:
        levels=sorted(set(tt[c]));tt[c]=pd.Categorical(tt[c],categories=levels);vv[c]=pd.Categorical(vv[c],categories=levels)
    for leaves in [7,15,31,63]:
        m=lgb.LGBMClassifier(n_estimators=1500,learning_rate=.025,num_leaves=leaves,max_depth=-1,min_child_samples=100,reg_lambda=10,reg_alpha=.1,colsample_bytree=.9,verbosity=-1,n_jobs=4,random_state=1103)
        m.fit(tt,yt,sample_weight=wt,eval_set=[(vv.loc[even],yv[even])],eval_sample_weight=[wv[even]],callbacks=[lgb.early_stopping(80,verbose=False)])
        add('lightgbm_l'+str(leaves),m.predict_proba(vv,num_threads=4)[:,1])
    for a,bname in [('authors','logistic_c1.0'),('authors','lightgbm_l7'),('authors_sigmoid','lightgbm_l15'),('authors','lightgbm_l31')]:add('blend_'+a+'__'+bname,(pred[a]+pred[bname])/2)
    frozen=json.loads((B/'fit2025/classifier_h/selection.json').read_text());old={r['name']:r['selection_weighted_logloss'] for r in frozen['scores']};assert set(old)==set(pred)
    delta=max(abs(r['selection_weighted_logloss']-old[r['name']]) for r in scores)
    eligible=[r for r in scores if r['name']!='constant'];winner=min(eligible,key=lambda r:r['selection_weighted_logloss'])['name'];assert winner==frozen['winners']['replacement']=='authors_sigmoid'
    assert delta<1e-6,delta
    out=dict(winner=winner,candidates=len(scores),max_validation_score_difference=delta,scores=scores)
    (R/'CLASSIFIER_SELECTION_RESULT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
