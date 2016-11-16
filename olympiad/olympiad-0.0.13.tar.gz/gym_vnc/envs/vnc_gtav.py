import string

from gym_vnc import spaces
from gym_vnc.spaces import vnc_event
from gym_vnc.envs import vnc_env
from gym_vnc.spaces.joystick_action_space import JoystickActionSpace


class VNCGTAVEnv(vnc_env.VNCEnv):
    def __init__(self):
        super(VNCGTAVEnv, self).__init__()
        self.action_space = JoystickActionSpace(axis_x=True, axis_z=True)

    def _step(self, action_n):
        self.error_buffer.check()

        action_n = self._compile_actions(action_n)
        # if self.diagnostics:
        #     action_n = self.diagnostics.add_probe(action_n)

        observation_n, obs_info_n = self.vnc_session.step({})

        if self.rewarder_session:
            self.rewarder_session.send_action(action_n, self.spec.id)
            reward_n, done_n, info_n = self.rewarder_session.pop()
        else:
            reward_n = done_n = [None] * len(observation_n)
            info_n = [{} for _ in range(len(observation_n))]

        self._propagate_obs_info(info_n, obs_info_n)
        return observation_n, reward_n, done_n,  {'n': info_n}
