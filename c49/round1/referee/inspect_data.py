import collections
import hashlib
import json
from pathlib import Path

b = set(map(int, Path('baseline.masks').read_text().split()))
cdata = json.loads(Path('candidate.json').read_text())
assert cdata['n'] == 28 and cdata['ports'] == [0, 1]
c = cdata['masks']
assert all(type(x) is int and 0 <= x < 2**28 for x in c)
assert len(c) == len(set(c))
c = set(c)
Path('candidate.masks').write_text('\n'.join(map(str,sorted(c)))+'\n')
delta=json.loads(Path('claimed_delta.json').read_text())
removed=sorted(b-c); added=sorted(c-b)
assert removed == delta['removed'] and added == delta['added']
assert len(c)-len(b)==delta['net_members']==11
# Identify the published exceptional region from its point supports,
# without consulting the delta lists for the classification.
h1=((1<<10)-1)<<8; h2=((1<<10)-1)<<18
exceptional=sorted(x for x in b if x & ~h1 == 0 or x == (h2 | (1<<2) | (1<<4) | (1<<5)))
assert len(exceptional)==21 and exceptional==removed
Path('exceptions21.masks').write_text('\n'.join(map(str,exceptional))+'\n')
assert all(x.bit_count()==7 and ((x & ~h1)==0 or (x & ~h2)==0) for x in added)
assert sum((x & ~h1)==0 for x in added)==16
assert sum((x & ~h2)==0 for x in added)==16
# Nonexceptional groups with an empty pendant: count full projection fibers.
common=b&c
fibers=[]
for empty,other,shift in [(h1,h2,18),(h2,h1,8)]:
    g=collections.defaultdict(set)
    for x in common:
        if not x&empty: g[x&255].add((x&other)>>shift)
    fibers.append({'members':sum(map(len,g.values())), 'fibers':len(g),
                   'fiber_size_histogram':dict(sorted(collections.Counter(map(len,g.values())).items()))})
result={'candidate_sha256':hashlib.sha256(Path('candidate.json').read_bytes()).hexdigest(),
        'baseline_members':len(b),'candidate_members':len(c),'common_members':len(common),
        'removed':removed,'added':added,'delta_exact':True,'new_member_sizes':[7],
        'new_members_per_pendant':[16,16],'lifted_fibers':fibers,
        'common_both_pendants_nonempty':sum(bool(x&h1) and bool(x&h2) for x in common),
        'candidate_min_mask':min(c),'candidate_max_mask':max(c),
        'candidate_point_union': __import__('functools').reduce(int.__or__,c),
        'candidate_size_histogram':dict(sorted(collections.Counter(x.bit_count() for x in c).items()))}
Path('logs/data_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
