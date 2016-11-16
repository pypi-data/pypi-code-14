import gym

def LimitWrapper(timestep_limit):
    class LimitWrapper(gym.Wrapper):
        def __init__(self, env):
            super(LimitWrapper, self).__init__(env)

            self.timestep_limit = timestep_limit
            self.timestep_count = 0

        def _reset(self):
            self.timestep_count = 0
            return self.env.reset()

        def _step(self, action):
            observation, reward, done, info = self.env.step(action)
            if self.timestep_count >= self.timestep_limit:
                done = True
            self.timestep_count += 1
            return observation, reward, done, info
    return LimitWrapper

def ShortEnv(timestep_limit, env_entry_point, env_kwargs):
    cls = gym.envs.registration.load(env_entry_point)
    env = cls(**env_kwargs)
    wrapper = LimitWrapper(timestep_limit)
    env = wrapper(env)
    return env
