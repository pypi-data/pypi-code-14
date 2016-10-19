from django.core.management.base import BaseCommand
from django_run_queues.models import *
from django.conf import settings
from crontab import CronTab


class Command(BaseCommand):
    help = 'Creates Crontab entries to schedule queue runs'

    def handle(self, *args, **options):

        tab = CronTab(user=True)
        del_list=[]
        for item in tab:
            if 'RunQueue' in item.command:
                del_list.append(item)
        for item in del_list:
            tab.remove(item)
        queue_details = settings.RUN_QUEUE_SCHEDULE

        if 'environment' not in queue_details:
            environ = ''
        else:
            environ = queue_details['environment']
        if 'settings' in queue_details:
            dj_settings ='--settings=%s' % queue_details['settings']
        else:
            dj_settings = ''

        for queue in queue_details['queues']:
            for times in queue_details['queues'][queue]:
                job = tab.new(command='. %s/bin/activate python %s/manage.py RunQueue --queue %s %s' % (environ,queue_details['base_dir'],queue,dj_settings))
                job.setall(times)
                print(job)
                if not job.is_valid():
                    tab.remove(job)
                    print('Command rejected %s %s' % (queue, times))
        tab.write(user=True)
