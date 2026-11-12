"""Read public GitHub metadata only; no foreign Python contents are requested."""
import base64,concurrent.futures,gzip,json,os,subprocess,sys,time
from pathlib import Path
phase=sys.argv[1] if len(sys.argv)>1 else 'initial'
items={
 'pr280':'repos/teorth/optimizationproblems/pulls/280',
 'pr330':'repos/teorth/optimizationproblems/pulls/330',
 'official':'repos/teorth/optimizationproblems/contents/constants/82a.md?ref=main',
 'open-prs':'repos/teorth/optimizationproblems/pulls?state=open&sort=updated&direction=desc&per_page=100',
 'repos':'search/repositories?q=Zhang+Zagier&sort=updated&order=desc&per_page=30',
 'repos-2026':'search/repositories?q=Zhang+Zagier+2026&sort=updated&order=desc&per_page=30',
 'awesome':'search/repositories?q=awesome+optimization+math&sort=updated&order=desc&per_page=30',
}
for repo in ['BakeLab/Epi-results','google-deepmind/alphaevolve_results','google-deepmind/alphaevolve_repository_of_problems','openai/math','kisonecat/openai-math','plasma-ai/erdos','togethercomputer/EinsteinArena-new-SOTA']:
    items[repo.replace('/','_')]='repos/'+repo+'/readme'
def read(item):
    name,url=item
    p=subprocess.Popen(['~/.local/bin/gh','api',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    with open('evidence/pids.jsonl','a') as f:f.write(json.dumps({'pid':p.pid,'kind':'public_metadata_read','endpoint':url})+'\n')
    out,err=p.communicate(timeout=60)
    filename=f'prior_sources/current-{phase}-{name}.json.gz'
    Path(filename).write_bytes(gzip.compress(out.encode()))
    obj=json.loads(out) if out else {}
    if name=='official' and 'content' in obj:Path(f'prior_sources/current-{phase}-82a.md').write_bytes(base64.b64decode(obj['content']))
    return {'file':filename,'endpoint':url,'exit_code':p.returncode,'stderr':err}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(read,items.items()))
Path(f'evidence/public-reads-{phase}.json').write_text(json.dumps({'epoch':time.time(),'sources':records},indent=2)+'\n')
for row in records:print(row['file'],row['exit_code'])
