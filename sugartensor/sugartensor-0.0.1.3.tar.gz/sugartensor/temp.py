import numpy as np
import matplotlib.pyplot as plt

# load data
x = np.genfromtxt('/home/mansour/Downloads/sample.csv', delimiter=',', dtype=np.float32)
x = x[1:, 1:]

window = 384  # window size
max = 3000  # max value

# delete zero pad data
n = ((np.where(np.any(x, axis=1))[0][-1] + 1) // window) * window
x = x[:n] / max

# make to matrix
X = np.asarray([x[i:i+window] for i in range(n-window)])
np.random.shuffle(X)

# plot result
_, ax = plt.subplots(10, 10, sharex=True, sharey=True)
for i in range(10):
    for j in range(10):
        ax[i][j].plot(X[i * 10 + j, :, 0])
        ax[i][j].plot(X[i * 10 + j, :, 1])
        ax[i][j].set_axis_off()
plt.savefig('/home/mansour/prj/sugartensor/sugartensor/example/asset/train/hyundai/original.png', dpi=600)
plt.show()

##

import numpy as np
import joblib
import matplotlib.pyplot as plt


# load data
data = joblib.load('/shared/asan/dild/data/patch.manufac.20x20.pkl')['siemens']
X = []
for klass in data:
    for im in klass:
        X.append(im)
X = np.asarray(X)

# shuffle and dimension matching
np.random.shuffle(X)

# plot result
_, ax = plt.subplots(10, 10, sharex=True, sharey=True)
for i in range(10):
    for j in range(10):
        ax[i][j].imshow(X[i * 10 + j], 'gray')
        ax[i][j].set_axis_off()
plt.savefig('/home/mansour/prj/sugartensor/sugartensor/example/asset/train/dild/original.png', dpi=600)
plt.show()

##

import nltk
nltk.download()

##
import joblib
import numpy as np
import matplotlib.pyplot as plt

# load data
data = joblib.load('/shared/asan/dild/data/patch.manufac.20x20.pkl')['siemens']
X, Y = [], []
for label, klass in enumerate(data):
    for im in klass:
        X.append(im)
        Y.append(label)
X, Y = np.asarray(X), np.asarray(Y)

##

import sugartensor as tf
import numpy as np

with tf.device('/cpu:0'):
    with tf.variable_scope('c'):
        a = tf.get_variable('a', (2000, 2000), dtype=tf.float32, initializer=tf.constant_initializer(1))

with tf.device('/gpu:0'):
    with tf.variable_scope('g'):
        b = tf.get_variable('b', (2000, 2000), dtype=tf.float32, initializer=tf.constant_initializer(1))


##

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    for _ in range(100):
        sess.run(tf.matmul(a, a))
print 'finished'
##