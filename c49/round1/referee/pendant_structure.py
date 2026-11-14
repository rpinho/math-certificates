"""Reconstruct only mathematical pendant projection families from their definition."""
import collections
import json
from pathlib import Path

seeds=[{0,1,2,3,4,5,6},{0,1,2,3,4,6,7},{0,1,2,6,9}]
squares={a*a%11 for a in range(1,11)}
H={sum(1<<((a*x+b)%11) for x in seed) for seed in seeds for a in squares for b in range(11)}
assert len(H)==121
avoiding={x>>1 for x in H if not x&1}
containing={x>>1 for x in H if x&1}
assert len(avoiding)==46 and len(containing)==75
assert not avoiding&containing
base=set(map(int,Path('baseline.masks').read_text().split()))
cand=set(map(int,Path('candidate.masks').read_text().split()))
common=base&cand
out=[]
for empty_shift,other_shift in [(8,18),(18,8)]:
    groups=collections.defaultdict(set)
    for x in common:
        if not ((x>>empty_shift)&1023): groups[x&255].add((x>>other_shift)&1023)
    assert len(groups)==15
    kinds={}
    for core,projection in groups.items():
        assert projection in (avoiding,containing)
        kinds[str(core)]='46 avoiding root' if projection==avoiding else '75 containing root (root removed)'
    assert collections.Counter(kinds.values())=={'46 avoiding root':11,'75 containing root (root removed)':4}
    out.append({'empty_pendant_first_point':empty_shift,'other_pendant_first_point':other_shift,'core_fibers':kinds})
result={'H_members':len(H),'root_avoiding':46,'root_containing':75,'both_pendant_fibers_complete':True,'pendants':out}
Path('logs/pendant_structure.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
