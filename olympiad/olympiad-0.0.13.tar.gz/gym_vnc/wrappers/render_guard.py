import logging
import os
from twisted.python.runtime import platform
from gym_vnc import vectorized

logger = logging.getLogger(__name__)

class RenderGuard(vectorized.Wrapper):
    def __init__(self, *args, **kwargs):
        if platform.isLinux() and not os.environ.get('DISPLAY'):
            self.renderable = False
        else:
            self.renderable = True
        self._observation = None
        super(RenderGuard, self).__init__(*args, **kwargs)

    def _configure(self, **kwargs):
        super(RenderGuard, self)._configure(**kwargs)
        self.metadata = self.metadata.copy()
        modes = self.metadata.setdefault('render.modes', [])
        if 'rgb_array' not in modes:
            modes.append('rgb_array')

    def _step(self, action_n):
        observation_n, reward_n, done_n, info_n = self.env.step(action_n)
        self._observation = observation_n[0]
        return observation_n, reward_n, done_n, info_n

    def _render(self, mode='human', *args, **kwargs):
        if not self.renderable and mode == 'human':
            return
        elif self.env is None:
            # Only when this breaks
            return
        elif mode == 'rgb_array':
            return self._observation
        # Could log, but no need.
        return self.env.render(mode=mode, *args, **kwargs)
