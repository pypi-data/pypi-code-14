#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt
K1=3.5
K2=9
M1=0.7
M2=1
alpha=1.57
delta=1
thetamin=0.005
Hmax=5
'''print('本次程序为双次晶格各向异性起始磁化曲线模拟\n')
print('请输入第一个次晶格各向异性常数K1：\n')
K1=input()
print('请输入第二个次晶格各向异性常数K2：\n')
K2=input()
print('请输入第一个次晶格饱和磁化强度M1：\n')
M1=input()
print('请输入第二个次晶格饱和磁化强度M2：\n')
M2=input()
print('请输入两个各向异性之间夹角alpha(rad)：\n')
alpha=input()
print('请输入反铁磁耦合系数delta：\n')
delta=input()
print('请输入最小角度变化thetamin(rad):\n')
thetamin=input()
#print('请输入最大外场Hmax:T\n')
#Hmax=input()'''
#使用的方法是划分网格寻找不同外场下能量的最小值
mag=[]
Hextenal=[]
k=0
while(k<Hmax):
	PI=3.1415926
	Hextenal.append(k)
	emin=K2*math.sin(alpha)*math.sin(alpha)-k*(M1+M2)+delta*M1*M2
	imin=jmin=0
	i=0
	while(i<alpha):
		j=0
		while(j<PI-alpha):
			E=K1*math.sin(i)*math.sin(i)+K2*math.sin(alpha+j)*math.sin(alpha+j)-k*(M1*math.cos(i)+M2*math.cos(j))+delta*M1*M2*math.cos(i+j)
			if E<emin:
				emin=E
				imin=i
				jmin=j
			j=j+thetamin
		i=i+thetamin
	mag.append(M1*math.cos(imin)+M2*math.cos(jmin))
	k=k+0.01
plt.plot(Hextenal,mag,'b')
plt.show()
del Hextenal
del mag
