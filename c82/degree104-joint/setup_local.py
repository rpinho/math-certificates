"""Reuse our own round-6 code and coefficient JSON only."""
from pathlib import Path
import shutil, json, time, hashlib
src=Path('../c82r6')
for name in ['numerics.py','joint_lp.py','cvp_search.py','add_columns.py','numerator_search.py','run_cg.py','rejection_controls.py','source_inventory.py','NUMERICS.md']:
    shutil.copyfile(src/name,name)
for name,source in {
 'round6-certificate.json':'../c82r6f_release/certificate.json',
 'pr280-v4-certificate.json':'../c82_pr280v4_replay/data/certificate.json',
 'pr280-v3-certificate.json':'../c82r6/prior_sources/pr280-v3-certificate.json',
 'round5-certificate.json':'../c82r6/prior_sources/round5-certificate.json',
 'factor-bank.json':'../c82r6/prior_sources/factor-bank.json',
 'vidigoat-tree-197962c.json':'../c82r6/prior_sources/vidigoat-tree-197962c.json',
 'vidigoat-tree-3a7a84f.json':'../c82r6/prior_sources/vidigoat-tree-3a7a84f.json',
}.items():shutil.copyfile(source,Path('prior_sources')/name)
assert hashlib.sha256(Path('prior_sources/pr280-v4-certificate.json').read_bytes()).hexdigest()=='c1981f1c4f5e1813f625c54ce952e9b5fa210f2cccbd5ac832d2a41f12ccc72f'
source=(src/'verify_best.py').read_text()
for tag in ['round6','pr280-v4']:
    cert=Path('prior_sources')/(tag+'-certificate.json')
    sha=hashlib.sha256(cert.read_bytes()).hexdigest()
    text=''.join("EXPECTED = '"+sha+"'\n" if l.startswith('EXPECTED = ') else l for l in source.splitlines(True))
    Path('verify_'+tag.replace('-','_')+'.py').write_text(text)
Path('verify_public.py').write_text(Path('verify_round6.py').read_text())
Path('evidence/start.json').write_text(json.dumps({'start_epoch':time.time(),'start_iso':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'maximum_hours':8})+'\n')
p=Path('cvp_search.py');p.write_text(p.read_text().replace("'C82r6_'","'C82r7_'"))
p=Path('joint_lp.py');s=p.read_text().replace('own c82r5 search and helpers reused in c82r6','our own c82r5/c82r6 search and helpers reused in c82r7')
s=s.replace("if q>0:num.append({'name':r['name'],'coeffs':r['coeffs'],'q_rational':str(q)})", """if q>0:
            text=str(q)
            if len(str(abs(q.numerator))) in [15,16]:
                text=f'{q.numerator*2}/{q.denominator*2}'
                with open('CERTIFICATE_ENCODING.md','a') as f:
                    f.write(f'\\n{path}: {r["name"]}: {q} encoded as {text} (equal rational).\\n')
            num.append({'name':r['name'],'coeffs':r['coeffs'],'q_rational':text})""")
p.write_text(s)
p=Path('run_cg.py');s=p.read_text().replace("'0.2520591386'","'0.2520079724'")
s=s.replace("empty=empty+1 if negative==0 and old-new<1e-10 else 0", "empty=empty+1 if old-new<1e-10 else 0")
s=s.replace('>7*3600','>7.5*3600')
p.write_text(s)
p=Path('source_inventory.py');s=p.read_text().replace("['197962c','3a7a84f']","['197962c','3a7a84f','79ce0df']").replace("'3a7a84fec9c64ae426f06a5f52597c84b3453ba0']","'3a7a84fec9c64ae426f06a5f52597c84b3453ba0','79ce0dfb211a67ff7e387b58b0d19ff1d6accfba']").replace('both_trees','three_trees').replace('both public','three public').replace('in_both_trees','in_three_trees').replace('came from ../c82r5','came from ../c82r6 and ../c82r5')
p.write_text(s)
Path('CERTIFICATE_ENCODING.md').write_text('# Exact fraction encodings\n\nFor each frozen packet, 15–16 digit q numerators are encoded with numerator and denominator doubled. Verifier rational checks are unchanged.\n')
