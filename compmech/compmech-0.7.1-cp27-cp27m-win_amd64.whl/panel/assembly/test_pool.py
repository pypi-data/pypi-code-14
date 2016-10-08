from multiprocessing import Pool

import numpy as np

class A(object):
    def calc_k0(self):
        return np.ones((1000, 1000))



if __name__ == '__main__':
    panels = [A(), A(), A(), A()]
    k0 = 0.
    p = Pool(4)
