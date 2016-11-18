#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function,
                            unicode_literals)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--eps", help="genereate .eps file", action="store_true")
args = parser.parse_args()

if args.eps:
  import matplotlib
  matplotlib.use('Agg')

import numpy as np
import ellc 
print ('version',ellc.__version__)

from ellc import ldy,lc


import matplotlib.pyplot as plt


lc_dat = np.loadtxt("NightfallCurve.dat")

phase = lc_dat[:,1]
flux_q = 10**(-0.4*lc_dat[:,5])  #  U,B,V,R,I = 2,3,4,5,6

r_1 = 0.143798
r_2 = 0.126998

#   From NightfallCurve.dat, R-band luminosities are ...
#   Band   3:     3.72708e+14     1.12038e+14
sbratio  = (1.12038/r_2**2)/(3.72708/r_1**2)
print ('sbratio = ',sbratio)


incl = 78.240
q = 0.707
shape_1 = 'roche'
shape_2 = 'roche'
ldy_ = ldy.LimbGravityDarkeningCoeffs('R')
a1,a2,a3,a4,y_1 = ldy_(11500,4.25,0.0)
ld_1 = 'claret'
ldc_1 = [a1,a2,a3,a4]
a1,a2,a3,a4,y_2 = ldy_(8180,4.25,0.0)
ld_2 = 'claret'
ldc_2 = [a1,a2,a3,a4]
print('y_1 = ',y_1)
print('y_2 = ',y_2)

alpha = 0.5
lc_1 = lc(phase,t_zero=0.5, q=q, 
    radius_1=r_1, radius_2=r_2,incl=incl,sbratio=sbratio,  
    ld_1=ld_2, ldc_1=ldc_1, gdc_1=y_1,
    ld_2=ld_2, ldc_2=ldc_2, gdc_2=y_2,
    heat_1=alpha, heat_2=alpha,
    shape_1=shape_1,shape_2=shape_2,exact_grav=False,verbose=3) 

heat_1 = [0.35,1.0,np.sum(ldc_1)]
heat_2 = [0.35,1.0,np.sum(ldc_2)]
lc_2 = lc(phase,t_zero=0.5, q=q, 
    radius_1=r_1, radius_2=r_2,incl=incl,sbratio=sbratio,  
    ld_1=ld_2, ldc_1=ldc_1, gdc_1=y_1,
    ld_2=ld_2, ldc_2=ldc_2, gdc_2=y_2,
    heat_1=heat_1, heat_2=heat_2,
    shape_1=shape_1,shape_2=shape_2,exact_grav=False) 

flux_q = flux_q/np.median(flux_q)
lc_1 = lc_1/np.median(lc_1)
lc_2 = lc_2/np.median(lc_2)

jkt_lc = np.loadtxt("jktebop.lc")
phase_jkt = jkt_lc[:,0]
flux_jkt  = 10**(-0.4*jkt_lc[:,1])
flux_jkt = flux_jkt/np.median(flux_jkt)

fig=plt.figure(1,figsize=(8,6))
line_q,=plt.plot(phase,flux_q,color='k',label='Nightfall')
line_1,=plt.plot(phase,lc_1,color='g',linestyle='--',label='ellc, simple')
line_2,=plt.plot(phase,lc_2,color='b',linestyle='--',label='ellc, heat')
line_j,=plt.plot(phase_jkt,flux_jkt,color='r',linestyle=':',label='jktebop')
plt.plot(phase_jkt-1,flux_jkt,color='r',linestyle=':')
plt.xlim([-0.25,0.75])
plt.ylim([0.9,1.05])
plt.xlabel("Phase")
plt.ylabel("Flux")
plt.legend(handles=[line_1,line_2,line_q,line_j],loc='upper right')

plt.tight_layout()

if args.eps:
  fig.savefig("Ellipsoidal.eps")
else:
  plt.show()
