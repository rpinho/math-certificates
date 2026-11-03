"""Checker-only strict positivity for an enclosure of a symmetric matrix.

Gershgorin is attempted first. If it is too conservative, interval
Cholesky recursively encloses the unique positive diagonal factor.
Every pivot must be strictly positive; a failed proposal never accepts.
No discovery code is imported.
"""
from flint import arb

def certified_pd(matrix):
 n=len(matrix)
 if not all(len(row)==n for row in matrix):return False
 if not all(matrix[i][j].is_finite()for i in range(n)for j in range(n)):return False
 if all(matrix[i][i]>sum(abs(matrix[i][j])for j in range(n)if i!=j)for i in range(n)):return True
 L=[[arb(0)for _ in range(n)]for _ in range(n)]
 for column in range(n):
  pivot=matrix[column][column]-sum(L[column][k]**2 for k in range(column))
  if not pivot>0:return False
  L[column][column]=pivot.sqrt()
  if not L[column][column]>0:return False
  for row in range(column+1,n):
   L[row][column]=(matrix[row][column]-sum(L[row][k]*L[column][k]for k in range(column)))/L[column][column]
   if not L[row][column].is_finite():return False
 return True
