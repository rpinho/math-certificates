from pathlib import Path
import json, os, subprocess as sp
root=Path(__file__).resolve().parent
u=root/'third_party/LeanShadow-19deb3ed555c'
m=root/'deps/third_party/mathlib4-db584cd6d46c'
dest=u/'.lake/packages'
dest.mkdir(exist_ok=True,parents=True)
for p in json.loads((u/'lake-manifest.json').read_text())['packages']:
    path=dest/p['name']
    local=m if p['name']=='mathlib' else m/'.lake/packages'/p['name']
    if not path.exists():
        if local.exists():
            path.symlink_to(os.path.relpath(local,dest),target_is_directory=True)
        else:
            path.mkdir()
            for args in [['init','-q'], ['remote','add','origin',p['url']], ['fetch','--depth','1','origin',p['rev']], ['checkout','-q','--detach','FETCH_HEAD']]:
                sp.run(['git','-C',path,*args],check=True)
    rev=sp.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
    assert rev==p['rev'], (path,rev,p)
    print(p['name'],rev)
