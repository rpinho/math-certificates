"""Interval matrix mean value after an exact dyadic congruence.

The Taylor remainder E is fixed at its rigorously computed box upper bound
while differentiating. This prevents dropping an uncomputed derivative of E.
"""
import math
from fractions import Fraction as Q
from flint import arb,acb,arb_mat
from c57c_checker_core_fast import Core as C
from c57c_checker_nested_fast import scalar_coefficients,quadratic_gram
from verify_c57c_center6 import rational,require

def preconditioner(A):
    n=9;order=list(range(1,n))+[0]
    try:
        M=[[float(A[i][k].mid()) for k in order] for i in order];L=[[0.]*n for _ in range(n)]
        for row in range(n):
            for col in range(row+1):
                entry=M[row][col]-sum(L[row][j]*L[col][j] for j in range(col))
                if row==col:
                    if not math.isfinite(entry) or entry<=0:return None
                    L[row][col]=math.sqrt(entry)
                else:L[row][col]=entry/L[col][col]
        proposal=[[0.]*n for _ in range(n)]
        for j in range(n):
            for i in range(j,-1,-1):proposal[i][j]=((1. if i==j else 0.)-sum(L[k][i]*proposal[k][j] for k in range(i+1,j+1)))/L[i][i]
        triangle=[[rational(Q.from_float(v)) for v in row] for row in proposal]
        require(all(triangle[i][i]>0 for i in range(n)),'noninvertible proposal')
        require(all(triangle[i][j]==0 for i in range(n) for j in range(i)),'nontriangular proposal')
        R=[[arb(0) for _ in range(n)] for _ in range(n)]
        for i,original in enumerate(order):R[original]=triangle[i]
        return R
    except (ValueError,ZeroDivisionError,OverflowError):return None

def rotate(A,R):
    rr=arb_mat(R);product=rr.transpose()*arb_mat(A)*rr
    return [[product[i,j]for j in range(9)]for i in range(9)]

def core_gram(cells,witness,R,kappa,t,q,E,point=False):
    xs=[]
    for axis,(n,d) in enumerate(cells):
        midpoint=arb(2*n+1)/2**(d+1);v=midpoint if point else arb(midpoint,arb(1)/2**(d+1))
        xs.append(C(v,partials=[int(not point and axis==j) for j in range(4)]))
    s=xs[0]/3;b=C(arb(2)/3)-s*s/2;phase=xs[2]*(arb.pi()/2);theta=xs[3]*(2*arb.pi())
    a=b*xs[1]*(phase.cos()+acb(0,1)*phase.sin());m=b*b*xs[1]*xs[1]
    center=s*((C(arb(2)/5)-m/3-s*s/5)*a.real-acb(0,1)*(C(arb(25)/24)-3*m/2-s*s/4)*a.imag)
    w0=center+R*(theta.cos()+acb(0,1)*theta.sin());epsilon=kappa*(-2500*(C(arb(1)/3)-s)**2-100*m).exp()
    w=(w0,C(1),C(acb(0,1)),C(),C(),C());coefficients=scalar_coefficients(s,a,w,t,q,witness)
    return quadratic_gram(s,a,m,epsilon,E,coefficients,witness['zeta'])

def positive_mean(cells,witness,R,kappa,t,q,E):
    midpoint=core_gram(cells,witness,R,kappa,t,q,E,True)
    center=[[-C(v).value.real for v in row] for row in midpoint];P=preconditioner(center)
    if P is None:return False
    B=rotate(center,P);whole=core_gram(cells,witness,R,kappa,t,q,E)
    for axis,(n,d) in enumerate(cells):
        derivative=[[-C(v).partials[axis].real for v in row] for row in whole];rotated=rotate(derivative,P);delta=arb(0,arb(1)/2**(d+1))
        for i in range(9):
            for j in range(9):B[i][j]+=rotated[i][j]*delta
    return all(B[i][i]>sum(abs(B[i][j]) for j in range(9) if j!=i) for i in range(9))
