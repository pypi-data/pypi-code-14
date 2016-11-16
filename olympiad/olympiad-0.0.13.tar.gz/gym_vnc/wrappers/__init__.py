from gym_vnc import envs
from gym_vnc.wrappers.action_space import SafeActionSpace
from gym_vnc.wrappers.atari_wrappers import DiscreteToVNCAction, CropAtari, Throttle
from gym_vnc.wrappers.blocking_reset import BlockingReset
from gym_vnc.wrappers.diagnostics import Diagnostics
from gym_vnc.wrappers.logger import Logger
from gym_vnc.wrappers.multiprocessing_env import WrappedMultiprocessingEnv, EpisodeID
from gym_vnc.wrappers.render_guard import RenderGuard
from gym_vnc.wrappers.throttle import Throttle
from gym_vnc.wrappers.timer import Timer
from gym_vnc.wrappers.vectorize import Vectorize, Unvectorize, WeakUnvectorize

def wrap(env):
    return Timer(RenderGuard(Logger(Throttle(env))))

def WrappedVNCEnv(*args, **kwargs):
    return wrap(envs.VNCEnv(*args, **kwargs))

def WrappedVNCCoreEnv(*args, **kwargs):
    return wrap(envs.VNCCoreEnv(*args, **kwargs))

def WrappedVNCCoreSyncEnv(*args, **kwargs):
    return wrap(envs.VNCCoreSyncEnv(*args, **kwargs))

def WrappedVNCFlashgamesEnv(*args, **kwargs):
    return wrap(envs.VNCFlashgamesEnv(*args, **kwargs))

def WrappedVNCStarCraftEnv(*args, **kwargs):
    return wrap(envs.VNCStarCraftEnv(*args, **kwargs))

def WrappedVNCGTAVEnv(*args, **kwargs):
    return wrap(envs.VNCGTAVEnv(*args, **kwargs))

def WrappedVNCWorldOfGooEnv(*args, **kwargs):
    return wrap(envs.VNCWorldOfGooEnv(*args, **kwargs))

def WrappedVNCInternetEnv(*args, **kwargs):
    return wrap(envs.VNCInternetEnv(*args, **kwargs))
