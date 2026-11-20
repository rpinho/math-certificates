from planes import read,WORDS,Oracle
from sat import face_probe
cache=read('data/planes-cache.gz')
o=Oracle()
try:
    for b in range(11):
        a=21-b
        ax=1 if b>1 else 0
        child=cache[f'{a-int(ax==0)}-{b-int(ax==1)}']
        face_probe((a,b,0),ax,child,WORDS,o)
finally:o.close()
