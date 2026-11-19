import urllib.request,urllib.parse,pathlib,json,hashlib,xml.etree.ElementTree as ET
root=pathlib.Path('/workspace/ref_luis_L064')
urls={
 'seshadri_correct':'https://pmc.ncbi.nlm.nih.gov/articles/PMC335443/',
 'kumar_pdf':'https://www.math.wustl.edu/~kumar/papers/seshadri.pdf',
 'endo_pdf':'https://www.jstage.jst.go.jp/article/jmath1948/15/3/15_3_339/_pdf',
 'openai_overview':'https://raw.githubusercontent.com/openai/math/main/overview.tex',
}
for repo in ['BakeLab/Epi-results','google-deepmind/alphaevolve_results','google-deepmind/alphaevolve_repository_of_problems','openai/math','vinid/einstein-arena','plasma-ai/erdos','kisonecat/openai-math']:
 for part in ['','/issues','/pulls']:
  urls[repo.replace('/','_')+(part.replace('/','_') or '_root')]='https://github.com/'+repo+part
for label,q in [('symplectic','cat:math.SG AND (all:cotangent OR all:Novikov) AND submittedDate:[202511020000 TO 202611022359]'),('generation','all:"ordinary generation" AND all:Fukaya')]:
 urls['arxiv_'+label]='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':q,'sortBy':'submittedDate','sortOrder':'descending','max_results':80})
receipts=[]
for label,url in urls.items():
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-referee'}),timeout=25) as r:
   data=r.read(15_000_000);code=r.status
  (root/'sources'/(label+('.pdf' if data.startswith(b'%PDF') else '.txt'))).write_bytes(data)
  rec={'label':label,'url':url,'status':code,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
  if label.startswith('arxiv'):
   ns={'a':'http://www.w3.org/2005/Atom'}
   entries=ET.fromstring(data).findall('a:entry',ns)
   rec['entries']=[{'title':e.findtext('a:title',namespaces=ns),'id':e.findtext('a:id',namespaces=ns),'summary':e.findtext('a:summary',namespaces=ns)} for e in entries]
  elif not data.startswith(b'%PDF'):
   text=data.decode(errors='replace')
   rec['term_counts']={t:text.lower().count(t) for t in ['fukaya','cotangent','novikov','seshadri','principal ideal','graded projective']}
 except Exception as ex:rec={'label':label,'url':url,'error':str(ex)}
 receipts.append(rec);(root/'more_source_receipts.json').write_text(json.dumps(receipts,indent=2))
 print(json.dumps({k:v for k,v in rec.items() if k!='entries'}),flush=True)
print('MORE_DONE',flush=True)
