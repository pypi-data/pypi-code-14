import logging
import time
from gym_vnc import pyprofile, vectorized

logger = logging.getLogger(__name__)

class Timer(vectorized.Wrapper):
    def _reset(self):
        with pyprofile.push('vnc_env.Timer.reset'):
            return self.env.reset()

    def _step(self, action_n):
        start = time.time()
        with pyprofile.push('vnc_env.Timer.step'):
            observation_n, reward_n, done_n, info = self.env.step(action_n)
        sleep = info['stats.throttle.sleep']
        if sleep < 0:
            sleep = 0
        pyprofile.timing('vnc_env.Timer.step.excluding_sleep', time.time() - start - sleep)
        return observation_n, reward_n, done_n, info
