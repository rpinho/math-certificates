"""Shared runner: one persistent compiled search worker, checked witnesses and no-trees."""
import subprocess,json,pathlib,gzip,os,time,resource
from check import tree,witness
class Runner:
 def __init__(self):
  self.p=subprocess.Popen(['src/poset'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
  pathlib.Path('logs/worker_pids.txt').open('a').write(str(self.p.pid)+'\n')
  self.cache={};self.no=0;self.yes=0;self.cpu0=time.process_time()
 def decide(self,word,c,t):
  key=(word,c,t)
  if key in self.cache:return self.cache[key]
  self.p.stdin.write(f'{word} {c} {t} certificates/search\n');self.p.stdin.flush()
  row=json.loads(self.p.stdout.readline())
  assert (row['word'],row['colour'],row['threshold'])==key
  if row['found']:
   witness(len(word)-1,word,c,t,row['family']);self.yes+=1
  else:
   tree(row['proof'],word,c,t);self.no+=1
   path=pathlib.Path(row['proof']);data=path.read_bytes()
   with gzip.open(str(path)+'.gz','wb') as out:out.write(data)
   path.unlink() # session-created temporary uncompressed copy
   row['proof']+='.gz'
  self.cache[key]=row
  return row
 def close(self):
  self.p.stdin.close();self.p.wait();assert self.p.returncode==0
 def __enter__(self):return self
 def __exit__(self,*exc):
  if exc[0]:self.p.terminate()
  self.close()

def canonical(w):
 inv=lambda s:''.join('1' if c=='0' else '0' for c in s)
 return min(w,w[::-1],inv(w),inv(w[::-1]))

def chain(word,c):return [(1<<i)-1 for i,ch in enumerate(word) if int(ch)==c]
