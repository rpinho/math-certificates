"""Own floating evaluator interface. Exact results come only from verify_exact.py."""
import ctypes as C, json, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
lib=C.CDLL(str(Path(__file__).with_name('libsearch.dylib')))
dp=C.POINTER(C.c_double)
lib.evaluate.argtypes=[C.c_int,dp,C.c_double,C.c_double,C.c_double,C.POINTER(C.c_int),C.c_char_p]
lib.evaluate.restype=C.c_double
lib.holes.argtypes=[C.c_int,dp,C.c_double,C.c_double,C.c_double,C.c_int,C.POINTER(C.c_ubyte)]
def load(path):
 d=json.loads(Path(path).read_text());d=d.get('measure',d)
 return float(F(str(d['Px']))),float(F(str(d['Py']))),np.array([[float(F(str(v))) for v in p] for p in d['pts']])
def evaluate(px,py,p,reach=6.,export=None):
 p=np.ascontiguousarray(p,dtype=np.float64);nr=C.c_int()
 a=lib.evaluate(len(p),p.ctypes.data_as(dp),px,py,reach,C.byref(nr),str(export).encode() if export else None)
 return a/p[:,2].sum(),a,nr.value
def holes(px,py,p,k=700,reach=6.):
 p=np.ascontiguousarray(p,dtype=np.float64);out=np.zeros((k,k),np.uint8)
 lib.holes(len(p),p.ctypes.data_as(dp),px,py,reach,k,out.ctypes.data_as(C.POINTER(C.c_ubyte)))
 return out
if __name__=='__main__':
 px,py,p=load('certificates/start59-measure.json');t=time.time()
 for i in range(3):print(evaluate(px,py,p),time.time()-t,flush=True)
