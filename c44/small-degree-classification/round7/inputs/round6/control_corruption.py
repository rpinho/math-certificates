"""Refresh hashes while falsifying mathematical data; both checks must reject.
All temporary mutations are in fresh session-created directories, removed
by TemporaryDirectory. No static artifact is changed.
"""
import pathlib,json,tempfile,shutil,subprocess,hashlib
P=pathlib.Path(__file__).resolve().parent
s=json.loads((P/'candidate.json').read_text());z=json.loads((P/'caps.json').read_text())
checks=['verify_caps_a.py','verify_caps_b.py'];receipts=[]
mutations=['wrong_cap','wrong_base','false_claim','missing_case','odd_grid_witness','bad_block_input']
for label in mutations:
    with tempfile.TemporaryDirectory(prefix='c44r6-reject-',dir=P) as temp:
        T=pathlib.Path(temp)
        for name in checks:shutil.copyfile(P/name,T/name)
        (T/'baseline').mkdir()
        for name in ['epi_certificate.json','spectral_certificate_round3.json']:
            shutil.copyfile(P/'baseline'/name,T/'baseline'/name)
        spec=json.loads(json.dumps(s));caps=json.loads(json.dumps(z))
        if label=='wrong_cap':
            r=caps['modes']['higher']['rows'][2];r['R']-=1;r['excluded']-=1
            r['cap']=str(__import__('fractions').Fraction(r['R'],2**r['degree']))
            spec['caps']['6']=r['cap'];caps['modes']['higher']['caps']['6']=r['cap']
        if label=='wrong_base':caps['base_caps']['3']='9/8'
        if label=='false_claim':spec['claim']='2.19'
        if label=='missing_case':caps['modes']['higher']['rows'].pop(2)
        if label=='odd_grid_witness':caps['modes']['higher']['rows'][10]['relaxation_witness']['lambda']='2049/1024'
        if label=='bad_block_input':
            (T/'baseline/epi_certificate.json').write_text('{}')
        raw=(json.dumps(caps,indent=2)+'\n').encode();(T/'caps.json').write_bytes(raw)
        spec['cap_sha256']=hashlib.sha256(raw).hexdigest()
        (T/'candidate.json').write_text(json.dumps(spec))
        for checker in checks:
            # A intentionally has no inherited raw-block dependency.
            if label=='bad_block_input' and checker=='verify_caps_a.py':continue
            p=subprocess.run(['python3',checker],cwd=T,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            assert p.returncode!=0,(label,checker)
            receipts.append({'mutation':label,'checker':checker,'rejected':True})
(P/'control_corruption.json').write_text(json.dumps({'status':'PASS','checks':receipts},indent=2)+'\n')
print('PASS',len(receipts),'rejections')
