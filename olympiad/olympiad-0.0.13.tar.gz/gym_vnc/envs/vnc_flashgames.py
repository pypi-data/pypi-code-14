from gym_vnc.envs import vnc_env

class VNCFlashgamesEnv(vnc_env.VNCEnv):
     def __init__(self):
        super(VNCFlashgamesEnv, self).__init__()
        self._probe_key = 0x60  # backtick `
