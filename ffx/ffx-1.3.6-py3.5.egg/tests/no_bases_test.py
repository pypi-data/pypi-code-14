import ffx
import numpy as np

X = np.genfromtxt("train_X.csv", delimiter=",")
y = np.genfromtxt("train_y.csv")
models = ffx.run(X, y, X, y, ["x0", "x1", "x2", "x3", "x4"])
for model in models:
    print model
