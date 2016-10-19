from django.core.management.base import BaseCommand
from django_run_queues.models import *
from django.conf import settings
import importlib
from django.db import transaction

tasklib = importlib.import_module(settings.DRQ_TASKS_LIB)


class Command(BaseCommand):
    help = 'Runs Tasks queued on a specific Queue Name for Django Run-Queue'

    def add_arguments(self, parser):
        parser.add_argument('--queue', dest='queue_name', required=True)
    @transaction.atomic()
    def handle(self, *args, **options):
        tasklist = DjangoRunQueue.objects.select_for_update().\
                       filter(TaskQueue=options['queue_name'], Proccessed=False)
        for task in tasklist:
            print('running task %d' % task.id)
            try:
                func = getattr(tasklib, task.TaskName)
                task.TaskResults = func(**task.TaskArgs)
                task.Proccessed = True
                task.save()
            except Exception as e:
                task.TaskResults = "Taskid %d failed with %s" % (task.id, e)
                task.Proccessed = True
                task.save()
                print(e)
            print(task.TaskResults)
