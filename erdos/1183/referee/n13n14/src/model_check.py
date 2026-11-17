# model_check.py n word colour K solverlog : decode x_S from model, check closed, monochromatic, >=K
import sys
n,word,c,K,log=int(sys.argv[1]),sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5]
sets=[S for S in range(1<<n) if word[bin(S).count('1')]==c]
lits=set()
for line in open(log):
    if line.startswith('v '): lits.update(int(x) for x in line[2:].split())
fam=[S for i,S in enumerate(sets,1) if i in lits]; F=set(fam)
viol=[(a,b) for a in fam for b in fam if (a|b) not in F or (a&b) not in F]
print(f"model: {len(fam)} sets; sizes={sorted(bin(S).count('1') for S in fam)}; closed={not viol}; violating pairs={viol[:4]} ({len(viol)//2} unordered); masks={sorted(fam)}")
