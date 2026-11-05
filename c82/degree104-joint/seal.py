"""Reseal this packet, including any subsequently added review/ and REPLAY.json.

Run from anywhere with python3 seal.py. Requires git for git hash-object.
An included Python blob matching either source tree, or an import of core/wlp,
is a blocker. This does not run or replace egress-gate.
"""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import subprocess

P=Path(__file__).resolve().parent

def js(name,obj):
    (P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory():
    trees={}
    tree_sources=[]
    for short in ['197962c','3a7a84f']:
        name=f'prior_sources/vidigoat-tree-{short}.json'
        path=P/name
        tree=json.loads(path.read_text())
        if tree.get('truncated') is not False:
            raise ValueError('BLOCKER: incomplete source tree '+name)
        trees[short]={r['sha']:[] for r in tree['tree'] if r['type']=='blob'}
        for r in tree['tree']:
            if r['type']=='blob':trees[short][r['sha']].append(r['path'])
        tree_sources.append(dict(file=name,sha256=digest(path),root_tree_sha=tree['sha'],truncated=False,blob_count=len(trees[short])))
    records=[]
    for path in sorted(P.rglob('*.py')):
        blob=subprocess.check_output(['git','hash-object','--',str(path)],text=True).strip()
        imports=[]
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
            elif isinstance(node,ast.ImportFrom):
                if node.module:imports.append(node.module)
                else:imports.extend(a.name for a in node.names)
            elif isinstance(node,ast.Call):
                is_dynamic=(isinstance(node.func,ast.Name) and node.func.id=='__import__') or (isinstance(node.func,ast.Attribute) and node.func.attr=='import_module')
                if is_dynamic and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):imports.append(node.args[0].value)
        matches=[dict(commit=short,paths=tree[blob]) for short,tree in trees.items() if blob in tree]
        prohibited=sorted(n for n in set(imports) if any(s in ['core','wlp'] for s in n.split('.')))
        # grep-style textual check alongside AST; comments quoting such imports are reported too.
        grep=[]
        for lineno,line in enumerate(path.read_text().splitlines(),1):
            if re.search(r'\bfrom\s+(?:[\w.]+\.)?(?:core|wlp)(?:\.|\s)|\bimport\s+(?:[\w.]+\.)?(?:core|wlp)\b',line):
                grep.append(dict(line=lineno,text=line.strip()))
        records.append(dict(file=str(path.relative_to(P)),git_blob_sha1=blob,foreign_blob_matches=matches,imports=sorted(set(imports)),prohibited_imports=prohibited,grep_import_matches=grep))
    blocked=any(r['foreign_blob_matches'] or r['prohibited_imports'] or r['grep_import_matches'] for r in records)
    js('PYTHON_BLOBS.json',dict(status='BLOCKED' if blocked else 'PASS',complete_trees=['197962c9610f583e9bc56efe37bfb994c1eeb834','3a7a84fec9c64ae426f06a5f52597c84b3453ba0'],tree_sources=tree_sources,files=records,all_python_blobs_distinct_from_every_blob_in_both_trees=not any(r['foreign_blob_matches'] for r in records),none_imports_core_or_wlp=not any(r['prohibited_imports'] or r['grep_import_matches'] for r in records),note='Metadata-only full-tree comparison against every blob, not only .py blobs. This check does not establish authorship. No source blobs from these trees were downloaded or executed.'))
    if blocked:raise ValueError('BLOCKER: Python blob or import match; see PYTHON_BLOBS.json')
    return len(records)

def main():
    python_files=inventory()
    cert_sha=digest(P/'certificate.json')
    receipt=json.loads((P/'receipts/release-verifier.json').read_text())
    if receipt['status']!='PASS' or receipt['certificate_sha256']!=cert_sha or receipt['source_sha256']!=digest(P/'verify_best.py') or receipt['target']!='0.2519964890':
        raise ValueError('Release verifier receipt does not match the packet')
    refresh=json.loads((P/'sources/source-refresh.json').read_text())
    files=[]
    for path in sorted(P.rglob('*')):
        rel=str(path.relative_to(P))
        if path.is_symlink():raise ValueError('Symlink not supported: '+rel)
        if path.is_file() and rel not in ['MANIFEST.json','SHA256SUMS']:
            files.append(dict(path=rel,bytes=path.stat().st_size,sha256=digest(path)))
    js('MANIFEST.json',dict(format='math-certificates-c82-degree104-joint-release-v1',sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),claim='0.2519964890',qualification='candidate, unrefereed; verification level L0 for the bound as a whole',upstream_main=refresh['main'],certificate_sha256=cert_sha,release_verification='receipts/release-verifier.json',review_status='Clean-room AI referee: HOLDS WITH CAVEATS (review/REFEREE.md, REPLAY.json); candidate, unrefereed',egress_status_at_packaging='PASS (egress-gate scan of the packet after the certificate encoding change)',source_transformations=['certificate.json and FACTOR_PROVENANCE.json are copied byte-for-byte from c82r6f_release; P3 exponent is 10908223350879106/1048576, doubled from its lowest-terms form over 524288 (same rational; see README Certificate encoding). verify_best.py differs from the finished producer only in its pinned certificate hash.', 'Finished producer documents, own scripts, egress-safe evidence and data-only prior_sources replace the earlier checkpoint; home paths are relative, the P3 exponent in REPORT.md uses the release notation, and public JSON secure-shell transport metadata is omitted.', 'Only final num-16-1 round files and restricted-16.json are retained. The duplicate round certificate and three evidence/corrupt-*.json copies containing the restricted P3 encoding are omitted; historical per-round hash pins remain archival.', 'NUMERICS.md corrects the inherited verifier filename; REPRODUCE.md adds release commands and retains the finished producer section with the historical search bar.', 'README.md, PROOF.md, METHOD.md, CLAIMS.json and RIGOR.json state the final certificate facts, bound and comparison gaps. certificate_facts.py recomputes exact facts and gaps from the release certificate and receipt.', 'No previous certificate review/ or REPLAY.json is reused. Final-certificate referee pending; Ricardo will add its report and reseal.'],files=files))
    lines=[]
    for path in sorted(P.rglob('*')):
        rel=str(path.relative_to(P))
        if path.is_file() and rel!='SHA256SUMS':lines.append(f'{digest(path)}  {rel}')
    (P/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(payload_files=len(files),python_files=python_files,total_files=len(lines)+1,certificate_sha256=cert_sha)))

if __name__=='__main__':main()
