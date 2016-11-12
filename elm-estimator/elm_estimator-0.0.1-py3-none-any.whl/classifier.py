# coding:utf-8
from sklearn import linear_model, svm, tree
import numpy as np


class Classifer(object):
    def __init__(self, n_hidden=2000):
        self.clf = None
        self.n_hidden = n_hidden
        self.a = None
        self.b = None
        self.beta = None

    def _forward(self, X):
        t = np.dot(self.a, X.T).T + self.b
        return 1.0/(1.0 + np.exp(-t))

    def fit(self, X, y):
        n, d = X.shape
        self.a = np.random.randn(self.n_hidden, d)
        self.b = np.random.randn(self.n_hidden)

        h = self._forward(X)

        self.beta = np.dot(np.linalg.pinv(h), y)

    def partial_fit(self, X, y):
        n, d = X.shape

        h = self._forward(X)
        self.clf.partial_fit(h, y)

    def predict(self, X):
        n, d = X.shape
        h = self._forward(X)
        return np.dot(h, self.beta)
