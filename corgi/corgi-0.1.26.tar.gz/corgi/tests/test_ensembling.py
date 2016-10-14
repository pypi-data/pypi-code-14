from unittest import TestCase

from sklearn.utils.estimator_checks import check_estimator

from ..ensembling import StackingClassifier, StackingRegressor


class TestEnsembling(TestCase):
    def test_check_regressor(self):
        check_estimator(StackingRegressor)

    def test_check_classifier(self):
        check_estimator(StackingClassifier)
