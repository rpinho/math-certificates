"""Check ASCII positive-hint LRAT by reverse unit propagation."""
from pathlib import Path
import sys

def verify(cnf,proof):
    with cnf.open() as f:
        fmt,kind,variables,number=f.readline().split()
        assert (fmt,kind)==('p','cnf')
        n=int(variables)
        db={}
        for i,line in enumerate(f,1):
            c=list(map(int,line.split()))
            assert c and c[-1]==0 and all(0<abs(l)<=n for l in c[:-1]),'invalid DIMACS clause'
            db[i]=c[:-1]
        assert len(db)==int(number),'DIMACS clause count'
    last=len(db)
    empty=False
    with proof.open() as f:
        for line in f:
            tokens=line.split()
            if tokens[1]=='d':
                deletes=[int(x) for x in tokens[2:]]
                assert deletes[-1]==0
                for i in deletes[:-1]:del db[i]
                continue
            i=int(tokens[0]); nums=list(map(int,tokens[1:]))
            pos=nums.index(0)
            clause,hints=nums[:pos],nums[pos+1:]
            assert i>last and hints and hints[-1]==0
            assert all(0<abs(l)<=n for l in clause)
            false=set(clause)
            assert all(-l not in false for l in false)
            conflict=False
            for j in hints[:-1]:
                assert j>0 and j in db,'invalid LRAT antecedent'
                source=db[j]
                assert not any(-lit in false for lit in source),'satisfied hint'
                unassigned=set(source)-false
                if not unassigned:
                    conflict=True
                    break
                assert len(unassigned)==1,'non-unit LRAT antecedent'
                false.add(-unassigned.pop())
            assert conflict,'no LRAT conflict'
            last=i;db[i]=clause
            if not clause:empty=True
    assert empty,'LRAT never derived the empty clause'

if __name__=='__main__':
    paths=[Path(p) for p in sys.argv[1:]] or sorted(Path('data').glob('*/*.cnf'))
    for f in paths:verify(f,f.with_suffix('.lrat'))
    print('VERIFIED UNSAT',len(paths),'LRAT proofs')
