import numpy as np


class Memory:
    def __init__(self, observation_shape, action_dims, gamma, max_memory=5000):
        self.max_memory = max_memory
        self.observation_shape = observation_shape
        self.action_dims = action_dims
        self.memories = []
        # Discount ratio for future reward
        self.gamma = gamma

    @classmethod
    def get_observation_dims(cls, observation_shape):
        '''
        Calculate observation dimension when it is flattened
        :param observation_shape:
        :return:
        '''
        observation_space_size = 1
        # Observation shape should be a tuple of each dimension size
        for n in observation_shape:
            observation_space_size *= n
        return observation_space_size

    def append(self, state, action, reward, state_prime, done):
        '''
        Add observed state
        :param state: The given state from environment.
        :param action:  The action an agent took actually.
        :param reward:  The reward an agent received with above action.
        :param state_prime: The next state transitioned with above action.
        :param done: indicates the episode is finished.
        :return: void
        '''
        # assert state.shape == self.observation_shape
        # assert state_prime.shape == self.observation_shape
        assert 0 <= action < self.action_dims
        self.memories.append((state, action, reward, state_prime, done))

    def get_batch(self, model, batch_size):
        '''
        Construct training batch from sampling memory data
        :param model: The target model which should be trained
        :param batch_size: The train batch size
        :return: Batch data sets which shapes (batch_size, observation_shape)
        '''
        memory_len = len(self.memories)

        if memory_len == 0:
            return

        batch_size = min(batch_size, memory_len)
        observation_dims = Memory.get_observation_dims(self.observation_shape)
        X = np.zeros((batch_size, observation_dims))
        y = np.zeros((batch_size, self.action_dims))

        # Samping training dataset
        train_idx = np.random.randint(0, memory_len, size=batch_size)

        for i, idx in enumerate(train_idx):
            s, a, r, s_prime, done = self.memories[idx]

            X[i, :] = s
            y[i, :] = model.predict(np.expand_dims(s, 0))[0]

            max_q = np.max(model.predict(np.expand_dims(s_prime, 0))[0])

            if done:
                y[i, a] = r
            else:
                y[i, a] = r + self.gamma * max_q

        return X, y

    def __len__(self):
        return len(self.memories)
