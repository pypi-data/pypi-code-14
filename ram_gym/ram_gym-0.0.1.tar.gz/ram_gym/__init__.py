from gym.envs.registration import register

register(
    id='openram-v2',
    entry_point='ram_gym.envs:OpenRAMEnv',
)
