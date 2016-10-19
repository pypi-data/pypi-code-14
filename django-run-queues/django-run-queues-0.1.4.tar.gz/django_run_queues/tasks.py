from .models import DjangoRunQueue
def add(taskname,queuename,taskArgs):
    try:
        rec=DjangoRunQueue.objects.create(TaskName=taskname,TaskQueue=queuename,TaskArgs=taskArgs)
        return 'Task %d has been added' % rec.id
    except:
        return 'Failed to add task'


def add_unique(taskname,queuename,taskArgs):
    try:
        if not DjangoRunQueue.objects.filter(TaskName=taskname, TaskQueue=queuename,
                                             TaskArgs=taskArgs, Proccessed=False).exists():
            rec = DjangoRunQueue.objects.create(TaskName=taskname, TaskQueue=queuename, TaskArgs=taskArgs)
            return 'Task %d has been added' % rec.id

    except:
        return 'Failed to add task'

def get_result(taskid):
    try:
        rec=DjangoRunQueue.objects.select_for_update(nowait=True).filter(id=taskid)
        if rec.Proccessed:
            return rec.TaskResults
        else:
            return "Not proccessed Yet"
    except:
        return "Still being proccessed"