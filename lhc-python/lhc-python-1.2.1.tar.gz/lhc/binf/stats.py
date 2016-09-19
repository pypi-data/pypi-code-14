#!/usr/bin/python

import numpy
import random

from scipy.stats.stats import mannwhitneyu as mwu


def mulTstCor_shuffle(pve, nve, n=1000, fn=mwu):
    scr, pval = fn(pve, nve)

    arr = pve + nve
    npve = len(pve)
    scrs = []
    for i in range(n):
        random.shuffle(arr)
        scrs.append(fn(arr[:len(pve)], arr[len(pve):])[0])
    scrs.sort()

    i = 0
    while i < len(scrs) and scrs[i] < scr:
        i += 1
    return pval, i / float(len(scrs))


class CumulativeStats:
    def __init__(self):
        self.__i = 0
        self.__avg = 0.
        self.__ssq = 0.

    def __len__(self):
        return self.__i

    def append(self, y):
        newavg = self.__avg + (y - self.__avg) / (self.__i + 1)
        dssq = self.__i * (newavg - self.__avg) * (newavg - self.__avg)

        self.__avg = newavg
        self.__ssq += dssq + (y - newavg) * (y - newavg)
        self.__i += 1

    def getMean(self):
        return self.__avg

    def getStd(self):
        if self.__i == 0:
            return 0
        return numpy.sqrt(self.__ssq / self.__i)

    def getSem(self):
        if self.__i == 0:
            return 0
        return numpy.sqrt(self.__ssq / self.__i) / numpy.sqrt(self.__i)


def ftest(cls, data):
    """ Calculate the F-score for a matrix of features. """
    amean = numpy.mean(data, 0)  # mean across rows
    nmean = numpy.mean(data[~cls], 0)
    pmean = numpy.mean(data[cls], 0)
    return ((nmean - amean) ** 2 + (pmean - amean) ** 2) / \
           (numpy.sum((data[~cls] - nmean) ** 2, 0) + numpy.sum((data[cls] - pmean) ** 2, 0))


def main(argv):
    if argv[1] == 'mulTstCor':
        pve = []
        nve = []
        with open(argv[2], encoding='utf-8') as fileobj:
            for line in fileobj:
                parts = line.split()
                if parts[0] == argv[2]:
                    pve.append(float(parts[1]))
                else:
                    nve.append(float(parts[1]))

        print(mulTstCor(pve, nve), numpy.mean(pve) / numpy.mean(nve))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
