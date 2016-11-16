import gym

# TODO: Replace this with an actual observation space
class VNCObservationSpace(gym.Space):
    def contains(self, x):
        return True
