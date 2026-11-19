"""Read public sources on the authorized pod; no local/private inputs."""
import urllib.request, urllib.parse, json, hashlib, pathlib, time
root = pathlib.Path('/workspace/ref_luis_L064')
(root/'sources').mkdir(parents=True, exist_ok=True)
urls = {
 'ad_html':'https://arxiv.org/html/2011.13478v2',
 'ad_pdf':'https://arxiv.org/pdf/2011.13478v2',
 'ad_journal':'https://www.diva-portal.org/smash/get/diva2:1783421/FULLTEXT01.pdf',
 'farber':'https://arxiv.org/pdf/0807.3240',
 'endo':'https://www.jstage.jst.go.jp/article/jmath1948/15/3/15_3_339/_pdf',
 'kumar':'https://www.math.wustl.edu/~kumar/papers/seshadri.pdf',
 'seshadri':'https://pmc.ncbi.nlm.nih.gov/articles/PMC335443/',
 'arxiv_recent':'https://export.arxiv.org/api/query?search_query=all:cotangent+AND+all:generation+AND+submittedDate:[202511020000+TO+202611022359]&sortBy=submittedDate&sortOrder=descending&max_results=30',
}
for repo in ['Bakelab/Epi-results','google-deepmind/alphaevolve_results','google-deepmind/alphaevolve_repository_of_problems','openai/math','EinsteinArena/EinsteinArena','plasma-ai/erdos','kisonecat/openai-math']:
 urls['repo_'+repo.replace('/','_')] = 'https://api.github.com/repos/'+repo
for label,q in [('title','"Monotone Lagrangians"'),('novikov','Novikov generation'),('2026','cotangent Fukaya 2026'),('awesome','awesome symplectic')]:
 urls['github_'+label]='https://api.github.com/search/repositories?'+urllib.parse.urlencode({'q':q,'sort':'updated','order':'desc','per_page':10})
receipts=[]
for label,url in urls.items():
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-referee/1.0'})
  with urllib.request.urlopen(req,timeout=35) as r:
   data=r.read(12_000_000); status=r.status; final=r.url
  ext='.pdf' if data.startswith(b'%PDF') else '.txt'
  (root/'sources'/(label+ext)).write_bytes(data)
  rec={'label':label,'url':url,'final':final,'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
  if 'api.github.com' in url:
   obj=json.loads(data)
   rec['summary']=[(x['full_name'],x.get('description'),x.get('updated_at')) for x in obj.get('items',[])] if 'items' in obj else {k:obj.get(k) for k in ['full_name','description','updated_at','open_issues_count']}
 except Exception as e: rec={'label':label,'url':url,'error':str(e)}
 receipts.append(rec)
 (root/'source_receipts.json').write_text(json.dumps(receipts,indent=2))
 print(json.dumps(rec),flush=True)
print('SOURCE_DONE',flush=True)
