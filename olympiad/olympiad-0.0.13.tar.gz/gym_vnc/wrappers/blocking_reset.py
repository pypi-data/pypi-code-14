from gym_vnc import rewarder, vectorized

class BlockingReset(vectorized.Wrapper):
    def __init__(self, *args, **kwargs):
        super(BlockingReset, self).__init__(*args, **kwargs)
        self.reward_n = None
        self.done_n = None
        self.info = None

    def _configure(self, **kwargs):
        super(BlockingReset, self)._configure(**kwargs)
        self.null_action = [[] for _ in range(self.n)]

    def _reset(self):
        observation_n = self.env.reset()
        self.reward_n = [0] * self.n
        self.done_n = [False] * self.n
        self.info = {'n': [{} for _ in range(self.n)]}

        while any(ob is None for ob in observation_n):
            observation_n, new_reward_n, new_done_n, new_info = self.env.step(self.null_action)
            rewarder.merge_n(
                self.reward_n, self.done_n, self.info,
                new_reward_n, new_done_n, new_info
            )
        return observation_n

    def _step(self, action_n):
        observation_n, reward_n, done_n, info = self.env.step(action_n)
        if self.reward_n is not None:
            rewarder.merge_n(
                reward_n, done_n, info,
                self.reward_n, self.done_n, self.info
            )
            self.reward_n = self.done_n = self.info = None

        while any(ob is None for ob in observation_n):
            observation_n, new_reward_n, new_done_n, new_info = self.env.step(self.null_action)
            rewarder.merge_n(
                reward_n, done_n, info,
                new_reward_n, new_done_n, new_info
            )
        return observation_n, reward_n, done_n, info
