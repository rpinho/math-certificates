# find a 9-set family of colour c violating exactly one encoder closure clause; print that clause index
import sys
n,word,c=int(sys.argv[1]),sys.argv[2],sys.argv[3]; base=[int(x) for x in sys.argv[4].split(',')]
col=lambda S: word[bin(S).count('1')]
sets=[S for S in range(1<<n) if col(S)==c]
def clauses_violated(F):
    out=[]
    for S in F:
        for T in F:
            if S<T and (S&T) not in (S,T):
                u,m=S|T,S&T; cu,cm=col(u)==c,col(m)==c
                if cu and u not in F: out.append((S,T,'u'))
                if cm and m not in F: out.append((S,T,'m'))
                if (not cu or not cm): out.append((S,T,'b'))
    return out
B=set(base); best=None
for X in sets:
    if X in B: continue
    v=clauses_violated(B|{X})
    if len(v)==1: best=(X,v[0]); break
print("witness extra set",best)
X,(S0,T0,kind)=best
idx=0; pos={S:i for i,S in enumerate(sets)}
for i,S in enumerate(sets):
    for T in sets[i+1:]:
        if (S&T) in (S,T): continue
        cu,cm=col(S|T)==c,col(S&T)==c
        for k,cond in (('u',cu),('m',cm),('b',(not cu or not cm))):
            if cond:
                idx+=1
                if (S,T,k)==(S0,T0,kind): print("DROP",idx,"family",sorted(B|{X})); sys.exit()
