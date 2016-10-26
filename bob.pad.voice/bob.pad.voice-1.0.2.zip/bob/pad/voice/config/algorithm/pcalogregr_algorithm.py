
import bob.pad.voice

algorithm = bob.pad.voice.algorithm.LogRegrAlgorithm(
    # use PCA to reduce dimension of features
    use_PCA_training = True,
)

