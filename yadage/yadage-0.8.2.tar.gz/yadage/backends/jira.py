import jirainterface
from packtivitybackend import PacktivityProxyBase
import yadage.yadagestep

class JiraProxy(PacktivityProxyBase):
    def proxyname(self):
        return 'JiraPacktivityProxy'

    @classmethod
    def fromJSON(cls,data):
        proxy = data['proxydetails']
        return cls(proxy)


class JiraBackend(object):
    def __init__(self,title = None, description = None, wflowid = None):
        if wflowid:
            self.parenttask = wflowid
        else:
            data = jirainterface.create('workflow request: {}'.format(title),description)
            self.parenttask = data['key']

    def submit(self,task):
        tasktype = type(task)
        if tasktype == yadage.yadagestep.yadagestep:
            spec = task.spec
            context = task.context
        else:
            spec = {'no':'spec'}
            context = {'no':'context'}

        taskid = jirainterface.submit(task.name,spec,task.attributes,context,self.parenttask)
        return JiraProxy({'task_id':taskid, 'task_name':task.name})

    def result(self,resultproxy):
        return jirainterface.getfile(resultproxy.proxy['task_id'],'published.json')

    def ready(self,resultproxy):
        status = jirainterface.getstatus(resultproxy.proxy['task_id'])
        return True if status else False

    def successful(self,resultproxy):
        status = jirainterface.getstatus(resultproxy.proxy['task_id'])
        return status['name'] == 'Done'

    def fail_info(self,resultproxy):
        return 'cannot give reason :('
