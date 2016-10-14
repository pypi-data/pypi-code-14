import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelBinarizer
from sklearn.utils import check_array, check_X_y
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_is_fitted


# TODO this needs to be savable

def get_default_estimators():
    print('---- get default ests')

class BaseStacker(object):
    def _model_predict(self, model, X):
        try:
            return model.predict_proba(X)[:,1]
        except AttributeError:
            return model.predict(X)

    def _predict_proba(self, X):
        return np.array([
            self._model_predict(model, X)
            for model in self._estimators
        ]).T

    def fit(self, X, y=None):
        X, y = check_X_y(X, y)
        #y = self._lb.fit_transform(y)

        for model in self._estimators:
            model.fit(X, y)

        results = self._predict_proba(X)
        self._stack_estimator.fit(results, y)
        self.fitted_ = True
        return self

class StackingRegressor(BaseEstimator, RegressorMixin, BaseStacker):

    def __init__(self, estimators=None, stack_estimator=None):
        self.estimators = estimators
        self.stack_estimator = stack_estimator
        self._lb = LabelBinarizer()

        if self.estimators is None:
            import xgboost as xgb
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.linear_model import LogisticRegression, BayesianRidge, SGDRegressor
            self._estimators = [
                xgb.sklearn.XGBRegressor(max_depth=50, n_estimators=300),
                BayesianRidge(),
                RandomForestRegressor(n_estimators=300),
                SGDRegressor(),
            ]
        else:
            self._estimators = self.estimators

        if self.stack_estimator is None:
            self._stack_estimator = xgb.sklearn.XGBRegressor(max_depth=50, n_estimators=1000)
        else:
            self._stack_estimator = self.stack_estimator

    def predict(self, X):
        check_is_fitted(self, 'fitted_')
        X = check_array(X)
        results = self._predict_proba(X)
        return self._stack_estimator.predict(results)

class StackingClassifier(BaseEstimator, ClassifierMixin, BaseStacker):

    def __init__(self, estimators=None, stack_estimator=None):
        self.estimators = estimators
        self.stack_estimator = stack_estimator
        self._lb = LabelBinarizer()

        if self.estimators is None:
            import xgboost as xgb
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.linear_model import LogisticRegression, BayesianRidge, SGDClassifier
            self._estimators = [
                xgb.sklearn.XGBClassifier(max_depth=50, n_estimators=300),
                BayesianRidge(),
                LogisticRegression(max_iter=2000),
                RandomForestClassifier(n_estimators=300),
                SGDClassifier(),
            ]
        else:
            self._estimators = self.estimators

        if self.stack_estimator is None:
            self._stack_estimator = xgb.sklearn.XGBClassifier(max_depth=50, n_estimators=1000)
        else:
            self._stack_estimator = self.stack_estimator


    def predict(self, X):
        check_is_fitted(self, 'fitted_')
        X = check_array(X)
        results = self._predict_proba(X)
        return self._stack_estimator.predict(results)

    def predict_proba(self, X):
        check_is_fitted(self, 'fitted_')
        X = check_array(X)
        results = self._predict_proba(X)
        return self._stack_estimator.predict_proba(results)


# TODO want an online kaggle ensembler....
#
# should take many features/transforms
# runs as long as you tell it too, continually running with cv & test set....
#
# should sample features, sample model, train, then add results to ensemble
#
# should be saveable
#
# should be online to allow runtime updates and improvements
#
