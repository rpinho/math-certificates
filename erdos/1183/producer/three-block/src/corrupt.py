"""Corrupt copies only. Exercise the checkers used for the accepted packet."""
from pathlib import Path
from itertools import chain
import tempfile
import check,check_roots
from lrat import verify
from check import DATA,key,read,face_path,family_image,direction

def reject(fn,message):
    try:fn()
    except AssertionError as exc:
        assert message in str(exc),(str(exc),message)
    else:raise ValueError(f'corruption accepted, expected {message}')

def flipped(f,s,z,ambient=23,threshold=14):
    for i,v in enumerate(f):
        for b in range(ambient):
            g=f.copy();g[i]=v^(1<<b)
            if len(set(g))!=len(g):continue
            try:family_image(g,s,z,ambient,threshold)
            except AssertionError as e:
                if str(e)=='witness closure':return g
    raise ValueError('need a nonduplicate, nonclosed single-bit flip')

def ancestor_witness(s):
    while True:
        for z,group in enumerate(read(face_path(s))):
            if group:return s,z,group[0]
        ax=direction(s)
        ch=list(s);ch[ax]-=1;s=tuple(ch)

def controls():
    cache=check.replay()
    with tempfile.TemporaryDirectory() as tmp:
        target=Path(tmp)
        counts={'flipped set':0,'dropped clause':0,'changed grid cell':0,'invalid LRAT':0}
        for area in ('face','split23','split22'):
            (target/area).mkdir()
            for original in (DATA/area).glob('*.cnf'):
                s=tuple(map(int,original.stem.split('-')))
                fake=target/area/original.name
                if area=='face':
                    face=s;ax=direction(s)
                    child=list(s);child[ax]-=1
                    def replay():
                        check.verify_face_cnf(s,ax,cache[tuple(child)],cache[s],target)
                    (fake.with_suffix('.cuts.gz')).write_bytes(original.with_suffix('.cuts.gz').read_bytes())
                    msg='face DIMACS regeneration'
                else:
                    if area=='split22':
                        src=original.with_suffix('.families.gz')
                        fake.with_suffix('.families.gz').write_bytes(src.read_bytes())
                    face=check_roots.root(s,cache)
                    def replay():check_roots.root(s,cache,target)
                    msg='split DIMACS regeneration'
                if area=='split22':
                    f=read(original.with_suffix('.families.gz'))[0]
                    g=flipped(f,s,0,22,13)
                    reject(lambda:family_image(g,s,0,22,13),'witness closure')
                else:
                    sh,z,f=ancestor_witness(face)
                    g=flipped(f,sh,z)
                    reject(lambda:family_image(g,sh,z),'witness closure')
                counts['flipped set']+=1
                lines=original.read_text().splitlines()
                hdr=lines[0].split();hdr[-1]=str(int(hdr[-1])-1)
                fake.write_text('\n'.join([' '.join(hdr)]+lines[1:-1])+'\n')
                reject(replay,msg)
                counts['dropped clause']+=1
                if area!='face':
                    broken=lines[:]
                    # The second clause is a selector's implication for the first grid cell.
                    bits=broken[2].split();bits[1]=str(-int(bits[1]));broken[2]=' '.join(bits)
                    fake.write_text('\n'.join(broken)+'\n')
                    reject(replay,msg)
                    counts['changed grid cell']+=1
                # An invalid antecedent in the first addition is never a valid RUP hint.
                proof=original.with_suffix('.lrat').read_text().splitlines()
                for k,line in enumerate(proof):
                    t=line.split()
                    if t[1]=='d':continue
                    t[t.index('0')+1]=str(10**9)
                    proof[k]=' '.join(t)
                    break
                bad=fake.with_suffix('.lrat');bad.write_text('\n'.join(proof)+'\n')
                reject(lambda:verify(original,bad),'invalid LRAT antecedent')
                counts['invalid LRAT']+=1
        # Corrupt the survivor itself as well as the encoding of a cell.
        shape=(7,7,7)
        lists=read(DATA/f'live-{key(shape)}.gz')
        w=lists[1][0]
        lists[1][0]=('0' if w[0]=='1' else '1')+w[1:]
        expected=[[],sorted(check.string(w,512) for w in cache[shape]),[]]
        assert lists!=expected
        print('corrupted balanced-face table differs from reconstructed survivors')
        print('corruptions rejected',counts)
if __name__=='__main__':controls()
