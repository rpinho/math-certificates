"""Public read-only provenance and prior-art coverage. No authentication."""
import urllib.request,hashlib,json,pathlib,datetime,concurrent.futures
urls={
'primary':'https://www.jbento.info/papers/nesterov_sdp.pdf',
'author_homepage':'https://www.jbento.info/',
'interpolation_paper':'https://proceedings.mlr.press/v80/taylor18a/taylor18a.pdf',
'public_method_readme':'https://raw.githubusercontent.com/QCGroup/quad-lyap-first-order/master/README.md',
'public_method_code':'https://raw.githubusercontent.com/QCGroup/quad-lyap-first-order/master/FixedStepMethod.m',
'public_method_issues':'https://api.github.com/repos/QCGroup/quad-lyap-first-order/issues?state=open&per_page=100',
'public_method_pulls':'https://api.github.com/repos/QCGroup/quad-lyap-first-order/pulls?state=open&per_page=100',
'recent_paper':'https://arxiv.org/html/2610.15125v1',
'recent_table':'https://arxiv.org/src/2610.15125v1/anc/images/nag_rate_curve/nag_rate_table.md',
'github_recent_search':'https://api.github.com/search/repositories?q=Nesterov+Lyapunov&sort=updated&order=desc&per_page=10',
'github_constant_search':'https://github.com/search?q=%2221%2F32%22+Nesterov&type=code&s=indexed&o=desc',
'awesome_list':'https://raw.githubusercontent.com/JiwenJ/Awesome-Optimizers/main/README.md',
'epi':'https://raw.githubusercontent.com/BakeLab/Epi-results/main/README.md',
'alphaevolve':'https://raw.githubusercontent.com/google-deepmind/alphaevolve_results/main/README.md',
'alphaevolve_problems':'https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/README.md',
'openai_math':'https://api.github.com/repos/openai/math/git/trees/main?recursive=1',
'kisonecat':'https://api.github.com/repos/kisonecat/openai-math/git/trees/main?recursive=1',
'erdos':'https://api.github.com/repos/plasma-ai/erdos/git/trees/main?recursive=1',
'einsteinarena':'https://einsteinarena.com/',
'autolyap':'https://autolyap.github.io/',
'gannot':'https://arxiv.org/pdf/1912.13494',
'dobson':'https://arxiv.org/pdf/2305.08658',
}
pathlib.Path('sources').mkdir(exist_ok=True)
def fetch(kv):
    key,url=kv
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-referee/1.0'})
        with urllib.request.urlopen(req,timeout=35) as r: data=r.read(6000000); status=r.status
        suffix='.pdf' if data.startswith(b'%PDF') else '.txt'
        filename='sources/'+key+suffix
        pathlib.Path(filename).write_bytes(data)
        return key,{'url':url,'status':status,'file':filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    except Exception as e:return key,{'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=dict(pool.map(fetch,urls.items()))
result['checked_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(result,open('public_audit.json','w'),indent=2)
print(json.dumps(result,indent=2))
