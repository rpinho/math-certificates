import sys,platform,importlib.metadata,json,ctypes
from pathlib import Path
x={'python':sys.version,'platform':platform.platform(),'packages':{k:importlib.metadata.version(k) for k in ['numpy','scipy','cvxpy','clarabel','scs','pynauty','highspy']},'gmp':ctypes.c_char_p.in_dll(ctypes.CDLL('libgmp.so.10'),'__gmp_version').value.decode()}
Path('receipts/environment.json').write_text(json.dumps(x,indent=2));print(json.dumps(x,indent=2))
