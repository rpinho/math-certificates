import sys,html,re
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'(?s)<(script|style).*?</\1>','',t)
t=re.sub(r'<br\s*/?>|</p>|</div>|</li>','\n',t)
t=html.unescape(re.sub(r'<[^>]+>','',t))
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
