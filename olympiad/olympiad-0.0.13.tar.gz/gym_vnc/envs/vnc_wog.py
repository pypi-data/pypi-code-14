from gym_vnc.envs import vnc_env
from gym_vnc.spaces import VNCActionSpace


class VNCWorldOfGooEnv(vnc_env.VNCEnv):
    def __init__(self):
        super(VNCWorldOfGooEnv, self).__init__()
        # TODO: set action space screen shape to match
        # HACK: empty keys list fails for some weird reason, give it an 'a'
        self.action_space = VNCActionSpace(keys=['a'], buttonmasks=[1])
