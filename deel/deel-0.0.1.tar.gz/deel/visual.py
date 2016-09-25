import numpy as np 
import matplotlib.pyplot as plt 
import math
from tensor import *
from network import *
from deel import *

def Visualize(nda):
	if nda.ndim >3:
		Visualize(nda[0])
	if nda.ndim == 3:
		fig = plt.figure()
		size = len(nda)
		wide = int(math.sqrt(size))+1
		n=1
		for kernel in nda:
			subfig = fig.add_subplot(wide,wide,n)
			subfig.imshow(kernel)
			n+=1
		plt.show()



