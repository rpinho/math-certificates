"""Required destructive-in-copy certificate controls; originals stay intact."""
import pathlib,json,gzip,lzma,subprocess,copy
from check import tree
from coverage import rejection
from check_balanced import row_check

out={}
def rejected(name,call):
 try:call()
 except (AssertionError,ValueError,KeyError,TypeError,EOFError):out[name]='REJECTED'
 else:raise AssertionError('corruption accepted: '+name)

# Drop a covering leaf known to cover the all-zero canonical word.
labels=pathlib.Path('logs/n4_T2_coverage.labels').read_text().splitlines()
idx=next(i for i,s in enumerate(labels) if s[0]=='R' and set(s.split()[1])=={'0'})
p=pathlib.Path('logs/corrupt_coverage.labels');p.write_text('\n'.join(labels[:idx]+labels[idx+1:])+'\n')
r=subprocess.run(['src/coverage','4',str(p)],capture_output=True,text=True)
assert r.returncode!=0;out['drop_coverage_leaf']='REJECTED: '+r.stderr.strip()

# Use a real nonzero suffix lift, then shift its offset by one.
lift=None
for p in sorted(pathlib.Path('certificates/n4_T2').glob('*.jsonl.gz')):
 with gzip.open(p,'rt') as f:
  for line in f:
   x=json.loads(line)
   if x[0]=='reject' and x[4]>0:lift=x;break
 if lift:break
assert lift;rejection(lift,2);x=copy.deepcopy(lift);x[4]+=1
rejected('shift_lift_offset',lambda:rejection(x,2))

# Flip one coordinate in one member of a balanced-word witness.
p=pathlib.Path('certificates/n21_balanced.txt')
opener=open
if not p.exists():p=pathlib.Path(str(p)+'.xz');opener=lzma.open
with opener(p,'rt') as f:line=next(f)
fields=line.split();fields[2]=str(int(fields[2])^1)
row_check(21,line)
rejected('flip_balanced_set',lambda:row_check(21,' '.join(fields)))

# Truncate one tree and alter a branch weight and the externally bound word.
row=json.load(open('certificates/upper_n21.json'));w=row['word'];c=row['colours'][0]
raw=gzip.open(c['proof'],'rt').readlines();p=pathlib.Path('logs/corrupt.tree.gz')
with gzip.open(p,'wt') as f:f.writelines(raw[:-1])
rejected('truncate_tree',lambda:tree(p,w,c['colour'],c['maximum']+1))
x=raw.copy();edges=json.loads(x[2]);edges[0][1]+=1;x[2]=json.dumps(edges)+'\n'
with gzip.open(p,'wt') as f:f.writelines(x)
rejected('change_weight',lambda:tree(p,w,c['colour'],c['maximum']+1))
rejected('flip_word',lambda:tree(c['proof'],('1' if w[0]=='0' else '0')+w[1:],c['colour'],c['maximum']+1))
pathlib.Path('logs/corruptions.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
