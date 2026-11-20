# Own LRAT checker (RUP with positive hints only; RAT/negative hints rejected). Usage: lrat.py cnf lrat
import sys
def check(cnf_path, lrat_path):
    db = {}
    nv = 0; i = 0
    for ln in open(cnf_path):
        if ln[0] == 'c': continue
        if ln[0] == 'p': nv = int(ln.split()[2]); continue
        t = list(map(int, ln.split()))
        if not t: continue
        assert t[-1] == 0
        i += 1; db[i] = t[:-1]
    empty = False
    for ln in open(lrat_path):
        t = ln.split()
        if not t or t[0] == 'c': continue
        cid = int(t[0])
        if t[1] == 'd':
            for x in t[2:-1]: db.pop(int(x), None)
            continue
        nums = list(map(int, t[1:]))
        z = nums.index(0); lits = nums[:z]; hints = nums[z + 1:]
        if not hints or hints[-1] != 0: return 'BAD syntax at %d' % cid
        hints = hints[:-1]
        if any(h <= 0 for h in hints): return 'REJECT: non-positive hint at %d' % cid
        if cid in db: return 'REJECT: id reuse %d' % cid
        asg = {-l for l in lits}
        conflict = False
        for h in hints:
            c = db.get(h)
            if c is None: return 'REJECT: missing antecedent %d at %d' % (h, cid)
            un = [l for l in c if -l not in asg]
            if any(l in asg for l in c): return 'REJECT: satisfied hint %d at %d' % (h, cid)
            if not un: conflict = True; break
            if len(un) > 1: return 'REJECT: non-unit hint %d at %d' % (h, cid)
            asg.add(un[0])
        if not conflict: return 'REJECT: no conflict at %d' % cid
        db[cid] = lits
        if not lits: empty = True; break
    return 'VERIFIED' if empty else 'REJECT: no empty clause'
if __name__ == '__main__':
    print(check(sys.argv[1], sys.argv[2]))
