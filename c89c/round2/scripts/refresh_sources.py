"""Read-only final public-source audit; no authentication, posts, or messages."""
import urllib.request,urllib.error,json,hashlib,time,gzip
from pathlib import Path
root=Path('sources/final');root.mkdir(exist_ok=True);records=[]
def fetch(label,url):
 path=root/label
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'ramsey-certificate-source-audit'})
  with urllib.request.urlopen(req,timeout=40) as r:data=r.read();code=r.status;headers=dict(r.headers)
 except urllib.error.HTTPError as e:data=e.read();code=e.code;headers=dict(e.headers)
 except Exception as e:records.append({'url':url,'file':str(path),'error':str(e),'utc':time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())});return None
 path.write_bytes(data);records.append({'url':url,'file':str(path),'status':code,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'utc':time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()),'etag':headers.get('ETag') or headers.get('Etag')})
 return data if code==200 else None
fetch('README.md','https://raw.githubusercontent.com/teorth/optimizationproblems/main/README.md')
fetch('89a.md','https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/89a.md')
for n in [277,279,308]:fetch(f'pr{n}.diff',f'https://github.com/teorth/optimizationproblems/pull/{n}.diff')
pulls=fetch('open_prs.json','https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=100')
if pulls:
 pp=json.loads(pulls);print('OPEN_PRS',len(pp),flush=True)
 for p in pp:
  if any(s in p['title'].lower() for s in ['89','ramsey','multiplicity']):print('RELEVANT_PR',p['number'],p['title'],flush=True)
fetch('code_search.json','https://api.github.com/search/repositories?q=ramsey+multiplicity&sort=updated&per_page=30')
fetch('code_search2026.json','https://api.github.com/search/repositories?q=ramsey+multiplicity+2026&sort=updated&per_page=30')
repos=['BakeLab/Epi-results','google-deepmind/alphaevolve_results','google-deepmind/alphaevolve_repository_of_problems','openai/math','togethercomputer/EinsteinArena-new-SOTA','plasma-ai/erdos','kisonecat/openai-math'];trees={}
for repo in repos:
 name=repo.replace('/','_');data=fetch(name+'_root.json','https://api.github.com/repos/'+repo+'/git/trees/HEAD')
 if data:
  x=json.loads(data);trees[repo]=x.get('sha');print('ROOT',repo,x.get('sha'),flush=True)
 else:
  fetch(name+'_tree.html','https://github.com/'+repo+'/tree/main');fetch(name+'_README.md','https://raw.githubusercontent.com/'+repo+'/HEAD/README.md')
fetch('openai_overview.tex','https://raw.githubusercontent.com/openai/math/main/overview.tex')
fetch('zenodo_metadata.json','https://zenodo.org/api/records/6602512')
(root/'root_hashes.json').write_text(json.dumps(trees,indent=2));(root/'fetch_receipts.json').write_text(json.dumps(records,indent=2));print('DONE',time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime()),flush=True)
