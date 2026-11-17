"""Separately written same-agent screen check; no search imports."""
import json,pathlib,itertools
m=json.loads(pathlib.Path('data/screen_n13_t8.json').read_text());seen=set();balanced=0
for line in pathlib.Path('data/screen_n13_t8_witnesses.jsonl').read_text().splitlines():
 d=json.loads(line);w=d['word'];assert len(w)==14 and w[0]=='1' and w not in seen;seen.add(w)
 f={frozenset(i for i in range(13) if (mask//2**i)%2) for mask in d['family']}
 assert len(f)==len(d['family'])>=8
 assert len({w[len(s)] for s in f})==1
 assert all(s|t in f and s&t in f for s,t in itertools.product(f,repeat=2))
 balanced+=w.count('1')==7
assert len(seen)==8192 and balanced==1716
assert seen=={'1'+''.join(bits) for bits in itertools.product('01',repeat=13)}
print(json.dumps({'result':'ALL RANK WORDS REJECTED FOR UPPER SEVEN','colour_swap_representatives':len(seen),'balanced_representatives':balanced,'balanced_words':2*balanced,'total_words':2*len(seen),'witness_check':'actual frozenset union/intersection for every pair','unrestricted_lower_argument':'If no monochromatic sublattice has eight members, every maximal chain of 14 sets has seven of each colour. Adjacent maximal chains differing at one rank force their two rank-r sets to have equal colours. Single-element exchanges connect all rank-r sets. Thus the colouring depends only on rank, contradicting this exhaustive witness list.'}))
