# -*- coding: utf-8 -*-
"""
Machine learning steps for processed data.

@author: Alan Xu
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn import decomposition
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble.base import _partition_estimators
from sklearn.ensemble.forest import _parallel_helper
from sklearn.externals import joblib
import seaborn as sns
from model_setup import RFbcRegressor


class GridLearn(object):
    """
    Build machine learning object that can find the best parameters for final run.

    """

    def __init__(self, in_file='', y_column=None, mask_column=None):
        """
        :param in_file: input h5 file that contains the training data
        :param y_column: column index for response variable y
        :param mask_column: column index for mask (if exist, and should be after popping y_column)
        :param: best_params: param set that can be used in further learning
        """
        self.in_file = in_file
        if type(y_column) is list:
            self.y_column = y_column
        else:
            self.y_column = [y_column]
        if type(mask_column) is list:
            self.mask_column = mask_column
        else:
            self.mask_column = [mask_column]
        self.best_params = {}
        self.mdl = Pipeline([('scale', StandardScaler())])

    def tune_param_set(self, params, k=5):
        """
        Find the best param set that used in learning.
        :param k: number of folds used in cv
        :param params: parameter set used in grid search
        :return: best_params: param set that can be used in further learning
        :return: mdl: updated model using best_params
        """
        # train = pd.read_csv(self.in_file, sep=',', header=None)
        train = pd.read_hdf(self.in_file, 'df0')
        if self.y_column[0] is None:
            sys.exit('"y_column" must be defined in training process...')
        else:
            predictors = [x for x in train.columns if x not in self.y_column + self.mask_column]

        grid_search = GridSearchCV(self.mdl, params, n_jobs=-1, verbose=1, cv=k)
        grid_search.fit(train[predictors], train[self.y_column[0]])
        for p in grid_search.grid_scores_:
            print(p)
        print(grid_search.best_params_)
        print(grid_search.best_score_)
        self.best_params = grid_search.best_params_
        self.mdl.set_params(**self.best_params)
        return self.best_params, self.mdl

    def split_training(self, test_file, fraction=0.3):
        """
        :param fraction:
        :return:
        """
        train = pd.read_hdf(self.in_file, 'df0')
        if self.y_column[0] is None:
            sys.exit('"y_column" must be defined in training process...')
        else:
            predictors = [x for x in train.columns if x not in self.y_column + self.mask_column]
        self.mdl.fit(train[predictors], train[self.y_column[0]])
        preds = self.mdl.predict(test[predictors])
        label = test[self.y_column[0]]


    def sklearn_test(self, test_file, plot_limit=(0, 50)):
        """
        sklearn and prediction and test
        :param plot_limit:
        :param test_file:
        :return:
        """
        # train = pd.read_csv(self.in_file, sep=',', header=None)
        # test = pd.read_csv(test_file, sep=',', header=None)
        train = pd.read_hdf(self.in_file, 'df0')
        test = pd.read_hdf(test_file, 'df0')
        if self.y_column[0] is None:
            sys.exit('"y_column" must be defined in training process...')
        else:
            predictors = [x for x in train.columns if x not in self.y_column + self.mask_column]

        self.mdl.fit(train[predictors], train[self.y_column[0]])
        preds = self.mdl.predict(test[predictors])
        label = test[self.y_column[0]]

        plot_name = '{}_scatterplot.png'.format(os.path.splitext(test_file)[0])
        df = pd.DataFrame({
            'Measured': label,
            'Predicted': preds,
        })
        g = sns.jointplot(
            x="Measured", y="Predicted", xlim=plot_limit, ylim=plot_limit, data=df,
            kind="reg")
        g.savefig(plot_name)

    def predict_bigdata(self, test_file, out_file_h5):
        """
        sklearn prediction for big data
        :param out_file_h5:
        :param test_file:
        :return:
        """
        train = pd.read_hdf(self.in_file, 'df0')
        if self.y_column[0] is None:
            sys.exit('"y_column" must be defined in training process...')
        else:
            predictors = [x for x in train.columns if x not in self.y_column + self.mask_column]
        self.mdl.fit(train[predictors], train[self.y_column[0]])
        with pd.HDFStore(out_file_h5, mode='w') as store:
            for df in pd.read_hdf(test_file, 'df0', chunksize=500000):
                preds = self.mdl.predict(df[predictors])
                df1 = pd.Series(preds, name='Est')
                df0 = pd.concat([df[['x', 'y']].reset_index(drop=True), df1], axis=1)
                store.append('df0', df0, index=False, data_columns=['Est'])
            store.create_table_index('df0', columns=['Est'], optlevel=9, kind='full')

    def setup_rfbc_model(self):
        """
        setup rfbc model
        :type rate: learning rate to specify
        :return: self.mdl
        """
        mdl1 = RFbcRegressor(
            n_estimators=100,
            max_features="sqrt",
            min_samples_split=5,
            oob_score=True,
        )

        estimators = [
            ('scale', StandardScaler()),
            ('learn', mdl1)
        ]
        self.mdl = Pipeline(estimators)
        return self.mdl

    def setup_rf_model(self):
        """
        setup rf model
        :type rate: learning rate to specify
        :return: self.mdl
        """
        mdl1 = RandomForestRegressor(
            n_estimators=100,
            max_features="sqrt",
            min_samples_split=5,
            oob_score=True,
        )

        estimators = [
            ('scale', StandardScaler()),
            ('learn', mdl1)
        ]
        self.mdl = Pipeline(estimators)
        return self.mdl


