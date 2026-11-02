"""Read-only fallback audit when GitHub API quota is unavailable.
Uses public git refs, raw files, PR diffs and public HTML; saves receipts locally.
Four network threads maximum. Adapted from predecessor audit methodology.
"""
import concurrent.futures as cf, datetime, gzip, hashlib, json, os, pathlib, re
import subprocess, sys, urllib.request, urllib.parse
R=pathlib.Path(__file__).resolve().parent
REPOS=['teorth/optimizationproblems','BakeLab/Epi-results',
 'google-deepmind/alphaevolve_results','google-deepmind/alphaevolve_repository_of_problems',
 'openai/math','togethercomputer/EinsteinArena-new-SOTA','plasma-ai/erdos',
 'kisonecat/openai-math','vidigoat/optimization-records','rpinho/c44-certificate',
 'queelius/boolean-degree-sensitivity']
def get(url):
    a={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'local-readonly-research'})
        with urllib.request.urlopen(req,timeout=40) as f: b=f.read()
        a.update(data=b.decode(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
    except Exception as e:a['error']=str(e)
    return a
def refs(repo):
    args=['git','ls-remote','https://github.com/'+repo+'.git','HEAD']
    if repo==REPOS[0]:args+=['refs/pull/*/head']
    p=subprocess.run(args,text=True,capture_output=True,timeout=60)
    return {'repo':repo,'returncode':p.returncode,'refs':p.stdout,'error':p.stderr}
def main(label):
    print('PID',os.getpid(),flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex: rs=list(ex.map(refs,REPOS))
    old=json.loads((R/'sources/initial_open_prs.json').read_text())
    nums=[p['number'] for p in old['open_prs']]
    urls=['https://github.com/teorth/optimizationproblems/pulls',
          'https://github.com/teorth/optimizationproblems/pulls?page=2',
          'https://github.com/teorth/optimizationproblems/issues',
          'https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md']
    urls+=['https://github.com/teorth/optimizationproblems/pull/'+str(n)+'.diff' for n in nums]
    urls+=['https://raw.githubusercontent.com/'+r+'/main/README.md' for r in REPOS[1:]]
    urls+=['https://raw.githubusercontent.com/openai/math/main/CONTENTS.md',
           'https://raw.githubusercontent.com/seewoo5/awesome-ai-for-math/main/README.md',
           'https://raw.githubusercontent.com/BakeLab/Epi-results/main/mathematics/wellens/README.md']
    urls+=['https://github.com/search?type=repositories&s=updated&o=desc&q='+urllib.parse.quote(q)
           for q in ['wellens boolean','"3.9819073803"','"3.1674542553"','"4.1225323803"',
                     '"relevant variables" boolean 2026','Reed Muller relevant variables','awesome ai math']]
    with cf.ThreadPoolExecutor(max_workers=4) as ex: fs=list(ex.map(get,urls))
    pr_nums=sorted(set(int(n) for a in fs[:2] for n in re.findall(r'/teorth/optimizationproblems/pull/(\d+)',a.get('data',''))))
    missing=[n for n in pr_nums if n not in nums]
    if missing:
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            fs+=list(ex.map(get,['https://github.com/teorth/optimizationproblems/pull/'+str(n)+'.diff' for n in missing]))
    relevant=[{'url':a['url'],'sha256':a.get('sha256'),'paths':re.findall(r'^diff --git a/(.*?) b/',a.get('data',''),re.M)}
              for a in fs if a['url'].endswith('.diff') and re.search(r'^diff --git a/constants/44',a.get('data',''),re.M)]
    heads=dict(line.split()[::-1] for line in rs[0]['refs'].splitlines())
    summary={'label':label,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'repos':[{**{k:v for k,v in a.items() if k!='refs'},'HEAD':a['refs'].splitlines()[0] if a['refs'] else None} for a in rs],
       'html_pr_numbers':pr_nums,'inherited_open_prs':nums,'new_prs':missing,'c44_diffs':relevant,
       'inherited_head_comparisons':[{'number':p['number'],'old':p['head'],'now':heads.get('refs/pull/'+str(p['number'])+'/head')} for p in old['open_prs']],
       'visible_pr_heads':{str(n):heads.get('refs/pull/'+str(n)+'/head') for n in pr_nums},
       'c44_mentions_in_added_lines':[{'url':a['url'],'lines':[
           line for line in a.get('data','').splitlines()
           if line.startswith('+') and re.search(r'(?:\[44\]|C.?44|relevant variables|4\.326404|4\.122533)',line,re.I)]}
           for a in fs if a['url'].endswith('.diff') and any(
               line.startswith('+') and re.search(r'(?:\[44\]|C.?44|relevant variables|4\.326404|4\.122533)',line,re.I)
               for line in a.get('data','').splitlines())],
       'errors':[{'url':a['url'],'error':a['error']} for a in fs if 'error' in a],
       'receipts':[{'url':a['url'],'sha256':a.get('sha256'),'bytes':a.get('bytes')} for a in fs]}
    with gzip.open(R/'sources'/('public_'+label+'.json.gz'),'wt') as f:json.dump({'refs':rs,'fetches':fs},f)
    (R/'sources'/('public_'+label+'_summary.json')).write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('receipts','inherited_head_comparisons')},indent=2),flush=True)
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'initial')
