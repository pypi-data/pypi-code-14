import numpy as np
import scipy.stats
import sklearn.pipeline
import sklearn.preprocessing
import sklearn.ensemble

categorical_data = np.random.randint(0, 5, size=(10, 4))
numerical_data = np.random.randn(10, 4)
data = np.hstack((categorical_data, numerical_data))

# Add missing values
data[0, 1] = np.NaN
data[1, 5] = np.NaN

X = data
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

pipeline = sklearn.pipeline.Pipeline((('ohe',
                                       sklearn.preprocessing.OneHotEncoder(
                                           categorical_features=[0, 1, 2, 3])),
                                      ('imp',
                                       sklearn.preprocessing.Imputer()),
                                      ('rf',
                                       sklearn.ensemble.RandomForestClassifier())))

# Does not work because of NaNs
#pipeline.fit(X, y)

pipeline = sklearn.pipeline.Pipeline((('imp',
                                       sklearn.preprocessing.Imputer(
                                           strategy='most_frequent')),
                                      ('ohe',
                                       sklearn.preprocessing.OneHotEncoder(
                                           categorical_features=[0, 1, 2, 3])),
                                      ('rf',
                                       sklearn.ensemble.RandomForestClassifier())))



Xt, _ = pipeline._pre_transform(X, y)
# Now uses the return value of scipy.stats.mode which makes only very little
# sense for a continuous value
print(scipy.stats.mode(data)[5])
print(Xt.toarray()[1])

pipeline = sklearn.pipeline.Pipeline((('imp_cat',
                                       sklearn.preprocessing.Imputer(
                                           strategy='most_frequent',
                                           columns=[0, 1, 2, 3])),
                                      ('imp_num',
                                       sklearn.preprocessing.Imputer(
                                           strategy='median',
                                           columns=[4, 5, 6, 7])),
                                      ('ohe',
                                       sklearn.preprocessing.OneHotEncoder(
                                           categorical_features=[0, 1, 2, 3])),
                                      ('rf',
                                       sklearn.ensemble.RandomForestClassifier())))