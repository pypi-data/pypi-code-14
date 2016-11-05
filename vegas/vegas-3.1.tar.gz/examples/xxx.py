#!/usr/bin/python
from __future__ import print_function
import numpy as np
import vegas

# Test parallel evaluation
# Global variables
twopi = 2.0 * np.pi
piSq = np.pi * np.pi

# Function to integrate
def f(p):
  num = np.zeros(p.shape[0], dtype = np.float)
  denom = np.zeros_like(num)
  for i in range(p.shape[0]):
    num[i] = np.cos(twopi * (p[i].sum()))
    denom[i] = ((np.sin(np.pi * p[i]))**2).sum()
  return piSq * num / denom

def main():
  integ = vegas.Integrator(4 * [[0.0, 1.0]])
  # Convert to MPI integrand
  fparallel = vegas.MPIintegrand(f)
  neval = 1e2
  integ(fparallel, nitn=10, neval=neval)             # Initial adaptation
  result = integ(fparallel, nitn=10, neval=neval)   # Actual estimation

  if fparallel.rank == 0:
    print(result.summary())
    print("result = %s    Q = %.2f" % (result, result.Q))

if __name__ == '__main__':
  main()