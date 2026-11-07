"""Keep compact source witnesses for offline cost checks and input provenance."""
from referee_costs import R,load_public,pq,caps_for
import numpy as np,pandas as pd,json,zipfile,hashlib

def main():
    f,b=load_public();alerts=pq(f,'FiFAR/alert_data/processed_data/alerts.parquet')
    paths=['FiFAR/alert_data/processed_data/alerts.parquet','FiFAR/synthetic_experts/expert_predictions.parquet']
    with zipfile.ZipFile(R/'public_source_witness.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n in paths:z.writestr(n,f.read(n))
        for n in f.namelist():
            if n.startswith('FiFAR/testbed/test/') and n.endswith('.csv'):z.writestr(n,f.read(n))
        for n in b.namelist():
            if n.endswith('best_model.pickle') and ('/selected_model/' in n or '/expert_models/deccaf/' in n):z.writestr(n,b.read(n))
            if '/classifier_h/selected_model/' in n and n.endswith('.yaml'):z.writestr(n,b.read(n))
    tags=[];aa=[];dd=[];sharedids=None
    for tag in [f'shuffle_{i}#team_{j}' for i in range(1,6) for j in range(1,6)]:
        d=pq(f,f'FiFAR/testbed/train_alert/{tag}/train.parquet');base=alerts.loc[d.index]
        for col in base:
            assert np.array_equal(d[col].astype(str).to_numpy(),base[col].astype(str).to_numpy()),(tag,col)
        if sharedids is None:sharedids=d.index.to_numpy()
        assert np.array_equal(sharedids,d.index.to_numpy())
        tags.append(tag);aa.append(d.assignment.str.split('#').str[1].astype(int).to_numpy(dtype=np.uint8));dd.append(d.decision.to_numpy(dtype=np.uint8))
    np.savez_compressed(R/'public_masked_annotations.npz',case_ids=sharedids,tags=np.asarray(tags),expert_number=np.asarray(aa),decision=np.asarray(dd))
    # Preserve source decisions and assignments for all original Table 7 variants.
    test=alerts.loc[alerts.month==7];ids=test.index.to_numpy();names=[];assignments=[];decisions=[]
    for n in b.namelist():
        if not n.endswith('/results.parquet') or '/deferral/results/' not in n:continue
        parts=n.split('/')
        if parts[3] not in ['DeCCaF','OvA']:continue
        a=pq(b,n.replace('results.parquet','assignments.parquet')).loc[ids].iloc[:,0]
        code=np.asarray([50 if w=='classifier_h' else int(w.split('#')[1]) for w in a],dtype=np.uint8)
        names.append('|'.join(parts[3:6]));assignments.append(code);decisions.append(pq(b,n).loc[ids].iloc[:,0].to_numpy(dtype=np.uint8))
    np.savez_compressed(R/'public_original_results.npz',case_ids=ids,names=np.asarray(names),assignment=np.asarray(assignments),decision=np.asarray(decisions))
    paths=[R/x for x in ['public_source_witness.zip','public_masked_annotations.npz','public_original_results.npz']]
    out=dict(masked_tables=25,original_runs=len(names),training_features_match_canonical_alerts=True,files=[dict(file=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])
    (R/'PUBLIC_WITNESS_RESULT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
