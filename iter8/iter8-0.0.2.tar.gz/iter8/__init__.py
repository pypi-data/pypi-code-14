import pkg_resources

__version__ = pkg_resources.get_distribution('iter8').version

from discrete import discrete
from generic import sig_enumerate, take, iside
from sliding import sliding, sliding_list
