"""Read-only, bounded primary-source refresh; no authentication or writes upstream."""
import concurrent.futures as cf
import hashlib
import json
import pathlib
import urllib.request
ROOT=pathlib.Path(__file__).resolve().parent/'sources'
repos=['BakeLab/Epi-results','google-deepmind/alphaevolve_results',
       'google-deepmind/repository_of_problems','openai/math','plasma-ai/erdos',
       'kisonecat/openai-math','vitplanocka/saw-connective-constant']
urls={repo.replace('/','_')+'_root.json':'https://api.github.com/repos/'+repo+'/contents/' for repo in repos}
urls.update({
 'table38a.md':'https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/38a.md',
 'pull313_files.json':'https://api.github.com/repos/teorth/optimizationproblems/pulls/313/files?per_page=100',
 'open_issues.json':'https://api.github.com/repos/teorth/optimizationproblems/issues?state=open&per_page=100',
 'jensen.html':'https://arxiv.org/html/cond-mat/0409381v2',
 'einstein.html':'https://einsteinarena.com/',
 'erdos528.html':'https://www.erdosproblems.com/528',
})
def fetch(item):
    name,url=item
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'C38-independent-referee-read-only'})
        with urllib.request.urlopen(req,timeout=20) as r:data=r.read(5_000_000)
        (ROOT/name).write_bytes(data)
        return {'file':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    except Exception as e:return {'file':name,'url':url,'error':str(e)}
with cf.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,urls.items()))
(ROOT/'READ_RECEIPTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
