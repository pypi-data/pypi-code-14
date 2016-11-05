from django_cron import CronJobBase, Schedule

from .models import Message


class SendAwaitingCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cms.emails.cron.SendAwaitingCronJob'

    def do(self):
        Message.send_awaiting()
