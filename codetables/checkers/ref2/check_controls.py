"""Known-distance controls and scalar witness multiplication."""
import collections,itertools,json,pathlib,subprocess
out={}
# Identity coordinates repeated 12 or 13 times exercises 128-byte words,
# weights > 127, base-five carries, and task splits above eight digits.
g=[[int(c%10==r) for c in range(128)] for r in range(10)]
p=pathlib.Path('control_repetition128_k10.txt');p.write_text('\n'.join(' '.join(map(str,r)) for r in g)+'\n')
x=json.loads(subprocess.check_output(['./checker',str(p),'4']))
h={0:1}
for size in [13]*8+[12]*2:
 z=collections.Counter(h)
 for w,c in h.items(): z[w+size]+=4*c
 h=z
assert x['weight_enumerator']=={str(w):c for w,c in h.items()}
pathlib.Path('results/control_repetition128_k10.json').write_text(json.dumps(x,indent=2)+'\n')
out['repeated_identity_full_distribution']='matches (1+4z^13)^8 (1+4z^12)^2'
# Full ordinary scalar enumeration of an actual five-row subcode at each width.
for name in ['q5_n74_k12_d43','q5_n128_k14_d79']:
 g=[list(map(int,r.split())) for r in pathlib.Path('inputs/'+name+'.txt').read_text().splitlines()]
 p=pathlib.Path('control_'+name+'_first5.txt');p.write_text('\n'.join(' '.join(map(str,r)) for r in g[:5])+'\n')
 v=json.loads(subprocess.check_output(['./checker',str(p),'1']))
 h=collections.Counter()
 for u in itertools.product(range(5),repeat=5):
  h[sum(sum(a*b for a,b in zip(u,col))%5!=0 for col in zip(*g[:5]))]+=1
 assert v['weight_enumerator']=={str(w):c for w,c in h.items()}
 out[name+'_scalar_first5']='all 3125 codewords match complete histogram'
 r=json.load(open('results/'+name.rsplit('_d',1)[0]+'.json'))
 c=[sum(a*b for a,b in zip(r['witness_message'],col))%5 for col in zip(*g)]
 assert c==r['witness_codeword'] and sum(a!=0 for a in c)==r['minimum_distance']
 assert sum(r['weight_enumerator'].values())==5**len(g)
 out[name+'_witness']='scalar multiplication matches minimum-weight witness'
print(json.dumps(out,indent=2))
