import bob.io.base
import numpy
import math
import bob.learn.mlp
import bob.core
from bob.pad.base.algorithm import Algorithm
import logging

logger = logging.getLogger("bob.paper.biosig2016")


class MLP (Algorithm):
  """Trains MLP and projects testing data on it."""

  def __init__(self, normalize_features=True, mlp_shape=(20, 1), batch=False, target=1, output_activation="sigmoid", mask=None, **kwargs):

    # call base class constructor registering that this tool performs everything.
    Algorithm.__init__(
        self,
        performs_projection=True,
        requires_projector_training=True,
        use_projected_features_for_enrollment=True,
    )
    self.normalize_features = normalize_features
    self.machine = None
    self.mlp_shape = mlp_shape
    self.batch = batch
    self.target = target
    self.output_activation = output_activation
    self.mask = mask

  def _check_feature(self, feature, machine=None):
    """Checks that the features are appropriate."""
    if not isinstance(feature, numpy.ndarray) or feature.ndim != 1 or feature.dtype != numpy.float64:
      raise ValueError("The given feature is not appropriate", feature)
    index = 0
    if machine is not None and feature.shape[0] != machine.shape[index]:
      logger.warn("The given feature is expected to have %d elements, but it has %d" % (machine.shape[index], feature.shape[0]))
      return False
    return True

  def train_projector(self, training_features, dev_features, projector_file):
    if len(training_features) < 2:
      raise ValueError("Training projector: features should contain two lists: real and attack!")

    # the format is specified in FileSelector.py:training_list() of bob.pad.base
    # load training set
    if isinstance(training_features[0][0][0], numpy.ndarray):
     logger.info(" - Training: each feature is a set of arrays")
     real_train_features = numpy.array([row if self._check_feature(row) else numpy.nan for feat in training_features[0] for row in feat], dtype=numpy.float64)
     attack_train_features = numpy.array([row if self._check_feature(row) else numpy.nan for feat in training_features[1] for row in feat], dtype=numpy.float64)
    else:
     logger.info(" - Training: each feature is a single array")
     real_train_features = numpy.array([feat if self._check_feature(feat) else numpy.nan for feat in training_features[0]], dtype=numpy.float64)
     attack_train_features = numpy.array([feat if self._check_feature(feat) else numpy.nan for feat in training_features[1]], dtype=numpy.float64)

    # load development set
    if isinstance(dev_features[0][0][0], numpy.ndarray):
     logger.info(" - Training: each feature is a set of arrays")
     real_dev_features = numpy.array([row if self._check_feature(row) else numpy.nan for feat in dev_features[0] for row in feat], dtype=numpy.float64)
     attack_dev_features = numpy.array([row if self._check_feature(row) else numpy.nan for feat in dev_features[1] for row in feat], dtype=numpy.float64)
    else:
     logger.info(" - Training: each feature is a single array")
     real_dev_features = numpy.array([feat if self._check_feature(feat) else numpy.nan for feat in dev_features[0]], dtype=numpy.float64)
     attack_dev_features = numpy.array([feat if self._check_feature(feat) else numpy.nan for feat in dev_features[1]], dtype=numpy.float64)

    # retain only dimensions specified by mask
    if self.mask is not None:
      real_train_features = real_train_features[:, self.mask]
      attack_train_features = attack_train_features[:, self.mask]
      real_dev_features = real_dev_features[:, self.mask]
      attack_dev_features = attack_dev_features[:, self.mask]

    logger.info("Training set - Real features shape: " + str(real_train_features.shape))
    logger.info("Training set - Attack features shape: " + str(attack_train_features.shape))
    logger.info("Development set - Real features shape: " + str(real_dev_features.shape))
    logger.info("Development set - Attack features shape: " + str(attack_dev_features.shape))

    from ..utils import norm

    mean = None
    std = None

    # compute mean and standard deviation of training data
    # use it to normalize features in training and development set
    if self.normalize_features:
      mean, std = norm.calc_mean_std(real_train_features, attack_train_features, nonStdZero=True)
      real_train_features = norm.zeromean_unitvar_norm(real_train_features, mean, std)
      attack_train_features = norm.zeromean_unitvar_norm(attack_train_features, mean, std)
      real_dev_features = norm.zeromean_unitvar_norm(real_dev_features, mean, std)
      attack_dev_features = norm.zeromean_unitvar_norm(attack_dev_features, mean, std)

    hdf5file = bob.io.base.HDF5File(projector_file, "w")

    # shuffle the data
    feature_size = real_train_features.shape[1]
    l_real = len(real_train_features)
    l_attack = len(attack_train_features)
    data = numpy.append(real_train_features, attack_train_features, axis=0)
    del real_train_features, attack_train_features
    label_real = self.target
    if(self.output_activation == "sigmoid"):
      label_attack = 1 - self.target
    else:
      label_attack = -self.target
    label = numpy.append(label_real * numpy.ones((l_real, 1)), label_attack * numpy.ones((l_attack, 1)), axis=0)
    data = numpy.append(data, label, axis=1)
    numpy.random.seed(4)
    numpy.random.shuffle(data)
    label = data[:, feature_size:]
    data = data[:, 0:feature_size:]

    # create the MLP machine and initialize it randomly with weights close to 0
    self.mlp_shape = (feature_size, self.mlp_shape[0], self.mlp_shape[1])
    self.machine = bob.learn.mlp.Machine(self.mlp_shape)
    self.machine.randomize(rng=bob.core.random.mt19937(34))

    # store mean and std in MLP machine
    if self.normalize_features:
      if mean is not None and std is not None:
        self.machine.input_subtract = mean
        self.machine.input_divide = std

    # setup MLP configuration. By default, the activation is a hyperbolic tangent.
    if(self.output_activation == "sigmoid"):
      self.machine.output_activation = bob.learn.activation.Logistic()

    # specify if the gradient descent is done in batches or stochastically
    if (self.batch):
      N = len(data)
    else:
      N = 1
    L = int(math.floor(len(data) / float(N)))

    trainer = bob.learn.mlp.BackProp(N, bob.learn.mlp.SquareError(self.machine.output_activation), self.machine, train_biases=True)
    err_old1 = float('Inf')
    err_old2 = float('Inf')
    weights_old1 = None
    weights_old2 = None

    # gradient descent loops: limit number of iterations to 2000 in case it does not converge
    for i in range(2000):
      logger.info("%d", i)
      # loop through whole date to compute gradient. N=(number of samples) and L=1 if batch gradient, N=1 and L=(number of samples) if stochastic gradient
      for j in range(L):
        data_temp = data[j * N:(j + 1) * N, :]
        label_temp = label[j * N:(j + 1) * N, :]
        trainer.train(self.machine, data_temp, label_temp)
      # every 5 iteration: compute the error on the development set and decide to stop or continue
      if (i % 5 == 0):
        y_real = self.machine(real_dev_features)
        y_attack = self.machine(attack_dev_features)
        err_real = numpy.sum(numpy.square(label_real * numpy.ones((len(real_dev_features), 1)) - y_real))
        err_attack = numpy.sum(numpy.square(label_attack * numpy.ones((len(attack_dev_features), 1)) - y_attack))
        err = (err_real + err_attack) / (len(real_dev_features) + len(attack_dev_features))
        logger.info("error on real accesses: " + str(err_real / (len(real_dev_features))))
        logger.info("error on attacks: " + str(err_attack / (len(attack_dev_features))))
        logger.info("t: " + str(err) + ", t-1: " + str(err_old1) + ", t-2: " + str(err_old2))

        # stopping criterion: if the error has been rising or is almost constant for two consecutive iterations, stop.
        # set MLP weights to the ones corresponding to the lowest error, i.e., the ones obtained two iterations ago.
        if ((err > 0.999 * err_old1) and (err_old1 > 0.999 * err_old2)):
          self.machine.weights = weights_old2
          break
        err_old2 = err_old1
        err_old1 = err
        weights_old2 = weights_old1
        weights_old1 = self.machine.weights

    # save MLP machine
    hdf5file.cd('/')
    hdf5file.create_group('MLP')
    hdf5file.cd('MLP')
    self.machine.save(hdf5file)
    logger.info("machine trained")

  def load_projector(self, projector_file):
    hdf5file = bob.io.base.HDF5File(projector_file)

    # read MLP Machine model
    hdf5file.cd('/MLP')
    self.machine = bob.learn.mlp.Machine(hdf5file)

  def project_feature(self, feature):
    feature = numpy.asarray(feature, dtype=numpy.float64)
    if self.mask is not None:
      feature = feature[self.mask]

    if self._check_feature(feature, machine=self.machine):
      # Projects the data on MLP classifier
      projection = self.machine(feature)
      return projection
    return numpy.zeros(1, dtype=numpy.float64)

  def project(self, feature):
    """project(feature) -> projected

    Projects the given feature into Fisher space.

    **Parameters:**

    feature : 1D :py:class:`numpy.ndarray`
      The 1D feature to be projected.

    **Returns:**

    projected : 1D :py:class:`numpy.ndarray`
      The ``feature`` projected into Fisher space.
    """

    if len(feature) > 0:
      if isinstance(feature[0], numpy.ndarray) or isinstance(feature[0], list):
        return [self.project_feature(feat) for feat in feature]
      else:
        return self.project_feature(feature)
    else:
      return numpy.zeros(1, dtype=numpy.float64)

  def enroll(self, enroll_features):
    """We do no enrollment here"""
    return enroll_features

  def score(self, toscore):
    """Returns the output of a classifier"""
    return toscore

  def score_for_multiple_projections(self, toscore):
    """Returns the output of a classifier"""
    return toscore


algorithm = MLP()
