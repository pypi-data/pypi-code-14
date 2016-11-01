import abc
import logging
from workflow_component import AbstractWorkflowComponent


class WorkflowBase(AbstractWorkflowComponent):
    __metaclass__ = abc.ABCMeta

    logger = logging.getLogger("WorkflowBase")
    format = '[%(levelname)s: %(asctime)s: %(name)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=format,
                        datefmt='%Y-%m-%d %H:%M:%S')

    # @abc.abstractmethod
    # def run(self, context):
    #     """Run a workflow with a given context."""
    #     return

    def run(self, context):
        """Run a workflow with a given context."""
        self.preInvoke()
        self.invoke(context)
        self.postInvoke()
        self.logger.info("Done.")


# public interface IWorkflow {
#   public void run(IWorkflowContext context);
# }
