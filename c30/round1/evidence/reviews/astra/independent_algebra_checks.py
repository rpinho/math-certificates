"""Exact symbolic checks of identities connecting the checker to the proof."""
from pathlib import Path
import ast
import json
import sympy as S

z,q,s,w,v,x,y=S.symbols('z q s w v x y')
Q=(1-S.sqrt(1-4*z))/2
H=1/(1-q*Q)
# Read only the displayed closed-form expressions, not their implementation.
tree=ast.parse((Path(__file__).resolve().parents[3]/'verify_baseline.py').read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='functions')
env={'q':q,'s':s,'D':2-q+q*s}
for node in fn.body:
    if isinstance(node,ast.Assign) and node.targets[0].id in ('h0','h2','h3'):
        name=node.targets[0].id
        env[name]=eval(compile(ast.Expression(node.value),'<expression>','eval'),{},env)
for j in (0,2,3):
    target=S.diff(z**j*H,z,j)/S.factorial(j)
    # Work in positive s=sqrt(1-4z).
    target=target.subs(z,(1-s*s)/4).subs(S.sqrt(s*s),s)
    assert S.simplify(target-env['h'+str(j)])==0,j
assert S.simplify(S.diff(z*H,z)-H-z*q*H**2/S.sqrt(1-4*z))==0
g=lambda t:z*z*t*t/(1-z*t)
R=z*z*(x+y-z*x*y)/((1-z*x)*(1-z*y))
assert S.factor((g(x)-g(y))/(x-y)-R)==0
assert S.factor((S.diff(g(x),x)-R)/(x-y)-z*z/((1-z*x)**2*(1-z*y)))==0

rho=S.Rational(4,27)
D=(1-w)*(1+w)**3
zw=w/(1+w)**3
p2=z*v-z*z*(1+v)-z*z*v*(1+v)
p1=-v+z*(1+2*v+v*v)+z*z*(1+v)*S.Rational(27,16)
p0=v-z*(1+v)*S.Rational(27,16)
assert S.factor((p1*p1-4*p2*p0).subs(z,rho)-(2*v-9)*(2*v-1)**3/729)==0
h=S.symbols('h')
eps=(rho-zw).subs(w,S.Rational(1,2)+h)
assert S.limit(eps/h**2,h,0)==S.Rational(16,81)
residual=(D-S.Rational(27,16)).subs(w,S.Rational(1,2)+h)+S.Rational(729,32)*eps
b=-S.limit(residual/h**3,h,0)/S.Rational(4,9)**3
assert b==S.Rational(2187,16)
assert 3*rho*b*S.Rational(4,9)==27
print(json.dumps({'status':'PASS','identities':['H0,H1,H2,H3 derivative definitions versus checker',
    'R divided difference','V divided difference','critical discriminant',
    'epsilon quadratic coefficient','D singular coefficient 2187/16',
    'first-moment normalization 4/27']},indent=2))
