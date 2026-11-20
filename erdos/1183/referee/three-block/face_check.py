# Structural regeneration of the 48 terminal face CNFs up to variable renaming, from my own child lists.
import sys, os, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['x', '../data', 'out_face']
import induct as I
I.run()
D = '../data/face'
okn = 0; rows = []
for s in sorted(I.S):
    if sum(s) != 21: continue
    name = '%d-%d-%d' % s
    path = os.path.join(D, name + '.cnf')
    if not os.path.exists(path): print('missing', name); continue
    j = I.child3(s) if s[2] else I.child2(s)
    c = list(s); c[j] -= 1; c = tuple(c)
    Z = I.S[c][2]
    pools = [sum(1 for zm in Z if (zm >> z) & 3) for z in range(3)]
    cls = [list(map(int, l.split()[:-1])) for l in open(path) if l[0] not in 'pc']
    ctx = cls[0]; rest = cls[1:]
    choice = {}; binar = set(); other = 0
    for cl in rest:
        if len(cl) >= 2 and cl[0] < 0 and -cl[0] in ctx and all(x > 0 for x in cl[1:]):
            choice.setdefault(-cl[0], []).append(set(cl[1:]))
        elif len(cl) == 2 and cl[0] < 0 and cl[1] < 0: binar.add(frozenset(cl))
        else: other += 1
    theirs = []; complete = True
    for cv in ctx:
        L, U = choice.get(cv, [set(), set()])
        theirs.append(len(L)); complete &= len(L) == len(U)
        complete &= all(frozenset((-l, -u)) in binar for l in L for u in U)
    nb = sum(p * p for p in pools)
    ok = (sorted(theirs) == sorted(pools) and theirs == pools and complete and len(binar) == nb and other == 0 and len(ctx) == 3)
    okn += ok
    if not ok: print(name, 'mine', pools, 'theirs', theirs, complete, len(binar), nb, other)
print('face CNFs structurally equal to my regeneration (3 contexts, pools = my child lists, all pairs forbidden):', okn, '/ 48')
