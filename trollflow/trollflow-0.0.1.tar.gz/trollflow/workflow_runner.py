import logging
from trollflow import utils

logger = logging.getLogger(__name__)


class WorkflowRunner(object):

    def __init__(self, workflow):
        self.components = [component.keys()[0] for component in workflow["Workflow"]]
        self.workflow = dict((component.items()[0] for component in workflow["Workflow"]))

    def get_class(self, clazz_path):
        return utils.get_class(clazz_path)

    def run(self, context):
        for module in self.components:
            clazz = self.get_class(module)
            component_clazz = clazz()
            component_clazz.slots = sorted(self.workflow[module].keys())

            component_clazz.pre_invoke()
            component_clazz.invoke(context)
            component_clazz.post_invoke()

class WorkflowException(Exception):
    pass
    # def __init__(self, msg, error):
    #     self.msg = msg
    #     self.error = error

    # def __str__(self):
    #     return repr("WorkflowException: {0} \nOriginal error: {1]".format(
    #         self.msg,
    #         self.error))
