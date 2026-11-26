"""Verify both witnesses from their words and the supplied v1 TeX. Standard library only."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def term(w, i):
    head, block = w['preperiod_terms'], w['period_terms']
    if i < len(head):
        return head[i]
    q, j = divmod(i-len(head), len(block))
    return q*w['m']+block[j]


def words(w):
    head, block = w['preperiod_terms'], w['period_terms']
    k,p,m = w['k'], w['p'], w['m']
    require(len(head)==k and len(block)==p and p>0 and m>0,'word lengths')
    require(w['f']>0 and w['d']>0 and w['g']==w['f']+w['d'],'parameters')
    require([term(w,i) for i in range(2)]==[w['f'],w['g']],'initial terms')
    gaps = [term(w,i+1)-term(w,i) for i in range(k+p)]
    require(all(x>0 for x in gaps),'positive gaps')
    require(gaps[:k]==w['preperiod_differences'] and gaps[k:]==w['period_differences'],'gap annotation')
    require(sum(gaps[k:])==m,'period displacement')
    for q in range(1,p):
        if p%q==0:
            require(gaps[k:]!=gaps[k:k+q]*(p//q),'imprimitive word')
    if k:
        require(gaps[k-1]!=gaps[-1],'extendible preperiod')
    # Any eventual period of a primitive infinite word is a multiple of p;
    # all such shifts see the same preceding periodic letter.


def member(w,n):
    return n in w['preperiod_terms'] or any(
        n>=b and (n-b)%w['m']==0 for b in w['period_terms'])


def finite(w):
    M, stop = w['M'], w['cutoff']
    require(M>w['g'] and stop==5*M,'cutoff')
    # At M+1 the proposed set must already repeat modulo M.
    require(M%w['m']==0 and M+1>=w['period_terms'][0],'alignment')
    selected=[w['f'],w['g']]
    excluded={sum(selected)}
    for n in range(w['g']+1,stop+1):
        if n not in excluded:
            excluded.update(n+s for s in selected)
            selected.append(n)
    values=set(selected)
    raw=[n in values for n in range(1,stop+1)]
    blocks=[raw[j*M:(j+1)*M] for j in range(5)]
    require(any(blocks[1]) and blocks[1:]==[blocks[1]]*4,'five-block theorem')
    require(all(bit==member(w,n) for n,bit in enumerate(raw,1)),'greedy prefix')
    return sum(blocks[1])


def multiply(a,b):
    out=Counter()
    for i,ai in a.items():
        for j,bj in b.items():
            out[i+j]+=ai*bj
    return out


def rational(w):
    # A=N/(1-z^m), with N=(1-z^m)P+B for the two finite words P,B.
    m=w['m']
    numer=Counter(w['period_terms'])
    for v in w['preperiod_terms']:
        numer[v]+=1
        numer[v+m]-=1
    # H/(1-z^(2m))^2 = A(z)^2 - A(z^2). Keep signed coefficients.
    T=2*m
    H=multiply(multiply(numer,numer),{0:1,m:2,T:1})
    for v,c in numer.items():
        H[2*v]-=c
        H[2*v+T]+=c
    base=max(max(H)+1,w['g']+1,w['period_terms'][-1]+1)
    coeff=[]
    for n in range(base+2*T):
        c=H[n]+(2*coeff[n-T] if n>=T else 0)-(coeff[n-2*T] if n>=2*T else 0)
        require(c>=0 and c%2==0,'unordered pair count')
        if n>w['g']:
            require((c==0)==member(w,n),'series greedy rule')
        coeff.append(c)
    # For n>=base the homogeneous second finite difference at lag T is 0.
    # Each residue is affine forever; nonmembers must stay positive and
    # members must stay at zero. Membership is already cyclic here.
    for n in range(base,base+T):
        slope=coeff[n+T]-coeff[n]
        require(slope>=0 and (not member(w,n) or slope==0),'series tail')
    return base,T


def formula(w,tex):
    f,d=w['f'],w['d']
    notes=w['tex_lines']
    if w['conjecture']==5:
        require((f,d)==(4,7),'period case')
        used=(286,294,295,300,301,302,338,339,340,341,403,404,405)
        b,lo,hi=1,f//2,(f+1)//2
        j=d-((2*b-1)*f+hi+1)
        require(0<=j<=lo+1 and d==2*b*f-1 and f<=4,'period branch')
        prediction=b*(f+1+lo)+hi+1-j*(b-1)-b
        actual=w['p']
    elif w['conjecture']==9:
        require((f,d)==(5,5),'preperiod case')
        used=(511,512,513,517,526,561,562,563,565,708,709,710,711)
        h,r0=divmod(d-1,2*f)
        r=r0+1
        require(f>=5 and r==f and h==0,'diagonal branch')
        prediction=(4*f+1)*h+5*f-3-(2*f+r)
        actual=w['k']
    else:
        raise Invalid('unknown conjecture')
    require(notes=={str(i):tex[i-1] for i in used},'verbatim TeX')
    require(w['formula_value']==prediction and prediction!=actual,'formula discrepancy')


def rejected(label,fn,message):
    try:
        fn()
    except Invalid as err:
        require(str(err)==message, f'{label} failed at unintended check: {err}')
        return
    raise Invalid(f'{label} was accepted')


def controls(w,tex):
    def changed(**kwargs):
        return dict(deepcopy(w),**kwargs)
    rejected('short cutoff',lambda:finite(changed(cutoff=w['cutoff']-1)),'cutoff')
    bad=deepcopy(w)
    bad['period_terms'][0]-=1
    rejected('altered tail, finite',lambda:finite(bad),'greedy prefix')
    rejected('altered tail, series',lambda:rational(bad),'series greedy rule')
    # Double a correct period and append one letter to a correct preperiod.
    B=w['period_terms']
    twice=changed(period_terms=B+[x+w['m'] for x in B],m=2*w['m'],p=2*w['p'],
                  period_differences=2*w['period_differences'])
    rejected('double period',lambda:words(twice),'imprimitive word')
    gap=w['period_differences']
    late=changed(preperiod_terms=w['preperiod_terms']+B[:1],k=w['k']+1,
                 period_terms=B[1:]+[B[0]+w['m']],
                 preperiod_differences=w['preperiod_differences']+gap[:1],
                 period_differences=gap[1:]+gap[:1])
    rejected('late onset',lambda:words(late),'extendible preperiod')
    rejected('false formula value',lambda:formula(changed(formula_value=-1),tex),'formula discrepancy')
    rejected('altered quotation',lambda:formula(changed(tex_lines={}),tex),'verbatim TeX')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('witness',nargs='?',type=Path,default=ROOT/'witness.json')
    args=parser.parse_args()
    doc=json.loads(args.witness.read_text())
    source=json.loads(gzip.decompress((ROOT/'inputs/2609.18522v1.tex.json.gz').read_bytes()))[0][1]
    source_hash='627fc91a31108750b06dc1f465a80d1768cc23448ec5f10ab239a086917d9bf3'
    require(hashlib.sha256(source.encode()).hexdigest()==doc['tex_sha256']==source_hash,'v1 source digest')
    cases=doc['cases']
    require(sorted(w['conjecture'] for w in cases)==[5,9],'both witnesses')
    for w in cases:
        words(w)
        ones=finite(w)
        base,lag=rational(w)
        formula(w,source.splitlines())
        controls(w,source.splitlines())
        print(f"C{w['conjecture']} f={w['f']} d={w['d']} (k,p,m)=({w['k']},{w['p']},{w['m']}) "
              f"formula={w['formula_value']} cutoff={w['cutoff']} ones/block={ones} "
              f"series affine from {base} with lag {lag}; 7 negative controls rejected")
if __name__=='__main__':
    main()
