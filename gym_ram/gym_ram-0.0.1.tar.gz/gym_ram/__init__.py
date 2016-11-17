from gym.envs.registration import register

  register(
      id='ram-v0',
      entry_point='gym_ram.envs:RAMEnv',
  )
