from algernon.memory import Memory

import pytest
import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import sgd

class MockModel:
    def __init__(self, output_dims, input_dims):
        self.w = np.random.random(size=(output_dims, input_dims))

    def predict(self, X):
        return np.dot(X, self.w.T)

class TestMemory:
    TEST_OBSERVATION_SHAPE = (4, 2)
    TEST_ACTION_DIMS = 3
    TEST_GAMMA = 0.3
    TEST_MAX_MEMORY = 1000

    def test_init_values(self):
        m = Memory(TestMemory.TEST_OBSERVATION_SHAPE,
                   TestMemory.TEST_ACTION_DIMS,
                   TestMemory.TEST_GAMMA,
                   TestMemory.TEST_MAX_MEMORY)

        assert m.observation_shape == TestMemory.TEST_OBSERVATION_SHAPE
        assert m.action_dims == TestMemory.TEST_ACTION_DIMS
        assert len(m.memories) == 0
        assert m.max_memory == TestMemory.TEST_MAX_MEMORY

    def test_observation_dims(self):
        ret = Memory.get_observation_dims(TestMemory.TEST_OBSERVATION_SHAPE)
        # 4 * 2
        assert ret == 8

    def test_append(self):
        m = Memory(TestMemory.TEST_OBSERVATION_SHAPE,
                   TestMemory.TEST_ACTION_DIMS,
                   TestMemory.TEST_GAMMA,
                   TestMemory.TEST_MAX_MEMORY)
        s = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE)
        s_prime = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE)

        m.append(s, 1, 0.2, s_prime, False)

        assert len(m.memories) == 1

    def test_invalid_append(self):
        m = Memory(TestMemory.TEST_OBSERVATION_SHAPE,
                   TestMemory.TEST_ACTION_DIMS,
                   TestMemory.TEST_GAMMA,
                   TestMemory.TEST_MAX_MEMORY)
        s = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE)
        s_prime = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE)

        with pytest.raises(AssertionError):
            # Action dimension shuld be 0~2
            m.append(s, 10, 0.3, s_prime, False)

    def test_get_batch(self):
        m = Memory(TestMemory.TEST_OBSERVATION_SHAPE,
                   TestMemory.TEST_ACTION_DIMS,
                   TestMemory.TEST_GAMMA,
                   TestMemory.TEST_MAX_MEMORY)
        for _ in range(10):
            s = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE).flatten()
            a = np.random.randint(TestMemory.TEST_ACTION_DIMS)
            r = np.random.random(size=1)[0]
            s_prime = np.random.random(size=TestMemory.TEST_OBSERVATION_SHAPE).flatten()

            m.append(s, a, r, s_prime, False)

        assert len(m.memories) == 10

        X, y = m.get_batch(MockModel(3, 8), 3)

        assert X.shape[0] == y.shape[0] == 3
        assert X.shape[1] == 8
        assert y.shape[1] == 3


