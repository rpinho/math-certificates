import json,urllib.request,hashlib,datetime,pathlib,sys,importlib.metadata
from flint import fmpq as Q
k=Q(25); b=Q(21,32)
r={}
for label,q in [('paper',Q(18,25)),('claim',Q(3599,5000))]:
    a=2*b*(k-1)
    c=q*b*(1-k)+q*q*((2+b)*k-1-b)
    d=q*(1+2*b)*(1-k)-q*q*k
    t=-d/(2*a)
    minimum=c-d*d/(4*a)
    assert t>0 and t*t<q
    r[label]={'q':str(q),'vertex_t':str(t),'min_frequency_polynomial_exact':str(minimum)}
assert Q(r['paper']['min_frequency_polynomial_exact'])==0
assert Q(r['claim']['min_frequency_polynomial_exact'])<0
json.dump(r,open('off_by_one_control.json','w'),indent=2)
urls={
'public_method_code_corrected':'https://raw.githubusercontent.com/QCGroup/quad-lyap-first-order/master/code/FixedStepMethod.m',
'gannot_html':'https://arxiv.org/html/1912.13494',
'dobson_html':'https://arxiv.org/html/2305.08658',
'github_issues_page':'https://github.com/QCGroup/quad-lyap-first-order/issues',
'github_pulls_page':'https://github.com/QCGroup/quad-lyap-first-order/pulls',
'final_recent_table':'https://arxiv.org/src/2610.15125v1/anc/images/nag_rate_curve/nag_rate_table.md',
'final_epi':'https://raw.githubusercontent.com/BakeLab/Epi-results/main/README.md',
'final_alphaevolve':'https://raw.githubusercontent.com/google-deepmind/alphaevolve_results/main/README.md',
}
reads={}
for key,url in urls.items():
    try:
        with urllib.request.urlopen(url,timeout=25) as f:data=f.read(6000000)
        path='sources/'+key+'.txt'; pathlib.Path(path).write_bytes(data)
        reads[key]={'url':url,'file':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    except Exception as e:reads[key]={'url':url,'error':str(e)}
reads['checked_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
reads['versions']={'python':sys.version,'python-flint':importlib.metadata.version('python-flint'),'sympy':importlib.metadata.version('sympy')}
json.dump(reads,open('final_sources.json','w'),indent=2)
print(json.dumps({'frequency_control':r,'source_reads':reads},indent=2))
