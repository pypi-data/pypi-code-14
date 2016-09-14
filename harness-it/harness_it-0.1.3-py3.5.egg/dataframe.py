# coding: utf-8

# In[4]:

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
    'Harness'
]


# In[5]:

class PandasBase(object):

    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **{
            key: value for key, value in kwargs.items()
            if not(key in self._metadata)
        })
        # Append metadata to the dataframe.
        for attr in self._metadata:
            if not hasattr(self, attr):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    setattr(self, attr, None)

    @property
    def _constructor(self):
        return self.__class__

    def copy(self, deep=True):
        data = self.values
        return self.__class__(
            data.values.copy() if deep else data.values, index=self.index.copy()
        ).__finalize__(self)

    def __dir__(self):
        return super().__dir__() + self._metadata


# In[6]:

class SeriesBase(PandasBase, pandas.Series):

    def __init__(self, *args, **kwargs):
        if ~('name' in self._metadata):
            self._metadata.append('name')
        super().__init__(*args, **kwargs)

    @property
    def _constructor_expanddim(self):
        return self._dataframe

    @property
    def _constructor(self):
        return self.__class__

    def __finalize__(self, other, method=None, **kwargs):
        """ propagate metadata from other to self """
        for attr in self._metadata:
            setattr(self, attr, getattr(other, attr, None))
        return self


# In[9]:

class FrameBase(PandasBase, pandas.DataFrame):

    @property
    def _constructor_sliced(self):
        return self._series

    def __getitem__(self, key):
        obj = super().__getitem__(key).__finalize__(self)
        if obj.name:
            obj.name = (*obj.name, key,)
        else:
            obj.name = (key,)
        return obj

    #
    # Implement pandas methods
    #

    def __finalize__(self, other, method=None, **kwargs):
        """propagate metadata from other to self """
        # merge operation: using metadata of the left object
        if method == 'merge':
            for name in self._metadata:
                setattr(self, name, getattr(other.left, name, None))
        # concat operation: using metadata of the first object
        elif method == 'concat':
            for name in self._metadata:
                setattr(self, name, getattr(other.objs[0], name, None))
        else:
            for name in self._metadata:
                setattr(self, name, getattr(other, name, None))
        return self


# In[10]:

class HarnessSeries(SeriesBase):
    _metadata = [
        'name', 'parent', 'model',
    ]


# In[11]:

class HarnessBase(FrameBase):
    """A dataframe as a test harness for machine learning."""
    _series = HarnessSeries

    _metadata = [
        'matrix', 'pipeline', 'parent',
        'scorer', 'model', 'n_folds', 'name'
    ]

    scorer = callables.DictCallable({
        'score': metrics.accuracy_score,
    })
    history = pandas.DataFrame([], columns=scorer.keys())


# In[12]:

class Harness(HarnessBase):

    def __init__(self, *args, n_folds=1, **kwargs):
        self.n_folds = n_folds
        super().__init__(*args, **kwargs)

    def cross_validation(self, **kwargs):
        if self.n_folds == 1:
            self.folds = [(range(len(self)),)]
        else:
            folds = cross_validation.StratifiedKFold(
                self.index.tolist(),
                n_folds=self.n_folds,
                **merge({
                        'random_state': 42
                        }, kwargs),
            )
            self.folds = list(folds)
        return self

    def fit(self, level=-1, **kwargs):
        self.cross_validation(**kwargs)
        self.matrix = []
        for fold in self.folds:
            # Fit the model for a fold
            self.matrix.append(
                self._fit_models(level, first(fold))
            )
        self.matrix = np.array(self.matrix)
        return self

    def _fit_models(self, level, indices):
        """Fit a few models with the same data set indices."""
        models = pipe(
            self.pipeline, map(sklearn.base.clone), list
        )
        for model in models:
            t = time.time()
            if level is None:
                model.fit(self.iloc[indices].values)
            else:
                model.fit(
                    self.iloc[indices].values,
                    self.iloc[indices].index.get_level_values(level)
                )
            self.history = self.history.append(
                pandas.DataFrame(
                    [{
                        'time': time.time() - t,
                        'model': model,
                        'model_id': id(model),
                        'data': self,
                        'length': len(model.steps) if hasattr(model, 'steps') else 1
                    }]
                ).set_index('model_id')
            )
        return models

    def predict(self, models=None):
        return self._predict_transform(
            'predict', models
        )

    def transform(self, models=None):
        return self._predict_transform(
            'transform', models
        )

    def _predict_transform(self, key, models=None):
        if models is None:
            models = self.matrix
        frames = []

        for model in concat(models):
            if hasattr(model, key):
                frames.append(
                    Harness(
                        getattr(model, key)(self.values), index=self.index,
                        model=model,
                    )
                )

        if frames:
            new_harness = pandas.concat(_X(frames).zip(
                _X(frames) * this().model.f * id > list
            ) > dict, axis=1)

            new_harness.parent, new_harness.history = self, self.history
            return new_harness
        return Harness(index=self.index)

    def score(self, models=None):
        predicted = self.predict(models)

        self.history.update(
            pandas.DataFrame(
                _X(predicted.iteritems()).map(
                    second
                ).map(
                    _X()[flip(self.scorer)](predicted.index).f
                ) > list,
                index=_X(predicted.iteritems()).map(first).map(first) > list
            )
        )
        return self.history

    def _id_to_model(self, index):
        return self.history.loc[index].model

    def _model_to_id(self, model):
        return self.history[self.history.model == model]

    def __getitem__(self, key):
        if isinstance(key, sklearn.base.BaseEstimator):
            key = id(key)
        return super().__getitem__(key)

HarnessSeries._dataframe = Harness
