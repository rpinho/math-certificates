"""Independent check of the analytic class-frequency control's risk optimality."""
from referee_costs import R,load_public,pq
import numpy as np,json

def main():
    f,b=load_public();q=np.load(R/'h_independent.npz')['q'];p=.057*q/(1-q+.057*q);rows=[]
    for file in sorted(R.glob('*_own_assignments.npz')):
        tag=file.name.removesuffix('_own_assignments.npz');d=pq(f,f'FiFAR/testbed/train_alert/{tag}/train.parquet');tr=d.loc[d.month<6]
        z=np.load(file);humans=[e for e in z['workers'].astype(str) if e!='classifier_h'];cols=[]
        for e in humans:
            probabilities=[]
            for label in [0,1]:
                sub=tr.loc[(tr.assignment==e)&(tr.fraud_bool==label)]
                probabilities.append(((sub.decision==sub.fraud_bool).sum()+1)/(len(sub)+2))
            cols.append(.057*(1-p)*(1-probabilities[0])+p*(1-probabilities[1]))
        cols.append(np.minimum(p,.057*(1-p)));risk=np.column_stack(cols);n,k=risk.shape
        record=json.loads((R/(tag+'_policy.json')).read_text())
        for item in record['assignment_checks']:
            env=item['name'].split('|')[1];a=z[env+'__frequency'];D=np.zeros((k,k))
            for j in range(k):
                ix=np.flatnonzero(a==j);D[j]=np.min(risk[ix]-risk[ix,j,None],axis=0)
            for m in range(k):D=np.minimum(D,D[:,m,None]+D[None,m,:])
            minimum=float(np.min(np.diag(D)));assert minimum>-1e-12,(tag,env,minimum)
            expected=float(risk[np.arange(n),a].sum());diff=abs(expected-item['frequency_expected_cost']);assert diff<1e-9
            rows.append(dict(tag=tag,env=env,minimum_exchange_cycle=minimum,risk_sum_difference=diff))
    assert len(rows)==125
    out=dict(scenarios=len(rows),max_risk_sum_difference=max(r['risk_sum_difference'] for r in rows),min_cycle=min(r['minimum_exchange_cycle'] for r in rows),checks=rows)
    (R/'FREQUENCY_VERIFICATION.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
