import itertools,json
src=open('verify_partial_b.py').read()
ns={}; exec("import itertools,json,time\n"+src[src.index('def patterns'):src.index('\nif a.positive')],ns)
Check=ns['Check']
class C2(Check):
    def visit(self,known,done):
        if self.leaves: return
        if self.nodes==0: self.trace=[]
        before=self.leaves
        # record whether the fresh-tensor branch is used
        avail=[j for j in range(self.n) if self.selected>>j&1 and not done>>j&1 and any(s>>j&1 for s in known)]
        if not avail and done&self.selected!=self.selected: self.fresh_hits=getattr(self,'fresh_hits',0)+1
        return Check.visit(self,known,done)
for omit in [(11,),(11,23)]:
    sel=((1<<24)-1)
    for o in omit: sel^=1<<o
    c=C2(24,128,sel,positive=True); r=c.run()
    print('omit',omit,r,'fresh-branch nodes',getattr(c,'fresh_hits',0))
# negative sanity: same but N=127 (one less norm) should give no leaf for the two-product structure? just report
