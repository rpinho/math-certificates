#!/usr/bin/env python3
"""Separate forest checker and exhaustive arithmetic receipt assembly.

The mathematical artifact is a manifest plus immutable gzip JSONL parts.
Default verification checks all global coverage edges and all arithmetic.
Part/range modes explicitly prove no full constant bound. Receipts record
actual checks; fresh users must replay them, not trust arbitrary receipts.
"""
import argparse,ast,gzip,hashlib,json,pathlib,time
from verify_c57c_fast import Arithmetic,prepare,require,Rejected
ROOT=pathlib.Path(__file__).resolve().parent
PARAMS=['radius','t','kappa','center','mu','bump','coefficient_caps']

def sha(path):
 h=hashlib.sha256()
 with pathlib.Path(path).open('rb')as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def code_hashes():
 todo=['verify_c57c_forest'];seen=set()
 while todo:
  name=todo.pop();p=ROOT/(name+'.py')
  if name in seen or not p.is_file():continue
  seen.add(name)
  for node in ast.walk(ast.parse(p.read_text())):
   if isinstance(node,ast.Import):todo.extend(v.name.split('.')[0]for v in node.names)
   elif isinstance(node,ast.ImportFrom)and node.module:todo.append(node.module.split('.')[0])
 return {n+'.py':sha(ROOT/(n+'.py'))for n in sorted(seen)}

def params(header):return {k:header[k]for k in PARAMS}

def open_data(path):return gzip.open(path,'rt')

def box_from_path(path):
 require(isinstance(path,str)and len(path)<=200 and all(v in '01234567'for v in path),'bad global leaf path')
 cells=[(0,0)]*4
 for digit in path:
  axis=int(digit)//2;n,d=cells[axis];cells[axis]=(2*n+int(digit)%2,d+1)
 return tuple(cells)

def scan(path,arithmetic=None,start=0,stop=None,precision=192):
 library=[];count=0;selected=0;paths=[];kinds={};last=None
 with open_data(path)as stream:
  header=json.loads(next(stream));Arithmetic(header,precision) # parameter/domain checks
  for line in stream:
   item=json.loads(line)
   if isinstance(item,dict):
    require(set(item)=={'D'},'invalid definition record');i,w=item['D'];require(type(i)is int and i==len(library)and i<1000000,'definition order/count')
    library.append(prepare(w)if arithmetic is not None else w)
   else:
    require(isinstance(item,list)and len(item)==2,'invalid leaf record');prefix,index=item;box=box_from_path(prefix)
    require(last is None or last<prefix,'duplicate or unordered part leaf');last=prefix
    require(type(index)is int and 0<=index<len(library),'undefined witness')
    paths.append(prefix);kind=library[index]['kind'];kinds[kind]=kinds.get(kind,0)+1
    if arithmetic is not None and count>=start and(stop is None or count<stop):arithmetic.leaf(box,library[index]);selected+=1
    count+=1;require(count<=5000000,'part leaf cap')
    if arithmetic is not None and selected and selected%500==0 and count>=start and(stop is None or count<=stop):print(json.dumps({'part':pathlib.Path(path).name,'selected':selected,'boxes':arithmetic.boxes}),flush=True)
 return header,paths,selected,kinds

def verify_part(path,start=0,stop=None,precision=192,receipt=None):
 begin=time.monotonic();path=pathlib.Path(path);digest=sha(path);codes=code_hashes()
 require(type(start)is int and start>=0 and(stop is None or type(stop)is int and stop>start),'bad range')
 with open_data(path)as stream:head=json.loads(next(stream))
 A=Arithmetic(head,precision);head,paths,selected,kinds=scan(path,A,start,stop,precision)
 end=len(paths)if stop is None else stop
 require(0<=start<end<=len(paths)and selected==end-start,'incomplete or out-of-range arithmetic')
 require(sha(path)==digest and code_hashes()==codes,'source/artifact changed during check')
 result={'status':'VERIFIED_ARITHMETIC_PART_NOT_FULL_PROOF'if start==0 and stop is None else 'VERIFIED_ARITHMETIC_RANGE_NOT_FULL_PROOF','artifact_sha256':digest,'parameters':params(head),'leaves':len(paths),'leaf_range':[start,end],'verified_leaves':selected,'kinds':kinds,'arithmetic_boxes':A.boxes,'extra_splits':A.extra,'precision':precision,'checker_files':codes,'seconds':time.monotonic()-begin}
 if receipt:pathlib.Path(receipt).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2),flush=True);return result

def structure(manifest):
 begin=time.monotonic();mp=pathlib.Path(manifest).resolve();data=json.loads(mp.read_text());require(data.get('format')=='c57c-forest-v1','invalid forest format');require(isinstance(data.get('parts'),list)and 0<len(data['parts'])<=32,'invalid part list')
 paths=[];parts=[];expected=None;seen=set()
 for row in data['parts']:
  name=row['file'];require(isinstance(name,str)and not pathlib.Path(name).is_absolute()and '..'not in pathlib.Path(name).parts,'invalid part path');p=mp.parent/name
  require(name not in seen,'duplicate part');seen.add(name);require(sha(p)==row['sha256'],'part hash mismatch')
  head,local,_,kinds=scan(p)
  require(sha(p)==row['sha256'],'part changed during structure check')
  if expected is None:expected=params(head)
  require(params(head)==expected,'part parameter mismatch');paths.extend(local);parts.append({'file':name,'path':str(p),'sha256':row['sha256'],'leaves':len(local),'kinds':kinds})
 require(expected==data['parameters'],'manifest parameter mismatch');paths.sort();require(0<len(paths)<=5000000,'global leaf cap');cursor=0
 def cover(prefix):
  nonlocal cursor
  require(cursor<len(paths),'missing global subtree');target=paths[cursor];require(target.startswith(prefix),'duplicate, wrong or overlapping subtree')
  if target==prefix:cursor+=1;return
  digit=int(target[len(prefix)]);require(digit%2==0,'missing global lower child');axis=digit//2
  cover(prefix+str(2*axis));cover(prefix+str(2*axis+1))
 cover('');require(cursor==len(paths),'extraneous global leaves')
 result={'status':'STRUCTURE_ONLY_NOT_A_PROOF','manifest_sha256':sha(mp),'parameters':expected,'leaves':len(paths),'parts':parts,'checker_files':code_hashes(),'seconds':time.monotonic()-begin};print(json.dumps({'global_structure':result['status'],'leaves':len(paths),'parts':len(parts)}),flush=True);return result

def aggregate(manifest,receipts,output=None,precision=192):
 begin=time.monotonic();s=structure(manifest);rows=[json.loads(pathlib.Path(p).read_text())for p in receipts];by_hash={};total=0;boxes=0;extra=0
 for row in rows:
  require(row['status']in['VERIFIED_ARITHMETIC_PART_NOT_FULL_PROOF','VERIFIED_ARITHMETIC_RANGE_NOT_FULL_PROOF'],'invalid arithmetic receipt')
  require(row['checker_files']==s['checker_files']and row['precision']==precision,'checker or precision mismatch')
  require(row['parameters']==s['parameters'],'receipt parameter mismatch');by_hash.setdefault(row['artifact_sha256'],[]).append(row)
 for part in s['parts']:
  rr=by_hash.pop(part['sha256'],[]);rr.sort(key=lambda row:row['leaf_range']);require(bool(rr),'unchecked forest part');cursor=0
  for row in rr:
   lo,hi=row['leaf_range'];require(lo==cursor and hi>lo and hi<=part['leaves'],'missing/overlapping arithmetic range');require(row['leaves']==part['leaves']and row['verified_leaves']==hi-lo,'incomplete arithmetic receipt');cursor=hi;boxes+=row['arithmetic_boxes'];extra+=row['extra_splits']
  require(cursor==part['leaves'],'unchecked part suffix');total+=cursor
 require(not by_hash and total==s['leaves'],'extra receipts or incomplete forest');result=dict(s,status='VERIFIED_CANDIDATE_UNREFEREED',verified_leaves=total,arithmetic_boxes=boxes,extra_splits=extra,precision=precision,verification_mode='complete global dyadic forest plus actual exhaustive separate arithmetic replays',receipt_sha256={str(pathlib.Path(p).name):sha(p)for p in receipts},aggregate_seconds=time.monotonic()-begin)
 if output:pathlib.Path(output).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2),flush=True);return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest',nargs='?');p.add_argument('--part');p.add_argument('--leaf-start',type=int,default=0);p.add_argument('--leaf-stop',type=int);p.add_argument('--precision',type=int,default=192);p.add_argument('--receipt');p.add_argument('--structure-only',action='store_true');p.add_argument('--aggregate',nargs='+');a=p.parse_args()
 try:
  if a.part:
   require(a.manifest is None and not a.aggregate and not a.structure_only,'incompatible part options');verify_part(a.part,a.leaf_start,a.leaf_stop,a.precision,a.receipt)
  else:
   require(a.manifest is not None,'supply manifest or --part')
   if a.aggregate:aggregate(a.manifest,a.aggregate,a.receipt,a.precision)
   elif a.structure_only:
    r=structure(a.manifest)
    if a.receipt:pathlib.Path(a.receipt).write_text(json.dumps(r,indent=2)+'\n')
   else:
    s=structure(a.manifest);receipts=[]
    # Full fresh verification: no external arithmetic receipts are inputs.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='forest-full-',dir=ROOT)as work:
     for i,row in enumerate(s['parts']):
      out=pathlib.Path(work)/f'part{i}.json';verify_part(row['path'],precision=a.precision,receipt=out);receipts.append(out)
     aggregate(a.manifest,receipts,a.receipt,a.precision)
 except (Rejected,ValueError,KeyError,TypeError,StopIteration,ZeroDivisionError,EOFError)as error:
  print('REJECTED:',str(error),flush=True);raise SystemExit(1)
