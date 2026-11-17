"""Direct closure and complete balanced-word coverage, no search imported."""
import sys,math,json,gzip,lzma,pathlib,time

def row_check(n,line):
 fields=line.split();w=fields[0];c=int(fields[1]);family=list(map(int,fields[2:]));F=set(family)
 assert len(w)==n+1 and set(w)<=set('01') and w.count('1')==(n+1)//2
 assert c in (0,1) and len(F)==len(family)>=(n+3)//2
 assert all(0<=x<(1<<n) and int(w[x.bit_count()])==c for x in F)
 for x in F:
  for y in F:assert x&y in F and x|y in F
 return int(w,2)

def check(n,path):
 start=time.time();seen=bytearray(1<<(n+1));count=0
 opener=lzma.open if str(path).endswith('.xz') else gzip.open if str(path).endswith('.gz') else open
 with opener(path,'rt') as inp:
  for line in inp:
   key=row_check(n,line);assert not seen[key],'duplicate word';seen[key]=1;count+=1
 assert count==math.comb(n+1,(n+1)//2)
 result=dict(n=n,balanced_words=count,threshold=(n+3)//2,seconds=time.time()-start)
 pathlib.Path(f'logs/balanced{n}_check.json').write_text(json.dumps(result,indent=2)+'\n')
 print('BALANCED PASS',result,flush=True)
 return result
if __name__=='__main__':check(int(sys.argv[1]),sys.argv[2])
