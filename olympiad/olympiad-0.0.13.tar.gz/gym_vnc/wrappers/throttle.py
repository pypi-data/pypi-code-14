import logging
import time
from gym_vnc import pyprofile, rewarder, vectorized

logger = logging.getLogger(__name__)

class Throttle(vectorized.Wrapper):
    def __init__(self, env):
        super(Throttle, self).__init__(env)

        self._steps = None

    def _configure(self, skip_metadata=False, fps=None, **kwargs):
        super(Throttle, self)._configure(**kwargs)
        if fps is None:
            fps = self.metadata['video.frames_per_second']
        self.fps = fps
        self.skip_metadata = skip_metadata

        self.diagnostics = self.unwrapped.diagnostics

    def _reset(self):
        observation = self.env.reset()
        self._start_timer()
        return observation

    def _step(self, action_n):
        if self._steps is None:
            self._start_timer()
        self._steps += 1

        start = time.time()
        # Submit the action
        old_observation_n, old_reward_n, old_done_n, old_info = self.env.step(action_n)

        delta = time.time() - start
        if delta > 1:
            logger.info('env.step took a long time: %.2fs', delta)

        if not self.skip_metadata and self.diagnostics is not None:
            # Run (slow) diagnostics
            self.diagnostics.add_metadata(old_observation_n, old_info['n'])

        if self.fps != -1:
            # Sleep with any time remaining
            delta = self._start + 1./self.fps * self._steps - time.time()
            old_info['stats.throttle.sleep'] = delta
            if delta > 0:
                pyprofile.timing('vnc_env.Throttle.sleep', delta)
                time.sleep(delta)
            else:
                delta = abs(delta)
                if delta >= 0.1:
                    logger.info('Throttle fell behind by %.2fs; lost %.2f frames', delta, self.fps*delta)
                pyprofile.timing('vnc_env.Throttle.lost_sleep', delta)
                self._start_timer()

        # TODO: we could potentially hit our target more faithfully by
        # undersleeping, but this is ok

        action = [[] for i in range(self.n)]

        start = time.time()
        observation_n, reward_n, done_n, info = self.env.step(action)
        delta = time.time() - start
        if delta > 1:
            logger.info('Follow-up env.step took a long time: %.2fs', delta)

        rewarder.merge_n(
            reward_n, done_n, info,
            old_reward_n, old_done_n, old_info,
        )
        return observation_n, reward_n, done_n, info

    def _start_timer(self):
        self._start = time.time()
        self._steps = 0
