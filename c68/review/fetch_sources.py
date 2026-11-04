import json, urllib.request, datetime, hashlib, pathlib
root=pathlib.Path('sources')
urls={x['name']:x['url'] for x in json.load(open('../c68r3/sources-final/read-receipts.json'))}
urls.update({'open-prs.json':'https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=100','open-issues.json':'https://api.github.com/repos/teorth/optimizationproblems/issues?state=open&per_page=100','repositories.json':'https://api.github.com/search/repositories?q=Korenblum&sort=updated&order=desc','repositories-2026.json':'https://api.github.com/search/repositories?q=Korenblum+2026&sort=updated&order=desc','wikstrom.html':'https://arxiv.org/html/2607.17748v1','hexagon.html':'https://hexagonmath.org/2610.00696v3'})
receipts=[]
for name,url in urls.items():
    r={'name':name,'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Independent-mathematical-referee'})
        with urllib.request.urlopen(req, timeout=25) as f: data=f.read(); r['status']=f.status
        (root/name).write_bytes(data); r['bytes']=len(data); r['sha256']=hashlib.sha256(data).hexdigest()
        lines=data.decode(errors='replace').splitlines()
        r['matches']=[s[:800] for s in lines if any(t in s.lower() for t in ['korenblum','0.446','0.447'])][:30]
    except Exception as e:r['error']=str(e)
    receipts.append(r)
    print(name,r.get('status',r.get('error')),flush=True)
(root/'read-receipts.json').write_text(json.dumps(receipts,indent=2))
