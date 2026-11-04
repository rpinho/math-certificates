"""Exact byte-level integrity check for the frozen review packets."""
import pathlib,json,hashlib,sys
class Reject(Exception):pass
def check(folder,overrides=None):
    P=pathlib.Path(folder);manifest=json.loads((P/'MANIFEST.json').read_text());expected=manifest['files']
    files={str(p.relative_to(P)):p.read_bytes() for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in ['MANIFEST.json','SHA256SUMS']}
    if overrides:
        for name,value in overrides.items():
            if value is None:files.pop(name,None)
            else:files[name]=value
    if set(files)!=set(expected):raise Reject('E_FILE_SET')
    for name in sorted(expected):
        data=files[name]
        if len(data)!=expected[name]['bytes']:raise Reject('E_SIZE:'+name)
        if hashlib.sha256(data).hexdigest()!=expected[name]['sha256']:raise Reject('E_HASH:'+name)
    sums=''.join(v['sha256']+'  '+k+'\n' for k,v in expected.items())
    if (P/'SHA256SUMS').read_text()!=sums:raise Reject('E_SUMS')
    return {'packet':P.name,'files':len(files),'bytes':sum(map(len,files.values())),'verdict':'FROZEN_BYTES_PASS'}
def controls(folder):
    P=pathlib.Path(folder);manifest=json.loads((P/'MANIFEST.json').read_text());name=next(iter(manifest['files']));data=(P/name).read_bytes();changed=bytes([data[0]^1])+data[1:]
    tests=[('same-size byte corruption',{name:changed},'E_HASH:'+name),('missing actual member',{name:None},'E_FILE_SET'),('extra member',{'unexpected.txt':b'bad'},'E_FILE_SET')];rows=[]
    for title,changes,expected in tests:
        try:check(P,changes)
        except Reject as e:
            actual=str(e)
            if actual!=expected:raise AssertionError((title,expected,actual))
        else:raise AssertionError((title,'CORRUPTION_ACCEPTED'))
        rows.append({'corruption':title,'expected':expected,'actual':actual})
    return rows
if __name__=='__main__':
    rows=[]
    for name in sys.argv[1:]:rows.append({'check':check(name),'rejections':controls(name)})
    print(json.dumps({'verdict':'ALL_FROZEN_BYTES_AND_EXPECTED_REJECTIONS_PASS','packets':rows},indent=2))
