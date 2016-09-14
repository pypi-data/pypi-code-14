# coding: utf-8

# In[2]:

"""setup"""
import pandas
from sklearn import *
import sklearn
from pandas import np
from typing import Iterable
from whatever.callables import DictCallable
from toolz.curried import *
from whatever import *
import time
from typing import Callable
__all__ = [
    'EasyPipeline'
]


# In[3]:

class EasyPipeline(object):
    """Build a pipeline from a list."""

    def __new__(self, *pipeline, n_jobs=1):
        pipeline = list(pipeline)
        for i, model in enumerate(pipeline):
            if not isinstance(model, Iterable):
                model = [model]

            model = _X(model) * callables.Dispatch({
                Callable: preprocessing.FunctionTransformer
            }, default=identity) > list

            if _X(model).map(
                lambda x: isinstance(x, sklearn.base.ClassifierMixin)
            ) > all:
                pipeline[i] = sklearn.ensemble.VotingClassifier(
                    _X(model) * [
                        _X().str[this().split('(', 1)[0].f].f, identity
                    ] > list
                )
            else:
                pipeline[i] = sklearn.pipeline.make_union(*model)
        return sklearn.pipeline.make_pipeline(*pipeline)


# In[4]:

"""test_pipeline"""
shoot = EasyPipeline(
    [decomposition.PCA(), decomposition.IncrementalPCA()],
    [discriminant_analysis.LinearDiscriminantAnalysis(), tree.DecisionTreeClassifier()]
)


# In[ ]:
