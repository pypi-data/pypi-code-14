import logging
import gym
import time
import numpy as np

from gym import spaces
from gym_vnc import vectorized
from gym_vnc.wrappers import action_space
from gym_vnc.envs.vnc_core_env.translator import AtariKeyState

logger = logging.getLogger(__name__)

ATARI_HEIGHT = 210
ATARI_WIDTH = 160

class CropAtari(vectorized.ObservationWrapper):
    def __init__(self, env):
        super(CropAtari, self).__init__(env)
        self.observation_space = spaces.Box(0, 255, shape=(ATARI_HEIGHT, ATARI_WIDTH, 3))

    def _observation(self, observation_n):
        return [ob[:ATARI_HEIGHT, :ATARI_WIDTH, :] for ob in observation_n]

class Throttle(vectorized.Wrapper):
    def __init__(self, env, fps=None):
        raise RuntimeError('This class is now DEPRECATED. To upgrade to a better and more correct Throttle implementation, simply: 1. remove this class from your wrappers, 2. install the latest go-vncdriver: pip install --ignore-installed --no-cache-dir -U go-vncdriver, 3. pass an optional `fps` argument to env.configure.')

def one_hot(indices, depth):
    return np.eye(depth)[indices]

class DiscreteToVNCAction(vectorized.ActionWrapper):
    def __init__(self, env):
        super(DiscreteToVNCAction, self).__init__(env)
        dummy = action_space.SafeActionSpace(env)

        self._actions = dummy.action_space.actions
        self.action_space = spaces.Discrete(len(self._actions))
        # TODO: generalize
        try:
            core_env_id = env.spec._kwargs['core_env_id']
        except KeyError:
            pass
        except:
            self.key_state = AtariKeyState(gym.make(core_env_id))

    def _action(self, action_n):
        # Each action might be a length-1 np.array. Cast to int to
        # avoid warnings.
        return [self._actions[int(action)] for action in action_n]

    def _reverse_action(self, action_n):
        # Only works for core envs currently
        self.key_state.apply_vnc_actions(action_n)
        return one_hot(self.key_state.to_index(), self.action_space.n)
