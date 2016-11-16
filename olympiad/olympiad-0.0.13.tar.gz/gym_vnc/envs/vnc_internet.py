from gym_vnc.envs import vnc_env

class VNCInternetEnv(vnc_env.VNCEnv):
     def __init__(self):
        super(VNCInternetEnv, self).__init__()
        self._probe_key = 0x60  # backtick `
