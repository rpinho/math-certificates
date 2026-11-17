import urllib.request,json,hashlib,datetime,concurrent.futures,sys,pathlib
phase=sys.argv[1]
urls={
'problem':'https://www.erdosproblems.com/1183',
'forum':'https://www.erdosproblems.com/forum/thread/1183',
'paper':'https://raw.githubusercontent.com/anaxia-research/Erdos-1183/HEAD/paper/Erdos.tex',
'readme':'https://raw.githubusercontent.com/anaxia-research/Erdos-1183/HEAD/README.md',
'issues':'https://api.github.com/repos/anaxia-research/Erdos-1183/issues?state=all&per_page=100',
'issue20':'https://api.github.com/repos/anaxia-research/Erdos-1183/issues/20',
'issue20_comments':'https://api.github.com/repos/anaxia-research/Erdos-1183/issues/20/comments',
'commits':'https://api.github.com/repos/anaxia-research/Erdos-1183/commits?per_page=1',
'github_search':'https://api.github.com/search/repositories?q=Erdos+1183&sort=updated&order=desc&per_page=30',
'omega':'https://raw.githubusercontent.com/the-omega-institute/trureturing/HEAD/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md',
'arxiv':'https://arxiv.org/abs/2610.02833',
'arxiv_search':'https://arxiv.org/search/?query=monochromatic+sublattice&searchtype=all&abstracts=show&order=-announced_date_first&size=50',
'certificate_tree':'https://api.github.com/repos/rpinho/math-certificates/git/trees/HEAD?recursive=1',
}
for name,repo in [('epi','BakeLab/Epi-results'),('alpha','google-deepmind/alphaevolve_results'),('openai','openai/math'),('kisonecat','kisonecat/openai-math'),('plasma','plasma-ai/erdos')]:
 urls[name+'_tree']='https://api.github.com/repos/'+repo+'/git/trees/HEAD?recursive=1'
def fetch(pair):
 name,url=pair; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Erdos1183-local-research'}),timeout=45) as r: data=r.read(); status=r.status
  pathlib.Path(f'sources/{phase}_{name}').write_bytes(data)
  return dict(name=name,url=url,utc=now,status=status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as e:return dict(name=name,url=url,utc=now,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(fetch,urls.items()))
pathlib.Path(f'sources/{phase}_fetch.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows: print(r['name'],r.get('status',r.get('error')),r.get('bytes',''))
