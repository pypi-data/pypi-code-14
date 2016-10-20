from .gmm_algorithm import GmmAlgorithm
from .logregr_algorithm import LogRegrAlgorithm

# to fix sphinx warnings of not able to find classes, when path is shortened
GmmAlgorithm.__module__ = "bob.pad.voice.algorithm"
LogRegrAlgorithm.__module__ = "bob.pad.voice.algorithm"

# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
