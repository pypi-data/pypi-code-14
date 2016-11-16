import threading
import time

from gym_vnc import error
from gym_vnc.rewarder import merge

# Buffers up incoming rewards
class RewardBuffer(object):
    def __init__(self):
        self.cv = threading.Condition()

        self.count = 0
        self.reward = 0.
        self.text = []
        self.done = False
        self.info = {}
        self._observation = None

    # A hack, only useful for the debugging core-envs with
    # vnc_pixels=False.
    def pop_observation(self):
        with self.cv:
            obs = self._observation
            self._observation = None
            return obs

    def set_observation(self, observation):
        with self.cv:
            self._observation = observation

    def push_text(self, text):
        with self.cv:
            self.text.append(text)
            self.cv.notifyAll()

    def push_info(self, info):
        # Just send some info
        with self.cv:
            merge.merge_infos(self.info, info)

    def push(self, reward, done, info, remote_time, local_time):
        with self.cv:
            self.count += 1
            self.reward += reward
            # Consider yourself done whenever a reward crosses episode
            # boundaries.
            self.done = self.done or done

            # Mere together the infos
            merge.merge_infos(self.info, info)
            # Sometimes helpful diagnostic info
            self.info['reward_buffer.remote_time'] = remote_time
            self.info['reward_buffer.local_time'] = local_time

            self.cv.notifyAll()

    def pop(self):
        with self.cv:
            self.cv.notifyAll()

            count = self.count
            reward = self.reward
            done = self.done
            info = self.info
            text = self.text

            self.count = 0
            self.reward = 0.
            self.done = False
            self.info = {}
            self.text = []
            self.remote_time = None
            self.local_time = None

            info['reward.count'] = count
            info['env.text'] = text

            return reward, done, info

    def reset(self):
        with self.cv:
            self.reward = 0.
            self.done = False

    def wait_for_step(self, error_buffer=None, timeout=None):
        # TODO: this might be cleaner using channels
        with self.cv:
            start = time.time()
            while True:
                if self.count != 0:
                    return
                elif timeout is not None and time.time() - start > timeout:
                    raise error.Error('No rewards received in {}s'.format(timeout))

                if error_buffer:
                    error_buffer.check()

                self.cv.wait(timeout=0.5)
