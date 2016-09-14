import numpy as np
import unittest

from pydlm.modeler.trends import trend
from pydlm.modeler.seasonality import seasonality
from pydlm.modeler.builder import builder
from pydlm.base.kalmanFilter import kalmanFilter

class testKalmanFilter(unittest.TestCase):

    def setUp(self):
        self.kf1 = kalmanFilter(discount = [1])
        self.kf0 = kalmanFilter(discount = [1e-10])
        self.kf11 = kalmanFilter(discount = [1, 1])
        
    def testForwardFilter(self):
        dlm = builder()
        dlm.add(trend(degree = 1, discount = 1))
        dlm.initialize()
        self.kf1.predict(dlm.model)
        self.assertAlmostEqual(dlm.model.prediction.obs, 0)

        # the prior on the mean is zero, but observe 1, with
        # discount = 1, one should expect the filterd mean to be 0.5
        self.kf1.forwardFilter(dlm.model, 1)
        self.assertAlmostEqual(dlm.model.obs, 0.5)
        self.assertAlmostEqual(dlm.model.prediction.obs, 0)
        self.assertAlmostEqual(dlm.model.sysVar, 0.375)

        self.kf1.predict(dlm.model)
        self.assertAlmostEqual(dlm.model.obs, 0.5)
        self.assertAlmostEqual(dlm.model.prediction.obs, 0.5)

        dlm.initialize()
        self.kf0.predict(dlm.model)
        self.assertAlmostEqual(dlm.model.prediction.obs, 0)

        # the prior on the mean is zero, but observe 1, with discount = 0
        # one should expect the filtered mean close to 1
        self.kf0.forwardFilter(dlm.model, 1)
        self.assertAlmostEqual(dlm.model.obs, 1)
        self.assertAlmostEqual(dlm.model.prediction.obs, 0)
        self.assertAlmostEqual(dlm.model.sysVar, 0.5)

        self.kf0.predict(dlm.model)
        self.assertAlmostEqual(dlm.model.obs, 1)
        self.assertAlmostEqual(dlm.model.prediction.obs, 1)

    def testForwardFilterMultiDim(self):
        dlm = builder()
        dlm.add(seasonality(period = 2, discount = 1))
        dlm.initialize()

        self.kf11.forwardFilter(dlm.model, 1)
        self.assertAlmostEqual(dlm.model.state[0], 0.33333333333)
        self.assertAlmostEqual(dlm.model.state[1], -0.33333333333)
        
        self.kf11.forwardFilter(dlm.model, -1)
        self.assertAlmostEqual(dlm.model.state[0], -0.5)
        self.assertAlmostEqual(dlm.model.state[1], 0.5)

    def testBackwardSmoother(self):
        dlm = builder()
        dlm.add(trend(degree = 1, discount = 1))
        dlm.initialize()

        # with mean being 0 and observe 1 and 0 consectively, one shall
        # expect the smoothed mean at 1 will be 1/3, for discount = 1
        self.kf1.forwardFilter(dlm.model, 1)
        self.kf1.forwardFilter(dlm.model, 0)
        self.kf1.backwardSmoother(dlm.model, \
                                  np.matrix([[0.5]]), \
                                  np.matrix([[0.375]]))
        self.assertAlmostEqual(dlm.model.obs, 1.0/3)
        self.assertAlmostEqual(dlm.model.sysVar, 0.18518519)

    # second order trend with discount = 1. The smoothed result should be
    # equal to a direct fit on the three data points, 0, 1, -1. Thus, the
    # smoothed observation should be 0.0
    def testBackwardSmootherMultiDim(self):
        dlm = builder()
        dlm.add(trend(degree = 2, discount = 1))
        dlm.initialize()

        self.kf11.forwardFilter(dlm.model, 1)
        state1 = dlm.model.state
        cov1 = dlm.model.sysVar
        
        self.kf11.forwardFilter(dlm.model, -1)        
        self.kf11.backwardSmoother(dlm.model, \
                                   rawState = state1, \
                                   rawSysVar = cov1)
        
        self.assertAlmostEqual(dlm.model.obs, 0.0)

    def testMissingData(self):
        dlm = builder()
        dlm.add(trend(degree = 1, discount = 1))
        dlm.initialize()
        
        self.kf0.forwardFilter(dlm.model, 1)
        self.assertAlmostEqual(dlm.model.obs, 1.0)
        self.assertAlmostEqual(dlm.model.obsVar, 1.0)

        self.kf0.forwardFilter(dlm.model, None)
        self.assertAlmostEqual(dlm.model.obs, 1.0)
        self.assertAlmostEqual(dlm.model.obsVar/1e10, 0.5)

        self.kf0.forwardFilter(dlm.model, None)
        self.assertAlmostEqual(dlm.model.obs, 1.0)
        self.assertAlmostEqual(dlm.model.obsVar/1e10, 0.5)

        self.kf0.forwardFilter(dlm.model, 0)
        self.assertAlmostEqual(dlm.model.obs, 0.0)

    def testMissingEvaluation(self):
        dlm = builder()
        dlm.add(trend(degree = 1, discount = 1))
        dlm.initialize()
       
        dlm.model.evaluation = np.matrix([[None]])
        self.kf1.forwardFilter(dlm.model, 1.0, dealWithMissingEvaluation = True)
        self.assertAlmostEqual(dlm.model.obs, 0.0)
        self.assertAlmostEqual(dlm.model.transition, 1.0)

unittest.main()
#kf1 = kalmanFilter(discount = [1])
#kf0 = kalmanFilter(discount = [0.01])
#dlm = builder()
#dlm.add(trend(degree = 1, discount = 1))
#dlm.initialize()
#kf1.predict(dlm.model)
#kf1.forwardFilter(dlm.model, 1)
