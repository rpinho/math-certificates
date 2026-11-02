"""Final exact consistency and frozen-byte checks, no search dependency."""
import datetime,hashlib,json
from decimal import Decimal,localcontext
from fractions import Fraction as Q
from pathlib import Path
R=Path(__file__).resolve().parent
def main():
    manifest=json.loads((R/'STATIC_MANIFEST.json').read_text())
    assert manifest['schema']=='c44-static-manifest-v1'
    for p,h in manifest['files'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
    a=json.loads((R/'verification_bound_row.json').read_text());b=json.loads((R/'verification_bound_column.json').read_text())
    old=json.loads((R/'baseline/verification_bound_row.json').read_text())
    for z in (a,b):assert z['status'].startswith('PASS') and z['claim']=='3.9819073803'
    assert a['B'][:73]==b['B'] and a['B']==old['B']
    assert Q(a['all_finite_degrees']['72'])==Q(b['finite'])
    assert Q(old['certified_bound'])-Q(a['certified_bound'])==Q(9,64)
    assert Q('4.1225323803')-Q(a['certified_bound'])>Q(1,10000)
    assert Q(a['certified_bound'])<Q(a['claim']) and Q(b['certified_bound'])<Q(b['claim'])
    controls=json.loads((R/'sources/structure_controls.json').read_text())
    rejects=json.loads((R/'sources/rejection_controls.json').read_text())
    assert controls['status'].startswith('PASS') and rejects['status']=='PASS' and len(rejects['controls'])==17
    assert sum(z['nonconstant_tables'] for z in controls['truth_tables'])==65804
    with localcontext() as ctx:
        ctx.prec=85;q=Q(a['certified_bound']);decimal=str(Decimal(q.numerator)/Decimal(q.denominator))
    out={'status':'PASS frozen exact certificate and two independent full verifiers','qualification':'candidate, unrefereed; written universal proof, no formalization or independent human review',
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'claim':'C44 < 3.9819073803','row_bound':a['certified_bound'],'row_decimal':decimal,
         'column_bound':b['certified_bound'],'exact_gain_over_c44r3':'9/64','gain_decimal':'0.140625','caps':a['caps'],
         'block_bounds_changed':False,'B8':a['B'][8],'cap_checks':a['cap_checks'],'common_degree72_finite':b['finite'],
         'static_manifest_sha256':hashlib.sha256((R/'STATIC_MANIFEST.json').read_bytes()).hexdigest(),'static_files_checked':len(manifest['files']),
         'structure_controls':controls,'rejection_controls':len(rejects['controls'])}
    (R/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','claim','row_decimal','exact_gain_over_c44r3','B8','static_files_checked')},indent=2))
if __name__=='__main__':main()
