'''
Example containing a simple 2D distribution of sampled
points along a uniform circle (4000 training points).

We will pass this into the MUNGE function to expand to 
40,000 training points. The resulting sample distribution
should closely resemble that of the uniform circle.
'''

import numpy as np
import matplotlib.pyplot as plt

# make the toy data
r = 0.5
num = 10000
x = np.random.uniform( low=0 , high=1 , size=num ) - 0.5
y = np.sqrt( r**2 - x**2 )
y[num/2:] *= -1

# add some noise 
param_scale = 0.25
x_noise = ( np.random.random( num ) - 0.5 ) * param_scale
y_noise = ( np.random.random( num ) - 0.5 ) * param_scale
x += x_noise
y += y_noise

# plt.figure()
# plt.plot(x, y, 'o')
# plt.savefig('./originaldata.png')
# plt.show()

T = np.vstack( ( x, y ) ).T

# munge the data
import munge
k = 10 # make 100k points
p = 0.5
s = 1.0
A_type = [True, True]

T_munged = munge.munge( T , k , p , s , A_type=A_type )

x , y = T_munged[:, 0], T_munged[:, 1]

plt.figure()
plt.plot(x, y, 'o')
plt.savefig('./mungeddata.png')
plt.show()