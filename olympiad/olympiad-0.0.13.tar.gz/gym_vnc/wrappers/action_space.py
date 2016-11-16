import gym
from gym_vnc import envs, error, spaces, vectorized

def atari_vnc(up=False, down=False, left=False, right=False, z=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right),
            spaces.KeyEvent.by_name('down', down=down),
            spaces.KeyEvent.by_name('z', down=z)]

def slither_vnc(space=False, left=False, right=False):
    return [spaces.KeyEvent.by_name('space', down=space),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right)]

def racing_vnc(up=False, left=False, right=False):
    return [spaces.KeyEvent.by_name('up', down=up),
            spaces.KeyEvent.by_name('left', down=left),
            spaces.KeyEvent.by_name('right', down=right)]

class SafeActionSpace(vectorized.Wrapper):
    def __init__(self, env):
        super(SafeActionSpace, self).__init__(env)
        unwrapped = self.unwrapped
        if isinstance(unwrapped, envs.VNCCoreEnv):
            self._apply_core_env()
        elif self.spec is None:
            pass
        elif self.spec.id == 'VNCSlitherIO-v0':
            self.action_space = spaces.Hardcoded([
                slither_vnc(left=True),
                slither_vnc(right=True),
                slither_vnc(space=True),
                slither_vnc(left=True, space=True),
                slither_vnc(right=True, space=True),
            ])
        elif self.spec.id in ['VNCKongregateDuskDrive-v0', 'VNCKongregateDuskDriveDebug-v0']:
            # TODO: be more systematic
            self.action_space = spaces.Hardcoded([
                racing_vnc(up=True),
                racing_vnc(left=True),
                racing_vnc(right=True),
            ])

    def _apply_core_env(self):
        spec = gym.spec(self.unwrapped.core_env_id)

        if spec.id == 'CartPole-v0':
            self.action_space = spaces.Hardcoded([
                [spaces.KeyEvent.by_name('left', down=True)],
                [spaces.KeyEvent.by_name('left', down=False)],
            ])
        elif spec._entry_point.startswith('gym.envs.atari:'):
            actions = []
            env = spec.make()
            for action in env.unwrapped.get_action_meanings():
                z = 'FIRE' in action
                left = 'LEFT' in action
                right = 'RIGHT' in action
                up = 'UP' in action
                down = 'DOWN' in action
                translated = atari_vnc(up=up, down=down, left=left, right=right, z=z)
                actions.append(translated)
            self.action_space = spaces.Hardcoded(actions)
        else:
            raise error.Error('Unsupported env type: {}'.format(spec.id))
