"""Compare every local Python git blob with both public metadata-only trees."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

if __name__=='__main__':
    with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'pid':os.getpid(),'kind':'source_inventory'})+'\n')
    trees={}
    foreign_stems=set()
    for commit in ['197962c','3a7a84f']:
        tree=json.loads(Path('prior_sources/vidigoat-tree-'+commit+'.json').read_text())
        assert not tree.get('truncated')
        trees[commit]={r['sha'] for r in tree['tree'] if r['type']=='blob'}
        foreign_stems.update(Path(r['path']).stem for r in tree['tree'] if r['path'].endswith('.py'))
    records=[]
    for path in sorted(Path('.').rglob('*.py')):
        sha=subprocess.check_output(['git','hash-object','--',str(path)],text=True).strip()
        imported=[]
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node,ast.Import):imported.extend(a.name for a in node.names)
            elif isinstance(node,ast.ImportFrom) and node.module:imported.append(node.module)
        matches=[commit for commit,blobs in trees.items() if sha in blobs]
        prohibited=sorted(n for n in set(imported) if n.split('.')[0] in foreign_stems)
        records.append({'file':str(path),'git_blob_sha1':sha,'foreign_blob_matches':matches,'imports':sorted(set(imported)),'foreign_module_name_matches':prohibited})
        assert not matches,(path,matches)
        assert not prohibited,(path,prohibited)
    result={'complete_trees':['197962c9610f583e9bc56efe37bfb994c1eeb834','3a7a84fec9c64ae426f06a5f52597c84b3453ba0'],
        'all_python_blobs_distinct_from_every_blob_in_both_trees':True,'none_imports_foreign_modules':True,'files':records,
        'note':'Tree metadata only was downloaded. Our reused files came from ../c82r5; no third-party Python was downloaded.'}
    Path('PYTHON_BLOBS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'python_files':len(records),'all_distinct':True,'no_foreign_imports':True}))
