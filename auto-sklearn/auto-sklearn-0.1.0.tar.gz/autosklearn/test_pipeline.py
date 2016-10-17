import numpy as np
import scipy.stats
import sklearn.pipeline
from sklearn.preprocessing import Imputer, OneHotEncoder
import sklearn.ensemble

from autosklearn.pipeline.implementations.item_selector import ItemSelector

categorical_data = np.random.randint(0, 5, size=(10, 4))
numerical_data = np.random.randn(10, 4)
data = np.hstack((categorical_data, numerical_data))

# Add missing values
data[0, 1] = np.NaN
data[1, 5] = np.NaN

X = data
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])


pipeline_categorical = sklearn.pipeline.Pipeline(
    [('is', ItemSelector(indices=None)),
     ('imp', Imputer(strategy='most_frequent')),
     ('ohe', OneHotEncoder(categorical_features='all'))])
pipeline_numerical = sklearn.pipeline.Pipeline(
    [('is', ItemSelector(indices=None)),
     ('imp', Imputer(strategy='median'))])

fu = sklearn.pipeline.FeatureUnion(transformer_list=[('categorical', pipeline_categorical),
                                                     ('numerical', pipeline_numerical)])

rf = sklearn.ensemble.RandomForestClassifier()
pipeline = sklearn.pipeline.Pipeline((('fu', fu), ('cls', rf)))

pipeline.set_params(fu__categorical__is__indices=[0, 1, 2, 3])
pipeline.set_params(fu__numerical__is__indices=[4, 5, 6, 7])

pipeline.fit(X, y)
print(pipeline._pre_transform(X, y)[0].toarray())