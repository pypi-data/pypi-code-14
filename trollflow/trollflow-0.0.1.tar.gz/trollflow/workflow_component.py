import abc


class AbstractWorkflowComponent(object):
    __metaclass__ = abc.ABCMeta

    # @abc.abstractproperty
    slots = []

    # logger = logging.getLogger("WorkflowBase")
    # format = '[%(levelname)s: %(asctime)s: %(name)s] %(message)s'
    # logging.basicConfig(level=logging.DEBUG,
    #                     format=format,
    #                     datefmt='%Y-%m-%d %H:%M:%S')

    @abc.abstractmethod
    def pre_invoke(self):
        """Execute block before invoking component."""
        return

    @abc.abstractmethod
    def invoke(context):
        """Execute the actual component."""
        return

    @abc.abstractmethod
    def post_invoke(self):
        """Execute block after invoking component."""
        return
