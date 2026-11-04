"""Data-only source/receipt hash audit. It does not establish numerical truth."""
import datetime
import hashlib
import json
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent/'c38/frozen'
roots=['c38_finite_strip','span17_all_length_stop','c38_secant_rescale',
       'c38_disjoint_extension','c38_power_secant',
       'rectangle_point/w22_h18_30_c5','rectangle_point/w23_h18_18_c5_parallel']
checks=[]
def check(path,expected,owner):
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual==expected,(str(path),expected,actual)
    checks.append({'file':str(path.relative_to(BASE)),'sha256':actual,'reference':str(owner.relative_to(BASE))})
for name in roots:
    base=BASE/name
    for manifest in sorted((base/'input').rglob('*MANIFEST.json')):
        data=json.loads(manifest.read_text())
        if isinstance(data.get('sha256'),dict):
            for rel,expected in data['sha256'].items():check(manifest.parent/rel,expected,manifest)
packetpath=BASE/'c38_finite_strip/packet.json'
packet=json.loads(packetpath.read_text())
for rel,expected in packet['source_sha256'].items():check(packetpath.parent/rel,expected,packetpath)
for key in ['frozen_input_manifest','frozen_replay_receipts']:
    check(packetpath.parent/packet[key]['path'],packet[key]['sha256'],packetpath)
for row in packet['spans']:
    for key in ['production','separate']:check(packetpath.parent/row[key]['path'],row[key]['sha256'],packetpath)
out={'status':'HASH_BINDINGS_PASS_NOT_A_NUMERICAL_REPLAY',
     'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'checked_references':len(checks),'checks':checks}
(ROOT/'results/ARTIFACT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],len(checks))
