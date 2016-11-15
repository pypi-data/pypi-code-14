

from time import time
import csv
import io
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

class clustering:


    @staticmethod
    def Kmeans(dat, k):
        km = KMeans(n_clusters=k, n_jobs=45)
        km.fit(dat)
        return km


    @staticmethod
    def prepare_dat(dat_path):
        dat_all = np.loadtxt(open(dat_path, "rb"), delimiter=",", skiprows=0, dtype=int)
        dat = scale(dat_all[:,1:])
        print("read in data shape: {}".format(dat.shape))
        return dat, dat_all
        # with open(dat_path) as ifile:
        #     line = next(ifile)
        #     row_count = 1 + sum(1 for row in ifile)
        #     column_count = len(line.split(','))
        #     nda = np.empty(dtype=int, shape=(row_count, column_count))
        #     print(nda.shape)
        #
        #     ifile.seek(0, io.SEEK_SET)
        #     reader = csv.reader(ifile)
        #     for line in reader:
        #         pass



if __name__ == "__main__":
    dat, dat_all = clustering.prepare_dat('train.csv')
    km = clustering.Kmeans(dat, 2)
    with open('out','w') as ofile:
        for i in range(len(km.labels_)):
            ofile.write("{}, {}\n".format(km.labels_[i], dat_all[i][0]))
    print(km.labels_[::10])