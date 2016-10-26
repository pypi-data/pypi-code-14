from autocloud.models import init_model, ComposeJobDetails

from retask.task import import Task
from retask.queue import import Queue

session = init_model()
compose_job_objs = session.query(ComposeJobDetails).filter_by(
    composei_id=compose_id).all()

for compose_job_obj in compose_job_objs:

    task = Task(info)
    jobenqueue.enqueue(task)

