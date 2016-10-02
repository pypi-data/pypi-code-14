import numpy as np

from algernon.memory import Memory

class Agent():
    '''
    Agent for reinforcement learning
    '''
    def __init__(self, model, observation_shape, action_dims,
                 episode=20, epsilon=0.1, gamma=0.9, batch_size=5000):
        self.model = model
        self.episode = episode
        self.epsilon = epsilon
        self.memory = Memory(observation_shape, action_dims, gamma)
        self.batch_size = batch_size

    def adapt_epsilon(self, epoch):
        if self.epsilon >= 0.1:
            self.epsilon *= 0.98

    def fit(self, environment, callback, checkpoint):
        '''
        Scikit like interface for training. Environment should be has
        compatible interface for OpenAI gym. (https://gym.openai.com/)
        :param environment:
        :param callback:
        :return:
        '''
        action_space = environment.action_space
        model = self.model

        for episode in range(self.episode):
            epoch = 0
            total_reward = 0
            environment.reset()
            s, _, done, _ = environment.step(action_space.sample())

            while not done:
                if np.random.random() < self.epsilon:
                    # Random action for epsilon greedy method
                    action = int(np.random.randint(action_space.n))
                else:
                    q = model.predict(np.expand_dims(s, 0))[0]
                    action = int(np.argmax(q))

                # Take action
                s_prime, reward, done, info = environment.step(action)

                self.memory.append(s.flatten(), action, reward, s_prime.flatten(), done)

                total_reward += reward
                s = s_prime
                epoch += 1
                callback(epoch, environment, total_reward)

            # Checkpoint callback
            checkpoint(epoch, environment, total_reward)

            # Experience reply training
            X, y = self.memory.get_batch(self.model, self.batch_size)
            self.model.fit(X, y, verbose=0)
            self.adapt_epsilon(epoch)

            print("episode: {:>5}, memory: {:>5}, epsilon: {:.5f}, total_reward: {:>5}".format(episode, len(self.memory), self.epsilon, total_reward))

    def predict(self, observations):
        return self.model.predict(observations)
