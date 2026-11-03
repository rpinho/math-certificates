"""Checker-only chain rule with exact zero-gradient fast paths.
Skipping arithmetic is permitted only when all four derivatives are exactly
zero. Active derivatives use the same four-component product/chain rules.
"""
from flint import acb as ball
ZERO=(ball(0),)*4
class Core:
 __slots__=('value','partials','active')
 def __init__(self,real=0,imag=None,partials=None):
  if isinstance(real,Core)and imag is None:
   self.value=real.value;self.partials=real.partials if partials is None else tuple(map(ball,partials));self.active=real.active if partials is None else not all(v==0 for v in self.partials);return
  if imag is not None:
   z=Core(real)+ball(0,1)*Core(imag);self.value=z.value;self.partials=z.partials;self.active=z.active;return
  self.value=ball(real);self.partials=ZERO if partials is None else tuple(map(ball,partials));self.active=partials is not None and not all(v==0 for v in self.partials)
 @staticmethod
 def wrap(v,d=None):
  z=object.__new__(Core);z.value=v;z.partials=ZERO if d is None else tuple(d);z.active=d is not None;return z
 def __add__(self,r):
  r=Core(r);v=self.value+r.value
  if not self.active and not r.active:return Core.wrap(v)
  if not self.active:return Core.wrap(v,r.partials)
  if not r.active:return Core.wrap(v,self.partials)
  return Core.wrap(v,[a+b for a,b in zip(self.partials,r.partials)])
 __radd__=__add__
 def __neg__(self):return Core.wrap(-self.value,[-a for a in self.partials]if self.active else None)
 def __sub__(self,r):return self+-Core(r)
 def __rsub__(self,r):return Core(r)+-self
 def __mul__(self,r):
  r=Core(r);v=self.value*r.value
  if not self.active and not r.active:return Core.wrap(v)
  if not self.active:return Core.wrap(v,[self.value*b for b in r.partials])
  if not r.active:return Core.wrap(v,[a*r.value for a in self.partials])
  return Core.wrap(v,[a*r.value+self.value*b for a,b in zip(self.partials,r.partials)])
 __rmul__=__mul__
 def inverse(self):
  v=1/self.value;return Core.wrap(v,[-a*v*v for a in self.partials]if self.active else None)
 def __truediv__(self,r):return self*Core(r).inverse()
 def __rtruediv__(self,r):return Core(r)*self.inverse()
 def __pow__(self,n):
  if n<0:return self.inverse()**(-n)
  if n==0:return Core(1)
  v=self.value**n;return Core.wrap(v,[n*self.value**(n-1)*a for a in self.partials]if self.active else None)
 def conjugate(self):return Core.wrap(self.value.conjugate(),[a.conjugate()for a in self.partials]if self.active else None)
 @property
 def real(self):return Core.wrap(ball(self.value.real),[ball(a.real)for a in self.partials]if self.active else None)
 @property
 def imag(self):return Core.wrap(ball(self.value.imag),[ball(a.imag)for a in self.partials]if self.active else None)
 def sin(self):return Core.wrap(self.value.sin(),[self.value.cos()*a for a in self.partials]if self.active else None)
 def cos(self):return Core.wrap(self.value.cos(),[-self.value.sin()*a for a in self.partials]if self.active else None)
 def exp(self):
  v=self.value.exp();return Core.wrap(v,[v*a for a in self.partials]if self.active else None)
